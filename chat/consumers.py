"""Used channels tutorial https://channels.readthedocs.io/en/stable/tutorial/index.html as initial reference"""

import json
from uuid import uuid4

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils.timezone import now

from chat.models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"room_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        await self.check_room()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]
        time = now().strftime(r"%Y%m%d%H%M%S")

        if message_type == "chat-message":
            message = text_data_json["message"]
            await self.save_chat_message(message)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "username": self.scope["user"].username,
                    "time": time,
                    "message": message
                }
            )
        elif message_type == "typing-status":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "typing_status",
                    "username": self.scope["user"].username
                }
            )

    async def chat_message(self, event):
        username = event["username"]
        time = event["time"]
        message = event["message"]

        await self.send(text_data=json.dumps({
            "type": "chat-message",
            "username": username,
            "time": time,
            "message": message
        }))
    
    async def typing_status(self, event):
        username = event["username"]

        await self.send(text_data=json.dumps({
            "type": "typing-status",
            "username": username,
        }))

    @sync_to_async
    def check_room(self):
        try:
            self.room = ChatRoom.objects.get(name=self.room_name)
        except ChatRoom.DoesNotExist:
            new_room = ChatRoom(name=self.room_name)
            new_room.save()
            self.room = ChatRoom.objects.get(name=self.room_name)
    
    @sync_to_async
    def save_chat_message(self, message):
        user = User.objects.get(id=self.scope["user"].id)
        new_message = ChatMessage(id=uuid4(), room=self.room, user=user, message=message, time=now())
        new_message.save()