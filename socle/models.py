from django.db import models
from multiselectfield import MultiSelectField
from django.apps import apps
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


today = timezone.now().date()



class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    color = models.CharField(max_length=255, default ="" , editable=False)
    shortname = models.CharField(max_length=10, default ="" , verbose_name="Abréviation")
 
    def __str__(self):
        return "{}".format(self.name)



class Theme(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.CharField(max_length=255, default ="" , editable=False)
    subject  = models.ForeignKey(Subject, related_name="theme", default="",  null = True , on_delete=models.PROTECT, verbose_name="Enseignement")

    def __str__(self):
        return "{}".format(self.name)

    def string_id(self):
        return "{}".format(self.id)

    def as_score_by_theme(self, student, group):

        Resultknowledge = apps.get_model('account', 'Resultknowledge')
        knowledges = self.knowledges.filter(level=group.level)
        resultknowledges = Resultknowledge.objects.filter(student = student, knowledge__in=knowledges)
        nb = len(resultknowledges)
        somme = 0
        for r in resultknowledges:
            somme += r.point
        try :
            avg = int(somme/nb)
        except :
            avg = ""
        return avg



    def all_details(self,parcours):
        Relationship = apps.get_model('qcm', 'Relationship')
        detail = {}
        detail["pub"] = Relationship.objects.filter(parcours=parcours, exercise__theme = self,is_publish=1).count()
        detail["total"] = Relationship.objects.filter(parcours=parcours, exercise__theme = self).count()        
        detail["done"] = Relationship.objects.filter(parcours=parcours, exercise__theme = self).exclude(date_limit=None).count()
        detail["in_air"] = Relationship.objects.filter(parcours=parcours, exercise__theme = self,date_limit__gte=today).count()
        return detail







class Level(models.Model):

    CYCLES = (
        ('c1', 'Cycle 1'),
        ('c2', 'Cycle 2'),
        ('c3', 'Cycle 3'),
        ('c4', 'Cycle 4'),
        ('c5', 'Cycle 5'),
    )

    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nom")
    shortname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Abréviation")
    cycle = models.CharField(max_length=10, default='c1', choices=CYCLES,  verbose_name="Cycle")
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name="Image")    
    themes = models.ManyToManyField(Theme, related_name = "theme_level", default="",  verbose_name="Thèmes")


    def __str__(self):
        return self.name

    def contrastColorText(self):
        """ donne le noir ou blanc selon la couleur initiale  """
        color1 = self.color[1:3]
        color2 = self.color[3:5]
        color3 = self.color[5:7]
        if 0.299 *  int(color1, 16) + 0.587 * int(color2, 16) + 0.114 * int(color3, 16)  > 150 :
            return "#000000"
        else :
            return "#FFFFFF"

    def nbknowlegde(self):
        return self.knowledges.filter(level=self).count()

    def exotot(self):
        return self.exercises.filter(supportfile__is_title=0).count()

    def notexo(self):
        nb, m  = 0 , 0
        Exercise = apps.get_model('qcm', 'Exercise')
        Knowledge = apps.get_model('socle', 'Knowledge')
        n = Knowledge.objects.filter(level=self).count()
        for k in Knowledge.objects.filter(level=self) : 
            if Exercise.objects.filter(level=self, knowledge =k).exists():
                m+=1

        nb = n - m
        return nb


class Knowledge(models.Model):
    level = models.ForeignKey(Level, related_name="knowledges", default="", on_delete=models.PROTECT, verbose_name="Niveau")
    theme = models.ForeignKey(Theme, related_name="knowledges", on_delete=models.PROTECT, verbose_name="Thème")
    name = models.CharField(max_length=10000, verbose_name="Nom")

    def __str__(self):
        return self.name

    def used(self):
        return self.nb_exercise() > 0

    def nb_exercise(self):
        return self.exercises.count()


    ### plus utilisée -----
    def nb_exercise_used(self,  parcours_tab): # parcours du groupe

        Relationship = apps.get_model('qcm', 'Relationship') 
        nb = 0
        relationships = Relationship.objects.filter(exercise__knowledge=self , parcours__in = parcours_tab).order_by("exercise").distinct()
      
        return nb 


    def send_scorek(self,student):

        try:
            r = self.results_k.get(student=student)
            score = r.point
        except ObjectDoesNotExist:
            score = ""

        return score


    def exercices_by_knowledge(self,student,group):

        Exercise = apps.get_model('qcm', 'Exercise')
        exercises = Exercise.objects.filter(knowledge=self)
        return exercises


    def score_student_parcours(self,student,parcours):

        Studentanswer = apps.get_model('qcm', 'Studentanswer')
        r = Studentanswer.objects.filter(student = student, parcours = parcours , exercise__knowledge = self).aggregate(Avg('point'))
        if r["point__avg"] :
            score = int(r["point__avg"])
        else :
            score = ""

        return score


    def association_knowledge_supportfile(self, supportfile):

        Exercise = apps.get_model('qcm', 'Exercise')
        Parcours = apps.get_model('qcm', 'Parcours')

        if Exercise.objects.filter(supportfile=supportfile, knowledge=self).count() > 0:
            test = True
            exercises = Exercise.objects.filter(supportfile=supportfile, knowledge=self)
            som = 0
            for exercise in exercises:
                if Parcours.objects.filter(exercises=exercise):
                    som += 1
            boolean = som > 0

        else:
            test = False
            boolean = False

        return {"exercise": test, "parcours": boolean}



class Skill(models.Model): 
    name = models.CharField(max_length=50 , verbose_name="Nom")
    subject  = models.ForeignKey(Subject, related_name="skill", default="", on_delete=models.PROTECT, null = True ,  verbose_name="Enseignement")

    def __str__(self):
        return "{}".format(self.name )