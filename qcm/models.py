import uuid
from django.db import models
from datetime import date, datetime, timedelta
from django.utils import timezone
from account.models import Student, Teacher, ModelWithCode, generate_code
from socle.models import  Knowledge, Level , Theme, Skill 
from django.apps import apps
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q, Min, Max
import os.path
from django.utils import timezone
from general_fonctions import *
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


def file_folder_path(instance, filename):
    return "files/{}/{}".format(instance.customexercise.teacher.user.id, filename)



def directory_path_mastering(instance, filename):
    return "mastering/{}/{}".format(instance.relationship.parcours.teacher.user.id, filename)
 
def directory_path(instance, filename):
    return "demandfiles/{}/{}".format(instance.level.id, filename)

def file_attach_path(instance, filename):
    return "attach_files/{}/{}".format(instance.level.id, filename)


def file_directory_student(instance, filename):
    return "files/{}/{}".format(instance.student.user.id, filename)

def file_directory_to_student(instance, filename):
    return "files/{}/{}".format(instance.customanswerbystudent.student.user.id, filename)


def convert_time(duree) :
    try :
        d = int(duree)
        if d < 59 :
            return duree+"s"
        elif d < 3600:
            s = d%60        
            m = int((d-s)/60)
            return str(m)+"min "+str(s)+"s"
        else :
            return  "td" #temps dépassé
    except :
        return ""


########################################################################################################
########################################################################################################
class Supportfile(models.Model):

    knowledge = models.ForeignKey(Knowledge, on_delete=models.PROTECT,  related_name='supportfiles', verbose_name="Savoir faire associé - Titre")
    annoncement = RichTextUploadingField( verbose_name="Précision sur le savoir faire")
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
    ggbfile = models.FileField(upload_to=quiz_directory_path, verbose_name="Fichier ggb",blank=True, default="" )
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

    is_ggbfile = models.BooleanField(default=1, verbose_name="Type de support")
    is_python = models.BooleanField(default=0, verbose_name="Python ?")
    is_scratch = models.BooleanField(default=0, verbose_name="Scratch ?")
    is_file = models.BooleanField(default=0, verbose_name="Fichier ?")
    is_image = models.BooleanField(default=0, verbose_name="Iage/Scan ?")
    is_text = models.BooleanField(default=0, verbose_name="Texte ?")

    correction = RichTextUploadingField( blank=True, default="", null=True, verbose_name="Corrigé")

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
        """
        group ou parcours car on s'en sert pour récupérer les élèves
        """
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

    def levels_used(self):

        exercises = Exercise.objects.filter(level=self.supportfile)
        return exercises

    def my_parcours_container(self, teacher):

        parcours = self.exercises_parcours.filter(teacher=teacher)
        return parcours

class Parcours(ModelWithCode):

    title = models.CharField(max_length=255, verbose_name="Titre")
    color = models.CharField(max_length=255, default='#00819F', verbose_name="Couleur")
    author = models.ForeignKey(Teacher, related_name="author_parcours", on_delete=models.CASCADE, default='', blank=True, null=True, verbose_name="Auteur")
    teacher = models.ForeignKey(Teacher, related_name="teacher_parcours", on_delete=models.CASCADE, default='', blank=True, editable=False)
    coteachers = models.ManyToManyField(Teacher, blank=True,  related_name="coteacher_parcours",  verbose_name="Enseignant en co-animation")

    exercises = models.ManyToManyField(Exercise, blank=True, through="Relationship", related_name="exercises_parcours")
    students = models.ManyToManyField(Student, blank=True, related_name='students_to_parcours', verbose_name="Elèves")
    is_share = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
    is_archive = models.BooleanField(default=0, verbose_name="Archivé ?", editable=False)

    level = models.ForeignKey(Level, related_name="level_parcours", on_delete=models.CASCADE, default='', blank=True, null=True, editable=False)
    linked = models.BooleanField(default=0, editable=False)
    is_favorite = models.BooleanField(default=1, verbose_name="Favori ?")

    is_evaluation = models.BooleanField(default=0, editable=False)
    duration = models.PositiveIntegerField(default=2, blank=True, verbose_name="Temps de chargement (min.)")
    start = models.DateTimeField(null=True, blank=True, verbose_name="Date de début de publication")
    stop = models.DateTimeField(null=True, blank=True, verbose_name="Verrouillé à partir de")

    vignette = models.ImageField(upload_to=vignette_directory_path, verbose_name="Vignette d'accueil", blank=True, default ="")
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)
    
    is_leaf = models.BooleanField(default=0, verbose_name="Sous-parcours ?")
    folder_parcours = models.ManyToManyField('self',  blank=True,  related_name="subparcours_parcours",  verbose_name="Nom de parcours")    
    
    is_folder = models.BooleanField(default=0, verbose_name="Dossier")
    leaf_parcours = models.ManyToManyField('self',  blank=True,  related_name="subparcours_parcours",  verbose_name="Nom de parcours")


    def __str__(self):
        return "{}".format(self.title)


    def is_done(self,student):
        Studentanswer = apps.get_model('qcm', 'Studentanswer')
        studentanswers = Studentanswer.objects.filter(student=student, parcours=self).values_list("exercise",flat=True).order_by("exercise").distinct()
        n = len(studentanswers) 
        return n

    def is_affect(self, student):
        nb_relationships = Relationship.objects.filter(parcours=self, exercise__supportfile__is_title=0,
                                                       students=student, is_publish=1).count()
        return nb_relationships

    def is_lock(self,today):
        lock = False
        try :
            if self.stop < today :
                lock = True 
        except :
            pass
        return lock


    def get_themes(self):
        exercises = self.exercises.all()
        theme_tab, theme_tab_id  = [] , []
        for exercise in exercises :
            data = {}
            if not exercise.theme.id in theme_tab_id :
                data["theme"] = exercise.theme
                data["annoncement"] = exercise.supportfile.annoncement              
                theme_tab_id.append(exercise.theme.id)
                theme_tab.append(data)
        return theme_tab

    def nb_leaf(self,student):
        nb = self.leaf_parcours.filter(is_publish=1, students=student).count()
        return nb

    def is_percent(self,student):
        ## Nombre de relationships dans le parcours => nbre  d'exercices
        if self.is_folder :
            nb_relationships , nb_customs , nb_customanswerbystudent , nb_studentanswers = 0 , 0, 0 , 0
            for pcs in self.leaf_parcours.filter(is_publish=1):
                nb_relationships +=  pcs.parcours_relationship.filter(students = student, is_publish=1,  exercise__supportfile__is_title=0 ).count()
                nb_customs +=  pcs.parcours_customexercises.filter(students = student, is_publish=1).count()

                ## Nombre de réponse avec exercice unique du parcours
                nb_studentanswers += Studentanswer.objects.filter(student=student, parcours=pcs).values_list("exercise",flat=True).order_by("exercise").distinct().count()
                nb_customanswerbystudent += Customanswerbystudent.objects.filter(student=student, customexercise__parcourses=pcs).values_list("customexercise",flat=True).order_by("customexercise").distinct().count()


        else :
            nb_relationships =  self.parcours_relationship.filter(students = student, is_publish=1,  exercise__supportfile__is_title=0 ).count()
            nb_customs =  self.parcours_customexercises.filter(students = student, is_publish=1).count()

            ## Nombre de réponse avec exercice unique du parcours
            nb_studentanswers = Studentanswer.objects.filter(student=student, parcours=self).values_list("exercise",flat=True).order_by("exercise").distinct().count()
            nb_customanswerbystudent = Customanswerbystudent.objects.filter(student=student, customexercise__parcourses=self).values_list("customexercise",flat=True).order_by("customexercise").distinct().count()

 
        data = {}
        nb_exercise_done = nb_studentanswers + nb_customanswerbystudent
        data["nb"] = nb_exercise_done
        data["nb_total"] = nb_relationships + nb_customs
        try :
            data["pc"] = int(nb_exercise_done * 100/(nb_relationships+nb_customs))
        except :
            data["pc"] = 0
        return data

    def nb_exercises(self):
        nb = self.exercises.filter(supportfile__is_title=0).count()
        nba = self.parcours_customexercises.all().count()     
        return nb + nba

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
        students = self.students.all() # tous les élèves du parcours
        group_tab = []
        for s  in students : 
            groups = s.students_to_group.filter(teacher = self.teacher) # Pour chaque élèves à quel groupe du prof il appartient 
            for group  in groups :
                if group not in group_tab:
                    group_tab.append(group) 
        return group_tab 

    def shared_group_list(self):

        Sharing_group = apps.get_model('group', 'Sharing_group')
        students = self.students.all() 
        group_tab = []
        for s  in students :
            sh_groups = Sharing_group.objects.filter(group__students = s )
            for sh_group  in sh_groups :
                if sh_group not in group_tab:
                    group_tab.append(sh_group) 
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
        if Customexercise.objects.filter(parcourses = self, date_limit__gte = today).count() > 0 :
            test = True
        return test 

    def is_task_folder_exists(self):
        today = timezone.now()
        test = False
        if Relationship.objects.filter(parcours__in= self.leaf_parcours.filter(is_publish=1),date_limit__gte = today).count() > 0 :
            test = True
        for p in self.leaf_parcours.filter(is_publish=1):
            if Customexercise.objects.filter(parcourses= p ,date_limit__gte = today).count() > 0 :
                test = True
                break
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

    def is_folder_courses_exists(self):

        test = False
        for p in self.leaf_parcours.filter(is_publish=1) :
            if p.course.count() > 0 :
                test = True
                break
        return test 

    def is_sections_exists(self) :

        test = False
        if self.parcours_relationship.filter(exercise__supportfile__is_title = 1).count() > 0 :
            test = True
        return test 

    def nb_task(self):

        today = timezone.now()
        nb = self.parcours_relationship.filter(date_limit__gte = today).count()
        return nb

    def evaluation_duration(self):
        """
        Calcul de la durée d'une évaluation par somme des temps d'exercices choisis
        """
        relationships = self.parcours_relationship.all()
        som = self.duration
        for r in relationships : 
            som += r.duration

        customexercises = self.parcours_customexercises.all()
        for c in customexercises : 
            som += c.duration

        return som 

    def min_score_parcours(self,student):
        """
        min score d'un parcours par élève
        """
        Stage = apps.get_model('school', 'Stage')
        data = {}
        max_tab = []
        nb_done = 0
        for exercise in self.exercises.all() :
            maxi = Studentanswer.objects.filter(student=student, parcours= self, exercise = exercise )
            if maxi.count()>0 :
                maximum = maxi.aggregate(Max('point'))
                max_tab.append(maximum["point__max"])
                nb_done +=1

        try :
            stage = Stage.objects.get(school = student.user.school)
            up = stage.up
            med = stage.medium
            low = stage.low
        except :
            up = 85
            med = 65
            low = 35

        if nb_done == Relationship.objects.filter(is_publish=1,students=student, parcours= self ).count() :
            max_tab.sort()

            if len(max_tab)>0 :
                score = max_tab[0]
            else :
                score = None

            if score :
                data["boolean"] = True
                if score > up :
                    data["colored"] = "darkgreen"
                elif score >  med :
                    data["colored"] = "green"
                elif score > low :
                    data["colored"] = "orange"
                else :
                    data["colored"] = "red"
            else :
                data["boolean"] = False
                data["colored"] = "red"     
        else :
            data["boolean"] = False
            data["colored"] = "red"       
        return data

    def is_pending_correction(self):
        """
        Correction en attente
        """
        submit = False
        customexercises = Customexercise.objects.filter(parcourses = self)
        for customexercise in customexercises :
            if customexercise.customexercise_custom_answer.exclude(is_corrected = 1).exists() :
                submit = True 
                break

        if not submit :
            if Writtenanswerbystudent.objects.filter(relationship__parcours  = self).exclude(is_corrected = 1).exists() : 
                submit = True 

        return submit

    def is_pending_folder_correction(self):
        """
        Correction en attente deuis un folder de parcours
        """
        submit = False
        for p in self.leaf_parcours.filter(is_publish=1) :
            customexercises = Customexercise.objects.filter(parcourses  = p )
            for customexercise in customexercises :
                if customexercise.customexercise_custom_answer.exclude(is_corrected = 1).exists() :
                    submit = True 
                    break

        if not submit :
            if Writtenanswerbystudent.objects.filter(relationship__parcours__in = self.leaf_parcours.all() ).exclude(is_corrected = 1).exists() : 
                submit = True 

        return submit


    def p_is_leaf(self,parcours):
        test = False
        if parcours :
            if self in parcours.leaf_parcours.all() : 
                test = True
        return test

class Relationship(models.Model):
    exercise = models.ForeignKey(Exercise,  null=True, blank=True,   related_name='exercise_relationship', on_delete=models.PROTECT,  editable= False)
    parcours = models.ForeignKey(Parcours, on_delete=models.PROTECT,  related_name='parcours_relationship',  editable= False)
    order = models.PositiveIntegerField(default=0, editable=False)
    is_publish = models.BooleanField(default=1)
    start = models.DateTimeField(null=True, blank=True, verbose_name="A partir de")
    date_limit = models.DateTimeField(null=True, blank=True, verbose_name="Date limite du rendu")
    is_evaluation = models.BooleanField(default=0)
    duration = models.PositiveIntegerField(default=15, verbose_name="Durée estimée en minutes")
    situation = models.PositiveIntegerField(default=10, verbose_name="Nombre minimal de situations", help_text="Pour valider le qcm")
    beginner = models.TimeField(null=True, blank=True, verbose_name="Heure du début")
    skills = models.ManyToManyField(Skill, blank=True, related_name='skills_relationship', editable=False)
    students = models.ManyToManyField(Student, blank=True, related_name='students_relationship', editable=False)
    instruction = models.TextField(blank=True,  null=True,  editable=False)

    is_lock = models.BooleanField(default=0, verbose_name="Exercice cloturé ?")
    is_mark = models.BooleanField(default=0, verbose_name="Notation ?")
    mark = models.CharField(max_length=3, default="", verbose_name="Sur ?")
    is_correction_visible = models.BooleanField(default=0, editable=False  )

    def __str__(self):

        try :
            return "{} : {}".format(self.parcours, cleanhtml(self.exercise.supportfile.annoncement))
        except :
            return "{}".format(self.parcours)  

    class Meta:
        unique_together = ('exercise', 'parcours')


    def score_student_for_this(self,student):
        studentanswer = Studentanswer.objects.filter(student=student, parcours= self.parcours , exercise = self.exercise ).last()
        return studentanswer

    def is_done(self,student):
        done = False
        sta = Studentanswer.objects.filter(student=student, exercise = self.exercise, parcours= self.parcours ).exists()
        stw = self.relationship_written_answer.filter(student=student).exists()
        if sta or stw :
            done = True
        return done

    def is_task(self):
        task = False
        today = timezone.now() 
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

    def is_header_of_section(self): # Contrainte. 
    
        header = False # On suppose que l'élève n'a pas obtenu le score minimum dans les exercices puisqu'il ne les a pas fait. 
        courses = Course.objects.filter(relationships = self).order_by("ranking") 
        data = {}
        if courses.count() > 0 : 
            header = True  
        
        data["header"] = header

        return header 

    def percent_student_done_parcours_exercice(self,parcours):

        students = self.students.all()
        nb_student = len(students)

        if self.exercise.supportfile.is_ggbfile :
            nb_exercise_done = Studentanswer.objects.filter(student__in= students, parcours= parcours, exercise = self.exercise).values_list("student",flat= True).order_by("student").distinct().count()
        else :
            nb_exercise_done = Writtenanswerbystudent.objects.filter(relationship= self, student__in= students ).values_list("student",flat= True).order_by("student").distinct().count()        
 
        try :
            percent = int(nb_exercise_done * 100/nb_student)
        except : 
            percent = 0
        data = {}
        data["nb"] = nb_student
        data["percent"] = percent
        data["nb_done"] = nb_exercise_done
        return data

    def is_submit(self,student):
        submit = False
        if self.relationship_written_answer.filter(student = student).exclude(is_corrected = 1).exists() :
            submit = True          
        return submit

    def noggb_data(self,student):
        try :
            data =  self.relationship_written_answer.get(student = student)   
        except :
            data = {'is_corrected' : False , 'skills' : [] , 'comment' : "" , }     
        return data

    def is_pending_correction(self):
        submit = False
        if self.relationship_written_answer.exclude(is_corrected = 1).exists() :
            submit = True          
        return submit

    def code_student_for_this(self,student):
        Stage = apps.get_model('school', 'Stage')
        studentanswer = Studentanswer.objects.filter(student=student, parcours= self.parcours , exercise = self.exercise ).last()
        try :
            point = studentanswer.point
        except :
            point = -1
 
        if student.user.school :
            school = student.user.school
            stage = Stage.objects.get(school = school)

     
            if point > stage.up :
                level = 4
            elif point > stage.medium :
                level = 3
            elif point > stage.low :
                level = 2
            elif point > -1 :
                level = 1
            else :
                level = 0

        else : 
            stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
 
            if point > stage["up"] :
                level = 4
            elif point > stage["medium"] :
                level = 3
            elif point > stage["low"] :
                level = 2
            elif point > -1 :
                level = 1
            else :
                level = 0

        return level

    def result_skill(self,skill,student):
        Stage = apps.get_model('school', 'Stage')
        try :
            studentanswer = Resultggbskill.objects.get(student=student, relationship= self,skill = skill )
            point = studentanswer.point
            if student.user.school :
                school = student.user.school
                stage = Stage.objects.get(school = school)
         
                if point > stage.up :
                    level = 4
                elif point > stage.medium :
                    level = 3
                elif point > stage.low :
                    level = 2
                elif point > -1 :
                    level = 1
                else :
                    level = 0
            else : 
                stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
 
                if point > stage["up"] :
                    level = 4
                elif point > stage["medium"] :
                    level = 3
                elif point > stage["low"] :
                    level = 2
                elif point > -1 :
                    level = 1
                else :
                    level = 0
        except :
            level = 0
        return level


    def mark_to_this(self,student,parcours_id): # parcours_id n'est pas utilisé mais on le garde pour utiliser la fontion exostante dans item_tags
        data = {}
 
        if Writtenanswerbystudent.objects.filter(relationship = self,  student = student,is_corrected=1).exists() :
            wa = Writtenanswerbystudent.objects.get(relationship = self,   student = student,is_corrected=1)
            data["is_marked"] = True
            data["marked"] = wa.point
        else :
            data["is_marked"] = False
            data["marked"] = ""            

        return data

class Studentanswer(models.Model):

    parcours = models.ForeignKey(Parcours,  on_delete=models.PROTECT, blank=True, null=True,  related_name='answers', editable=False)
    exercise = models.ForeignKey(Exercise,  on_delete=models.PROTECT, blank=True,  related_name='ggbfile_studentanswer', editable=False) 
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='answers', editable=False)
    point  = models.PositiveIntegerField(default=0 )  
    numexo  = models.PositiveIntegerField(default=10 )  
    date = models.DateTimeField(default=timezone.now)
    secondes = models.CharField(max_length=255, editable=False)

    def __str__(self):        
        return "{}".format(self.exercise.knowledge.name)

class Resultggbskill(models.Model): # Pour récupérer tous les scores des compétences d'une relationship
    student = models.ForeignKey(Student, related_name="student_resultggbskills", default="", on_delete=models.CASCADE, editable=False)
    skill = models.ForeignKey(Skill, related_name="skill_resultggbskills", on_delete=models.CASCADE, editable=False)
    point = models.PositiveIntegerField(default=0)
    relationship = models.ForeignKey(Relationship,  on_delete=models.PROTECT, blank=True, null=True,  related_name='relationship_resultggbskills', editable=False)

    def __str__(self):
        return f"{self.skill} : {self.point}"

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

class Writtenanswerbystudent(models.Model): # Commentaire pour les exercices non autocorrigé coté enseignant

    relationship = models.ForeignKey(Relationship,  on_delete=models.PROTECT,   related_name='relationship_written_answer', editable=False)
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='student_written_answer', editable=False)
    date = models.DateTimeField(auto_now_add=True)
    # rendus
    imagefile = models.ImageField(upload_to= file_directory_student, blank = True, null=True,   verbose_name="Scan ou image ou Photo", default="")
    answer = RichTextUploadingField( default="", null=True,  blank=True, ) 
    comment = models.TextField( default="", null=True,   editable=False) # Commentaire de l'enseignant sur l'exercice
    audio = models.FileField(upload_to=file_directory_path,verbose_name="Commentaire audio", blank=True, null= True, default ="")
    point = models.CharField(default="", max_length=10, verbose_name="Note")
    is_corrected = models.BooleanField( default=0, editable=False ) 

    def __str__(self):        
        return "{}".format(self.relationship.exercise.knowledge.name)

########################################################################################################################################### 
########################################################################################################################################### 
############################################################ Exercice customisé ###########################################################
########################################################################################################################################### 
########################################################################################################################################### 
class Customexercise(ModelWithCode):

    instruction = RichTextUploadingField( verbose_name="Consigne*") 
    teacher = models.ForeignKey(Teacher, related_name="teacher_customexercises", blank=True, on_delete=models.CASCADE)
    calculator = models.BooleanField(default=0, verbose_name="Calculatrice ?")
 
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    #### pour donner une date de remise - Tache     
    start = models.DateTimeField(null=True, blank=True, verbose_name="A partir de")
    date_limit = models.DateTimeField(null=True, blank=True, verbose_name="Date limite du rendu")
    lock = models.DateTimeField(null=True, blank=True, verbose_name="Verrouillé à partir de")

    imagefile = models.ImageField(upload_to=vignette_directory_path, blank=True, verbose_name="Vignette d'accueil", default="")

    duration = models.PositiveIntegerField(default=15, blank=True, verbose_name="Durée estimée (min.)")
    
    skills = models.ManyToManyField(Skill, blank=True, related_name='skill_customexercises', verbose_name="Compétences évaluées")
    knowledges = models.ManyToManyField(Knowledge, blank=True, related_name='knowledge_customexercises', verbose_name="Savoir faire évalués")
    parcourses = models.ManyToManyField(Parcours, blank=True, related_name='parcours_customexercises', verbose_name="Parcours attachés")
    students = models.ManyToManyField(Student, blank=True, related_name='students_customexercises' )   
    
    is_share = models.BooleanField(default=0, verbose_name="Mutualisé ?")

    is_python = models.BooleanField(default=0, verbose_name="Python ?")
    is_scratch = models.BooleanField(default=0, verbose_name="Scratch ?")
    is_file = models.BooleanField(default=0, verbose_name="Fichier ?")
    is_image = models.BooleanField(default=0, verbose_name="Image/Scan ?")
    is_text = models.BooleanField(default=0, verbose_name="Texte ?")
    is_mark = models.BooleanField(default=0, verbose_name="Notation ?")
    mark = models.PositiveIntegerField(default=0, verbose_name="Sur ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)

    text_cor = RichTextUploadingField(  blank=True, null=True,  verbose_name="Correction écrite") 
    file_cor = models.ImageField(upload_to=vignette_directory_path, blank=True, verbose_name="Fichier de correction", default="")
    video_cor = models.CharField(max_length = 100, blank=True, verbose_name="Code de la vidéo Youtube", default="")
    is_publish_cor = models.BooleanField(default=0, verbose_name="Publié ?")    

    def __str__(self):       
        return "{}".format(self.instruction)
 

    def subjects(self):
        subjects = []
        for k in self.knowledges.all() :
            if k.theme.subject  not in subjects :
                subjects.append(k.theme.subject)

        for s in self.skills.all() :
            if s.subject not in subjects :
                subjects.append(s.subject)

        if len(subjects) == 0 :
            for sb in self.teacher.subjects.all() :
                if sb  not in subjects :
                    subjects.append(sb)       
        return subjects

    def levels(self):
        levels = []
        for k in self.knowledges.all() :
            if k.level  not in levels :
                levels.append(k.level)

 
        if len(levels) == 0 :
            for sb in self.teacher.levels.all() :
                if sb  not in levels :
                    levels.append(sb)       
        return levels

    def percent_student_done_parcours_exercice(self, parcours):

        students = self.students.all()
        nb_student = len(students)
        nb_exercise_done = Customanswerbystudent.objects.filter(student__in= students, customexercise__parcourses = parcours, customexercise = self).values_list("student",flat= True).order_by("student").distinct().count()
        
        try :
            percent = int(nb_exercise_done * 100/nb_student)
        except : 
            percent = 0
        data = {}
        data["nb"] = nb_student
        data["percent"] = percent
        data["nb_done"] = nb_exercise_done
        return data

    def is_done(self,student):
        done = False
        if Customanswerbystudent.objects.filter(student=student, customexercise = self).exists():
            done = True
        return done

    def score_student_for_this(self,student):

        correction = Customanswerbystudent.objects.filter(student=student, customexercise = self ).exclude(is_corrected=1)

        if correction.exists() :
            cor = correction.last()
            try :
                score = int(cor.point)
            except:
                score = "C"
        else :
            score = False

        return score

    def is_corrected_for_this(self,student,parcours): # devoir corrigé
        correction = Customanswerbystudent.objects.filter(student=student, customexercise = self, parcours =parcours,is_corrected=1)
        is_corrected = False
        data = {}
        if correction.exists() :
            correction = Customanswerbystudent.objects.get(student=student, customexercise = self, parcours =parcours,is_corrected=1)
            answer = correction.answer
            is_corrected = True
        else :
            answer=None
        data["answer"] = answer
        data["is_corrected"] = is_corrected
        return data

    def is_lock(self,today):
        locker = False
        try :
            if self.lock < today :
                locker = True
        except :
            pass
        return locker


    def is_submit(self,parcours,student):
        submit = False
        if Customanswerbystudent.objects.filter(customexercise = self, parcours = parcours, student = student).exclude(is_corrected=1).exists() :
            submit = True          
        return submit

    def result_k_s(self,k_s, student, parcours_id,typ):
        Stage = apps.get_model('school', 'Stage')

        if typ == 1 :
            if Correctionskillcustomexercise.objects.filter(customexercise = self, parcours_id = parcours_id, student = student, skill = k_s).exists() :
                c = Correctionskillcustomexercise.objects.get(customexercise = self, parcours_id = parcours_id, student = student, skill = k_s)    
                point = int(c.point)
            else :
                point = -1  
        else :
            if Correctionknowledgecustomexercise.objects.filter(customexercise = self, parcours_id = parcours_id, student = student, knowledge = k_s).exists() :
                c = Correctionknowledgecustomexercise.objects.get(customexercise = self, parcours_id = parcours_id, student = student, knowledge = k_s)    
                point = int(c.point)   
            else :
                point = -1  
 
        if student.user.school :
            school = student.user.school
            stage = Stage.objects.get(school = school)

            if point > stage.up :
                level = 4
            elif point > stage.medium :
                level = 3
            elif point > stage.low :
                level = 2
            elif point > -1 :
                level = 1
            else :
                level = 0
        else : 
            stage = { "low" : 50 ,  "medium" : 70 ,  "up" : 85  }
 
            if point > stage["up"]  :
                level = 4
            elif point > stage["medium"]  :
                level = 3
            elif point > stage["low"]  :
                level = 2
            elif point > -1 :
                level = 1
            else :
                level = 0
        return level

    def mark_to_this(self,student,parcours_id):
        data = {}
        if Customanswerbystudent.objects.filter(customexercise = self, parcours_id = parcours_id, student = student,is_corrected=1).exists() :
            c = Customanswerbystudent.objects.get(customexercise = self, parcours_id = parcours_id, student = student,is_corrected=1)
            data["is_marked"] = True
            data["marked"] = c.point
        else :
            data["is_marked"] = False
            data["marked"] = ""            

        return data

    def all_results_custom(self,student,parcours): # résultats vue élève
        data = {}
        if Customanswerbystudent.objects.filter(customexercise = self, parcours = parcours, student = student,is_corrected=1).exists() :
            c = Customanswerbystudent.objects.get(customexercise = self, parcours = parcours, student = student,is_corrected=1)
            data["is_corrected"] = True            
            data["comment"] = c.comment
            data["audio"] =  c.audio
            data["point"] = c.point
            c_skills = Correctionskillcustomexercise.objects.filter(customexercise = self, parcours = parcours, student = student)
            c_knowledges = Correctionknowledgecustomexercise.objects.filter(customexercise = self, parcours = parcours, student = student)
            data["skills"] = c_skills
            data["knowledges"] = c_knowledges
        else :
            data["is_corrected"] = False
            data["comment"] = False           
            data["skills"] = []
            data["knowledges"] = []
            data["point"] = False
            data["audio"] = False
        return data

    def is_pending_correction(self):
        submit = False
        if self.customexercise_custom_answer.exclude(is_corrected = 1).exists() :
            submit = True      
        return submit

    def nb_task_parcours_done(self, parcours):
        studentanswer_tab = []
        for s in parcours.students.all():
            studentanswer = Studentanswer.objects.filter(exercise=self, student=s).first()
            if studentanswer:
                studentanswer_tab.append(studentanswer)
        nb_task_done = len(studentanswer_tab)
        return nb_task_done

    def nb_task_done(self, group):
        """
        group ou parcours car on s'en sert pour récupérer les élèves
        """
        try:
            custom_tab = []
            for s in group.students.all():
                custom_answer = Customanswerbystudent.objects.filter(customexercise=self, student=s).first()
                if custom_answer:
                    custom_tab.append(custom_answer)
            nb_task_done = len(custom_tab)
        except:
            nb_task_done = 0

        data = {}
        data["nb_task_done"] = nb_task_done
        data["custom_tab"] = custom_tab
        return data

class Customanswerbystudent(models.Model): # Commentaire et note pour les exercices customisés coté enseignant

    customexercise = models.ForeignKey(Customexercise,  on_delete=models.CASCADE,   related_name='customexercise_custom_answer', editable=False)
    parcours = models.ForeignKey(Parcours,  on_delete=models.CASCADE,   related_name='parcours_custom_answer', editable=False)    
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='student_custom_answer', editable=False)
    date = models.DateTimeField(auto_now_add=True)
    # rendus
    file = models.FileField(upload_to= file_directory_student, blank = True, null=True,   verbose_name="Fichier pdf ou texte", default="")
    answer = RichTextUploadingField( default="", null=True,  blank=True, ) 
    # eval prof
    comment = models.TextField( default="", null=True) 
    point = models.CharField(default="", max_length=10, verbose_name="Note")
    is_corrected = models.BooleanField( default=0, editable=False ) 
    audio = models.FileField(upload_to=file_folder_path,verbose_name="Commentaire audio", blank=True, null= True,  default ="")

    def __str__(self):        
        return "{}".format(self.customexercise)

    class Meta:
        unique_together = ['student', 'parcours', 'customexercise']

class Customanswerimage(models.Model): # Commentaire et note pour les exercices customisés coté enseignant

    customanswerbystudent = models.ForeignKey(Customanswerbystudent,  on_delete=models.CASCADE,   related_name='customexercise_custom_answer_image', editable=False)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to= file_directory_to_student, blank = True, null=True,   verbose_name="Scan ou image ou Photo", default="")
    

    def __str__(self):        
        return "{}".format(self.customanswerbystudent)

class Correctionskillcustomexercise(models.Model): # Evaluation des compétences pour les exercices customisés coté enseignant 

    customexercise = models.ForeignKey(Customexercise,  on_delete=models.CASCADE,   related_name='customexercise_correctionskill', editable=False)
    parcours = models.ForeignKey(Parcours,  on_delete=models.CASCADE,   related_name='parcours_customskill_answer', editable=False)    
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='student_correctionskill', editable=False)
    skill = models.ForeignKey(Skill,  on_delete=models.CASCADE,   related_name='skill_correctionskill', editable=False)
    date = models.DateTimeField(auto_now_add=True)
    point = models.PositiveIntegerField(default=-1,  editable=False)
    
    def __str__(self):        
        return "{}".format(self.customexercise)

    class Meta:
        unique_together = ['student', 'customexercise','skill']

class Correctionknowledgecustomexercise(models.Model): # Evaluation des savoir faire pour les exercices customisés coté enseignant

    customexercise = models.ForeignKey(Customexercise,  on_delete=models.CASCADE,   related_name='customexercise_correctionknowledge', editable=False)
    parcours = models.ForeignKey(Parcours,  on_delete=models.CASCADE,   related_name='parcours_customknowledge_answer', editable=False)    
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='student_correctionknowledge', editable=False)
    knowledge = models.ForeignKey(Knowledge,  on_delete=models.CASCADE,   related_name='knowledge_correctionknowledge', editable=False)
    date = models.DateTimeField(auto_now_add=True)
    point = models.PositiveIntegerField(default=-1,  editable=False)
    
    def __str__(self):        
        return "{}".format(self.customexercise)

    class Meta:
        unique_together = ['student', 'customexercise','knowledge']

class Exerciselocker(ModelWithCode):

    relationship = models.ForeignKey(Relationship,  on_delete=models.PROTECT, blank=True, null=True,  related_name='relationship_exerciselocker', editable=False) 
    customexercise = models.ForeignKey(Customexercise,  on_delete=models.PROTECT, blank=True, null=True,  related_name='customexercise_exerciselocker', editable=False) 
    custom  = models.BooleanField(default=0, editable=False)    
    student = models.ForeignKey(Student,  on_delete=models.CASCADE, blank=True,  related_name='student_exerciselocker', editable=False)
    lock = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):        
        return "{}".format(self.student)

########################################################################################################################################### 
########################################################################################################################################### 
################################################################   Cours    ############################################################### 
########################################################################################################################################### 
########################################################################################################################################### 
class Course(models.Model): # pour les 

    parcours = models.ForeignKey(Parcours,  on_delete=models.CASCADE, blank=True, null=True,  related_name='course', editable=False) 
    title = models.CharField(max_length=50, default='',  blank=True, verbose_name="Titre")    
    annoncement = RichTextUploadingField( blank=True, verbose_name="Texte*") 
    teacher = models.ForeignKey(Teacher, related_name = "course", on_delete=models.CASCADE, editable=False )
    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée de lecture")  

    is_publish = models.BooleanField( default= 0, verbose_name="Publié ?")
    publish_start = models.DateTimeField(default=timezone.now,  blank=True, max_length=255, verbose_name="Début à", help_text="Changer les dates des cours peut remplacer les réglages de leur durée de disponibilité et leur placement dans les pages de cours ou le tableau de bord. Veuillez confirmer les dates d’échéance avant de modifier les dates des cours. ")
    publish_end = models.DateTimeField( blank=True, null=True,  max_length=255, verbose_name="Se termine à")


    ranking = models.PositiveIntegerField(  default=1,  blank=True, null=True,  verbose_name="Ordre") 
    
    is_task = models.BooleanField( default=0,    verbose_name="Tache à rendre ?") 
    is_paired = models.BooleanField( default=0,    verbose_name="Elèves créateurs ?") 
    is_active = models.BooleanField( default=0,  verbose_name="Contenu en cours")  
    is_share = models.BooleanField( default=0,  verbose_name="Mutualisé ?")  
 
    date_limit = models.DateTimeField( null=True, blank=True, verbose_name="Date limite du rendu")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification") 

    notification = models.BooleanField( default=0,  verbose_name="Informer des modifications ?", help_text="Envoie un message aux participants." )     
 
    students = models.ManyToManyField(Student, blank=True,  related_name='students_course', verbose_name="Attribuer à/au")
    creators = models.ManyToManyField(Student, blank=True,  related_name='creators_course', verbose_name="Co auteurs élève") 
    relationships = models.ManyToManyField(Relationship, blank=True,  related_name='relationships_courses', verbose_name="Lier ce cours à") 
 
    def __str__(self):
        return self.title 


    def subjects(self):
        subjects = []
        for k in self.parcours.knowledges.all() :
            if k.theme.subject  not in subjects :
                subjects.append(k.theme.subject)

        for s in self.skills.all() :
            if s.subject not in subjects :
                subjects.append(s.subject)

        if len(subjects) == 0 :
            for sb in self.teacher.subjects.all() :
                if sb  not in subjects :
                    subjects.append(sb)       
        return subjects



    def levels(self):
        levels = []
        for k in self.knowledges.all() :
            if k.level  not in levels :
                levels.append(k.level)

 
        if len(levels) == 0 :
            for sb in self.teacher.levels.all() :
                if sb  not in levels :
                    levels.append(sb)       
        return levels


########################################################################################################################################### 
########################################################################################################################################### 
#############################################################  Remediation       ########################################################## 
########################################################################################################################################### 
###########################################################################################################################################  
class Remediation(models.Model):

    title = models.CharField(max_length=255, default='',  blank=True,verbose_name="Titre")
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, default='',   blank=True, related_name='relationship_remediation') 
    video = models.CharField(max_length=255, default='',  blank=True,   verbose_name="url de la vidéo")
    mediation = models.FileField(upload_to=file_directory_path,verbose_name="Fichier", blank=True,   default ="")
    audio = models.BooleanField( default=0,    verbose_name="Audio texte ?") 
    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée (en min.)")  
    consigne = models.BooleanField( default=0,    verbose_name="Consigne ?") 
    courses = models.ManyToManyField(Course, blank=True,  related_name='courses_remediation', verbose_name="Cours") 

    def __str__(self):        
        return "title {}".format(self.title)

class Remediationcustom(models.Model):

    title = models.CharField(max_length=255, default='',  blank=True,verbose_name="Titre")
    customexercise = models.ForeignKey(Customexercise,  on_delete=models.CASCADE, default='',   blank=True, related_name='customexercise_remediation') 
    video = models.CharField(max_length=255, default='',  blank=True,   verbose_name="url de la vidéo")
    mediation = models.FileField(upload_to=file_folder_path,verbose_name="Fichier", blank=True,   default ="")
    audio = models.BooleanField( default=0,    verbose_name="Audio texte ?") 
    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée (en min.)")  
    consigne = models.BooleanField( default=0,    verbose_name="Consigne ?") 
    courses = models.ManyToManyField(Course, blank=True,  related_name='courses_remediationcustom', verbose_name="Cours") 

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


########################################################################################################################################### 
########################################################################################################################################### 
########################################################   Mastering        ############################################################### 
########################################################################################################################################### 
########################################################################################################################################### 
class Mastering(models.Model):

    relationship = models.ForeignKey(Relationship, related_name="relationship_mastering", on_delete=models.PROTECT, verbose_name="Exercice")
    consigne = models.CharField(max_length=255, default='',  blank=True,   verbose_name="Consigne")   
    video = models.CharField(max_length=50, default='',  blank=True,   verbose_name="code de vidéo Youtube")   
    mediation = models.FileField(upload_to= directory_path_mastering, verbose_name="Fichier", default="", null = True, blank= True) 
    writing = models.BooleanField( default=0,  verbose_name="Page d'écriture", ) 
    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée")    

    scale = models.PositiveIntegerField(default=3, editable= False) 
    ranking = models.PositiveIntegerField(default=0,  editable= False) 
    exercise = models.ForeignKey(Exercise, related_name = "exercise", on_delete=models.PROTECT, editable=False, default="", null = True, blank= True )   
    courses = models.ManyToManyField(Course, blank=True, related_name='courses_mastering')
    
    def __str__(self):
        return "{}".format(self.relationship)

    def is_done(self,student): 
        is_do = False  
        if Mastering_done.objects.filter(mastering = self, student = student).count() > 0 :  
            is_do = True  
        return is_do       


class Mastering_done(models.Model):

    mastering = models.ForeignKey(Mastering, related_name="mastering_done", editable=False, on_delete=models.PROTECT, verbose_name="Exercice")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, editable=False, related_name='students_mastering_done')
    writing = RichTextUploadingField( blank=True, verbose_name="Texte*") 
    
    def __str__(self):
        return "{}".format(self.mastering)


########################################################################################################################################### 
########################################################################################################################################### 
################################################   Mastering  from customexercise       ################################################### 
########################################################################################################################################### 
########################################################################################################################################### 
class Masteringcustom(models.Model):

    customexercise = models.ForeignKey(Customexercise, related_name="customexercise_mastering_custom", on_delete=models.PROTECT, verbose_name="Exercice")
    consigne = models.CharField(max_length=255, default='',  blank=True,   verbose_name="Consigne")   
    video = models.CharField(max_length=50, default='',  blank=True,   verbose_name="code de vidéo Youtube")   
    mediation = models.FileField(upload_to= directory_path_mastering, verbose_name="Fichier", default="", null = True, blank= True) 
    writing = models.BooleanField( default=0,  verbose_name="Page d'écriture", ) 
    duration = models.PositiveIntegerField(  default=15,  blank=True,  verbose_name="Durée estimée")    

    scale = models.PositiveIntegerField(default=3, editable= False) 
    ranking = models.PositiveIntegerField(default=0,  editable= False) 
    exercise = models.ForeignKey(Exercise, related_name = "exercise_mastering_custom", on_delete=models.PROTECT, editable=False, default="", null = True, blank= True )   
    courses = models.ManyToManyField(Course, blank=True, related_name='courses_mastering_custom')
    
    def __str__(self):
        return "{}".format(self.customexercise)



    def is_done(self,student): 
        is_do = False  
        if Masteringcustom_done.objects.filter(mastering = self, student = student).count() > 0 :  
            is_do = True  
        return is_do       

class Masteringcustom_done(models.Model):

    mastering = models.ForeignKey(Masteringcustom, related_name="mastering_custom_done", editable=False, on_delete=models.PROTECT, verbose_name="Exercice")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, editable=False, related_name='students_mastering_custom_done')
    writing = RichTextUploadingField( blank=True, verbose_name="Texte*") 
    
    def __str__(self):
        return "{}".format(self.mastering)

########################################################################################################################################### 
########################################################################################################################################### 
##############################################################  Annotations       ######################################################### 
########################################################################################################################################### 
########################################################################################################################################### 

class Comment(models.Model): # Commentaire du l'enseignant vers l'élève pour les exercices non autocorrigé coté enseignant

    teacher = models.ForeignKey(Teacher,  on_delete=models.CASCADE, blank=True,  related_name='teacher_comment', editable=False)
    comment = models.TextField() 

    def __str__(self):        
        return "{} : {}".format(self.comment, self.teacher)

class Generalcomment(models.Model): # Commentaire conservé d'une copie  coté enseignant

    teacher = models.ForeignKey(Teacher,  on_delete=models.CASCADE, blank=True,  related_name='teacher_generalcomment', editable=False)
    comment = models.TextField() 

    def __str__(self):        
        return "{} : {}".format(self.comment, self.teacher)

class CommonAnnotation(models.Model):
 
    classe = models.CharField(max_length=255, editable=False)   
    style = models.CharField(max_length=255, editable=False) 
    attr_id = models.CharField(max_length=255, editable=False) 
    content = models.TextField(editable=False) 
  
    class Meta:
        abstract = True

class Annotation(CommonAnnotation):

    writtenanswerbystudent = models.ForeignKey(Writtenanswerbystudent, on_delete=models.CASCADE,related_name='annotations') 

    def __str__(self):
        return "{}".format(self.writtenanswerbystudent)

    class Meta:
        unique_together = ['writtenanswerbystudent', 'attr_id']

class Customannotation(CommonAnnotation):

    customanswerbystudent = models.ForeignKey(Customanswerbystudent, on_delete=models.CASCADE, related_name='annotations') 

    def __str__(self):
        return "{}".format(self.customanswerbystudent)


    class Meta:
        unique_together = ['customanswerbystudent', 'attr_id']    