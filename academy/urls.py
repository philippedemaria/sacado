
from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('academy_index', academy_index , name='academy_index'),
    path('details_adhesion/<int:level_id>', details_adhesion , name='details_adhesion'),
    path('historic_adhesions/<int:level_id>', historic_adhesions , name='historic_adhesions'),

    path('autotests', autotests , name='autotests'),
    path('create_autotest', create_autotest , name='create_autotest'),
    path('delete_autotest/<int:test_id>', delete_autotest , name='delete_autotest'),

]


 