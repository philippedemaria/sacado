from django.core.exceptions import PermissionDenied
from account.models import Teacher, User, Parent, Student
from group.models import Group
from django.contrib import messages

def user_can_create(user):
    return user.is_teacher


def user_is_superuser(user):
    return user.is_superuser == 1


def decide(this_student, role, asker):
    test = False
    if role == 0:  # role = request.user.user_type
        if this_student.user == asker:  # asker = request.user
            test = True
    elif role == 1:
        parent = Parent.objects.get(user=asker)
        parents = Parent.objects.filter(students=this_student)
        if parent in parents:
            test = True
    else:
        teacher = Teacher.objects.get(user=asker)
        groups = Group.objects.filter(students=this_student, teacher=teacher)
        if len(groups) > 0:
            test = True
    return test


def user_can_read_details(function):  # id est associé à un user
    # def wrap(request, *args, **kwargs):
    #     user = User.objects.get(pk=kwargs['id'])
    #     student = Student.objects.get(user=user)  # détail de ce student
    #     testeur = decide(student, user.user_type, user)
    #     if testeur:
    #         return function(request, *args, **kwargs)
    #     else:
    #         #raise PermissionDenied
    #         messages.error(request, " Vous passez par un espace interdit.")
    #         return function(request, *args, **kwargs)
    # return wrap
    pass


def who_can_read_details(function):   # id est associé à un student
    # def wrap(request, *args, **kwargs):

    #     print("====================================") 
    #     print("====================================")   
    #     print(request.user) 
    #     print("====================================")   
    #     print("====================================") 

    #     student = Student.objects.get(pk=kwargs['id'])
    #     testeur = decide(student, request.user.user_type, request.user)

    #     if testeur:
    #         return function(request, *args, **kwargs)
    #     else:
    #         #raise PermissionDenied
    #         messages.error(request, " Vous passez par un espace interdit.")
    #         return function(request, *args, **kwargs)
    # return wrap
    pass


def is_manager_of_this_school(function): 
    # def wrap(request, *args, **kwargs):

    #     print("====================================") 
    #     print("====================================")   
    #     print(request.user) 
    #     print("====================================")   
    #     print("====================================") 
    #     users = User.objects.filter(is_manager=1, school=request.user.school)
    #     user = request.user

    #     if user in users or user.is_superuser:
    #         return function(request, *args, **kwargs)
    #     else:
    #         #raise PermissionDenied
    #         return function(request, *args, **kwargs)
    # return wrap
    pass


def can_register(function): 
    # def wrap(request, *args, **kwargs):

    #     print("====================================") 
    #     print("====================================")   
    #     print(request.user) 
    #     print("====================================")   
    #     print("====================================")  

    #     users = User.objects.filter(is_manager=1)
    #     user = request.user

    #     if user in users or user.is_superuser:
    #         return function(request, *args, **kwargs)
    #     else:
    #         #raise PermissionDenied
    #         return function(request, *args, **kwargs)
    # return wrap
    pass



def user_is_admin_school(function): 
    # def wrap(request, *args, **kwargs):
    #     print("====================================") 
    #     print("====================================")   
    #     print(request.user) 
    #     print("====================================")   
    #     print("====================================") 
    #     if request.user.is_manager:
    #         return function(request, *args, **kwargs)
    #     else:
    #         #raise PermissionDenied
    #         return function(request, *args, **kwargs)
    # return wrap
    pass