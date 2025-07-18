from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Extended User model if needed
class User(AbstractUser):
    # Add custom fields here if needed
    pass


class Conversation(models.Model):
    """
    A conversation that includes multiple users
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    A message sent from one user in a conversation
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages_sent")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in conversation {self.conversation.id}"
