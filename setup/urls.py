
from django.urls import path, re_path
from .views import *

urlpatterns = [

    re_path(r'^$', index, name='index'),


    re_path('send_message', send_message, name='send_message'),

    path('ajax/change_color_account', ajax_changecoloraccount , name='ajax_changecoloraccount'), 
]
