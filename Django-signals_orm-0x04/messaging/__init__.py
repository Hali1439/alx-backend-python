from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Message(models.Model):
    """
    Represents a message between users with edit tracking capabilities
    """
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        verbose_name='Sender'
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE,
        verbose_name='Recipient'
    )
    content = models.TextField(
        verbose_name='Message Content',
        help_text='The text content of the message'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    edited = models.BooleanField(
        default=False,
        verbose_name='Edited?'
    )
    edited_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Last Edited At'
    )
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies',
        verbose_name='Parent Message'
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['edited']),
        ]

    def __str__(self):
        return f"Message {self.id} ({'edited' if self.edited else 'original'})"

    def save(self, *args, **kwargs):
        """Custom save to handle edit tracking"""
        if self.pk and self.content != Message.objects.get(pk=self.pk).content:
            self.edited = True
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)


class MessageHistory(models.Model):
    """
    Tracks historical versions of edited messages
    """
    message = models.ForeignKey(
        Message,
        related_name='history',
        on_delete=models.CASCADE,
        verbose_name='Related Message'
    )
    content = models.TextField(
        verbose_name='Content Snapshot'
    )
    saved_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Version Timestamp'
    )

    class Meta:
        ordering = ['-saved_at']
        verbose_name = 'Message History'
        verbose_name_plural = 'Message Histories'
        get_latest_by = 'saved_at'

    def __str__(self):
        return f"History #{self.id} for Message {self.message.id}"


def create_message_history(sender, instance, **kwargs):
    """
    Signal receiver to create message history before edits
    """
    if instance.pk:  # Only for existing messages
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    content=original.content
                )
        except Message.DoesNotExist:
            pass


# Connect the signal
from django.db.models.signals import pre_save
pre_save.connect(create_message_history, sender=Message)