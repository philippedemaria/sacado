from django.urls import path, re_path
from .views import *

urlpatterns = [


    path('create_payment', create_payment, name='create_payment'), 

    path('thanks_for_payment', thanks_for_payment, name='thanks_for_payment'), 
 

]
 