"""
Routing configuration for WebSocket consumers in the ci_chathub project.

This module defines the WebSocket URL patterns for connecting to
different consumers, such as `PostConsumer` for handling channel posts
and `CommentConsumer` for handling post comments and MessageConsumer for handling messages.

WebSocket URL Patterns:
- ws/channel_posts/(?P<channel_id>\d+)/$: Connects to `PostConsumer` for channel posts.
- ws/post_comments/(?P<post_id>\d+)/$: Connects to `CommentConsumer` for post comments.
"""
from django.urls import re_path
from group_chat import consumers as gc_consumer
from messaging import consumers as msg_consumer
from .consumers import GlobalConsumer

websocket_urlpatterns = [
    re_path(r'ws/channel_posts/(?P<channel_id>\d+)/$', gc_consumer.PostConsumer.as_asgi()),
    re_path(r'ws/post_comments/(?P<post_id>\d+)/$', gc_consumer.CommentConsumer.as_asgi()),
    re_path(r'ws/messaging/(?P<conversation_id>\d+)/$', msg_consumer.MessageConsumer.as_asgi()),
    re_path(r'ws/global_consumer/(?P<user_id>\d+)/$', GlobalConsumer.as_asgi()),
]
