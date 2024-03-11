from datetime import datetime, timedelta
import json
from uuid import uuid4

from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.timezone import now

from chat.models import ChatRoom, ChatMessage, ChatTypingStatus

def chat(request, room_name):
    context_dict = {}
    username = request.user.username
    context_dict["room_name"] = room_name
    context_dict["username"] = username

    try:
        room = ChatRoom.objects.get(name=room_name)
        chat_logs = ChatMessage.objects.filter(room=room)
        chat_log_texts = {}
        for log in chat_logs:
            message = {
                "type": "chat_message",
                "username": log.user.username,
                "time": log.time.strftime(r"%Y%m%d%H%M%S"),
                "message": log.message
            }
            chat_log_texts.update({str(log.id): message})
        
        context_dict["chat_log"] = chat_log_texts
    except ChatRoom.DoesNotExist:
        new_room = ChatRoom(name=room_name)
        new_room.save()
        room = ChatRoom.objects.get(name=room_name)
        context_dict["chat_log"] = None

    return render(request, "chat.html", context_dict)

def send_message(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            if (data["type"] == "chat_message"):
                process_chat_message(data)
            elif (data["type"] == "typing_status"):
                process_typing_status(data)
            else:
                return JsonResponse({'status': 'Invalid request'})

            return JsonResponse({'status': 'Success'})
        return JsonResponse({'status': 'Invalid request'})
    else:
        return HttpResponseBadRequest('Invalid request')

def process_chat_message(message):
    user = User.objects.get(username=message["username"])
    room = find_room(message['room'])

    new_message = ChatMessage(id=uuid4(), room=room, user=user, message=message['content'], time=now())
    new_message.save()

def process_typing_status(message):
    user = User.objects.get(username=message["username"])
    room = find_room(message['room'])
    
    try:
        typing_status = ChatTypingStatus.objects.get(room=room, user=user)
        typing_status.time = now()
        typing_status.save()
    except ChatTypingStatus.DoesNotExist:
        typing_status = ChatTypingStatus(room=room, user=user, time=now())
        typing_status.save()
    

def update(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            #to_return = process_update(data)
            return JsonResponse(get_log(data['room'], data['last-timestamp']))
        return JsonResponse({'status': 'Invalid request'}, status=200)
    else:
        return HttpResponseBadRequest('Invalid request')

def get_log(room_name, last_timestamp=""):

    chat_message = get_chat_message_log(room_name, last_timestamp)
    typing_status = get_typing_status_log(room_name)

    return {"chat_message": chat_message, "typing_status": typing_status}

def get_chat_message_log(room_name, last_timestamp):

    try:
        room = ChatRoom.objects.get(name=room_name)

        if last_timestamp == "":
            chat_logs = ChatMessage.objects.filter(room=room)
        else:
            last_datetime = datetime.strptime(last_timestamp, r"%Y%m%d%H%M%S%f")
            chat_logs = ChatMessage.objects.filter(room=room, time__gt=last_datetime)
            
        chat_log_texts = {}
        for log in chat_logs:
            message = {
                "type": "chat_message",
                "username": log.user.username,
                "time": log.time.strftime(r"%Y%m%d%H%M%S%f"),
                "message": log.message
            }
            id_text = str(log.id)
            chat_log_texts.update({id_text: message})
        
        return chat_log_texts
    except ChatRoom.DoesNotExist:
        return None

def get_typing_status_log(room_name):

    try:
        room = ChatRoom.objects.get(name=room_name)
        recently = now() - timedelta(seconds=3)
        typing_status = ChatTypingStatus.objects.filter(room=room, time__gt=recently)

        typing_status_texts = {}
        for log in typing_status:
            message = {
                "type": "typing_status",
                "username": log.user.username
            }
            id_text = str(log.id)
            typing_status_texts.update({id_text: message})
        
        return typing_status_texts
    except ChatRoom.DoesNotExist:
        return None


def process_update(message):
    user = User.objects.get(username=message["username"])
    room = find_room(message['room'])
    chat_messages = ChatMessage.objects.filter(room=room)
    data = {}
    i = 0
    for chat_message in chat_messages:
        sender = User.objects.get(id=chat_message.user_id)
        data.update({
            i: {
                "type": "chat_message",
                "uuid": chat_message.id,
                "username": sender.username,
                "time": chat_message.time,
                "message": chat_message.message
            }
        })
        i += 1

    return data

def find_room(room_name: str):
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        new_room = ChatRoom(name=room_name)
        new_room.save()
        room = ChatRoom.objects.get(name=room_name)
    return room