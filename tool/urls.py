
from django.urls import path, re_path
from .views import *

urlpatterns = [

 

    path('list_tools', list_tools, name='list_tools'),
    path('new', create_tool, name='create_tool'),
    path('update/<int:id>', update_tool, name='update_tool'),
    path('delete/<int:id>', delete_tool, name='delete_tool'),
    path('show/<int:id>', show_tool, name='show_tool'), 

    path('my_quizz/list', list_quizzes, name='list_quizzes'),
    path('create_quizz/new', create_quizz, name='create_quizz'),
    path('update_quizz/<int:id>', update_quizz, name='update_quizz'),
    path('delete_quizz/<int:id>', delete_quizz, name='delete_quizz'),
    path('show_quizz/<int:id>', show_quizz, name='show_quizz'), 


    path('create_question/<int:idq>/<int:qtype>', create_question, name='create_question'),
    path('update_question/<int:id>/<int:idq>', update_question, name='update_question'),   
    path('delete_question/<int:id>/<int:idq>', delete_question  , name='delete_question'),




    path('list_diaporama', list_diaporama, name='list_diaporama'),
    path('create_diaporama/new', create_diaporama, name='create_diaporama'),
    path('update_diaporama/<int:id>', update_diaporama, name='update_diaporama'),
    path('show_diaporama/<int:id>', show_diaporama, name='show_diaporama'),     
    path('delete_diaporama/<int:id>', delete_diaporama, name='delete_diaporama'),


    path('create_slide/<int:id>', create_slide, name='create_slide'),
    path('update_slide/<int:id>/<int:idp>', update_slide, name='update_slide'),
    path('delete_slide/<int:id>/<int:idp>', delete_slide, name='delete_slide'),


    path('play_printing_teacher/<int:id>', play_printing_teacher, name='play_printing_teacher'), 
    path('play_quizz_teacher/<int:id>', play_quizz_teacher, name='play_quizz_teacher'), 

    path('list_questions', list_questions, name='list_questions'),

    path('create_question/<int:id>/<int:qtype>', create_question, name='create_question'),
    path('update_question/<int:id>/<int:idq>/<int:qtype>', update_question, name='update_question'),
    path('delete_question/<int:id>/<int:idq>', delete_question, name='delete_question'),

    path('remove_question/<int:id>/<int:idq>', remove_question, name='remove_question'), # from a quizz
    path('show_question/<int:id>', show_question, name='show_question'), 


    ############## Ajax
    path('delete_my_tool', delete_my_tool, name='delete_my_tool'),

 
    path('ajax_chargeknowledges', ajax_chargeknowledges, name='ajax_chargeknowledges'),
 
    path('question_sorter', question_sorter, name='question_sorter'), 



    path('get_this_tool', get_this_tool, name='get_this_tool'),

    path('remove_slide/<int:id>/<int:idquizz>', remove_slide, name='remove_slide'), # from a quizz
 
    path('send_slide', send_slide, name='send_slide'), 
    path('slide_sorter', slide_sorter, name='slide_sorter'),


    ############## Random_quizz
    path('create_quizz_random/<int:id>', create_quizz_random, name='create_quizz_random'),


 




]
 