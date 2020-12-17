from django.db import models
from multiselectfield import MultiSelectField
from django.apps import apps
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from general_fonctions import *

 



class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    color = models.CharField(max_length=255, default ="" , editable=False)
    shortname = models.CharField(max_length=10, default ="" , verbose_name="Abréviation")
 
    def __str__(self):
        return "{}".format(self.shortname)

class Theme(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.CharField(max_length=255, default ="" , editable=False)
    subject  = models.ForeignKey(Subject, related_name="theme", default="",  null = True , on_delete=models.PROTECT, verbose_name="Enseignement")

    def __str__(self):
        return "{} : {}".format(self.subject,self.name)

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
        today = time_zone_user(parcours.teacher.user)
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

class Waiting(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nom")
    theme  = models.ForeignKey(Theme, related_name="waitings",  on_delete=models.CASCADE, verbose_name="Thème")
    level = models.ForeignKey(Level, related_name="waitings", default="", on_delete=models.CASCADE, verbose_name="Niveau")

    def __str__(self):
        return "{} : {}".format(self.theme,self.name)


    def send_scorek(self,student):


        try:

            coef, score , score_ce = 0, 0 , 0            
            for k in self.knowledges.all():

                if k.results_k.filter(student=student).exists() :
                    r = k.results_k.filter(student=student).last()
                    score += int(r.point)
                    coef += 1

                if k.knowledge_correctionknowledge.filter(student=student).exists() :
                    ce = k.knowledge_correctionknowledge.filter(student=student).last()
                    score_ce += ce.point + 1 
                    coef += 1
 
            if coef != 0:
                score = int((score + score_ce)/coef)
            else :
                score = ""

        except ObjectDoesNotExist:
            score = ""

        return score










class Knowledge(models.Model):
    level = models.ForeignKey(Level, related_name="knowledges", default="", on_delete=models.CASCADE, verbose_name="Niveau")
    theme = models.ForeignKey(Theme, related_name="knowledges", on_delete=models.CASCADE, verbose_name="Thème")
    name = models.CharField(max_length=10000, verbose_name="Nom")
    waiting  = models.ForeignKey(Waiting, related_name="knowledges", default="",  null = True , on_delete=models.CASCADE, verbose_name="Attendu")


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
            coef, score , score_ce = 0, 0 , 0
            if self.results_k.filter(student=student).exists() :
                r = self.results_k.filter(student=student).last()
                score = r.point
                coef += 1

            if self.knowledge_correctionknowledge.filter(student=student).exists() :
                ce = self.knowledge_correctionknowledge.filter(student=student).last()
                score_ce = ce.point + 1 
                coef += 1

            if coef != 0:
                score = int((score + score_ce)/coef)
            else :
                score = ""                

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

    def custom_score(self, customexercise, student, parcours):
        Stage = apps.get_model('school', 'Stage')    
        try :
            stage = Stage.objects.get(school = student.user.school)
            up = stage.up
            med = stage.medium
            low = stage.low
        except :
            up = 85
            med = 65
            low = 35
        try :
            c_knowledge = self.knowledge_correctionknowledge.filter(customexercise = customexercise,  parcours = parcours, student = student).last()
            point = c_knowledge.point
            if point > up :
                crit = 4
            elif point > med :
                crit = 3
            elif point > low :  
                crit = 2
            elif point > -1 :  
                crit = 1
            else :  
                crit = 0
        except :
            crit = 0
        return crit

class Skill(models.Model): 
    name = models.CharField(max_length=10000, verbose_name="Nom")
    subject  = models.ForeignKey(Subject, related_name="skill", default="", on_delete=models.PROTECT, null = True ,  verbose_name="Enseignement")

    def __str__(self):
        return "{}".format(self.name )


    def custom_score(self, customexercise, student, parcours):

        Stage = apps.get_model('school', 'Stage')
        try :
            stage = Stage.objects.get(school = student.user.school)
            up = stage.up
            med = stage.medium
            low = stage.low
        except :
            up = 85
            med = 65
            low = 35
        try :
            c_skill = self.skill_correctionskill.filter(customexercise = customexercise,  parcours = parcours, student = student).last()
            pt = c_skill.point
            if pt > up :
                crit = 4
            elif pt > med :
                crit = 3
            elif pt > low :  
                crit = 2
            elif pt > -1 :  
                crit = 1
            else :  
                crit = 0
        except :
            crit = 0
        return crit



    def used(self):
        return self.nb_exercise() > 0

    def nb_exercise(self):
        return self.skills_relationship.count()


    def send_scorek(self,student):

        try:
            coef, score , score_ce = 0, 0 , 0
            if self.results_s.filter(student=student).exists() :
                r = self.results_s.filter(student=student).last()
                score = r.point
                coef += 1

            if self.skill_correctionskill.filter(student=student).exists() :
                ce = self.skill_correctionskill.filter(student=student).last()
                score_ce = ce.point 
                coef += 1

            if coef != 0:
                score = int((score + score_ce)/coef)
            else :
                score = ""                

        except ObjectDoesNotExist:
            score = ""

        return score 


    def send_scorekp(self,student,parcours):

        try:
            coef, score   = 0, 0  
            for result_s in  self.skill_resultggbskills.filter(student=student,relationship__in = parcours.parcours_relationship.all()):
                score += result_s.point
                coef += 1

            for ce in  self.skill_correctionskill.filter(student=student,parcours=parcours) :
                score += ce.point 
                coef += 1

            if coef != 0:
                score = int(score/coef)
            else :
                score = ""                

        except ObjectDoesNotExist:
            score = ""

        return score 