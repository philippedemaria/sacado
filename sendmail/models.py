from django.db import models
from account.models import Teacher, User
from socle.models import Subject
from group.models import Group
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
 


class Email(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, on_delete=models.CASCADE,   related_name="author_email"  ) 
    subject = models.CharField(max_length=255, blank=True,verbose_name="Objet")    
    texte = RichTextUploadingField(  verbose_name="Texte")      
    receivers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True,    related_name="receiver_email"  ) 
    today = models.DateTimeField( default=timezone.now)
    
    def __str__(self):
        return "{} {} : {}".format(self.author.last_name, self.author.first_name, self.subject)  




class Communication(models.Model):

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, on_delete=models.CASCADE,   related_name="teacher_communication"  ) 
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




class Discussion(models.Model):

    CATEGORIES = (
        ('Sacado', 'Sacado'),
        ('Pédagogie et Didactique', 'Pédagogie et Didactique'),
        ('Geogebra', 'Geogebra'),
        ('Python', 'Python'),
        ('Jeu et concours', 'Jeu et concours'),

    )

    category     = models.CharField(max_length=100,  blank=True, choices=CATEGORIES, verbose_name="Catégorie")
    user         = models.ForeignKey(User, blank = True, on_delete=models.CASCADE,   related_name="user_discussion")
    subject      = models.ForeignKey(Subject, blank = True, on_delete=models.CASCADE,   related_name="subject_discussion")      
    topic        = models.CharField(max_length=255, blank=True, verbose_name="Objet")    
    date_created = models.DateTimeField( auto_now_add= True)
    active       = models.BooleanField( default=1,    verbose_name="Afficher la communication ?") 
    solve        = models.BooleanField( default=0,    verbose_name="Résolu ?") 
    nb_display   = models.PositiveIntegerField( default=0, editable=False) 

    def __str__(self):
        return "{}".format(self.topic)


    def details(self):
        data={}
        messages = Message.objects.filter(discussion = self)
        message = messages.last()
        data["user"] = message.user
        data["date_created"] =  message.date_created
        data["answers_count"] = messages.count()-1
        return data

 

class Message(models.Model):

    discussion   = models.ForeignKey(Discussion, blank = True, null=True , on_delete=models.CASCADE,   related_name="discussion_message")
    user         = models.ForeignKey(User, blank = True, on_delete=models.CASCADE,   related_name="user_message")
    texte        = RichTextUploadingField(  verbose_name="Texte")      
    date_created = models.DateTimeField( auto_now_add= True)
 

    def __str__(self):
        return "{}".format(self.user)
 
 