from django.db import models
from datetime import date

from account.models import Student, Teacher, ModelWithCode, generate_code
from socle.models import Level
from qcm.models import Parcours
from account.models import ModelWithCode
from django.apps import apps
from django.utils import   timezone
from django.db.models import Q
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()


 
class Group(ModelWithCode):
    """ Group est une classe d'élèves coté enseignant -- Ce qui permet de faire un groupe avec une ou plusieurs divisions """
    name = models.CharField(max_length=255, verbose_name="Nom*")
    color = models.CharField(max_length=255, default='#46119c', blank=True, null=True, verbose_name="Couleur*")
    students = models.ManyToManyField(Student, related_name="students_to_group", blank=True, verbose_name="Élèves*")
    teacher = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.CASCADE, related_name="groups", verbose_name="Enseignant*")
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name="groups", verbose_name="Niveau*")
    assign = models.BooleanField(default=1)
    suiviparent = models.BooleanField(default=0)
    lock = models.BooleanField(default=0)    

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
        return nb_group == nb


    def is_task_exists(self):
        Relationship = apps.get_model('qcm', 'Relationship')
        today = timezone.now().date()
        test = False
        students = self.students.prefetch_related("students_relationship")
        for student in students:
            if Relationship.objects.filter(students=student, date_limit__gte=today).count() > 0:
                test = True
                break
        return test



    def parcours_counter(self):
        """
        Donne le nombre total de parcours, le nombre de visibles et de publiés du groupe
        """
        students = self.students.order_by("user__last_name")
        number_of_parcours_of_this_level_by_this_teacher = self.teacher.teacher_parcours.filter(level = self.level).count()
        parcours_tab = []
        parcours_id_tab = []

        for student in students:
            parcourses = student.students_to_parcours.all()
            parcours_tab = [parcours for parcours in parcourses if parcours.id not in parcours_id_tab]
            if len(parcours_tab) == number_of_parcours_of_this_level_by_this_teacher:
                break

        data, nb, nbf, nbp, nbef , nbe = {}, 0, 0, 0, 0, 0
        for parcours in parcours_tab:
            if parcours.is_favorite and not parcours.is_evaluation :
                nbf += 1
            if parcours.is_publish:
                nbp += 1
            if parcours.is_evaluation:
                nbef += 1
            if not parcours.is_evaluation:
                nb += 1
            if parcours.is_evaluation and parcours.is_favorite :
                nbe += 1

        data["count_students"] = students.values("user").count()
        data["students"] = students.values("user__id", "user__last_name", "user__first_name")
        data["nb_parcours"] = nb
        data["nb_parcours_visible"] = nbp
        data["nb_parcours_favorite"] = nbf
        data["nb_evaluation_favorite"] = nbef 
        data["nb_evaluation"] = nbe 

        return data

 


 