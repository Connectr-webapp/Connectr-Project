
"""
ASGI application configuration for the Django Channels routing.

- Uses the ProtocolTypeRouter to route HTTP and WebSocket protocols separately.
- For HTTP requests, it uses the Django ASGI application.
- For WebSocket connections, it uses the 
AllowedHostsOriginValidator to validate the origin of the connection.
- It then applies the AuthMiddlewareStack for 
handling authentication in WebSocket connections.
- Finally, it uses the URLRouter to route WebSocket 
connections to the specified URL patterns in the 'websocket_urlpatterns' module.

Note: Ensure that the 'DJANGO_SETTINGS_MODULE' 
environment variable is set to your Django project's settings module.
"""
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from .routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ci_chathub.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
