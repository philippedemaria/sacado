from qcm.models import Parcours
from account.models import Teacher
from django.core.exceptions import PermissionDenied




def user_is_parcours_teacher(function):
    def wrap(request, *args, **kwargs):
        parcours = Parcours.objects.get(pk=kwargs['id'])
        teacher = Teacher.objects.get(user= request.user)
        if parcours.teacher == teacher :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

 