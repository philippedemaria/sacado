from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from qcm.consumers import TableauConsumer



application = ProtocolTypeRouter({
     "websocket": AuthMiddlewareStack(
         URLRouter([

             path("qcm/tableau/", TableauConsumer.as_asgi()),

         ]),
     ),

})

