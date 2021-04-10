import pytz
from django.utils import timezone
from account.models import Teacher, Student, User
from qcm.models import Parcours, Studentanswer, Exercise, Demand
from sendmail.models import Email, Message
from socle.models import Level
from school.models import School
from group.models import Group
from tool.models import Tool

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
            #nbs = Studentanswer.objects.filter(parcours__teacher=teacher, date=today).count()
            nbe = Email.objects.distinct().filter(receivers=request.user, today=today).count()
            #nb_not = nbs + nbe
            levels = Level.objects.all()
            nb_demand = Demand.objects.filter(done=0).count()

            mytools = Tool.objects.filter(is_publish=1, teachers = teacher).order_by("title")

            ### Exercice traités non vus par l'enseignant -> un point orange dans la barre de menu sur message
            is_pending_studentanswers = False
            pending_s = Studentanswer.objects.filter(parcours__teacher = teacher, is_reading = 0)
            if pending_s  :
                is_pending_studentanswers = True
 
            ### Permet de vérifier qu'un enseignant est dans un établissement sacado
            if teacher.user.school :
                if teacher.user.school.is_active :
                    sacado_asso = True

            return {'today': today, 'nbe': nbe, 'levels': levels,  'nb_demand' : nb_demand , 'mytools' : mytools , 'sacado_asso' : sacado_asso , "is_pending_studentanswers" : is_pending_studentanswers  }

        elif request.user.is_student:
            
            student = Student.objects.get(user=request.user)
            groups = student.students_to_group.all()

            teacher_to_student = False
            if "_e-test" in student.user.username :
                teacher_to_student = True

            if student.user.school :
                if student.user.school.is_active :
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
                'teacher_to_student' : teacher_to_student ,                
            }

        elif request.user.is_parent:
            this_user = User.objects.get(pk=request.user.id)
            students = this_user.parent.students.all()
            last_exercises_done = Studentanswer.objects.filter(student__in= students).order_by("-date")[:10]

            return {
                'this_user': this_user,
                'last_exercises_done': last_exercises_done,
                 'sacado_asso' : sacado_asso , 
            }


    else:
 
 
 
        contributeurs = User.objects.filter(is_superuser=1)
 
 
        return {
 
            'contributeurs': contributeurs,
  
        }
