"""
    apps.py is for performing any necessary setup when the app is loaded.
    This might include registering signals,
    loading initial data, or any other actions required
    during the app's initialization.
"""
from django.apps import AppConfig

class ChannelsConfig(AppConfig):
    """
    Channels AppConfig for the 'group_chat' Django app.

    Attributes:
    - default_auto_field: A string representing the name
    of the default auto field for models.
    - name: A string representing the name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group_chat'
