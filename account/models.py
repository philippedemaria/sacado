import uuid

import pytz
from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from socle.models import Level, Knowledge, Skill, Subject
from school.models import School

from templated_email import send_templated_mail

# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()

def file_directory_path(instance, filename):
    return "factures/{}/{}".format(instance.user.id, filename)


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
    code = models.CharField(max_length=100, unique=True, blank=True, default=generate_code, verbose_name="Code")

    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Modèle représentant un utilisateur. Possède les champs suivants hérités de la classe AbstractUser :

    first_name : Optional (blank=True). 100 characters or fewer.
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

    STUDENT, PARENT, TEACHER = 0, 1, 2
    USER_TYPES = (
        (STUDENT, "Élève"),
        (PARENT, "Parent"),
        (TEACHER, "Enseignant"),
    )

    CIVILITIES = (
        ('Mme', 'Mme'),
        ('M.', 'M.'),
    )

    TZ_SET = []
    for tz in pytz.common_timezones:
        TZ_SET.append((tz,tz))

    user_type = models.PositiveSmallIntegerField(editable=False, null=True, choices=USER_TYPES)
    civilite = models.CharField(max_length=10, default='M.', blank=True, choices=CIVILITIES, verbose_name="Civilité")
    time_zone = models.CharField(max_length=100, null=True, blank=True, choices=TZ_SET, verbose_name="Fuseau horaire")
    is_extra = models.BooleanField(default=0)
    is_manager = models.BooleanField(default=0)
    school = models.ForeignKey(School, blank=True, null=True, related_name="users", default=None, on_delete = models.PROTECT)
    cgu = models.BooleanField(default=1)
    closure = models.DateTimeField(blank=True, null=True, default = None ,  verbose_name="Date de fin d'adhésion")
    
    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)

    @property
    def is_student(self):
        return self.user_type == self.STUDENT

    @property
    def is_parent(self):
        return self.user_type == self.PARENT

    @property
    def is_teacher(self):
        return self.user_type == self.TEACHER

    @property
    def is_creator(self):
        return self.is_staff == True




class Adhesion(ModelWithCode):
    """docstring for Facture"""
    user = models.ForeignKey(User, blank=True,  null=True, related_name="adhesions", on_delete=models.CASCADE, editable= False)
    file = models.FileField(upload_to=file_directory_path,verbose_name="fichier", blank=True, null= True, default ="", editable= False)
    date_start = models.DateTimeField(auto_now_add=True, verbose_name="Date de création", editable= False)
    date_end = models.DateTimeField( verbose_name="Date de fin", editable= False)
    amount = models.CharField(max_length=10,  verbose_name="Montant", editable= False)
    menu = models.CharField(max_length=50,  verbose_name="Menu", editable= False)
    children = models.PositiveIntegerField( default=1,  verbose_name="Nb enfant", editable= False)
    duration = models.PositiveIntegerField( default=1,  verbose_name="Durée de l'adhésion", editable= False)    

    def __str__(self):
        return "{} {}".format(self.user, self.file)


class Student(ModelWithCode):
    """
    Modèle représentant un élève.
    """
    user = models.OneToOneField(User, blank=True, related_name="student", on_delete=models.CASCADE, primary_key=True)
    level = models.ForeignKey(Level, blank=True, related_name="level_student", default='', on_delete=models.PROTECT, verbose_name="Niveau")
    task_post = models.BooleanField(default=True, verbose_name="Notification de tache ?")

    def __str__(self):
        lname = self.user.last_name.capitalize()
        fname = self.user.first_name.capitalize()

        return "{} {}".format(lname, fname)


    def nb_parcours(self):
        nb = self.students_to_parcours.all().count()
        return nb


    def resultexercises(self):
        ''' résultats de l'étudiant aux exercices '''
        return self.results_e.all().select_related('exercise__knowledge')


    def resultexercises_dict(self):
        ''' dictionnaire des résultats de l'étudiant aux exercices
        cle : exercise_id
        valeur : score de l'étudiant à cet exercice
        '''
        return {exercise_id: point for exercise_id, point in self.results_e.values_list('exercise_id', 'point')}


    def resultexercises_by_theme(self, theme):
        ''' résultats de l'étudiant pour les évaluations de savoirs-faire d'un thème donné'''
        return self.results_e.filter(exercise__theme=theme).select_related('exercise')


    def resultknowledge(self):
        ''' résultats de l'étudiant aux évaluations de savoirs-faire '''
        return self.results_k.all()


    def resultknowledge_dict(self):
        ''' dictionnaire des résultats de l'étudiant aux évaluations de savoirs-faire
        cle : knowledge_id
        valeur : score de l'étudiant pour ce savoir faire
        '''
        return {knowledge_id: point for knowledge_id, point in self.results_k.values_list('knowledge_id', 'point')}


    def resultknowledge_by_theme(self, theme):
        ''' résultats de l'étudiant pour les évaluations de savoirs-faire d'un thème donné'''
        return self.results_k.filter(knowledge__theme=theme)


    def result_skills(self, skill):
        ''' résultats de l'étudiant aux 3 derniers exercices de compétences de la compétence en paramètre'''
        n = 3
        relationships = self.students_relationship.filter(skills = skill).order_by("-id")[:n]
        results = self.results_s.filter(skill=skill).order_by("-id")[:n]

        relationships = list(relationships)
        if len(relationships) < n :
            for i in range( n - len(relationships)  ) :
                relationships.append("")

        results = list(results)
        if len(results) < n :
            for i in range( n - len(results)  ) :
                results.append("")

        data = {}
        data["relationships"] = relationships
        data["results"] = results

        return data





    def bilan_skills(self, skill):
        ''' résultats de l'étudiant aux 3 derniers exercices de compétences de la compétence en paramètre'''
        n = 3
        results = self.results_s.filter(skill=skill).order_by("-id")[:10] 
        nb = len(results) 
        somme , i , coef = 0 , 0, 0
        for r in results:
            coef += 2**(nb-i)
            somme += r.point*2**(nb-i)
            i +=1
        try :
            avg = int(somme/coef)
        except :
            avg = None
        return avg





    def result_waitings(self, waiting):
        ''' résultats de l'étudiant aux 3 derniers exercices '''
        results = self.results_k.filter(knowledge__waiting = waiting).order_by("-id") 
        nb = len(results) 
        somme = 0
        for r in results:
            somme += r.point
        try :
            avg = int(somme/nb)
        except :
            avg = None
        return avg


    def result_skills_custom(self, skill):
        data = {}
        n = 3
        customexercises = self.students_customexercises.filter(skills = skill).order_by("-id")[:n] 
        results = self.student_correctionskill.filter(skill=skill).order_by("-id")[:n] 

        customexercises = list(customexercises)
        if len(customexercises) < n :
            for i in range( n - len(customexercises)  ) :
                customexercises.append("")

        results = list(results)
        if len(results) < n :
            for i in range( n - len(results)  ) :
                results.append("")

        data = {}
        data["customexercises"] = customexercises
        data["results"] = results
        return data


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
 

    def has_customexercise(self, customexercise):
        if self in customexercise.students.all() :
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
        studentanswer = self.students_relationship.order_by("id").last()
        return studentanswer


    def is_task_exists(self,parcours):

        if parcours.is_folder :
            relationships = self.students_relationship.filter(parcours__in = parcours.leaf_parcours.filter(is_publish=1)).exclude(date_limit = None)
        else :
            relationships = self.students_relationship.filter(parcours = parcours).exclude(date_limit = None)

        if len(relationships) == 0 :
            test = False #Aucune tache créée.
        else :
            test =  True #Tache créée.
        som = 0
        for relationship in relationships :
            if self.answers.filter(exercise = relationship.exercise).count()> 0:#Tache effectuée.
                som  +=1
        if len(relationships) == som :
            test = False
 
        return test


    def this_exercise_is_locked(self,exercise, parcours , custom, today):
        
        booleen , test , tst , tsst , tsste   = False , False , False  , False  , False 

        try :
            if parcours.stop < today :
                tst = True
        except :
            pass 
 
        if int(custom) == 1 :
            if self.student_exerciselocker.filter(customexercise = exercise, custom = 1, lock__lt= today ).exists() :
                test = True 

            try :
                if exercise.lock < today :
                    tsst = True
            except :   
                pass 


        else :
            if self.student_exerciselocker.filter(relationship = exercise, custom = 0, lock__lt= today ).exists() :
                test = True

            try :
                if exercise.is_lock :
                    tsste = True       
            except :   
                pass


        if test and (tsst or tst or tsste) :
            booleen = True
 
        return booleen
                

    def is_lock_this_parcours(self,parcours,today):

        
        booleen , test , teest , tst   = False , False , False  , False    

        if parcours.stop < today :
            tst = True 

        nbe = self.students_relationship.filter(parcours=parcours).count()

        nbc = self.students_customexercises.filter(parcourses = parcours).count()
 

        n = 0
        for el in  self.student_exerciselocker.filter(customexercise__parcourses = parcours, custom = 1, lock__gt= today ) :
            n +=1
        if n == nbe :
            teest = True  

        m = 0
        for exl in  self.student_exerciselocker.filter(relationship__parcours = parcours, custom = 0, lock__gt= today ) :
            m +=1
        if m == nbc :
            test = True 



        if tst and (teest or test)  :
            booleen = True
 
        return booleen


class Teacher(models.Model):
    """
    Modèle représentant un enseignant.
    """
    user = models.OneToOneField(User, blank=True, related_name="teacher", on_delete=models.CASCADE,
                                primary_key=True)
    levels = models.ManyToManyField(Level, related_name="levels_to_group", blank=True, verbose_name="Niveaux préférés")
    notification = models.BooleanField(default=1, verbose_name="Réception de notifications ?")
    exercise_post = models.BooleanField(default=1, verbose_name="Réception de notification de création d'exercice ?")
    subjects = models.ManyToManyField(Subject, related_name="teacher", verbose_name="Enseignements")
    is_mailing = models.BooleanField(default=1, verbose_name="Réception de messages ?")


    def __str__(self):
        return f"{self.user.last_name.capitalize()} {self.user.first_name.capitalize()}"

    def notify_registration(self):
        """
        Envoie un email à l'enseignant l'informant de la réussite de son inscription
        """
        if self.user.email != '':
            send_templated_mail(
                template_name="teacher_registration",
                from_email="info@sacado.xyz",
                recipient_list=[self.user.email, ],
                context={"teacher": self.user, }, )


    def notify_registration_to_admins(self):
        """
        Envoie un email aux administrateurs informant de l'inscription d'un nouvel enseignant
        """
        admins = User.objects.filter(is_superuser=1)
        admins_emails = list(admins.values_list('email', flat=True))
        send_templated_mail(
            template_name="teacher_registration_notify_admins",
            from_email="info@sacado.xyz",
            recipient_list=admins_emails,
            context={"teacher": self.user,}, )




    def sacado(self):
        """
        L'enseignant est un membre bénéficiaire de sacado
        """
        sacado_asso = False
        if self.user.school  :
            sacado_asso = True
        return sacado_asso


    def is_creator(self):
        """
        L'enseignant est un membre bénéficiaire de sacado
        """
        creator = False
        if self.user.is_creator  :
            creator = True
        return creator


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
    user = models.OneToOneField(User, blank=True, related_name="parent", on_delete=models.CASCADE, primary_key=True)
    students = models.ManyToManyField(Student, related_name="students_parent", editable=False)
    task_post = models.BooleanField(default=1, verbose_name="Notification de tache ?")

    def __str__(self):
        lname = self.user.last_name.capitalize()
        fname = self.user.first_name.capitalize()

        child = ""
        for s in self.students.all():
            child += s.user.last_name + " " + s.user.first_name + "-"

        return "{} {} - {}".format(lname, fname, child)
