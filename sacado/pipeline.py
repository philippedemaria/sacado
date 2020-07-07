from account.models import Student

def complete_user(**kwargs):
    import pdb;pdb.set_trace()
    user = kwargs['user']
    Student.objects.create(user_id=user.pk, level_id=1)
    return kwargs