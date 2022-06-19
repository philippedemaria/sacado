
from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('academy_index', academy_index , name='academy_index'),
    path('details_adhesion/<int:level_id>', details_adhesion , name='details_adhesion'),
    path('historic_adhesions/<int:level_id>', historic_adhesions , name='historic_adhesions'),
    path('delete_adhesion/<int:ida>', delete_adhesion , name='delete_adhesion'),

    path('delete_student_academy/<int:ids>/<int:level_id>', delete_student_academy , name='delete_student_academy'),

    path('autotests', autotests , name='autotests'),
    path('create_autotest', create_autotest , name='create_autotest'),
    path('delete_autotest/<int:test_id>', delete_autotest , name='delete_autotest'),


    path('synthese_parcours/<int:user_id>', synthese_parcours , name='synthese_parcours'),





]


 