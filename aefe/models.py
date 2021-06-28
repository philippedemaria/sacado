from django.db import models
from account.models import Teacher
from qcm.models import Parcours

class Testhistoric(models.Model):

 
    teacher = models.ForeignKey(Teacher,  related_name="teacher_to_test", on_delete=models.CASCADE, default='', blank=True, editable=False)
    clone   = models.ForeignKey(Parcours, related_name="clone_to_test", on_delete=models.CASCADE, default='', blank=True, editable=False)
    origin  = models.ForeignKey(Parcours, related_name="origin_to_test", on_delete=models.CASCADE, default='', blank=True, editable=False)

    def __str__(self):
        return "{} - {} - {}".format(self.teacher , self.clone , self.origin )
