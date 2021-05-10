from django.urls import path
from qcm.consumers import RealConsumer


ws_urlpatterns = [

	path('/qcm/<int:parcours_id>/', RealConsumer.as_asgi())
	
]

