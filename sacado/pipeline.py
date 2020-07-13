from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from account.models import User, Student, Parent, Teacher


def complete_user(**kwargs):

    user = kwargs['user']
    usertype = int(kwargs['details']['usertype'])
    import pdb
    pdb.set_trace()
    if usertype == User.STUDENT:
        Student.objects.create(user_id=user.pk, level_id=1)
    elif usertype == User.PARENT:
        Parent.objects.create(user_id=user.pk)
    elif usertype == User.TEACHER:
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

