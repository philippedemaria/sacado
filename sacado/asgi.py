"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
"""
import os
import django
from channels.routing import get_default_application
#from django.core.asgi import get_asgi_application
#from channels.auth import AuthMiddlewareStack
#from .routing import ws_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sacado.settings")

django.setup()
application= get_default_application()
#application = ProtocolTypeRouter({
# Django's ASGI application to handle traditional HTTP requests
#"http": get_asgi_application() ,
# WebSocket handler
#    "websocket": AuthMiddlewareStack(  URLRouter(ws_urlpatterns)  )
#})


"""
import os

import django
django.setup()

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from .routing import ws_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sacado.settings")

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application() ,
    # WebSocket handler
    "websocket": AuthMiddlewareStack(  URLRouter(ws_urlpatterns)  ) 
})

