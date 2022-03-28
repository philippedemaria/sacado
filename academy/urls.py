
from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('academy_index', academy_index , name='academy_index'),
    path('details_adhesion/<int:level_id>', details_adhesion , name='details_adhesion'),
    path('historic_adhesions/<int:level_id>', historic_adhesions , name='historic_adhesions'),


]


 