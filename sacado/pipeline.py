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
            Student.objects.create(user_id=user.pk, level_id=1)
        elif usertype == User.PARENT:
            user.user_type = User.PARENT
            user.save()
            Parent.objects.create(user_id=user.pk)
        elif usertype == User.TEACHER:
            user.user_type = User.TEACHER
            user.save()
            Teacher.objects.create(user_id=user.pk)
    return kwargs



#################### Oauth

@partial
def get_usertype(strategy, details, user=None, is_new=False, *args, **kwargs):

    if user:
        return
    elif is_new and not details.get('usertype'):
        usertype = strategy.request_data().get('usertype')
        if usertype:
            details['usertype'] = usertype
        else:
            return redirect('ask_usertype')

