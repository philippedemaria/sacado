"""
from django.urls import path

#from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from qcm.consumers import TableauConsumer
#from QuesFlash.consumers import QFConsumer
#from canvas.consumers import CanvasConsumer  #modifCanvas
from tool.consumers import VisioConsumer
#from qcm.consumers import CepythonConsumer
application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("qcm/tableau/", TableauConsumer.as_asgi()),
            #path("QF/RT/",QFConsumer.as_asgi()),
            #path("canvas/",CanvasConsumer.as_asgi()), #modifCanvas
            path("tool/visiocast/", VisioConsumer.as_asgi()), #modifVisio
            #path("qcm/cepython/",CepythonConsumer.as_asgi())
        ]),
    ),

})


"""

from django.urls import path
from qcm.consumers import TableauConsumer
from tool.consumers import VisioConsumer

ws_urlpatterns = [

	path('qcm/tableau/', TableauConsumer.as_asgi()),
	path('tool/visiocast/', VisioConsumer.as_asgi())
]



