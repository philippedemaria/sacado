import uuid
from django.db import models
from datetime import date, datetime, timedelta
from django.utils import timezone
from account.models import Student, Teacher, ModelWithCode, generate_code
from socle.models import  Knowledge, Level , Theme, Skill 
from django.apps import apps
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
import os.path
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User 
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()
########################################################################################################
########################################################################################################
# cette parties sert à créer un répertoire par user pour sauvegarder les fichiers
 
 
def quiz_directory_path(instance, filename):
    return "ggbfiles/{}/{}".format(instance.level.id, filename)

def image_directory_path(instance, filename):
    return "ggbimages/{}/{}".format(instance.level.id, filename)

def vignette_directory_path(instance, filename):
    return "vignettes/{}/{}".format(instance.teacher.user.id, filename)


def file_directory_path(instance, filename):
    return "files/{}/{}".format(instance.relationship.parcours.teacher.user.id, filename)


 
def directory_path(instance, filename):
    return "demandfiles/{}/{}".format(instance.level.id, filename)

def file_attach_path(instance, filename):
    return "attach_files/{}/{}".format(instance.level.id, filename)


def convert_time(duree) :
    d = int(duree)
    if d < 59 :
        return duree+"s"
    elif d < 3600:
        s = d%60        
        m = int((d-s)/60)
        return str(m)+"min "+str(s)+"s"
    else :
        return  "td" #temps dépassé





########################################################################################################
########################################################################################################




class Supportfile(models.Model):

    knowledge = models.ForeignKey(Knowledge, on_delete=models.PROTECT,  related_name='supportfiles', verbose_name="Savoir faire associé - Titre")
    annoncement = models.TextField( verbose_name="Précision sur le savoir faire")
    author = models.ForeignKey(Teacher, related_name="supportfiles", on_delete=models.PROTECT, editable=False)

 
    code = models.CharField(max_length=100, unique=True, blank=True, default='', verbose_name="Code*")
    #### pour validation si le qcm est noté

    situation = models.PositiveIntegerField(default=10, verbose_name="Nombre minimal de situations", help_text="Pour valider le qcm")
    calculator = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    #### pour donner une date de remise
 
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    level = models.ForeignKey(Level, related_name="supportfiles", on_delete=models.PROTECT, verbose_name="Niveau")
    theme = models.ForeignKey(Theme, related_name="supportfiles", on_delete=models.PROTECT, verbose_name="Thème")

    width = models.PositiveIntegerField(default=750, verbose_name="Largeur")
    height = models.PositiveIntegerField(default=550, verbose_name="Hauteur")
    ggbfile = models.FileField(upload_to=quiz_directory_path, verbose_name="Fichier ggb", default="")
    imagefile = models.ImageField(upload_to=image_directory_path, verbose_name="Vignette d'accueil", default="")

    toolBar = models.BooleanField(default=0, verbose_name="Barre des outils ?")
    menuBar = models.BooleanField(default=0, verbose_name="Barre de menu ?")
    algebraInput = models.BooleanField(default=0, verbose_name="Multi-fenêtres ?")
    resetIcon = models.BooleanField(default=0, verbose_name="Bouton Reset ?")
    dragZoom = models.BooleanField(default=0, verbose_name="Zoom/déplacement ?")

    is_title = models.BooleanField(default=0, editable=False, verbose_name="titre pour l'organisation des parcours")
    is_subtitle = models.BooleanField(default=0 , verbose_name="sous-titre pour l'organisation des parcours")
    attach_file = models.FileField(upload_to=file_attach_path, blank=True,  verbose_name="Fichier pdf attaché", default="")

    duration = models.PositiveIntegerField(default=15, blank=True, verbose_name="Durée estimée - en minutes")
    skills = models.ManyToManyField(Skill, blank=True, related_name='skills_supportfile', verbose_name="Compétences ciblées")

    def __str__(self): 
        knowledge = self.knowledge.name[:20]       
        return "{} > {} > {}".format(self.level.name, self.theme.name, knowledge)

    def levels_used(self):
        return self.exercises.select_related('level')



 
    def in_folder(self) :

        folder_path = "/home/c1398844c/sacado/media/"
        data = {}
        #folder_path  = "D:/uwamp/www/sacadogit/sacado/media/"
        
        if os.path.isfile(folder_path+str(self.ggbfile)):
            data["file_in_folder"] = True
        else:
            data["file_in_folder"] = False

        if os.path.isfile(folder_path+str(self.imagefile)):
            data["image_in_folder"] = True
        else:
            data["image_in_folder"] = False
        return data



    def used_in_parcours(self, teacher):
        exercises = self.exercises.all()
        parcours = Parcours.objects.filter(exercises__in= exercises, author=teacher)
        return parcours



 



class Exercise(models.Model):
    level = models.ForeignKey(Level, related_name="exercises", on_delete=models.PROTECT, verbose_name="Niveau")
    theme = models.ForeignKey(Theme, related_name="exercises", on_delete=models.PROTECT, verbose_name="Thème")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.PROTECT, related_name='exercises',
                                  verbose_name="Savoir faire associé - Titre")
    supportfile = models.ForeignKey(Supportfile, blank=True, default=1, related_name="exercises",
                                    on_delete=models.PROTECT, verbose_name="Fichier Géogebra")
 

    def __str__(self):
        return "{}".format(self.knowledge.name)

    class Meta:
        unique_together = ('knowledge', 'supportfile')


    def send_score(self, student):
        try:
            r = Resultexercise.objects.get(student=student, exercise=self)
            return int(r.point)
        except:
            return ""


    #############################################
    # non utilisée ?????? 
    def send_scores(self, student_id):
        score = ""
        student = Student.objects.get(pk=student_id)
        if Studentanswer.objects.filter(student=student).filter(exercise=self.pk).exists():
            studentanswers = Studentanswer.objects.filter(student=student, exercise=self.pk)
            for studentanswer in studentanswers:
                score = score + str(studentanswer.point) + " - "
        return score
    ############################################# 

    def score_and_time(self, student_id):
        scores_times_tab = []
        student = Student.objects.get(pk=student_id)
        if Studentanswer.objects.filter(student=student).filter(exercise=self.pk).exists():
            studentanswers = Studentanswer.objects.filter(student=student, exercise=self.pk)
            for studentanswer in studentanswers:
                scores_times = {}
                scores_times["score"] = studentanswer.point
                scores_times["time"] = convert_time(studentanswer.secondes)
                scores_times["numexo"] = studentanswer.numexo
                scores_times["date"] = studentanswer.date
                scores_times_tab.append(scores_times)
        return scores_times_tab





    def details(self, parcours):
        details, tab = {}, []
        somme = 0
        for student in parcours.students.all():
            try:
                studentanswer = Studentanswer.objects.filter(student=student, exercise=self, parcours=parcours).last()
                somme += studentanswer.point
                tab.append(studentanswer.point)
            except:
                pass

        try:
            avg = somme / len(tab)
            tab.sort()
            details["min"] = tab[0]
            details["max"] = tab[-1]
            details["avg"] = int(avg)
        except:
            details["min"] = 0
            details["max"] = 0
            details["avg"] = 0

        return details


    def last_score_and_time(self, parcours, student_id):
        student = Student.objects.get(pk=student_id)
        scores_times = {}
        if Studentanswer.objects.filter(student=student).filter(exercise=self.pk, parcours=parcours).exists():
            studentanswer = Studentanswer.objects.filter(student=student, exercise=self.pk, parcours=parcours).last()
            scores_times["score"] = studentanswer.point
            scores_times["time"] = convert_time(studentanswer.secondes)
        else :
            scores_times["score"] = None
            scores_times["time"] = None


        return scores_times


    def timer(self, parcours, student_id):
        reponse, datetime_object = "", ""
        student = Student.objects.get(pk=student_id)
        if Studentanswer.objects.filter(student=student).filter(exercise=self.pk, parcours=parcours).exists():
            studentanswer = Studentanswer.objects.filter(student=student, exercise=self.pk).last()
            reponse = int(studentanswer.secondes)
            if reponse > 59:
                minutes = int(reponse / 60)
                scdes = reponse % 60

                datetime_object = str(minutes) + "min" + str(scdes) + "s"
            else:
                datetime_object = str(reponse) + " s"
        return datetime_object


    def is_selected(self, parcours):
        relationship = Relationship.objects.filter(parcours=parcours, exercise=self)
        return relationship.count() == 1


 

    def is_relationship(self ,parcours):
        try:
            relationship = Relationship.objects.get(parcours=parcours, exercise=self)
        except:
            relationship = False
        return relationship


    def used_in_parcours(self, teacher):
        parcours = Parcours.objects.filter(exercises=self, author=teacher)
        return parcours



    def is_used(self):
        '''
        Vérifie si l'exercice a été associé à un parcours
        '''
        return Relationship.objects.filter(exercise=self).exists()


    def is_done(self,student):
        return Studentanswer.objects.filter(student=student, exercise=self).exists()


    def nb_task_done(self, group):
        try:
            studentanswer_tab = []
            for s in group.students.all():
                studentanswer = Studentanswer.objects.filter(exercise=self, student=s).first()
                if studentanswer:
                    studentanswer_tab.append(studentanswer)
            nb_task_done = len(studentanswer_tab)
        except:
            nb_task_done = 0
        return nb_task_done


    def who_are_done(self, group):
        studentanswer_tab = []
        try:
            for s in group.students.all():
                studentanswer = Studentanswer.objects.filter(exercise=self, student=s).first()
                if studentanswer:
                    studentanswer_tab.append(studentanswer)
        except:
            pass
        return studentanswer_tab


    def nb_task_parcours_done(self, parcours):
        studentanswer_tab = []
        for s in parcours.students.all():
            studentanswer = Studentanswer.objects.filter(exercise=self, student=s).first()
            if studentanswer:
                studentanswer_tab.append(studentanswer)
        nb_task_done = len(studentanswer_tab)
        return nb_task_done



    def who_are_done_parcours(self,parcours):
        studentanswer_tab = []
        for s in parcours.students.all():
            studentanswer = Studentanswer.objects.filter(exercise = self, student = s).first()
            if studentanswer :
                studentanswer_tab.append(studentanswer)
        return studentanswer_tab



    def percent_student_done_parcours_exercice(self,parcours,students_from_p_or_g):

        students = students_from_p_or_g
        nb_student = len(students)

        nb_exercise_done = Studentanswer.objects.filter(student__in= students, parcours= parcours, exercise = self).values_list("student",flat= True).order_by("student").distinct().count()
 
        try :
            percent = int(nb_exercise_done * 100/nb_student)
        except : 
            percent = 0
        data = {}
        data["nb"] = nb_student
        data["percent"] = percent
        data["nb_done"] = nb_exercise_done
        return data


    def levels_used(self):

        exercises = Exercise.objects.filter(level=self.supportfile)
        return exercises


    def my_parcours_container(self, teacher):

        parcours = self.exercises_parcours.filter(teacher=teacher)
        return parcours


class Parcours(ModelWithCode):

    title = models.CharField(max_length=255, verbose_name="Titre")
    color = models.CharField(max_length=255, default='#00819F', verbose_name="Couleur")
    author = models.ForeignKey(Teacher, related_name="author_parcours", on_delete=models.PROTECT, default='', blank=True, null=True, verbose_name="Auteur")
    teacher = models.ForeignKey(Teacher, related_name="teacher_parcours", on_delete=models.PROTECT, default='', blank=True, editable=False)

    exercises = models.ManyToManyField(Exercise, blank=True, through="Relationship", related_name="exercises_parcours")
    students = models.ManyToManyField(Student, blank=True, related_name='students_to_parcours', verbose_name="Elèves")
    is_share = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
    is_archive = models.BooleanField(default=0, verbose_name="Archivé ?", editable=False)

    level = models.ForeignKey(Level, related_name="level_parcours", on_delete=models.PROTECT, default='', blank=True, null=True, editable=False)
    linked = models.BooleanField(default=0, editable=False)
    is_favorite = models.BooleanField(default=1, verbose_name="Favori ?")

    is_evaluation = models.BooleanField(default=0, editable=False)
    duration = models.PositiveIntegerField(default=2, blank=True, verbose_name="Temps de chargement (min.)")
    start = models.DateField(null=True, blank=True, verbose_name="Date de début de publication")
    starter = models.TimeField(null=True, blank=True, verbose_name="Heure de début de publication")
    stop = models.DateField(null=True, blank=True, verbose_name="Date de fin de publication")
    stopper = models.TimeField(null=True, blank=True, verbose_name="Heure de fin de publication")

    vignette = models.ImageField(upload_to=vignette_directory_path, verbose_name="Vignette d'accueil", blank=True, default ="")
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)

    def __str__(self):
        return "{}".format(self.title)


    def is_done(self,student):
        Studentanswer = apps.get_model('qcm', 'Studentanswer')
        exercises = self.exercises.all()
        n = 0
        exercise_done = []
        for e in exercises:
            if not e in exercise_done:
                if Studentanswer.objects.filter(student=student, exercise=e).exists():
                    n += 1
        return n

    def is_affect(self, student):
        nb_relationships = Relationship.objects.filter(parcours=self, exercise__supportfile__is_title=0,
                                                       students=student, is_publish=1).count()
        return nb_relationships




    def is_percent(self,student):
        ## Nombre de relationships dans le parcours => nbre  d'exercices
        nb_relationships =  Relationship.objects.filter(students = student, parcours=self,is_publish=1).count()
        ## Nombre de réponse avec exercice unique du parcours
        studentanswers = Studentanswer.objects.filter(student=student, parcours=self).values_list("exercise",flat=True).order_by("exercise").distinct()
           
        nb_exercise_done = len(studentanswers) 
        try :
            percent = int(nb_exercise_done * 100/nb_relationships)
        except :
            percent = 0
        return percent


    def nb_exercises(self):
        nb = self.exercises.filter(supportfile__is_title=0).count()
        return nb 


    def exercises_only(self):
        exercises = self.exercises.filter(supportfile__is_title=0).prefetch_related('level')
        return exercises 


    def level_list(self):
        
        exercises = self.exercises.filter(supportfile__is_title=0).prefetch_related("level").order_by("level")
        exercises_level_tab = []
        for e  in exercises :
            if e.level not in exercises_level_tab:
                exercises_level_tab.append(e.level)
        return exercises_level_tab


    def duration_overall(self):
        som = self.duration
        for d in self.parcours_relationship.values_list('duration',flat=True):
            som += d
        return som 

    def level_by_exercises(self):
        
        exercises = self.exercises.filter(supportfile__is_title=0).prefetch_related("level").order_by("level")
        dct , tab =  {} , [] 
        for l in Level.objects.all():
            dct[l.shortname] = 0
        for e  in exercises :
            dct[e.level.shortname] +=1
        tab = []
        for k, v in sorted(dct.items(), key=lambda x: x[1]):
            name = k
        return name


    def group_list(self):
        students = self.students.all() 
        group_tab = []
        for s  in students :
            groups = s.students_to_group.filter(teacher = self.teacher)
            for group  in groups :
                if group not in group_tab:
                    group_tab.append(group)       
        return group_tab 

    def parcours_shared(self):

        students = self.students.all() #Elève d'un parcours
        shared = False
        for s  in students :
            if len(s.students_to_group.all()) > 1 :
                shared = True
                break
        return shared



    def parcours_group_students_count(self,group):

        data = {}
        group_students = group.students.all()
        parcours_students = self.students.all()
        intersection = list(set(group_students) & set(parcours_students))

        data["nb"]= len(intersection)
        data["students"] = intersection
        return data 


 
    def is_task_exists(self):

        today = timezone.now()
        test = False
        if Relationship.objects.filter(parcours= self,date_limit__gte = today).count() > 0 :
            test = True
        return test 

 
    def is_individualized(self):

        test = False
        nb_students_parcours = self.students.count() # élève du parcours
        relation_ships = self.parcours_relationship.all()
        for r in relation_ships :
            if r.students.count() != nb_students_parcours :
                test = True 
        return test 


 
    def is_courses_exists(self):

        test = False
        if self.course.count() > 0 :
            test = True
        return test 




    def nb_task(self):

        today = timezone.now()
        nb = self.parcours_relationship.filter(date_limit__gte = today).count()
        return nb


    def evaluation_duration(self):

        relationships = self.parcours_relationship.all()
        som = self.duration
        for r in relationships : 
            som += r.duration
        return som 



class Relationship(models.Model):
    exercise = models.ForeignKey(Exercise,  null=True, blank=True,   related_name='exercise_relationship', on_delete=models.PROTECT,  editable= False)
    parcours = models.ForeignKey(Parcours, on_delete=models.PROTECT,  related_name='parcours_relationship',  editable= False)
    order = models.PositiveIntegerField(default=0, editable=False)
    is_publish = models.BooleanField(default=1)
    start = models.DateField(null=True, blank=True, verbose_name="A partir de")
    date_limit = models.DateField(null=True, blank=True, verbose_name="Date limite du rendu")
    is_evaluation = models.BooleanField(default=0)
    duration = models.PositiveIntegerField(default=15, verbose_name="Durée estimée en minutes")
    situation = models.PositiveIntegerField(default=10, verbose_name="Nombre minimal de situations", help_text="Pour valider le qcm")
    beginner = models.TimeField(null=True, blank=True, verbose_name="Heure du début")
    skills = models.ManyToManyField(Skill, blank=True, related_name='skills_relationship', editable=False)
    students = models.ManyToManyField(Student, blank=True, related_name='students_relationship', editable=False)

    def __str__(self):
        return "{} : {}".format(self.parcours, self.exercise)

    class Meta:
        unique_together = ('exercise', 'parcours')


    def score_student_for_this(self,student):
        studentanswer = Studentanswer.objects.filter(student=student, parcours= self.parcours , exercise = self.exercise ).last()
        return studentanswer



    def is_done(self,student):
        done = False
        if Studentanswer.objects.filter(student=student, exercise = self.exercise, parcours= self.parcours ).exists():
            done = True
        return done

    def is_task(self):
        task = False
        today = timezone.now().date()
        try :
            if self.date_limit >= today:
                task = True
        except :
            task = False
        return task



    def constraint_to_this_relationship(self,student): # Contrainte. 
    
        under_score = True # On suppose que l'élève n'a pas obtenu le score minimum dans les exercices puisqu'il ne les a pas fait. 
        constraints = Constraint.objects.filter(relationship = self).select_related("relationship__exercise")
        somme = 0
        for constraint in constraints : # On étudie si les contraignants ont un score supérieur à score Min
            exercises = Exercise.objects.filter(supportfile__code = constraint.code)
            if Studentanswer.objects.filter(student=student, exercise__in = exercises, parcours= self.parcours, point__gte= constraint.scoremin ).exists():
                somme += 1
        if somme == len(constraints): # Si l'élève a obtenu les minima à chaque exercice
            under_score = False # under_score devient False

        return under_score  


########################################################################################################################################### 
########################################################################################################################################### 
######################################################### FIN  Types de question ########################################################## 
########################################################################################################################################### 
########################################################################################################################################### 


class Studentanswer(models.Model):

    parcours = models.ForeignKey(Parcours,  on_delete=models.PROTECT, blank=True, null=True,  related_name='answers', editable=False)
    exercise = models.ForeignKey(Exercise,  on_delete=models.PROTECT, blank=True,  related_name='ggbfile_studentanswer', editable=False) 
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='answers', editable=False)
    point  = models.PositiveIntegerField(default=0 )  
    numexo  = models.PositiveIntegerField(default=10 )  
    date = models.DateTimeField(auto_now_add=True)
    secondes = models.CharField(max_length=255, editable=False)

    def __str__(self):        
        return "{}".format(self.exercise.knowledge.name)


class Resultexercise(models.Model):  # Last result

    student = models.ForeignKey(Student, related_name="results_e", default="",
                                on_delete=models.CASCADE, editable=False)
    exercise = models.ForeignKey(Exercise, related_name="results_e",
                                 on_delete=models.PROTECT, editable=False)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}".format(self.point)

    class Meta:
        unique_together = ['student', 'exercise']


########################################################################################################################################### 
########################################################################################################################################### 
######################################################### FIN  Types de question ########################################################## 
########################################################################################################################################### 
########################################################################################################################################### 

 
class Remediation(models.Model):

    title = models.CharField(max_length=255, default='',  blank=True,verbose_name="Titre")
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, default='',   blank=True, related_name='relationship_remediation') 
    video = models.CharField(max_length=255, default='',  blank=True,  verbose_name="url de la vidéo")
    mediation = models.FileField(upload_to=file_directory_path,verbose_name="Fichier - pdf", blank=True, default ="")
    sort = models.BooleanField( default=0,    verbose_name="Type du document") 
    duration = models.PositiveIntegerField(  default=15,   verbose_name="Durée estimée (en min.)")  

    def __str__(self):        
        return "title {}".format(self.title)

 
class Constraint(models.Model):

    code = models.CharField(max_length=8, default='', editable=False)# code de l'exo qui constraint
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, default='',   blank=True, related_name='relationship_constraint') 
    scoremin = models.PositiveIntegerField(  default=80, editable=False)  


    def __str__(self):        
        return "{} à {}%".format(self.code , self.scoremin)


########################################################################################################################################### 
########################################################################################################################################### 
################################################################   Cours    ############################################################### 
########################################################################################################################################### 
########################################################################################################################################### 

class Course(models.Model): # pour les 

    parcours = models.ForeignKey(Parcours,  on_delete=models.PROTECT, blank=True, null=True,  related_name='course', editable=False) 
    title = models.CharField(max_length=50, default='',  blank=True, verbose_name="Titre")    
    annoncement = RichTextUploadingField( blank=True, verbose_name="Texte*") 
    teacher = models.ForeignKey(Teacher, related_name = "course", on_delete=models.PROTECT, editable=False )
    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée de lecture")  

    is_publish = models.BooleanField( default= 0, verbose_name="Publié ?")
    publish_start = models.DateField(default=timezone.now,  blank=True, max_length=255, verbose_name="Début à", help_text="Changer les dates des cours peut remplacer les réglages de leur durée de disponibilité et leur placement dans les pages de cours ou le tableau de bord. Veuillez confirmer les dates d’échéance avant de modifier les dates des cours. ")
    publish_end = models.DateField( blank=True, null=True,  max_length=255, verbose_name="Se termine à")


    ranking = models.PositiveIntegerField(  default=1,  blank=True, null=True,  verbose_name="Ordre") 
    
    is_task = models.BooleanField( default=0,    verbose_name="Tache à rendre ?") 
    is_paired = models.BooleanField( default=0,    verbose_name="Elèves créateurs ?") 
    is_active = models.BooleanField( default=0,  verbose_name="Contenu en cours")  

 
    date_limit = models.DateTimeField( null=True, blank=True, verbose_name="Date limite du rendu")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification") 

    notification = models.BooleanField( default=0,  verbose_name="Informer des modifications ?", help_text="Envoie un message aux participants." )     
 
    students = models.ManyToManyField(Student, blank=True,  related_name='students_course', verbose_name="Attribuer à/au")
    creators = models.ManyToManyField(Student, blank=True,  related_name='creators_course', verbose_name="Co auteurs élève") 

 
    def __str__(self):
        return self.parcours.title 



########################################################################################################################################### 
########################################################################################################################################### 
########################################################   Demande d'exo    ############################################################### 
########################################################################################################################################### 
########################################################################################################################################### 


class Demand(models.Model):
    level = models.ForeignKey(Level, related_name="demand", on_delete=models.PROTECT, verbose_name="Niveau")
    theme = models.ForeignKey(Theme, related_name="demand", on_delete=models.PROTECT, verbose_name="Thème")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.PROTECT, related_name='demand', verbose_name="Savoir faire associé - Titre")
    demand = models.TextField(blank=True, verbose_name="Votre demande explicitée*")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    file = models.FileField(upload_to= directory_path, verbose_name="Exercice souhaité", default="", null = True, blank= True) 
    teacher = models.ForeignKey(Teacher, related_name = "demand", on_delete=models.PROTECT, editable=False, default="" )    
    done = models.BooleanField( default=0,  verbose_name="Fait", null = True, blank= True) 
    code = models.CharField(max_length=10, default='',  blank=True, null=True,  verbose_name="id de l'exercice créé")    

    def __str__(self):
        return "{}".format(self.demand)