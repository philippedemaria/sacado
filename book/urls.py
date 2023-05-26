#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################
from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [


    #################################################################
    # book
    #################################################################

    path('books', books, name='books'),

    path('create_book/0', create_book, name='create_book'),
    path('update_book/<int:idb>', update_book, name='update_book'),
    path('delete_book/<int:idb>', delete_book, name='delete_book'), 
    path('show_book/<int:idb>', show_book, name='show_book'),
    path('conception_book/<int:idb>/<int:idch>', conception_book, name='conception_book'),

    #################################################################
    # chapter
    #################################################################
    path('update_chapter/<int:idb>/<int:idch>', update_chapter, name='update_chapter'),
    path('delete_chapter/<int:idb>/<int:idch>', delete_chapter, name='delete_chapter'),
    path('show_chapter/<int:idb>/<int:idch>', show_chapter, name='show_chapter'),
    path('sorter_chapter', sorter_chapter, name='sorter_chapter'),

    #################################################################
    # document
    #################################################################
    path('delete_document', delete_document, name='delete_document'),
    path('show_document', show_document, name='show_document'),
    path('sorter_document', sorter_document, name='sorter_document'),

    path('get_type_document', get_type_document, name='get_type_document'),



    path('update_section', update_section, name='update_section'),
    path('delete_section', delete_section, name='delete_section'),
    path('sorter_section', sorter_section, name='sorter_section'),
 ]
