from django.conf import settings
from account.models import Teacher, Student, User
from socle.models import Level
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from group.models import Group
from qcm.models import Parcours, Studentanswer, Exercise, Relationship
from sendmail.models import Email
from django.db.models import Q
from datetime import datetime, timedelta
import time
import pytz
from itertools import chain
from django.utils import timezone


def menu(request):
    if request.user.is_authenticated:

        if request.user.time_zone:
            time_zone = request.user.time_zone
            timezone.activate(pytz.timezone(time_zone))
            today = timezone.localtime(timezone.now())
        else:
            today = timezone.now()

        if request.user.user_type == User.TEACHER:

            teacher = request.user.user_teacher
            nbs = Studentanswer.objects.filter(parcours__teacher=teacher, date=today).count()
            nbe = Email.objects.distinct().filter(receivers=request.user, today=today).count()
            nb_not = nbs + nbe
            levels = Level.objects.all()

            return {
                'today': today,
                'nb_not': nb_not,
                'levels': levels,
            }

        elif request.user.user_type == User.STUDENT:

            student = Student.objects.get(user=request.user)
            last_exercises_done = Studentanswer.objects.filter(student=student).order_by("-date")[:10]
            parcours = Parcours.objects.filter(is_publish=1, exercises__level=student.level).exclude(author=None)
            parcourses = Parcours.objects.filter(is_publish=1,
                                                 is_evaluation=0,
                                                 students=student)  # tous les parcours attribués à cet élève
            groups = student.students_to_group.all()

            return {
                'student': student,
                'parcourses': parcourses,
                'parcours': parcours,
                'last_exercises_done': last_exercises_done,
                'groups': groups,
                'today': today,
            }

        elif request.user.user_type == User.PARENT:
            this_user = User.objects.get(pk=request.user.id)

            return {
                'this_user': this_user,
                'today': today,
            }

    else:
        nb_teacher = Teacher.objects.all().count()
        nb_exercise = Exercise.objects.all().count()
        nb_student = Student.objects.all().count()
        nb_parcours = Parcours.objects.all().count()
        contributeurs = User.objects.filter(is_superuser=1)

        return {
            'nb_teacher': nb_teacher,
            'nb_exercise': nb_exercise,
            'nb_student': nb_student,
            'nb_parcours': nb_parcours,
            'contributeurs': contributeurs,
        }
