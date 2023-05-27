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

    path('reset_all_chapters/<int:idb>', reset_all_chapters, name='reset_all_chapters'),

    #################################################################
    # document
    #################################################################

    path('update_book_document/<int:idb>/<int:idch>/<int:idd>', update_book_document, name='update_book_document'),
    path('duplicate_book_document/<int:idb>/<int:idch>/<int:idd>', duplicate_book_document, name='duplicate_book_document'),
    path('delete_book_document', delete_book_document, name='delete_book_document'),
    path('show_book_document', show_book_document, name='show_book_document'),
    path('sorter_book_document', sorter_book_document, name='sorter_book_document'),

    path('get_type_book_document', get_type_book_document, name='get_type_book_document'),
 


    path('update_book_section', update_book_section, name='update_book_section'),
    path('delete_book_section', delete_book_section, name='delete_book_section'),
    path('sorter_book_section', sorter_book_section, name='sorter_book_section'),
 ]
