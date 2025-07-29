from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Automatically creates a notification when a new message is sent
    Skip notification if user is messaging themselves
    """
    if created and instance.receiver != instance.sender:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def track_message_edits(sender, instance, **kwargs):
    """
    Tracks message edits by saving previous content to MessageHistory
    Marks message as edited when content changes
    """
    if instance.pk:  # Only for existing messages
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    content=original.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def clean_user_data(sender, instance, **kwargs):
    """
    Cleanup function when a user is deleted
    Note: Most cleanup is handled by CASCADE, this is for any additional cleanup
    """
    # Add any custom cleanup logic here if needed
    pass