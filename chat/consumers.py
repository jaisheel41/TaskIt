"""Used channels tutorial https://channels.readthedocs.io/en/stable/tutorial/index.html as initial reference"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"room_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

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
