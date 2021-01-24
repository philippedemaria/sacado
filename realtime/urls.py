from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [


    path('as_ck', as_ck , name='as_ck'),
 

 

 ]
