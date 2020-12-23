import pytz
from django.utils import timezone

from account.models import Teacher, Student, User
from qcm.models import Parcours, Studentanswer, Exercise, Demand
from sendmail.models import Email
from socle.models import Level
from school.models import School
from group.models import Group

def menu(request):

    if request.user.is_authenticated:
        sacado_asso = False
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

            if teacher.user.school :
                sacado_asso = True

            return {'today': today, 'nb_not': nb_not, 'levels': levels,  'nb_demand' : nb_demand , 'sacado_asso' : sacado_asso ,  }

        elif request.user.is_student:

            student = Student.objects.get(user=request.user)
            groups = student.students_to_group.all()

            if student.user.school :
                sacado_asso = True

            group_id = request.session.get("group_id",None)

            if group_id :
                group = Group.objects.get(pk=group_id)
            else :
                group = None

            return {
                'student': student,
                'sacado_asso' : sacado_asso , 
                'group' : group ,
                'groups' : groups,
            }

        elif request.user.is_parent:
            this_user = User.objects.get(pk=request.user.id)
            students = this_user.parent.students.all()
            last_exercises_done = Studentanswer.objects.filter(student__in= students).order_by("-date")[:10]

            return {
                'this_user': this_user,
                'last_exercises_done': last_exercises_done,
                 'sacado_asso' : sacado_asso , 
                 'group' : group,
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
