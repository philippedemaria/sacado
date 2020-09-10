import pytz
from django.utils import timezone

from account.models import Teacher, Student, User
from qcm.models import Parcours, Studentanswer, Exercise, Demand
from sendmail.models import Email
from socle.models import Level
from school.models import School

def menu(request):
    if request.user.is_authenticated:

        if request.user.time_zone:
            time_zome = request.user.time_zone
            timezone.activate(pytz.timezone(time_zome))
            today = timezone.localtime(timezone.now())
        else:
            today = timezone.now()
 
        if request.user.is_teacher:
            teacher = request.user.teacher
            nbs = Studentanswer.objects.filter(parcours__teacher=teacher, date=today).count()
            nbe = Email.objects.distinct().filter(receivers=request.user, today=today).count()
            nb_not = nbs + nbe
            levels = Level.objects.all()
            nb_demand = Demand.objects.filter(done=0).count()
            return {'today': today, 'nb_not': nb_not, 'levels': levels,  'nb_demand' : nb_demand  }

        elif request.user.is_student:
            student = Student.objects.get(user=request.user)
            last_exercises_done = Studentanswer.objects.filter(student=student).order_by("-date")[:10]
            parcours = Parcours.objects.filter(is_publish=1, exercises__level=student.level).exclude(author=None).order_by("ranking")
            parcourses = Parcours.objects.filter(is_publish=1, is_evaluation=0,
                                                 students=student).order_by("ranking")  # tous les parcours attribués à cet élève
            groups = student.students_to_group.all()

            return {
                'student': student,
                'parcourses': parcourses,
                'parcours': parcours,
                'last_exercises_done': last_exercises_done,
                'groups': groups,
            }

        elif request.user.is_parent:
            this_user = User.objects.get(pk=request.user.id)
            return {
                'this_user': this_user,
            }


    else:
        nb_teacher = Teacher.objects.all().count()
        nb_exercise = Exercise.objects.all().count()
        nb_student = Student.objects.all().count()
        nb_parcours = Parcours.objects.all().count()
        contributeurs = User.objects.filter(is_superuser=1)
        nb_school = School.objects.all().count()
        schools = School.objects.all()
        return {
            'nb_teacher': nb_teacher,
            'nb_exercise': nb_exercise,
            'nb_student': nb_student,
            'nb_parcours': nb_parcours,
            'contributeurs': contributeurs,
            'nb_school' : nb_school,
            'schools' : schools,
        }
