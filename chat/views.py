from django.shortcuts import render
from chat.models import ChatRoom, ChatMessage

# Create your views here.
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
        print(chat_log_texts)
        
        context_dict["chat_log"] = chat_log_texts
    except ChatRoom.DoesNotExist:
        context_dict["chat_log"] = None

    return render(request, "chat.html", context_dict)