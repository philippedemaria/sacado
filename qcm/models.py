import uuid
from django.db import models
from datetime import date, datetime, timedelta
from django.utils import timezone
from account.models import Student, Teacher, ModelWithCode, generate_code
from socle.models import  Knowledge, Level , Theme, Skill
from django.apps import apps
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import   timezone
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

    knowledge = models.ForeignKey(Knowledge, on_delete=models.PROTECT,  related_name='knowledge_ggbfile', verbose_name="Savoir faire associé - Titre")   
    annoncement = models.TextField( verbose_name="Précision sur le savoir faire") 
    author = models.ForeignKey(Teacher, related_name = "author_ggbfile", on_delete=models.PROTECT,  editable=False)

 
    code = models.CharField(max_length=100, unique=True, blank=True, default='', verbose_name="Code*")
    #### pour validation si le qcm est noté
 
    situation = models.PositiveIntegerField(default = 10, verbose_name="Nombre minimal de situations", help_text="Pour valider le qcm")    
    calculator = models.BooleanField( default=0,    verbose_name="Calculatrice ?") 
    #### pour donner une date de remise
 
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")   
       
    level = models.ForeignKey(Level, related_name = "level_ggbfile", on_delete=models.PROTECT,    verbose_name="Niveau") 
    theme = models.ForeignKey(Theme,    related_name = "theme_ggbfile", on_delete=models.PROTECT,  verbose_name="Thème") 

    width = models.PositiveIntegerField(default = 750 , verbose_name="Largeur")
    height = models.PositiveIntegerField(default = 550 , verbose_name="Hauteur") 
    ggbfile = models.FileField(upload_to=quiz_directory_path,verbose_name="Fichier ggb", default ="")
    imagefile = models.ImageField(upload_to=image_directory_path, verbose_name="Vignette d'accueil", default ="")

    toolBar = models.BooleanField( default=0,    verbose_name="Barre des outils ?") 
    menuBar = models.BooleanField( default=0,  verbose_name="Barre de menu ?")  
    algebraInput = models.BooleanField( default=0,    verbose_name="Multi-fenêtres ?") 
    resetIcon = models.BooleanField( default=0,    verbose_name="Bouton Reset ?") 
    dragZoom = models.BooleanField( default=0,    verbose_name="Zoom/déplacement ?") 

    is_title = models.BooleanField( default=0, editable=False,   verbose_name="titre pour l'organisation des parcours") 
    is_subtitle = models.BooleanField( default=0, editable=False,   verbose_name="sous-titre pour l'organisation des parcours")

    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée - en minutes")   
    skills = models.ManyToManyField(Skill,  blank=True,  related_name='skills_supportfile',verbose_name="Compétences ciblées" ) 

    def __str__(self): 
        knowledge = self.knowledge.name[:20]       
        return "{} > {} > {}".format(self.level.name, self.theme.name, knowledge)


    def levels_used(self):

        exercises = Exercise.objects.filter(supportfile = self)
        return exercises


 




class Exercise(models.Model):

    knowledge = models.ForeignKey(Knowledge, on_delete=models.PROTECT,  related_name='knowledge_exercise', verbose_name="Savoir faire associé - Titre")   
    students = models.ManyToManyField(Student, blank=True,  related_name='students_exercise', verbose_name="Travail fait") 
    level = models.ForeignKey(Level, related_name = "level_exercise", on_delete=models.PROTECT,    verbose_name="Niveau") 
    theme = models.ForeignKey(Theme,    related_name = "theme_exercise", on_delete=models.PROTECT,  verbose_name="Thème") 
    supportfile = models.ForeignKey(Supportfile, blank=True,  default=1,  related_name = "supportfile_exercise", on_delete=models.PROTECT,  verbose_name="Fichier Géogebra") 
 
   
    def __str__(self):        
        return "{}".format(self.knowledge.name)


    class Meta:
        unique_together = ('knowledge', 'supportfile')




    def send_score(self,student):
        try :
            r = Resultexercise.objects.get(student = student, exercise = self)
            score = int(r.point)
        except :
            score ="" 
        return score

    #############################################
    # non utilisée ?????? 
    def send_scores(self,student_id):
        score = ""
        student = Student.objects.get(pk=student_id)
        if Studentanswer.objects.filter(student = student).filter(exercise = self.pk).exists() :
            studentanswers =  Studentanswer.objects.filter(student = student,exercise = self.pk)
            for studentanswer in studentanswers :
                score = score+str(studentanswer.point)+" - " 
        return score
    ############################################# 


    def score_and_time(self,student_id):
        scores_times_tab = []
        student = Student.objects.get(pk=student_id)
        if Studentanswer.objects.filter(student = student).filter(exercise = self.pk).exists() :
            studentanswers =  Studentanswer.objects.filter(student = student,exercise = self.pk)
            for studentanswer in studentanswers :
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
        for student in parcours.students.all() :
            try :
                studentanswer =  Studentanswer.objects.filter(student = student,exercise = self,parcours=parcours).last()
                somme += studentanswer.point
                tab.append(studentanswer.point)
            except : 
                pass

        try :
            avg = somme/len(tab)
            tab.sort()
            details["min"] = tab[0]
            details["max"] = tab[-1]
            details["avg"] = int(avg)
        except : 
            avg = 0
            details["min"] = 0
            details["max"] = 0
            details["avg"] = 0

        return details





    def last_score_and_time(self,parcours,student_id):
        student = Student.objects.get(pk=student_id)
        scores_times = {}
        if Studentanswer.objects.filter(student = student).filter(exercise = self.pk,parcours=parcours).exists() :
            studentanswer =  Studentanswer.objects.filter(student = student,exercise = self.pk,parcours=parcours).last() 
            scores_times["score"] = studentanswer.point 
            scores_times["time"] = convert_time(studentanswer.secondes)
        return scores_times


    def timer(self,parcours,student_id):
        reponse, datetime_object = "", ""
        student = Student.objects.get(pk=student_id)
        if Studentanswer.objects.filter(student = student).filter(exercise = self.pk,parcours=parcours).exists() :
            studentanswer =  Studentanswer.objects.filter(student = student,exercise = self.pk).last()
            reponse = int(studentanswer.secondes) 
            if reponse > 59  :
                minutes = int(reponse/60)
                scdes = reponse % 60

                datetime_object =  str(minutes) + "min"+ str(scdes) + "s"
            else :
                datetime_object = str(reponse)+ " s"
        return datetime_object


    def is_selected(self,parcours):
        test = False 
        relationship = Relationship.objects.filter(parcours=parcours, exercise=self) 
        if relationship.count() == 1 : 
            test = True
        return test


 

    def is_relationship(self ,parcours):
        try :
            relationship = Relationship.objects.get(parcours=parcours, exercise=self)
        except :
            relationship = False
        return relationship


    def used_in_parcours(self ,teacher): 
        parcours = Parcours.objects.filter(exercises=self, author=teacher)
        return parcours



    def is_used(self):

        if Parcours.objects.filter(exercises = self).count() > 0 :
            test = True
        else :
            test = False
        return test




    def is_done(self,student):
        done = False
        if Studentanswer.objects.filter(student=student, exercise = self).exists():
            done = True
        return done



    def nb_task_done(self,group):
        try :
            studentanswer_tab = []
            for s in group.students.all():
                studentanswer = Studentanswer.objects.filter(exercise = self, student = s).first()
                if studentanswer :
                    studentanswer_tab.append(studentanswer)
            nb_task_done = len(studentanswer_tab)
        except :
            nb_task_done = 0
        return nb_task_done

    def who_are_done(self,group):
        studentanswer_tab = []
        try :
            for s in group.students.all():
                studentanswer = Studentanswer.objects.filter(exercise = self, student = s).first()
                if studentanswer :
                    studentanswer_tab.append(studentanswer)
        except : 
            pass
        return studentanswer_tab




    def nb_task_parcours_done(self,parcours):
        studentanswer_tab = []
        for s in parcours.students.all():
            studentanswer = Studentanswer.objects.filter(exercise = self, student = s).first()
            if studentanswer :
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
        exercise_done = []

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

        exercises = Exercise.objects.filter(level = self.supportfile)
        return exercises







 
class Parcours(ModelWithCode):

    title = models.CharField(max_length=255, verbose_name="Titre")
    color = models.CharField(max_length=255, default='#00819F', verbose_name="Couleur")
    author = models.ForeignKey(Teacher, related_name = "author_parcours", on_delete=models.PROTECT, default='', blank=True,  null= True,  verbose_name="Auteur")
    teacher = models.ForeignKey(Teacher, related_name = "teacher_parcours", on_delete=models.PROTECT,  default='', blank=True,  editable=False)
 
    exercises = models.ManyToManyField(Exercise,   blank=True, through="Relationship", related_name = "exercises_parcours" )   
    students = models.ManyToManyField(Student, blank=True,  related_name='students_to_parcours', verbose_name="Elèves de ce parcours")
    is_share = models.BooleanField( default = 1 ,  verbose_name="Partagé ?")
    is_publish = models.BooleanField( default = 0,  verbose_name="Publié ?" )    


    level = models.ForeignKey(Level, related_name = "level_parcours", on_delete=models.PROTECT,  default='', blank=True, null= True,  editable=False)
    linked  = models.BooleanField( default = 0 ,  editable=False)
    is_favorite  = models.BooleanField( default = 1  ,  verbose_name="Favori ?" )

    is_evaluation = models.BooleanField( default = 0,   verbose_name="Evaluation ?" )  
    duration = models.PositiveIntegerField(  default=0,   verbose_name="Temps de chargement (min.)")   
    start =  models.DateField( null=True, blank=True, verbose_name="Date de début de publication")
    starter = models.TimeField( null=True, blank=True,  verbose_name="Heure de début de publication")
    stop =  models.DateField( null=True, blank=True, verbose_name="Date de fin de publication")
    stopper = models.TimeField( null=True, blank=True,verbose_name="Heure de fin de publication")

    vignette = models.ImageField(upload_to=vignette_directory_path, verbose_name="Image du parcours", blank=True, default ="")


    def __str__(self):        
        return "{}".format(self.title)



    def is_done(self,student):
        Studentanswer = apps.get_model('qcm', 'Studentanswer')
        exercises = self.exercises.all()
        n = 0
        exercise_done = []
        for e  in exercises :
            if not e in exercise_done:
                if Studentanswer.objects.filter(student=student, exercise = e).exists():
                    n +=1
        return n


    def is_affect(self,student):

        nb_relationships = Relationship.objects.filter(parcours=self,exercise__supportfile__is_title=0,students = student,is_publish=1).count()
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
        for e in self.exercises.all().prefetch_related('supportfile'):
            som += e.supportfile.duration
        return som 



    def evaluation_duration(self):

        relationships = Relationship.objects.filter(parcours= self)
        som = self.duration
        for r in relationships : 
            som += r.duration
        return som 


    def group_list(self):
        Group = apps.get_model('group', 'Group')
        students = self.students.all() 
        group_tab = []
        for s  in students :
            groups = Group.objects.filter(students = s)
            for group  in groups :
                if group not in group_tab:
                    group_tab.append(group)       

        return group_tab 




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



class Relationship(models.Model):
    exercise = models.ForeignKey(Exercise,  null=True, blank=True,   related_name='exercise_relationship', on_delete=models.PROTECT,  editable= False) 
    parcours = models.ForeignKey(Parcours, on_delete=models.PROTECT,  related_name='parcours_relationship',  editable= False) 
    order = models.PositiveIntegerField( default=0,  editable= False) 
    is_publish = models.BooleanField( default = 1 )
    start = models.DateField( null=True, blank=True, verbose_name="A partir de")
    date_limit = models.DateField( null=True, blank=True, verbose_name="Date limite du rendu")
    is_evaluation = models.BooleanField( default = 0 )  
    duration = models.PositiveIntegerField(  default=15,   verbose_name="Durée estimée en minutes")   
    situation = models.PositiveIntegerField(default = 10, verbose_name="Nombre minimal de situations", help_text="Pour valider le qcm")  
    beginner = models.TimeField( null=True, blank=True, verbose_name="Heure du début")
    skills = models.ManyToManyField(Skill,  blank=True,  related_name='skills_relationship',  editable= False) 
    students = models.ManyToManyField(Student, blank=True,  related_name='students_relationship',  editable= False) 



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


########################################################################################################################################### 
########################################################################################################################################### 
######################################################### FIN  Types de question ########################################################## 
########################################################################################################################################### 
########################################################################################################################################### 


class Studentanswer(models.Model):

    parcours = models.ForeignKey(Parcours,  on_delete=models.PROTECT, blank=True, null=True,  related_name='parcours_studentanswer', editable=False) 
    exercise = models.ForeignKey(Exercise,  on_delete=models.PROTECT, blank=True,  related_name='ggbfile_studentanswer', editable=False) 
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='student_studentanswer', editable=False)
    point  = models.PositiveIntegerField(default=0 )  
    numexo  = models.PositiveIntegerField(default=10 )  
    date = models.DateTimeField(auto_now_add=True)
    secondes = models.CharField(max_length=255, editable=False)

    def __str__(self):        
        return "{}".format(self.exercise.knowledge.name)




 
class Resultexercise(models.Model): # Last result

    student = models.ForeignKey(Student,   related_name = "student_resultexercise", default="", on_delete=models.CASCADE, editable=False)
    exercise = models.ForeignKey(Exercise,   related_name = "knowledge_resultexercise", on_delete=models.PROTECT, editable=False)
    point  = models.PositiveIntegerField(default=0 ) 

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

 
class Contraint(models.Model):

    code = models.CharField(max_length=8, default='', editable=False)
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, default='',   blank=True, related_name='relationship_contraint') 
    scoremin = models.PositiveIntegerField(  default=80, editable=False)  

    def __str__(self):        
        return "{} à {}%".format(self.code , self.scoremin)