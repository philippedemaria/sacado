from sendmail.models import Email
from account.models import Teacher
from django.core.exceptions import PermissionDenied
from django.contrib import messages

 

def user_is_email_teacher(function):
    def wrap(request, *args, **kwargs):
        email = Email.objects.get(pk=kwargs['id'])
        print("====================================") 
        print("====================================")   
        print(request.user) 
        print("====================================")   
        print("====================================") 
        if email.author ==  request.user :
            return function(request, *args, **kwargs)
        else:
            #raise PermissionDenied
            return function(request, *args, **kwargs)
    return wrap



def user_is_active(function):
    def wrap(request, *args, **kwargs):
        print("====================================") 
        print("====================================")   
        print(request.user) 
        print("====================================")   
        print("====================================") 
        if request.user.is_active :
            return function(request, *args, **kwargs)
        else:
            #raise PermissionDenied
            return function(request, *args, **kwargs)
    return wrap 