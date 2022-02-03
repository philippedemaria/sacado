from django.db import models
from datetime import date, datetime, timedelta
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
    title         = models.CharField(max_length=255, default='', blank=True,  verbose_name="Titre")

    question      = RichTextUploadingField( default='',  verbose_name="Question écrite")
    calculator    = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    date_modified = models.DateTimeField(auto_now=True)
    answer        = RichTextUploadingField( default='',  verbose_name="Réponse attendu")
    helper        = RichTextUploadingField( null = True,   blank=True, verbose_name="Aide proposée")

    is_validate  = models.BooleanField(default=1, verbose_name="Flashcard validée par l'enseignant ?")
    is_publish   = models.BooleanField(default=1, verbose_name="Publié ?")
    students     = models.ManyToManyField(Student, blank=True, through="Answercard", related_name="flashcards", editable=False)

    is_globalset = models.BooleanField(default=1, verbose_name="Contenue dans le flashpack annuel ?")

    waiting   = models.ForeignKey(Waiting, related_name="flashcards", blank=True, null=True, on_delete=models.CASCADE, default="")
    theme     = models.ForeignKey(Theme, related_name="flashcards", blank=True,  null=True,  on_delete=models.CASCADE, default="")
    levels    = models.ManyToManyField(Level, related_name="flashcards", blank=True )
    subject   = models.ForeignKey(Subject, related_name="flashcards", blank=True, null = True, on_delete=models.CASCADE, default="")

    authors   = models.ManyToManyField(User, blank=True, related_name="flashcards", editable=False)
 
    def __str__(self):
        return self.title 


    def is_commented(self):
        t = False
        if self.comments.count():
            t = True
        return t


    def is_result_by_student( self , flashpack , student ) :
        data = {}
        try :
            answer = self.answercards.get( flashpack=flashpack , student=student)
            data["rappel"] =  answer.rappel
            string, cpt = "" , 0
            for a in answer.answers :
                if a == '1' : color = "danger"
                elif a == '3' : color = "validate"
                elif a == '5' : color = "success"
                else : color = None
                if a != "-" :
                    string += "<i class='bi bi-square-fill text-"+color+"'></i> "
                    cpt += int(a)
            data["first"] =  answer.rappel - timedelta(days = cpt)
            data["answers"] =  string
        except :
            pass

        return data


    def to_display_results(self):
        today = timezone.now()
        t = False
        if self.answercards.filter(rappel__gte=today) :
            t = True
        return t



    def in_flashpack(self,flashpack):
        t = False
        try :
            if self in flashpack.flashcards.all() :
                t = True
        except :
            pass
        return t 



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
    is_publish   = models.BooleanField(default=1, verbose_name="Publié ?")
    
    start = models.DateTimeField(null=True, blank=True, verbose_name="Début de publication")
    stop  = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")

    is_creative  = models.BooleanField(default=0, verbose_name="Création de flashCard par les élèves ?")

    is_global    = models.BooleanField(default=0, verbose_name="Flashpack annuel ?")

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
        to_validate = False
        if self.is_creative == 1 :
            if self.flashcards.filter(is_validate=0).count() :
                to_validate = True
        return to_validate
 

    def today_cards(self,today,student) :

        data = {}
        if self.answercards.count() > 0 :
            today_cards =  self.flashcards.filter(is_validate=1 , answercards__rappel=today)

        else :
            today_cards =  self.flashcards.filter(is_validate=1)

        nb_today_cards = today_cards.count()
        data["cards"]  = today_cards
        data["count"]  = nb_today_cards
        return data


    def is_comments(self):
        d = False
        if self.comments.exclude(comment="").count() :
            d = True
        return d


    def is_result_by_student( self ,   student ) :
        nb_answer = self.answercards.filter( student=student).count()
        return nb_answer


class Madeflashpack(models.Model):

    flashpack   = models.ForeignKey(Flashpack,  related_name="madeflashpack",  on_delete=models.CASCADE, default='' ) 
    student     = models.ForeignKey(Student,  null=True, blank=True,   related_name='madeflashpack', on_delete=models.CASCADE,  editable= False)
    date        = models.DateField(auto_now=True )

    def __str__(self):
        return self.date


class Answercard(models.Model):

    flashpack   = models.ForeignKey(Flashpack,  related_name="answercards",  on_delete=models.CASCADE, default='' ) 
    flashcard   = models.ForeignKey(Flashcard,  related_name="answercards",  on_delete=models.CASCADE ) 
    student     = models.ForeignKey(Student,  null=True, blank=True,   related_name='answercards', on_delete=models.CASCADE,  editable= False)
    weight      = models.FloatField(default=0, editable= False)
    date        = models.DateField(auto_now=True )
    rappel      = models.DateField(auto_now=True , null=True, blank=True )
    answers     = models.CharField(max_length=255, default='', editable= False)


    def __str__(self):
        return str(self.date)



class Commentflashcard(models.Model):

    flashpack  = models.ForeignKey(Flashpack,  related_name="comments",  on_delete=models.CASCADE, default='' ) 
    flashcard  = models.ForeignKey(Flashcard,  related_name="comments",  on_delete=models.CASCADE ) 
    comment    = models.TextField(verbose_name="Commentaire")
    date       = models.DateField(auto_now=True )

    def __str__(self):
        return str(self.flashcard)