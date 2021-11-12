from django.urls import path
from qcm.consumers import TableauConsumer


ws_urlpatterns = [

	path('qcm/tableau/', TableauConsumer.as_asgi())
	
]



