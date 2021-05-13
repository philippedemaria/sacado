import pytz
from django.utils import timezone
from account.models import Teacher, Student, User
from qcm.models import Parcours, Studentanswer, Exercise, Demand
from school.models import School
from association.models import Accounting , Rate
from sendmail.models import Email, Message
from socle.models import Level
from school.models import School
from group.models import Group
from tool.models import Tool
from datetime import datetime 

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
            renew_propose = False
            if teacher.user.school :
                if teacher.user.school.is_active :
                    sacado_asso = True
                    
                ### Rapelle le renouvellement de la cotisation
                renew = request.session.get("renewal", None)
                if not renew :
                    rates = Rate.objects.all() #tarifs en vigueur 
                    school_year = rates.first().year #tarifs pour l'année scolaire
                    school_year_tab = school_year.split("-")
                    renew_date = datetime(int(school_year_tab[0]),5,15)
                    next_renew_date = datetime(int(school_year_tab[1]),5,15)
                    renewal = True
                    if Accounting.objects.filter(school = teacher.user.school, is_active = 1, date__gte=renew_date, date__lte=next_renew_date ).count() == 1:
                        renewal = False
                        request.session["renewal"] = True

                    renew_propose = False
                    now =  datetime.now()
                    if now > datetime(int(today.year),5,15) and renewal :
                        renew_propose = True


            return {'today': today, 'index_tdb' : False , 'nbe': nbe, 'levels': levels, 'renew_propose' : renew_propose ,  'nb_demand' : nb_demand , 'mytools' : mytools , 'sacado_asso' : sacado_asso , "is_pending_studentanswers" : is_pending_studentanswers  }

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
                'index_tdb' : False ,              
            }

        elif request.user.is_parent:
            this_user = User.objects.get(pk=request.user.id)
            students = this_user.parent.students.all()
            last_exercises_done = Studentanswer.objects.filter(student__in= students).order_by("-date")[:10]

            return {
                'this_user': this_user,
                'last_exercises_done': last_exercises_done,
                 'sacado_asso' : sacado_asso , 
                 'index_tdb' : False , 
            }


    else:
 
 
 
        contributeurs = User.objects.filter(is_superuser=1)
 
 
        return {
 
            'contributeurs': contributeurs,
  
        }
