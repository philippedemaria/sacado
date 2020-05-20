from group.models import Group
from account.models import Teacher
from django.core.exceptions import PermissionDenied




def user_is_group_teacher(function):
    def wrap(request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['id'])
        teacher = Teacher.objects.get(user= request.user)
        if group.teacher == teacher :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


