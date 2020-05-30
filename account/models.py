import uuid
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.apps import apps
from socle.models import Level, Knowledge,Skill


import pytz
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()

def generate_code():
    '''
    Fonction qui génère un code pour les modèles suivantes :
    - Parcours
    - Group
    - Student
    - Supportfile
    '''
    return str(uuid.uuid4())[:8]


class ModelWithCode(models.Model):
    '''
    Ajoute un champ code à un modèle
    '''
    code = models.CharField(max_length=100, unique=True, blank=True, default=generate_code, verbose_name="Code du parcours*")

    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Modèle représentant un utilisateur. Possède les champs suivants hérités de la classe AbstractUser :

    first_name : Optional (blank=True). 30 characters or fewer.
    last_name : Optional (blank=True). 150 characters or fewer.
    email : Optional (blank=True). Email address.
    password : Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password.)
    groups : Many-to-many relationship to Group
    user_permissions : Many-to-many relationship to Permission
    is_staff : Boolean. Designates whether this user can access the admin site.
    is_active : Boolean. Designates whether this user account should be considered active.
    is_superuser : Boolean. Designates that this user has all permissions without explicitly assigning them.
    last_login : A datetime of the user’s last login.
    date_joined : A datetime designating when the account was created. Is set to the current date/time by default when the account is created.

    """
 
    #### user_type = 0 for student, 2 for teacher, 2 + is_superuser for admin,  5 for superuser


    CIVILITIES = (
        ('Mme', 'Mme'),
        ('M.', 'M.'),
    )
    TZ_SET = []
    for tz in pytz.common_timezones :
        TZ_SET.append((tz,tz))
 

    user_type = models.PositiveSmallIntegerField(editable=False)
    civilite = models.CharField(max_length=10, default='M.', blank=True,  choices=CIVILITIES, verbose_name="Civilité")
    time_zone = models.CharField(max_length=100, null=True, blank=True,  choices=TZ_SET, verbose_name="Fuseau horaire")
    is_extra = models.BooleanField( default=0 , editable=0)


    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)



class Student(ModelWithCode):
    """
    Modèle représentant un élève.
    """
    user = models.OneToOneField(User, blank=True,  related_name="user_student",  on_delete=models.CASCADE, primary_key=True)
    level = models.ForeignKey(Level, blank=True, related_name = "level_student", default='' , on_delete=models.PROTECT,    verbose_name="Niveau") 
    task_post = models.BooleanField( default=1 ,    verbose_name="Notification de tache ?") 


    def __str__(self):
        lname  = self.user.last_name.capitalize() 
        fname  = self.user.first_name.capitalize() 

        return "{} {}".format(lname, fname)

 
    def nb_parcours(self):

        nb =  self.students_to_parcours.all().count()
        return nb
 


    def resultexercises(self):
        return self.results_e.all().select_related('exercise__knowledge')

    def resultexercisesdict(self):
        return {exercise_id: score for exercise_id, score in self.results_e.values_list('exercise_id', 'point')}


    def resultexercises_by_theme(self,theme):

        return self.results_e.filter(exercise__theme=theme).select_related('exercise')



    def resultknowledge(self):
        ''' résultats de l'étudiant aux évaluations de savoirs-faire '''
        return self.results_k.all()

    def resultknowledgedict(self):
        ''' dictionnaire des résultats de l'étudiant aux évaluations de savoirs-faire
        cle : knowledge_id
        valeur : score de l'étudiant pour ce savoir faire
        '''
        return {knowledge_id: score for knowledge_id, score in self.results_k.values_list('knowledge_id', 'point')}

    def resultknowledge_by_theme(self, theme):
        ''' résultats de l'étudiant pour les évaluations de savoirs-faire d'un thème donné'''
        return self.results_k.filter(knowledge__theme=theme)



    def result_skills(self, skill):
        ''' résultats de l'étudiants aux 5 dernières évaluations de compétences de la compétence en paramètre'''
        return self.results_s.filter(skill=skill).order_by("-id")[:5]



    def knowledge_average(self, group):

        Resultknowledge = apps.get_model('account', 'Resultknowledge')
        knowledges = group.level.knowledges.all()
        resultknowledges = Resultknowledge.objects.filter(student = self, knowledge__in=knowledges) 
        nb = len(resultknowledges)
        somme = 0

        for r in resultknowledges:
            somme += r.point
        try :
            avg = int(somme/nb)
        except :
            avg = ""
        return avg


    def nb_knowledge_worked(self, group):

        Resultknowledge = apps.get_model('account', 'Resultknowledge')
        Relationship = apps.get_model('qcm', 'Relationship')

        relationships = Relationship.objects.filter(students = self).values_list("exercise__knowledge__id").order_by("exercise__knowledge__id").distinct()
            
        n = relationships.count()
        knowledges = group.level.knowledges.all()

        nb = Resultknowledge.objects.filter(student = self, knowledge__in=knowledges).count()

        return  str(nb)+"/"+str(n) 


    def is_in_parcours(self, parcours):

        if self in parcours.students.all() :
            test =  True
        else :
            test = False

        return test

    def has_exercise(self, relationship):
        if self in relationship.students.all() :
            test =  True
        else :
            test = False
        return test
 

    def suiviparent(self):
        test = False
        groups = self.students_to_group.all()
        for group in groups :
            if group.suiviparent :
                test = True
                break
        return test


    def last_exercise(self):
        Studentanswer = apps.get_model('qcm', 'Studentanswer')
        studentanswer = Studentanswer.objects.filter(student=self).order_by("id").last()
        return studentanswer



    def is_task_exists(self,parcours):
        Studentanswer = apps.get_model('qcm', 'Studentanswer')
        Relationship = apps.get_model('qcm', 'Relationship')
        relationships = Relationship.objects.filter(exercise__students = self, parcours = parcours).exclude(date_limit = None)

        test =  False # Aucune tache.
        for relationship in relationships :
            if Studentanswer.objects.filter(student=self, exercise = relationship.exercise).count()== 0:
                test = True 
 
        return test






class Teacher(models.Model):
    """
    Modèle représentant un enseignant.
    """
    user = models.OneToOneField(User, blank=True, related_name="user_teacher", on_delete=models.CASCADE, primary_key=True)
    levels = models.ManyToManyField(Level, related_name="levels_to_group", blank=True,  verbose_name="Niveaux préférés")
    notification = models.BooleanField( default=1 ,    verbose_name="Notification ?") 
    exercise_post = models.BooleanField( default=1 ,    verbose_name="Notification de création d'exercice ?") 



    def __str__(self):
        return "{} - {} {}".format(self.user.username  , self.user.first_name.capitalize() , self.user.last_name.capitalize() )



class Resultknowledge(models.Model):
    student = models.ForeignKey(Student, related_name="results_k", default="", on_delete=models.CASCADE, editable=False)
    knowledge = models.ForeignKey(Knowledge, related_name="results_k", on_delete=models.CASCADE, editable=False)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}".format(self.point)

    class Meta:
        unique_together = ['student', 'knowledge']



class Resultskill(models.Model): # Pour récupérer tous les scores des compétences
    student = models.ForeignKey(Student, related_name="results_s", default="", on_delete=models.CASCADE, editable=False)
    skill = models.ForeignKey(Skill, related_name="results_s", on_delete=models.CASCADE, editable=False)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.skill} : {self.point}"




class Resultlastskill(models.Model): # Pour récupérer la moyenne des 10 derniers score des compétences
    student = models.ForeignKey(Student,   related_name = "student_resultskill", default="", on_delete=models.CASCADE, editable=False)
    skill = models.ForeignKey(Skill,   related_name = "student_resultskill", on_delete=models.CASCADE, editable=False)
    point  = models.PositiveIntegerField(default=0 ) 

    def __str__(self):
        return "{} : {}".format(self.skill, self.point)  


    class Meta:
        unique_together = ['student', 'skill']
 



class Parent(models.Model):
    """
    Modèle représentant un parent.
    """
    user = models.OneToOneField(User, blank=True,  related_name="user_parent", on_delete=models.CASCADE, primary_key=True)
    students = models.ManyToManyField(Student, related_name="students_parent", editable = False)
    task_post = models.BooleanField( default=1 ,    verbose_name="Notification de tache ?") 

    def __str__(self):
        lname  = self.user.last_name.capitalize() 
        fname  = self.user.first_name.capitalize()

        child = ""
        for s in self.students.all():
            child += s.user.last_name+" "+s.user.first_name+ "-" 

        return "{} {} - {}".format(lname, fname, child)

 