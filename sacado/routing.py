from django.urls import path
from qcm.consumers import RealConsumer


ws_urlpatterns = [
	path('ws/qcm/', RealConsumer.as_asgi())
]

