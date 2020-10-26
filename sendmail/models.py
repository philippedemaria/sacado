from django.db import models
from account.models import User, Teacher
from group.models import Group
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

 


class Email(models.Model):
    author = models.ForeignKey(User, blank = True, on_delete=models.CASCADE,   related_name="author_email"  ) 
    subject = models.CharField(max_length=255, blank=True,verbose_name="Objet")    
    texte = RichTextUploadingField(  verbose_name="Texte")      
    receivers = models.ManyToManyField(User, blank = True,    related_name="receiver_email"  ) 
    today = models.DateTimeField( default=timezone.now)
    
    def __str__(self):
        return "{} {} : {}".format(self.author.last_name, self.author.first_name, self.subject)  




class Communication(models.Model):

    teacher = models.ForeignKey(User, blank = True, on_delete=models.CASCADE,   related_name="teacher_communication"  ) 
    subject = models.CharField(max_length=255, blank=True, verbose_name="Objet")    
    texte = RichTextUploadingField(  verbose_name="Texte")      
    today = models.DateField( auto_now_add= True)
    active = models.BooleanField( default=1,    verbose_name="Afficher la communication ?") 
    teachers = models.ManyToManyField(Teacher, blank = True,  related_name="teachers_communication", editable = False  ) 
    
    def __str__(self):
        return "{} {} : {}".format(self.teacher.last_name, self.teacher.first_name, self.subject)


    def com_is_reading(user):
        teacher = Teacher.objects.get(user = user)
        is_read = False
        if Communication.objects.filter(teachers = teacher).count() == Communication.objects.count()   :
            is_read = True
        return is_read