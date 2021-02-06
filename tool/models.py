from django.db import models
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField
from group.models import Group
from socle.models import *
from account.models import Student, Teacher, ModelWithCode , User
from django.apps import apps
from django.utils import   timezone
from django.db.models import Q
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()

def choice_directory_path(instance, filename):
    return "choices/{}".format(filename) 

def question_directory_path(instance, filename):
    return "questions/{}".format(filename)

def quizz_directory_path(instance, filename):
    return "quizzes/{}/{}".format(instance.teacher.user.id, filename)

def tool_directory_path(instance, filename):
    return "tool/asso/{}".format( filename)



class Tool(models.Model):
    """
    Modèle représentant un associé.
    """
    title         = models.CharField(max_length=255, default='',  blank=True, verbose_name="Titre")  
    remark        = RichTextUploadingField( blank=True, verbose_name="Texte*") 
    teachers      = models.ManyToManyField(Teacher, related_name = "tools", blank=True,   editable=False ) 
    date_created  = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification") 
    imagefile     = models.ImageField(upload_to=tool_directory_path,   verbose_name="Image", default="")
    is_publish    = models.BooleanField(default=1, verbose_name="Publié ?")
    is_asso       = models.BooleanField(default=1, verbose_name="Nécessite l'adhésion SACADO ?")
    url           =  models.CharField(max_length=255, default='' ,   blank=True, verbose_name="url de substitution")  


    def __str__(self):
        return self.title 







class Question(models.Model):
    """
    Modèle représentant un associé.
    """


    title         = models.TextField(max_length=255, default='',  blank=True, verbose_name="Réponse écrite")
    calculator    = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    date_modified = models.DateTimeField(auto_now=True)
    #### pour donner une date de remise - Tache     
    qtype         = models.PositiveIntegerField(default=3, editable=False)

    knowledge  = models.ForeignKey(Knowledge, related_name="question", blank=True, null = True,  on_delete=models.CASCADE) 

    imagefile  = models.ImageField(upload_to=question_directory_path, blank=True, verbose_name="Image", default="")
    is_publish = models.BooleanField(default=1, verbose_name="Publié ?")
    is_radio   = models.BooleanField(default=0, verbose_name="Type de réponse ?")

    is_correction = models.BooleanField(default=0, verbose_name="Correction ?")
    duration      = models.PositiveIntegerField(default=20, blank=True, verbose_name="Durée")
    point         = models.PositiveIntegerField(default=1000, blank=True, verbose_name="Point")

 
    is_correct = models.BooleanField(default=1, verbose_name="Réponse correcte ?")
    ranking    = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)
    students   = models.ManyToManyField(Student, blank=True, through="Questionplayer", related_name="question",   editable=False)

    def __str__(self):
        return self.title 
 


class Choice(models.Model):
    """
    Modèle représentant un associé.
    """

    imageanswer = models.ImageField(upload_to=choice_directory_path,  null=True,  blank=True, verbose_name="Image", default="")
    answer      = models.TextField(max_length=255, default='', null=True,  blank=True, verbose_name="Réponse écrite")
    is_correct  = models.BooleanField(default=0, verbose_name="Réponse correcte ?")
    question  = models.ForeignKey(Question, related_name="choices", blank=True, null = True,  on_delete=models.CASCADE)
    def __str__(self):
        return self.answer 


class Quizz(ModelWithCode):
    """
    Modèle représentant un associé.
    """
    title         = models.CharField( max_length=255, verbose_name="Titre du quizz") 
    teacher       = models.ForeignKey(Teacher, related_name="teacher_quizz", blank=True, on_delete=models.CASCADE, editable=False ) 
    date_modified = models.DateTimeField(auto_now=True)

    #### pour donner une date de remise - Tache 
    levels    = models.ManyToManyField(Level, related_name="quizz", blank=True)
    themes    = models.ManyToManyField(Theme, related_name="quizz", blank=True)
    subject   = models.ForeignKey(Subject, related_name="quizz", blank=True, null = True, on_delete=models.CASCADE)
 
    vignette   = models.ImageField(upload_to=quizz_directory_path, verbose_name="Vignette d'accueil", blank=True, null = True , default ="")
    is_music   = models.BooleanField(default=0, verbose_name="En musique ?")
    is_share   = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")

    is_questions = models.BooleanField(default=0, editable=False )  # presentation ou questionnaire
    is_numeric   = models.BooleanField(default=0,   verbose_name="Type de réponse" )    # réponse sur papier ou sur smartphone
    is_mark      = models.BooleanField(default=0, verbose_name="Récupérer les notes ?") 
    is_lock      = models.BooleanField(default=0, verbose_name="Verrouiller ?") 
    is_random    = models.BooleanField(default=0, verbose_name="Aléatoire ?") 

    interslide   = models.PositiveIntegerField(default=10, blank=True, verbose_name="Temps entre les questions")


    groups       = models.ManyToManyField(Group, blank=True, related_name="quizz" , editable=False) 
    questions    = models.ManyToManyField(Question, blank=True, related_name="quizz" , editable=False)  

    def __str__(self):
        return self.title 

 


class Player(models.Model):

    student    = models.ForeignKey(Student,  null=True, blank=True,   related_name='player', on_delete=models.PROTECT,  editable= False)
    quizz      = models.ForeignKey(Quizz,  null=True, blank=True, related_name='player', on_delete=models.PROTECT, editable= False)
    scoretotal = models.PositiveIntegerField(default=0, editable=False)
 
    def __str__(self):
        return self.student 

    class Meta:
        unique_together = ('student', 'quizz')




class Questionplayer(models.Model):

    student  = models.ForeignKey(Student,  null=True, blank=True,   related_name='student_player', on_delete=models.PROTECT,  editable= False)
    question = models.ForeignKey(Question,  null=True, blank=True, related_name='question_player', on_delete=models.PROTECT, editable= False)
    answer   = models.CharField( max_length=255, verbose_name="Réponse")  
    score    = models.PositiveIntegerField(default=0, editable=False)
    timer    = models.CharField(max_length=255, editable=False)  

    def __str__(self):
        return self.student 


    class Meta:
        unique_together = ('student', 'question')


class Slide(models.Model):
    """
    Modèle représentant un associé.
    """
    title         = models.CharField( max_length=255, default="",  verbose_name="Titre") 
    content      = RichTextUploadingField(  default="", verbose_name="Texte ")
    ranking    = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)
    duration   = models.PositiveIntegerField(default=0, blank=True, verbose_name="Durée d'affichage")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
 

    def __str__(self):
        return self.title 


class Diaporama(ModelWithCode):
    """
    Modèle représentant un associé.
    """
    title         = models.CharField( max_length=255, verbose_name="Titre du quizz") 
    teacher       = models.ForeignKey(Teacher, related_name="teacher_presentation", blank=True, on_delete=models.CASCADE, editable=False ) 
    students      = models.ManyToManyField(Student, related_name="user_presentation", blank=True , editable=False ) 
    date_modified = models.DateTimeField(auto_now=True)

    #### pour donner une date de remise - Tache 
    levels    = models.ManyToManyField(Level, related_name="presentation", blank=True)
    themes    = models.ManyToManyField(Theme, related_name="presentation", blank=True)
    subject   = models.ForeignKey(Subject, related_name="presentation", blank=True, null = True, on_delete=models.CASCADE)
 
    vignette   = models.ImageField(upload_to=quizz_directory_path, verbose_name="Vignette d'accueil", blank=True, null = True , default ="")

    is_share   = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
 
    groups     = models.ManyToManyField(Group, blank=True, related_name="presentation" , editable=False) 
    slides  = models.ManyToManyField(Slide, blank=True, related_name="diapositive" , editable=False) 
 
    def __str__(self):
        return self.title 


