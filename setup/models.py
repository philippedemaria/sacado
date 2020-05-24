from django_cron import CronJobBase, Schedule
from qcm.models import Parcours
from django.utils import formats, timezone
        
    
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    today = timezone.now()

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'setup.my_cron_job'    # a unique code

    def do(self):
        Parcours.objects.filter(stop__lt=today).update(is_publish=0)