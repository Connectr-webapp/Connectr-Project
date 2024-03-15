"""
Module Docstring:

This module defines WebSocket consumers for handling real-time notifications
related to posts and comments in a channel-based chat application.

Classes:
- BaseConsumer: A base class for common WebSocket consumer functionality.
- PostConsumer: Handles WebSocket connections and events related to posts.
- CommentConsumer: Handles WebSocket connections and events related to comments.

"""

import json
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class GlobalConsumer(AsyncWebsocketConsumer):
    """
    Base WebSocket consumer class providing common functionality.

    Methods:
    - connect: Called when the WebSocket is handshaking as part of the connection process.
    - disconnect: Called when the WebSocket closes for any reason.
    - get_room_group_name: Must be implemented by subclasses to determine the group name.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = 'global_consumer'
        self.user_id = None

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def get_room_group_name(self):
        """
        Must be implemented by subclasses to determine the group name.
        """
        raise NotImplementedError("Subclasses must implement this method")

    async def global_consumer(self, event):
        """
        Send a post notification to the WebSocket.

        Args:
        - event: Dictionary containing post notification details.

        """
        if await self.is_user_allowed(event['model_name'], event['model_id']):
            await self.send(text_data=json.dumps({
                'type': 'global_consumer',
                'timestamp': event['timestamp'],
                'message': event['message'],
                'created_by': event['created_by'],
                'img_url': event['img_url'],
            }))

    async def is_user_allowed(self, model_name, model_id):
        """
        Check if the user is allowed to receive notifications based on the model type.

        Args:
        - model_name: String representing the type of 
        model (e.g., 'channel', 'post', 'conversation').
        - model_id: ID of the specific model instance.

        Returns:
        - True if the user is allowed, False otherwise.

        """
        from group_chat.models import ChannelModel, PostsModel
        from messaging.models import Conversation
        model_mapping = {
            'channel': ChannelModel,
            'post': PostsModel,
            'conversation': Conversation,
        }

        try:
            user = await self.get_user(self.user_id)
            model = await self.get_model(model_mapping.get(model_name), model_id)

            if isinstance(model, ChannelModel):  # posts
                users = await self.get_channel_users(model)
                return user in users
            if isinstance(model, PostsModel):  # comments
                commented_users = await self.get_commented_users(model)
                return user.id in commented_users
            if isinstance(model, Conversation):  # messages
                result = await self.get_conversation_users(user, model)
                return result
        except Exception as e:
            print(e)
            return False

    @database_sync_to_async
    def get_user(self, user_id):
        """
        Retrieve a user asynchronously.

        Args:
        - user_id: ID of the user.

        Returns:
        - User object.

        """
        user_model = get_user_model()
        return get_object_or_404(user_model, id=user_id)

    @database_sync_to_async
    def get_model(self, model_class, model_id):
        """
        Retrieve a model instance asynchronously.

        Args:
        - model_class: Class of the model.
        - model_id: ID of the model instance.

        Returns:
        - Model instance.

        """
        return get_object_or_404(model_class, id=model_id)

    @database_sync_to_async
    def get_channel_users(self, channel_model):
        """
        Retrieve users associated with a channel asynchronously.

        Args:
        - channel_model: ChannelModel instance.

        Returns:
        - List of users associated with the channel.

        """
        return list(channel_model.users.all())

    @database_sync_to_async
    def get_conversation_users(self, user, conversation_model):
        """
        Check if a user is part of a conversation asynchronously.

        Args:
        - user: User object.
        - conversation_model: ConversationModel instance.

        Returns:
        - True if the user is part of the conversation, False otherwise.

        """
        conv_users = conversation_model.participants.all()
        return user in conv_users

    @database_sync_to_async
    def get_commented_users(self, posts_model):
        """
        Retrieve users who have commented on a post asynchronously.

        Args:
        - posts_model: PostsModel instance.

        Returns:
        - List of users who have commented on the post.

        """
        from group_chat.models import CommentsModel
        commented_users = [
            item['created_by'] for item in
            CommentsModel.objects.filter(comment_post=posts_model).values('created_by').distinct()
        ]
        if posts_model.created_by.id not in commented_users:
            commented_users.append(posts_model.created_by.id)
        return commented_users
