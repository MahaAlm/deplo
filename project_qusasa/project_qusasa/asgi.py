# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import qusasa.routing  # Make sure this points to your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_qusasa.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            qusasa.routing.websocket_urlpatterns  # Define your WebSocket routes
        )
    ),
})
