from django.db import models

from account.models import Student
from socle.models import  Knowledge


def directory_path(instance,filename):
    return "autotests/{}/{}".format(student.user.id,filename)



class Autotest(models.Model):

    student    = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='autotests', editable=False)
    dateback   = models.DateTimeField(verbose_name="A partir du ?", blank=True )
    date       = models.DateTimeField(auto_now=True)
    file       = models.FileField(upload_to=directory_path, verbose_name="Fichier pdf" )
    is_done    = models.BooleanField( default=0, editable=False )
    knowledges = models.ForeignKey(Knowledge,  on_delete=models.CASCADE, blank=True,  related_name='autotests', editable=False)  

    def __str__(self):        
        return "{}".format(self.student)
