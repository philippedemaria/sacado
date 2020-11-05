from group.models import Group , Sharing_group
from account.models import Teacher
from django.core.exceptions import PermissionDenied
from django.contrib import messages



def user_is_group_teacher(function):
    # def wrap(request, *args, **kwargs):

    #     print("====================================") 
    #     print("====================================")   
    #     print(request.user) 
    #     print("====================================")   
    #     print("====================================") 
        
    #     group = Group.objects.get(pk=kwargs['id'])
    #     teachers = Sharing_group.objects.filter(group = group).values_list("teacher", flat=True)	

    #     teacher = Teacher.objects.get(user= request.user)
    #     if group.teacher == teacher or teacher.user.id in teachers:
    #         return function(request, *args, **kwargs)
    #     else:
    #         #raise PermissionDenied
    #         return function(request, *args, **kwargs)
    # return wrap
    pass


