import uuid

from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ManyToManyField(User)

class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=2500)
    time = models.DateTimeField()

class ChatTypingStatus(models.Model):
    """For keeping latest status."""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'user'], name='unique_chat_typing_status_room_user'
            )
        ]