
from django.urls import path, re_path
from .views import *

urlpatterns = [



    path('', aefe , name='aefe'),
    path('<int:id>', get_this_parcours_aefe , name='get_this_parcours_aefe'),

]


 