from django.db import models
from datetime import date

from account.models import Student, Teacher, ModelWithCode, generate_code
from socle.models import Level
from qcm.models import Parcours, ModelWithCode
from django.apps import apps
from django.utils import   timezone
from django.db.models import Q
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()


 
class Group(ModelWithCode):
    """ Group est une classe d'élèves coté enseignant -- Ce qui permet de faire un groupe avec une ou plusieurs divisions """
    name = models.CharField(max_length=255, verbose_name="Nom*")
    color = models.CharField(max_length=255, default='#46119c', verbose_name="Couleur*")
    students = models.ManyToManyField(Student, related_name="students_to_group",  blank=True,verbose_name="Élèves*")
    teacher = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.CASCADE, related_name="teacher_to_group", verbose_name="Enseignant*")
    level = models.ForeignKey(Level,  on_delete=models.PROTECT, related_name="level_to_group", verbose_name="Niveau*")
    parcours = models.OneToOneField(Parcours, related_name="parcours_group", default='', blank=True, on_delete=models.SET_DEFAULT) 
    assign = models.BooleanField( default = 1 )
    suiviparent = models.BooleanField( default = 0 )


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def contrastColorText(self):
        """ donne le noir ou blanc selon la couleur initiale  """
        color1 = self.color[1:3]
        color2 = self.color[3:5]
        color3 = self.color[5:7]
        if 0.299 * int(color1, 16) + 0.587 * int(color2, 16) + 0.114 * int(color3, 16) > 150:
            return "#000000"
        else:
            return "#FFFFFF"

    def nb_exos_in(self):
        Exercise = apps.get_model('qcm', 'Exercise')
        nb = Exercise.objects.filter(level=self.level).count()
        return nb
 
    def all_selected_exercices(self):
        Exercise = apps.get_model('qcm', 'Exercise')
        nb_group = self.parcours.exercises.count()
        nb = Exercise.objects.filter(level=self.level).count()
        if nb_group == nb :
            ok = True
        else :
            ok = False
        return ok
 

    def is_task_exists(self):
        Relationship = apps.get_model('qcm', 'Relationship')
        today = timezone.now()
        test = False
        students = self.students.all()
        for student in students :
            if Relationship.objects.filter(exercise__students = student, date_limit__gte = today).count() > 0:
                test = True
                break

        return test 


    def nb_parcours(self):

        students = self.students.all()
        parcours_tab = []
        for student in students :
            parcourses = student.students_to_parcours.all()
            for parcours in parcourses :
                if parcours.id not in parcours_tab :
                    parcours_tab.append(parcours.id)
        nb_parcours  = len(parcours_tab)  
        return nb_parcours 





    def nb_parcours_visible(self):

        students = self.students.all()
        parcours_tab = []
        for student in students :
            parcourses = student.students_to_parcours.filter(is_publish=1)
            for parcours in parcourses :
                if parcours.id not in parcours_tab :
                    parcours_tab.append(parcours.id)
        nb_parcours  = len(parcours_tab)  
        return nb_parcours 




    def nb_parcours_favorite(self):
 
        students = self.students.all()
        parcours_tab = []
        for student in students :
            parcourses = student.students_to_parcours.filter(is_favorite=1)
            for parcours in parcourses :
                if parcours.id not in parcours_tab :
                    parcours_tab.append(parcours.id)
        nb_parcours  = len(parcours_tab) 
        return nb_parcours  

       