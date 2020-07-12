from django.shortcuts import redirect
from social_core.pipeline.partial import partial

from account.models import Student


def complete_user(**kwargs):
    import pdb;pdb.set_trace()
    user = kwargs['user']
    Student.objects.create(user_id=user.pk, level_id=1)
    return kwargs



#################### Oauth

@partial
def get_usertype(strategy, details, user=None, is_new=False, *args, **kwargs):
    email = strategy.request_data().get('email')
    if email:
        details['email'] = email
    else:
        return redirect('ask_usertype')

