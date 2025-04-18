"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import polls.routing

# ← point this at your real settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# ← import your app's routing, e.g. camera.routing if your app is named camera

# this application will serve both HTTP and WebSocket
application = ProtocolTypeRouter({
    # Django's normal HTTP handling
    "http": get_asgi_application(),

    # WebSocket handling via Channels
    "websocket": AuthMiddlewareStack(
        URLRouter(
            polls.routing.websocket_urlpatterns
        )
    ),
})
