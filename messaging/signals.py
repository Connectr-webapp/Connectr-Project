"""
Signals module for the messaging app.

This module contains Django signals that are used to perform certain actions
in response to specific events in the messaging app. Currently, it includes a
signal receiver for the post-save event of the Message model, which creates
an UnreadMessage instance when a new message is created.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UnreadMessage, Message

@receiver(post_save, sender=Message)
def create_unread_message(sender, instance, created, **kwargs):
    """
    Signal receiver to create an UnreadMessage instance when a new Message is created.

    This function is a post-save signal receiver that is triggered when a new Message
    instance is created. It checks if there's already an UnreadMessage for the corresponding
    conversation and receiver. If not, it creates a new UnreadMessage instance for the
    receiver of the message.

    Parameters:
    - sender: The model class that sends the signal (Message in this case).
    - instance: The actual instance being saved (the new Message instance).
    - created (bool): A boolean indicating whether the instance was created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if created:
        # Check if there's already an UnreadMessage for this conversation 
        existing_unread_message = UnreadMessage.objects.filter(
            conversation=instance.conversation,
        ).first()

        if not existing_unread_message:
            # Create an UnreadMessage instance 
            UnreadMessage.objects.create(
                conversation=instance.conversation,
            )