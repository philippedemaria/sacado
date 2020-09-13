from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('', list_emails, name='emails'),
    path('new', create_email, name='create_email'),
    path('delete/<int:id>/', delete_email, name='delete_email'),
    path('ajax/show_email/', show_email, name='show_email'),


    path('communications', list_communications, name='communications'),
    path('new_communication', create_communication, name='create_communication'),
    path('update_communication/<int:id>/', update_communication, name='update_communication'),
    path('delete_communication/<int:id>/', delete_communication, name='delete_communication'),
    path('ajax/show_communication/', show_communication, name='show_communication'),
    path('ajax/show_communication/', show_communication, name='show_communication'),
    path('ajax/reader_communication/', reader_communication, name='reader_communication'),
]
