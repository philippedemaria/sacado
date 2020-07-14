from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from account.models import User, Student, Parent, Teacher


def complete_user(**kwargs):
    if kwargs['is_new']:
        user = kwargs['user']
        usertype = int(kwargs['details']['usertype'])
        if usertype == User.STUDENT:
            user.user_type = User.STUDENT
            user.save()
            level_id = int(kwargs['details']['level'])
            Student.objects.create(user_id=user.pk, level_id=level_id)
        elif usertype == User.PARENT:
            user.user_type = User.PARENT
            user.save()
            Parent.objects.create(user_id=user.pk)
        elif usertype == User.TEACHER:
            user.user_type = User.TEACHER
            user.save()
            Teacher.objects.create(user_id=user.pk)
    return kwargs


@partial
def get_usertype(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user:
        return
    elif is_new and not details.get('usertype'):
        usertype = strategy.request_data().get('usertype')
        level = strategy.request_data().get('level')
        if usertype:
            details['usertype'] = usertype
            details['level'] = level
        else:
            return redirect('ask_usertype')
