"""
Models module for the messaging app.

This module defines Django models that represent
various entities in the messaging app,
including images, emojis, conversations, messages,
and unread messages. Each model
has specific attributes and methods to capture and
manage relevant data.

Models:
- ImageModel: Model for storing images.
- EmojiModel: Model for storing emojis.
- Conversation: Model for storing conversation details.
- Message: Model for storing messages.
- UnreadMessage: Model for storing unread messages.

For detailed information about each model and its attributes,
refer to the individual
docstrings within the respective class definitions.

"""
from django.db import models
from django.contrib.auth import get_user_model

# pylint: disable=no-member

user = get_user_model()


class ImageModel(models.Model):
    """
    Model for storing images.

    Attributes:
    - image: ImageField for uploading images.

    """
    image = models.ImageField(upload_to='images/')


class EmojiModel(models.Model):
    """
    Model for storing emojis.

    Attributes:
    - emoji_colon_name: Text field for storing the
    colon representation of the emoji.
    - users_who_incremented: Many-to-Many relationship
    with users who incremented the emoji.

    Methods:
    - get_incremented_users: Returns the users who incremented the emoji.

    """
    emoji_colon_name = models.TextField(unique=False)
    incremented_by = models.ManyToManyField(
        user,
        related_name='%(class)s_incremented_by',
        blank=True
    )

    def get_incremented_users(self):
        """
        - get_incremented_users: Returns the users who incremented the emoji.

        """
        return self.users_who_incremented.all()


class Conversation(models.Model):
    """
    Model for storing conversation details.

    Attributes:
    - participants (ManyToManyField): Relationship
    with users participating in the conversation.

    """
    participants = models.ManyToManyField(user)

    def delete(self, *args, **kwargs):
        """
        Overrides the delete method to delete all
        messages related to this conversation.

        """
        self.messages.all().delete()
        super(Conversation, self).delete(*args, **kwargs)


class Message(models.Model):
    """
    Model for storing messages.

    Attributes:
    - sender (ForeignKey): User who sent the message.
    - receiver (ForeignKey): User who received the message.
    - content (TextField): Content of the message.
    - timestamp (DateTimeField): Timestamp when the message was created.
    - images (TextField): Comma-separated image URLs.
    - emojis (ManyToManyField): Relationship with emojis in the message.
    - conversation (ForeignKey): Conversation to which the message belongs.

    Methods:
    - __str__: String representation of the message.
    - get_image_urls: Returns a list of image URLs.

    """
    sender = models.ForeignKey(user,
                               on_delete=models.CASCADE,
                               related_name='sent_messages')
    receiver = models.ForeignKey(user,
                                 on_delete=models.CASCADE,
                                 related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    images = models.TextField(blank=True, default="")
    emojis = models.ManyToManyField(EmojiModel, blank=True)
    conversation = models.ForeignKey(Conversation,
                                     on_delete=models.CASCADE,
                                     related_name='messages')

    def __str__(self):
        """
        Returns a string representation of the message.

        Returns:
        - str: String representation.

        """
        return f"{self.sender} to {self.receiver} - {self.timestamp}"

    def get_image_urls(self):
        """
        - get_image_urls: Returns a list of image URLs.

        """
        return [url.strip() for url in self.images.split(',') if url.strip()]


class UnreadMessage(models.Model):
    """
    Model for storing unread messages.

    Attributes:
    - conversation (ForeignKey): Conversation related to the unread message.

    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
