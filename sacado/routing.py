from django.urls import path
from tool.consumers import RealConsumer


ws_urlpatterns = [
	path('ws/tool/', RealConsumer.as_asgi())
]

