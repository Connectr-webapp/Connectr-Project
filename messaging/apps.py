"""
    AppConfig class for the messaging app.
"""
from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """
    AppConfig class for the messaging app.

    This class defines configuration settings for
    the messaging app. It specifies the
    default auto field and the app's name. The `ready`
    method is utilized to import
    signals when the app is ready.

    Attributes:
    - default_auto_field (str): The default auto field for model creation.
    - name (str): The name of the app.

    Methods:
    - ready: Method called when the app is ready,
    used for importing signals.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        """
        Method called when the app is ready.

        This method is used for additional setup when the app is loaded.
        In this case,
        it imports signals from the messaging module.

        """
        import messaging.signals
