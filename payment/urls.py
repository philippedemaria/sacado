from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('traite_notif', traite_notif, name='traite_notif'),

]
 