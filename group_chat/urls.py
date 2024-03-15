"""
URL patterns for routing requests to the
appropriate views in Django application.

"""
from django.urls import path
from .views.channels_view import (ChannelsView,
                                  AddUserToChannelView,
                                  get_all_channels)
from .views.posts_comments_view import PostsView, CommentsView
from .views.util_views import (ImageUploadView,
                               AddOrUpdateEmojiView,
                               SavePostView)
from .views.util_views import GenericObjectDeleteView

urlpatterns = [
     path('', ChannelsView.as_view(), name='channels'),
     path('view_channel/<int:channel_id>/',
          ChannelsView.as_view(), name='view_channel'),
     path('saved-post/<int:channel_id>/<int:post_id>',
          ChannelsView.as_view(), name='saved-post'),
     path('channel_posts/<int:channel_id>/',
          PostsView.as_view(), name='channel_posts'),
     path('channel_posts/<int:channel_id>/<int:post_id>/',
          PostsView.as_view(), name='channel_posts'),
     path('post_comments/<int:post_id>/',
          CommentsView.as_view(), name='post_comments'),
     path('post_comments/<int:post_id>/<int:comment_id>/',
          CommentsView.as_view(), name='post_comments'),
     path('add_user_to_channel/<int:channel_id>/<int:user_id>/',
          AddUserToChannelView.as_view(), name='add_user_to_channel'),
     path('upload-image/',
          ImageUploadView.as_view(), name='image_upload'),
     path('emoji_home/<str:model>/<int:instance_id>/',
          AddOrUpdateEmojiView.as_view(), name='emoji_home'),
     path('delete/<str:model>/<int:pk>/',
          GenericObjectDeleteView.as_view(), name='delete_object'),
     path('save_post/<int:post_id>/',
          SavePostView.as_view(), name='save_post'),
     path('get_all_channels/',
          get_all_channels, name='get_all_channels'),
]
