from django.db import models
from datetime import date

from account.models import Student, Teacher, ModelWithCode, generate_code
from socle.models import Level, Subject , Waiting
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
    teachers = models.ManyToManyField(Teacher, blank=True,   editable=False, through="Sharing_group", related_name="teacher_group")
    subject = models.ForeignKey(Subject, default = "" ,  null=True, on_delete=models.PROTECT, related_name="subject_group", verbose_name="Matière*")
 

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
        today = timezone.now() 
        test = False
        students = self.students.prefetch_related("students_relationship")
        for student in students:
            if Relationship.objects.filter(students=student, date_limit__gte=today).count() > 0:
                test = True
                break
        return test



    def parcours_counter(self,teacher):
        """
        Donne le nombre total de parcours/évaluations, le nombre de visibles et de publiés du groupe
        """
        unameTest = teacher.user.username+"Test"
        students = self.students.exclude(user__username=unameTest).order_by("user__last_name")
        snt = students.count()

        if self.students.filter(user__username__contains=unameTest).count() == 1 : 
            profilTest = True
        else :
            profilTest = False





        parcourses = []
        for student in students:
            for p in student.students_to_parcours.filter(Q(author=teacher)|Q(teacher=teacher)|Q(coteachers=teacher),level = self.level).exclude(is_leaf=1) :
                if p not in parcourses  :
                    parcourses.append(p)


        data, nb, nbf, nbp, nbef , nbe = {}, 0, 0, 0, 0, 0
        for parcours in parcourses :
            if parcours.is_favorite and not parcours.is_evaluation :
                nbf += 1
            if parcours.is_publish and not parcours.is_evaluation :
                nbp += 1
            if parcours.is_evaluation:
                nbe  += 1
            if not parcours.is_evaluation:
                nb += 1
            if parcours.is_evaluation and parcours.is_favorite :
                nbef += 1

        data["count_students"] = snt
        data["students"] = students.values("user__id", "user__last_name", "user__first_name")
        data["nb_parcours"] = nb
        data["nb_parcours_visible"] = nbp
        data["nb_parcours_favorite"] = nbf
        data["nb_evaluation_favorite"] = nbef 
        data["nb_evaluation"] = nbe
        data["students_no_test"] = snt
        data["profiltest"] = profilTest                 

        return data



    def parcours(self):
        parcours_set = set()
        for student in self.students.all() :
            parcours_set.update(student.students_to_parcours.filter( subject = self.subject))
        return list(parcours_set)


    def parcours_visible(self):
        parcours_set = set()
        for student in self.students.all() :
            parcours_set.update(student.students_to_parcours.filter(is_publish = 1))
        return list(parcours_set)


    def folders(self):
        parcours_set = set()
        for student in self.students.all() :
            parcours_set.update(student.students_to_parcours.filter(is_folder=1, subject = self.subject))
        return list(parcours_set)


    def themes(self):
        parcours_set = set()
        for student in self.students.all() :
            parcours_set.update(student.students_to_parcours.filter(Q(is_folder=1)|Q(is_leaf=0), subject = self.subject))

        return list(parcours_set)



    def sharing_role(self,teacher):
        """
        Renvoie le role d'un enseignant pour un groupe donné
        """
        data = {}
        reader , publisher = False , False
        if self.group_sharingteacher.filter(teacher=teacher).exists() :
            shared_grps = Sharing_group.objects.get(group = self , teacher=teacher)
            if shared_grps.role == 0 :
                reader = True
            else :
                publisher = True

        data["publisher"] = publisher
        data["reader"] = reader 
        return data


    def is_pending_correction(self):
        """
        Prédicat pour tester s'il existe des corrections en attente
        """

        submit = False

        for student in self.students.all() :
            if student.student_custom_answer.filter(is_corrected = 0) :
                submit = True 
                break
            if student.student_written_answer.filter(is_corrected = 0) :
                submit = True 
                break
        return submit

 
    def is_shared(self):
        """
        Prédicat pour tester si le groupe est en co animation
        """
        is_shared = False
        if len(self.group_sharingteacher.all()) > 0 :
            is_shared = True

        return is_shared



    def waitings(self):
        return Waiting.objects.filter(level = self.level, theme__subject = self.subject)
    

 
    def authorize_access(self, teacher): 
        """
        Authorise l'acces de ce groupe à un enseignant
        """
        access, role = False, False
        if teacher.teacher_sharingteacher.filter(group = self).count() > 0 :
            access = True
        if self.teacher == teacher or access :
            access = True 
        if access and teacher.teacher_sharingteacher.filter(group = self).exists():
            sg = teacher.teacher_sharingteacher.filter(group = self).last()
            role = sg.role

        data = {}
        data["role"] = role
        data["access"] = access

        return data



class Sharing_group(models.Model):

    group = models.ForeignKey(Group, on_delete=models.PROTECT,  null=True, blank=True,   related_name='group_sharingteacher',  editable= False)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True, blank=True,  related_name='teacher_sharingteacher',  editable= False)
    role = models.BooleanField(default=0)
 
    

    def __str__(self):
        return "{} : {} : {}".format(self.group, self.teacher, self.role)
 
    

