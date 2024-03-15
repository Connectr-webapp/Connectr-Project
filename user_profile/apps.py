"""
    apps.py is for performing any necessary setup when the app is loaded.
    This might include registering signals,
    loading initial data, or any other actions required during the app's initialization.
"""

from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    """
    Configuration class for the 'user_profile' app.

    Attributes:
        default_auto_field (str): The default
        auto-generated field for models.
        name (str): The name of the app.

    Methods:
        ready(): Method called when the app is ready
        to perform initialization tasks.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'


    def ready(self):
        import user_profile.signals 