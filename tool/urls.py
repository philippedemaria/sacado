
from django.urls import path, re_path
from .views import *

urlpatterns = [

 

    path('list_tools', list_tools, name='list_tools'),
    path('new', create_tool, name='create_tool'),
    path('update/<int:id>', update_tool, name='update_tool'),
    path('delete/<int:id>', delete_tool, name='delete_tool'),
    path('show/<int:id>', show_tool, name='show_tool'), 

    

    path('list_quizzes', list_quizzes, name='list_quizzes'),
    path('create_quizz/new', create_quizz, name='create_quizz'),
    path('delete_quizz/<int:id>', delete_quizz, name='delete_quizz'),
    path('show_quizz/<int:id>', show_quizz, name='show_quizz'), 


    path('list_questions', list_questions, name='list_questions'),
    path('create_question/<int:id>', create_question, name='create_question'),

    path('delete_question/<int:id>/<int:idquizz>', delete_question, name='delete_question'),
    path('show_question/<int:id>', show_question, name='show_question'), 


    ############## Ajax
    path('get_question_type', get_question_type, name='get_question_type'),
    path('get_an_existing_question', get_an_existing_question, name='get_an_existing_question'),

    path('ajax_update_question', ajax_update_question, name='ajax_update_question'),
    path('send_question', send_question, name='send_question'), 
    path('question_sorter', question_sorter, name='question_sorter'), 
]
 