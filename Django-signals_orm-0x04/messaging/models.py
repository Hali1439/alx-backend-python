from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(
        User, 
        related_name='sent_messages', 
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, 
        related_name='received_messages', 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    objects = models.Manager()  # Default manager

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['read']),
        ]

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False)

Message.unread = UnreadMessagesManager()

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"

class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message,
        related_name='history',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Message Histories"
        ordering = ['-edited_at']

    def __str__(self):
        return f"History snapshot for message {self.message.id}"