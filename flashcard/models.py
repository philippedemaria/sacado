from django.db import models
from datetime import date, datetime
from ckeditor_uploader.fields import RichTextUploadingField
from group.models import Group
from socle.models import *
from account.models import Student, Teacher, ModelWithCode , User
from qcm.models import Parcours , Exercise , Folder
 
from django.utils import   timezone
from django.db.models import Q
from random import uniform , randint
from sacado.settings import MEDIA_ROOT
from time import strftime

POLICES = (
        (16, '16'),
        (24, '24'), 
        (32, '32'), 
        (40, '40'),
        (48, '48'),
        (56, '56'),
    )


def flashcard_directory_path(instance, filename):
    return "flashcards/{}/{}".format(instance.subject.id, filename)

def flashpack_directory_path(instance, filename):
    return "bibliocards/{}/{}".format(instance.teacher.user.id, filename)


class Flashcard(models.Model):
    """
    Modèle représentant un associé.
    """
    title         = models.TextField(max_length=255, default='',  blank=True, verbose_name="Titre")

    question      = models.TextField(max_length=255, default='',  blank=True, verbose_name="Question écrite")
    calculator    = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    date_modified = models.DateTimeField(auto_now=True)
    answer        = models.CharField(max_length=255, null = True,   blank=True, verbose_name="Réponse attendu")
    size       = models.PositiveIntegerField(default=32, choices=POLICES,  verbose_name="Taille de police")

    imagefile  = models.ImageField(upload_to=flashcard_directory_path, blank=True, verbose_name="Image", default="")
    audio      = models.FileField(upload_to=flashcard_directory_path, blank=True, verbose_name="Audio", default="")
    video      = models.TextField( default='',  blank=True, verbose_name="Vidéo intégrée")

    duration   = models.PositiveIntegerField(default=20, blank=True, verbose_name="Durée")

    students   = models.ManyToManyField(Student, blank=True, through="Answercard", related_name="flashcards", editable=False)

    waiting    = models.ManyToManyField(Waiting, related_name="flashcards", blank=True)
    theme      = models.ManyToManyField(Theme, related_name="flashcards", blank=True)
    levels     = models.ManyToManyField(Level, related_name="flashcards", blank=True)
    subject    = models.ForeignKey(Subject, related_name="flashcards", blank=True, null = True, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.title 
 


class Flashpack(models.Model):
    """
    Modèle représentant un ensemble de flashcard.
    """
    title         = models.CharField( max_length=255, verbose_name="Titre du flashpack") 
    teacher       = models.ForeignKey(Teacher, related_name="flashpacks", blank=True, on_delete=models.CASCADE, editable=False ) 
    date_modified = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=255, default='#5d4391', verbose_name="Couleur")
    
    levels    = models.ManyToManyField(Level, related_name="flashpacks", blank=True)
    themes    = models.ManyToManyField(Theme, related_name="flashpacks", blank=True)
    subject   = models.ForeignKey(Subject, related_name="flashpacks", blank=True, null = True, on_delete=models.CASCADE)
 
    vignette   = models.ImageField(upload_to=flashpack_directory_path, verbose_name="Vignette d'accueil", blank=True, null = True , default ="")
 
    is_share   = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_archive   = models.BooleanField(default=0, verbose_name="Archivé ?")

    interslide   = models.PositiveIntegerField(default=10, blank=True, verbose_name="Temps entre les questions")
    
    is_publish = models.BooleanField(default=1, verbose_name="Publié ?")
    start = models.DateTimeField(null=True, blank=True, verbose_name="Début de publication")
    stop  = models.DateTimeField(null=True, blank=True, verbose_name="Verrouillé dès le")

    groups       = models.ManyToManyField(Group, blank=True, related_name="flashpacks" ) 
    parcours     = models.ManyToManyField(Parcours, blank=True, related_name="flashpacks"  ) 
    folders      = models.ManyToManyField(Folder, blank=True, related_name="flashpacks"  ) 
    
    def __str__(self):
        return self.title 

 
    def duration(self):
        d = 0
        for q in self.questions.filter(is_publish=1) :
            d += q.duration + self.interslide
        return d



class Answercard(models.Model):

    flashcard   = models.ForeignKey(Flashcard,  related_name="answercards",  on_delete=models.CASCADE ) 
    student     = models.ForeignKey(Student,  null=True, blank=True,   related_name='answercards', on_delete=models.CASCADE,  editable= False)
    weight      = models.PositiveIntegerField(default=0, editable= False)
    is_correct  = models.BooleanField(default=0, editable=False) 

    def __str__(self):
        return self.student.user.last_name