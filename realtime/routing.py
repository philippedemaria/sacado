from django.urls import path

from .consumers import RealConsumer


ws_urlpatterns = [

	path('ws/realtime/', RealConsumer.as_asgi())

]