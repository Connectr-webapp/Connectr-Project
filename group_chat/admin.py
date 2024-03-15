"""
    Django administration configuration for the 'group_chat' app.

    Registers the Models for administration.

    The admin.py file in a Django app is used to define the 
    configuration for the Django admin interface 
    related to the models in that app. 
    This file allows you to customize how the app's models are 
    displayed and managed through the Django admin.
"""

from django.contrib import admin
from .models import ChannelModel,CommentsModel,PostsModel

admin.site.register(ChannelModel)
admin.site.register(PostsModel)
admin.site.register(CommentsModel)
