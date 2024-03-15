"""
Module Docstring:

This module defines WebSocket consumers for handling real-time messagin

Classes:
- MessageConsumer: Handles WebSocket connections and events related to posts.

"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MessageConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time messaging.

    This consumer class extends the AsyncWebsocketConsumer
    provided by the Channels library.
    It is responsible for handling WebSocket connections,
    receiving and sending messages
    in real-time.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.conversation_id = None

    async def connect(self):
        """
        Called when the WebSocket is handshaking as
        part of the connection process.
        """
        self.room_group_name = self.get_room_group_name()
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)

    async def messaging_notification(self, event):
        """
        Send a post message to the WebSocket.

        Args:
        - event: Dictionary containing post notification details.

        """
        await self.send(text_data=json.dumps({
            'type': 'messaging_notification',
            'message': event['message'],
            'html': event['html'],
            'created_by': event['created_by'],
            'edit_id': event['edit_id'],
        }))

    def get_room_group_name(self):
        """
        Returns the group name for comment-related events.
        """
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        return f"messaging_{self.conversation_id}"
