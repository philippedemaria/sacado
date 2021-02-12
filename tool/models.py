from django.db import models
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField
from group.models import Group
from socle.models import *
from account.models import Student, Teacher, ModelWithCode , User
from django.apps import apps
from django.utils import   timezone
from django.db.models import Q
from random import uniform , randint
from sacado.settings import MEDIA_ROOT
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

def variable_directory_path(instance, filename):
    return "tool/variable_qr/{}".format(filename)

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



class Qrandom(models.Model):
    title      = models.CharField(max_length=50,  blank=True, verbose_name="Titre")
    texte      = RichTextUploadingField(  blank=True, verbose_name="Enoncé")
    knowledge  = models.ForeignKey(Knowledge, related_name="qrandom", blank=True, null = True,  on_delete=models.CASCADE) 
    is_publish = models.BooleanField(default=1, verbose_name="Publié ?")
    teacher    = models.ForeignKey(Teacher, related_name = "qrandom", blank=True,   editable=False ,  on_delete=models.CASCADE)
    ####  type de question
    qtype      = models.PositiveIntegerField(default=2, editable=False)
    calculator = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    tool       = models.BooleanField(default=0, verbose_name="Barre d'outils ?")
    duration   = models.PositiveIntegerField(default=20, blank=True, verbose_name="Durée")


    def __str__(self):
        return self.title


    def instruction(self):

        var_dict = {}
        for v in self.variables.all():
            if v.variable_img.count() > 0 :
                vi_tab = list(v.variable_img.all())
                n_aleatoire = random.randint(0,len(vi_tab)-1)
                variable = "<img src='"+MEDIA_ROOT+"/"+vi_tab[n_aleatoire]+"' width='400px'/>"

            elif v.words :  
                word_tab = v.words.split(";")
                n_aleatoire = random.randint(0,len(word_tab)-1)
                variable =  word_tab[n_aleatoire]
            else :
                if v.is_integer :
                    variable = randint(v.minimum,v.maximum)
                else :
                    variable = uniforme(v.minimum,v.maximum)
            var_dict[v.name] = variable

        txt = self.texte
        for key,value in var_dict.items() :
            txt = txt.replace("__"+str(key)+"__",str(value))

        return txt

            

class Variable(models.Model):

    name  = models.CharField(max_length=50,  blank=True, verbose_name="variable")
    qrandom  = models.ForeignKey(Qrandom, related_name="variables", blank=True, null = True,  on_delete=models.CASCADE)
    ## Variable numérique
    is_integer = models.BooleanField(default=1, verbose_name="Valeur entière ?")        
    maximum = models.IntegerField(default=10)
    minimum = models.IntegerField(default=0)
    ## Variable littérale
    words  = models.CharField(max_length=255,  blank=True, verbose_name="Liste de valeurs")

    def __str__(self):
        return self.name 


class VariableImage(models.Model):

    variable  = models.ForeignKey(Variable, related_name="variable_img", blank=True, null = True,  on_delete=models.CASCADE)
    image  = models.ImageField(upload_to=variable_directory_path,   verbose_name="Image", default="")

    def __str__(self):
        return self.variable.name 




class Question(models.Model):
    """
    Modèle représentant un associé.
    """

    title         = models.TextField(max_length=255, default='',  blank=True, verbose_name="Réponse écrite")
    calculator    = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    date_modified = models.DateTimeField(auto_now=True)
    ####  type de question
    qtype         = models.PositiveIntegerField(default=3, editable=False)
    answer        = models.CharField(max_length=255, null = True,   blank=True, verbose_name="Réponse attendu")

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
    is_numeric   = models.BooleanField(default=0, verbose_name="Type de réponse" )    # réponse sur papier ou sur smartphone
    is_mark      = models.BooleanField(default=0, verbose_name="Récupérer les réponses ?") 
    is_lock      = models.BooleanField(default=0, verbose_name="Verrouiller ?") 
    is_random    = models.BooleanField(default=0, verbose_name="Aléatoire ?") 
    nb_slide     = models.PositiveIntegerField(default=0, editable=False)  # Nombre de diapositive si le quizz est randomisé

    interslide   = models.PositiveIntegerField(default=10, blank=True, verbose_name="Temps entre les questions")


    groups       = models.ManyToManyField(Group, blank=True, related_name="quizz" , editable=False) 
    questions    = models.ManyToManyField(Question, blank=True, related_name="quizz" , editable=False)  
    qrandoms     = models.ManyToManyField(Qrandom, blank=True, related_name="quizz" , editable=False)  
    
    def __str__(self):
        return self.title 


    def quizz_generated(self,group):
        return self.generate_quizz.filter(group=group).order_by("-date_created")




class Generate_quizz(ModelWithCode):
    """
    Modèle qui récupère le quizz de questions aléatoires question par question.
    """
    quizz        = models.ForeignKey(Quizz,  related_name="generate_quizz",  on_delete=models.CASCADE, editable=False) 
    group        = models.ForeignKey(Group,  null=True, blank=True, related_name='generate_quizz', on_delete=models.CASCADE, editable= False)
    date_created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quizz.title 


class Generate_qr(models.Model):
    """
    Modèle qui récupère les questions du quizz généré.
    """
    gquizz       = models.ForeignKey(Generate_quizz,  related_name="generate_qr",  on_delete=models.CASCADE, editable=False) 
    qr_text      = models.TextField( editable=False) 
    ranking      = models.PositiveIntegerField(default = 1 , editable=False)    
 
    def __str__(self):
        return self.qr_text


    def is_correct_answer_quizz_random(self , student) :

        test = False
        quizz_student_answers = self.quizz_student_answers.filter(student = student)
        if quizz_student_answers.count() == 0:
            test = "A"
        else :
            for qsa in quizz_student_answers :
                if quizz_student_answer : 
                    test = quizz_student_answer.is_correct
            
        return test


class Quizz_student_answer(models.Model):
    """
    Modèle qui récupère les réponses numérique.
    """
    qrandom     = models.ForeignKey(Generate_qr, null=True, blank=True, related_name="quizz_student_answers",  on_delete=models.CASCADE, editable=False) # Si le quizz est aléatoire ce champ est complété sinon laissé vide
    question    = models.ForeignKey(Question, null=True, blank=True, related_name="quizz_student_answers",  on_delete=models.CASCADE, editable=False) # Si le quizz est aléatoire ce champ est complété sinon laissé vide
    anwser      = models.CharField( max_length=255, editable=False) 
    is_correct  = models.BooleanField(default=0, editable=False) 
    student     = models.ForeignKey(Student,  related_name="quizz_student_answers",  on_delete=models.CASCADE, editable=False)
    duration    = models.PositiveIntegerField(default=20, blank=True, editable=False) 

    def __str__(self):
        return self.is_correct
 

    class Meta:
        unique_together = ('qrandom', 'student')



 


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
    title      = models.CharField( max_length=255, default="",  verbose_name="Titre") 
    content    = RichTextUploadingField(  default="", verbose_name="Texte ")
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


