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
    title         = models.CharField(max_length=255, default='', verbose_name="Titre")

    question      = RichTextUploadingField( default='',  verbose_name="Question écrite")
    calculator    = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    date_modified = models.DateTimeField(auto_now=True)
    answer        = RichTextUploadingField( default='',  verbose_name="Réponse attendu")
    helper        = RichTextUploadingField( null = True,   blank=True, verbose_name="Aide proposée")

    #duration   = models.PositiveIntegerField(default=20, blank=True, verbose_name="Durée")
    is_validate  = models.BooleanField(default=1, verbose_name="Validée par l'enseignant ?")
    students   = models.ManyToManyField(Student, blank=True, through="Answercard", related_name="flashcards", editable=False)

    waiting   = models.ForeignKey(Waiting, related_name="flashcards", blank=True, null=True, on_delete=models.CASCADE, default="")
    theme     = models.ForeignKey(Theme, related_name="flashcards", blank=True, on_delete=models.CASCADE, default="")
    levels    = models.ManyToManyField(Level, related_name="flashcards", blank=True )
    subject   = models.ForeignKey(Subject, related_name="flashcards", blank=True, null = True, on_delete=models.CASCADE, default="")

    authors   = models.ManyToManyField(User, blank=True, related_name="flashcards", editable=False)
 
    def __str__(self):
        return self.title 
 


class Flashpack(models.Model):
    """
    Modèle représentant un ensemble de flashcard.
    """
    title         = models.CharField( max_length=255, verbose_name="Titre du flashpack") 
    teacher       = models.ForeignKey(Teacher, related_name="flashpacks", blank=True, on_delete=models.CASCADE, editable=False ) 
    date_modified = models.DateTimeField(auto_now=True)
    color         = models.CharField(max_length=255, default='#5d4391', verbose_name="Couleur")

    flashcards    = models.ManyToManyField(Flashcard, related_name="flashpacks", blank=True)
    
    levels    = models.ManyToManyField(Level, related_name="flashpacks", blank=True)
    themes    = models.ManyToManyField(Theme, related_name="flashpacks", blank=True)
    subject   = models.ForeignKey(Subject, related_name="flashpacks", blank=True, null = True, on_delete=models.CASCADE)
 
    vignette   = models.ImageField(upload_to=flashpack_directory_path, verbose_name="Vignette d'accueil", blank=True, null = True , default ="")
 
    is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_archive   = models.BooleanField(default=0, verbose_name="Archivé ?")
    is_favorite  = models.BooleanField(default=1, verbose_name="Favori ?")
 
    
    is_publish = models.BooleanField(default=1, verbose_name="Publié ?")
    start = models.DateTimeField(null=True, blank=True, verbose_name="Début de publication")
    stop  = models.DateTimeField(null=True, blank=True, verbose_name="Verrouillé dès le")

    is_creative  = models.BooleanField(default=0, verbose_name="Création par les élèves de flashCard ?")

    groups       = models.ManyToManyField(Group, blank=True, related_name="flashpacks" ) 
    parcours     = models.ManyToManyField(Parcours, blank=True, related_name="flashpacks"  ) 
    folders      = models.ManyToManyField(Folder, blank=True, related_name="flashpacks"  ) 
    students     = models.ManyToManyField(Student, blank=True, related_name="flashpacks", editable=False)

    def __str__(self):
        return self.title 

 
    def duration(self):
        d = 0
        for q in self.questions.filter(is_publish=1) :
            d += q.duration + self.interslide
        return d

    def flashcards_to_validate(self):
        d = False
        if self.flashcards.filter(is_validate=0).count() :
            d = True
        return d





class Answercard(models.Model):

    flashpack   = models.ForeignKey(Flashpack,  related_name="answercards",  on_delete=models.CASCADE, default='' ) 
    flashcard   = models.ForeignKey(Flashcard,  related_name="answercards",  on_delete=models.CASCADE ) 
    student     = models.ForeignKey(Student,  null=True, blank=True,   related_name='answercards', on_delete=models.CASCADE,  editable= False)
    weight      = models.FloatField(default=0, editable= False)
 

    def __str__(self):
        return self.student.user.last_name