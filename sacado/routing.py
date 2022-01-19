from django.urls import path
from qcm.consumers import TableauConsumer
from tool.consumers import VisioConsumer

ws_urlpatterns = [

	path('qcm/tableau/', TableauConsumer.as_asgi()),
	path('tool/visiocast', VisioConsumer.as_asgi())
]



