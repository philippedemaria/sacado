from sendmail.models import Email
from account.models import Teacher
from django.core.exceptions import PermissionDenied


 

def user_is_email_teacher(function):
    def wrap(request, *args, **kwargs):
        email = Email.objects.get(pk=kwargs['id'])
        teacher = Teacher.objects.get(user= request.user)
        if email.author == teacher :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


 