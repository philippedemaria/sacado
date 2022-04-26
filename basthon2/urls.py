from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', basthon , name='basthon'),
    path('pyodide', pyodide , name='pyodide'),
    
]
 
