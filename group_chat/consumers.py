"""
Module Docstring:

This module defines WebSocket consumers for handling real-time notifications
related to posts and comments in a channel-based chat application.

Classes:
- BaseConsumer: A base class for common WebSocket consumer functionality.
- PostConsumer: Handles WebSocket connections and events related to posts.
- CommentConsumer: Handles WebSocket connections and events related to
comments.

"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BaseConsumer(AsyncWebsocketConsumer):
    """
    Base WebSocket consumer class providing common functionality.

    Methods:
    - connect: Called when the WebSocket is handshaking as part of
    the connection process.
    - disconnect: Called when the WebSocket closes for any reason.
    - get_room_group_name: Must be implemented by subclasses to
    determine the group name.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.post_id = None
        self.channel_id = None

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the
        connection process.
        """
        self.room_group_name = self.get_room_group_name()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def get_room_group_name(self):
        """
        Must be implemented by subclasses to determine the group name.
        """
        raise NotImplementedError("Subclasses must implement this method")

    async def post_notification(self, event):
        """
        Send a post notification to the WebSocket.

        Args:
        - event: Dictionary containing post notification details.

        """
        await self.send(text_data=json.dumps({
            'type': 'post_notification',
            'message': event['message'],
            'html': event['html'],
            'created_by': event['created_by'],
            'edit_id': event['edit_id'],
        }))

    async def comment_notification(self, event):
        """
        Send a comment notification to the WebSocket.

        Args:
        - event: Dictionary containing comment notification details.

        """
        await self.send(text_data=json.dumps({
            'type': 'comment_notification',
            'message': event['message'],
            'html': event['html'],
            'created_by': event['created_by'],
            'edit_id': event['edit_id'],
        }))


class PostConsumer(BaseConsumer):
    """
    WebSocket consumer for handling events related to posts.

    Methods:
    - get_room_group_name: Returns the group name for post-related events.

    """

    def get_room_group_name(self):
        """
        Returns the group name for post-related events.
        """
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        return f"post_{self.channel_id}"


class CommentConsumer(BaseConsumer):
    """
    WebSocket consumer for handling events related to comments.

    Methods:
    - get_room_group_name: Returns the group name for comment-related events.

    """

    def get_room_group_name(self):
        """
        Returns the group name for comment-related events.
        """
        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]
        return f"comment_{self.post_id}"
