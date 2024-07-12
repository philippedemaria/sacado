import pytz
from django.utils import timezone
from association.models import Customer
from account.models import Teacher, Student, User
from qcm.models import Parcours, Studentanswer, Exercise, Demand
from school.models import School
from association.models import Accounting , Rate , Abonnement
from sendmail.models import Email, Message
from socle.models import Level
from school.models import School
from book.models import Mybook
from group.models import Group
from tool.models import Tool,Qtype
from datetime import datetime , timedelta 

##############################################################################################################################################
##############################################################################################################################################
###              L'établissement est-t-il membre sacado 
##############################################################################################################################################
##############################################################################################################################################


def is_sacado_asso(this_user, today):
    is_sacado = False
    is_active = False
    try :
        customer = this_user.school.customer 
        if today.date() < customer.date_stop  :
            is_sacado = True
            is_active = True
    except :
        pass

    if this_user.is_superuser :
        is_sacado = True
        is_active = True
        
    return is_sacado, is_active


# def is_sacado_asso(this_user, today):
#     is_sacado = False
#     is_active = False
#     try :
#         abonnement = this_user.school.abonnement.last()
#         if today < abonnement.date_stop and abonnement.is_active :
#             is_sacado = True
#             is_active = True
#     except :
#         pass
#     if this_user.is_superuser :
#         is_sacado = True
#         is_active = True
#     return is_sacado, is_active



def is_quite_finish_sacado_asso(this_user, today):

    is_quite_finish = False
    try :
        customer = this_user.school.customer
        the_end_day = today+timedelta(days=15)

        if the_end_day.date() > customer.date_stop and customer.status == 3 :
            is_quite_finish = True
    except :
        pass

    return is_quite_finish

##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################


def menu(request):

    if request.user.is_authenticated:

        is_gar_check = request.session.get("is_gar_check",None)

        try : # Vérifie qu'un user ne crée pas un compte annexe pour scunter le GAR
            if not is_gar_check and request.user.school.gar :
                request.session["is_gar_check"] = True
        except : 
            pass

        theme_color        =  'css/Admin_'+request.user.color+'.css'
        navbar_theme_color =  'css/navbar_'+request.user.color+'.css'

        sacado_asso = False
        if request.user.time_zone:
            time_zome = request.user.time_zone
            timezone.activate(pytz.timezone(time_zome))
            today = timezone.localtime(timezone.now())
        else:
            today = timezone.now()

        if request.user.is_teacher:

            dico_helper = { "/account/profile" : "profile" , "/account/avatar" : "avatar" , "/account/updatepassword" : "updatepassword" , "/school/get_school" : "get_school" , "/account/background" : "background" ,
                            "/" : "groupe" , "/#" : "groupe" ,  "/qcm/folders" : "folders" ,  "/qcm/parcours" : "parcours" ,  "/qcm/evaluations" : "evaluations" ,  "/qcm/evaluations" : "evaluations" ,  "qcm/parcours_my_courses" : "parcours_my_courses" , 
                            "/tool_list" : "quizzes" , "/bibliotex/my_bibliotexs" : "my_bibliotexs" ,  "/flashcard/my_flashpacks" : "my_flashpacks" ,  "/qcm/exercises" : "exercises" ,  "/tool/list_visiocopie" : "list_visiocopie" ,  
                            "/tool/list_tools" : "list_tools" , "/tool/show/" : "tool_show"  , "/sendmail/" : "sendmail" , "/aefe/" : "aefe" , "/admin_tdb" : "admin_tdb" ,"/qcm/parcours_group/" : "parcours_group",
                            "/qcm/parcours_sub_parcours/" : 'parcours_sub_parcours' , '/qcm/parcours_update/' : "parcours_update" , "/group/show/" :"group_show" , "/group/update/" : "group_update" , '/qcm/parcours_show/' :  'parcours_show',
                            "/school/groups" : 'school_groups' , '/school/new_student/' : 'school_new_student' , '/school/new_student_list/' : 'school_new_student_list'  }

            nb_customers = 0
            nb_pendings  = 0
            nb_else      = 0  
            if request.user.is_superuser :
                nb_customers = Customer.objects.filter(status=3).count()
                nb_pendings  = Customer.objects.filter(status=2).count()
                nb_else      = Customer.objects.filter(status=1).count()

            ihelp=0 
            request_path = str(request.path) 
            while ihelp < len(request_path) and not('0'<=request_path[ihelp]<='9' ) : ihelp+=1  
            helper_key = request_path[:ihelp] 
            try :
                url_helper = "helpers/" + dico_helper[helper_key] + ".html"
            except :
                url_helper = "helpers/no_helper.html"
            
            qtypes = Qtype.objects.filter(is_online=1).exclude(pk=100).order_by('ranking')
            teacher = request.user.teacher

            nb_groups = teacher.groups.count()
            nb_levels = teacher.levels.count()
            #nbs = Studentanswer.objects.filter(parcours__teacher=teacher, date=today).count()
            nbe = Email.objects.values_list("id").distinct().filter(receivers=request.user, today=today).count()
            #nb_not = nbs + nbe
            levels = Level.objects.exclude(pk=13).order_by("ranking")
            nb_demand = Demand.objects.filter(done=0).count()

            mytools = Tool.objects.filter(is_publish=1, teachers = teacher).order_by("title")

            ### Exercice traités non vus par l'enseignant -> un point orange dans la barre de menu sur message
            is_pending_studentanswers = False
            pending_s = Studentanswer.objects.filter(parcours__teacher = teacher, is_reading = 0)
            if pending_s  :
                is_pending_studentanswers = True
 
            ### Permet de vérifier qu'un enseignant est dans un établissement sacado
            sacado_asso, sacado_is_active = is_sacado_asso(teacher.user,today)
            is_quite_finish = is_quite_finish_sacado_asso(teacher.user, today)
 
            
            return {    'is_quite_finish':is_quite_finish,'nb_else' : nb_else ,'nb_pendings' :nb_pendings , 'nb_customers' :nb_customers ,  'url_helper' : url_helper , 
                        'qtypes':qtypes, 'theme_color' : theme_color , 'navbar_theme_color' : navbar_theme_color , 'nb_levels' : nb_levels , 'nb_groups' : nb_groups ,  
                        'is_gar_check' : is_gar_check,'today': today, 'index_tdb' : False , 'nbe': nbe, 'levels': levels,   'nb_demand' : nb_demand ,
                        'mytools' : mytools , 'sacado_asso' : sacado_asso , "is_pending_studentanswers" : is_pending_studentanswers  }

        elif request.user.is_student:
            
            student = Student.objects.get(user=request.user)
            groups = student.students_to_group.all()

            can_get_the_book = False
            mybookGroupIds = Mybook.objects.values_list("group_id",flat=True).filter(book_id=9) # MyBook est la table qui lie le livre au groupe
            open("logs/debug.log",'a').write(str(mybookGroupIds))
 
            for g in groups:
                if g.id in mybookGroupIds :
                    can_get_the_book = True
                    break

            teacher_to_student = False
            if "_e-test" in student.user.username :
                teacher_to_student = True


            sacado_asso, sacado_is_active = is_sacado_asso(student.user,today)

            group_id = request.session.get("group_id",None)

            if group_id :
                group = Group.objects.get(pk=group_id)
            else :
                group = None

            url_helper =  "helpers/no_helper.html"

            nb_flashpacks = student.flashpacks.count()
            quiz = student.quizz.all()
            nb_quizz      = quiz.filter(is_random=0,is_archive=0).count()
            nb_qflash     = quiz.filter(is_random=1,is_archive=0).count()

            return {
                'is_gar_check' : is_gar_check,
                'student': student,
                'can_get_the_book' : can_get_the_book,
                'sacado_asso' : sacado_asso , 
                'group' : group , 'url_helper' : url_helper ,
                'groups' : groups,
                'teacher_to_student' : teacher_to_student ,   
                'index_tdb' : False , 'theme_color' : theme_color , 'navbar_theme_color' : navbar_theme_color ,  
                'nb_flashpacks' : nb_flashpacks , 'nb_quizz' : nb_quizz , 'nb_qflash' : nb_qflash ,     
            }

        elif request.user.is_parent:
            this_user = User.objects.get(pk=request.user.id)
            students = this_user.parent.students.all()
            last_exercises_done = Studentanswer.objects.filter(student__in= students).order_by("-date")[:10]
            url_helper =  "helpers/no_helper.html"

            return {
                'this_user': this_user,
                'last_exercises_done': last_exercises_done,
                'sacado_asso' : sacado_asso , 
                 'sacado_asso' : False ,  'url_helper' : url_helper , 
                 'index_tdb' : False ,
                 'is_gar_check' : None, 'theme_color' : theme_color , 'navbar_theme_color' : navbar_theme_color ,
            }


    else:
 
 
 
        contributeurs = User.objects.filter(is_superuser=1)
 
 
        return {
 
            'contributeurs': contributeurs,
  
        }
