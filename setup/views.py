from django.shortcuts import render,redirect
from django.forms import formset_factory
from django.contrib.auth.forms import  UserCreationForm,  AuthenticationForm
from account.forms import  UserForm, TeacherForm, StudentForm , BaseUserFormSet
from django.contrib.auth import   logout
from account.models import  User, Teacher, Student  ,Parent , Adhesion
from qcm.models import Parcours, Exercise, Relationship,Studentanswer, Supportfile, Customexercise, Customanswerbystudent,Writtenanswerbystudent , Course
from tool.models import Quizz, Question, Choice
from group.models import Group, Sharing_group
from association.models import Accounting , Detail
from group.views import student_dashboard
from setup.models import Formule 
from association.models import Rate
from school.models import Stage , School
from sendmail.models import Communication
from school.forms import  SchoolForm
from socle.models import Level
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Count, Q
from datetime import date, datetime , timedelta
from django.utils import formats, timezone
from django.contrib import messages
import random
import pytz
import uuid
import time
import os
from itertools import chain
from account.decorators import is_manager_of_this_school
from general_fonctions import *
import fileinput 
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.forms import formset_factory
##############   bibliothèques pour les impressions pdf    #########################
import os
from pdf2image import convert_from_path # convertit un pdf en autant d'images que de pages du pdf
from django.utils import formats, timezone
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT 
############## FIN bibliothèques pour les impressions pdf  #########################


def end_of_contract() :

    data = {}
    date = datetime.now()

    if date.month < 6 :
        end = date.year
    else :
        end = int(date.year) + 1
    return end
 
def index(request):

    if request.user.is_authenticated :
  
        today = time_zone_user(request.user)

        if request.user.closure : 
            if request.user.closure < today :
                return redirect("logout")

        ############################################################################################
        #### Mise à jour et affichage des publications  
        ############################################################################################  
        # relationships = Relationship.objects.filter(is_publish = 0,start__lte=today)
        # for r in relationships :
        #     Relationship.objects.filter(id=r.id).update(is_publish = 1)

        # parcourses = Parcours.objects.filter(start__lte=today).exclude(start = None)
        # for p in parcourses :
        #     Parcours.objects.filter(id=p.id).update(is_publish = 1)

        # customexercises = Customexercise.objects.filter(start__lte=today).exclude(start = None)
        # for c in customexercises :
        #     Customexercise.objects.filter(id=c.id).update(is_publish = 1)
        ############################################################################################
        #### Fin de Mise à jour et affichage des publications
        ############################################################################################
        timer = today.time()

        if request.user.last_login.date() != today.date() :
            request.user.last_login = today
            request.user.save()

        if request.user.is_teacher:


            courses = Course.objects.all()
            for c in courses :
                c.author = c.teacher
                c.save()




            teacher = Teacher.objects.get(user=request.user)

            grps = Group.objects.filter(teacher=teacher)
            shared_grps_id = Sharing_group.objects.filter(teacher=teacher).values_list("group_id", flat=True)
            sgps = []
            for sg_id in shared_grps_id :
                grp = Group.objects.get(pk=sg_id)
                sgps.append(grp)

            groups = chain(grps, sgps)

            this_user = request.user
            nb_teacher_level = teacher.levels.count()
            relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today).order_by("date_limit").order_by("parcours")
            parcourses = teacher.teacher_parcours.filter(is_evaluation=0, is_favorite =1,is_folder=0 ).order_by("-is_publish")
            communications = Communication.objects.values('id', 'subject', 'texte', 'today').filter(active=1).order_by("-id")
            parcours_tab = Parcours.objects.filter(students=None, teacher=teacher, is_favorite=1) ## Parcours favoris non affectés

            request.session["tdb"] = True
 
            template = 'dashboard.html'
            context = {'this_user': this_user, 'teacher': teacher, 'groups': groups,  'parcours': None, 'today' : today , 'timer' : timer , 'nb_teacher_level' : nb_teacher_level , 
                       'relationships': relationships, 'parcourses': parcourses, 
                       'communications': communications, 'parcours_tab': parcours_tab,
                       }
        
        elif request.user.is_student:  ## student

            template, context = student_dashboard(request, 0)

        elif request.user.is_parent:  ## parent
            parent = Parent.objects.get(user=request.user)
            students = parent.students.order_by("user__first_name")
            context = {'parent': parent, 'students': students, 'today' : today ,  }
            template = 'dashboard.html'

        return render(request, template , context)


    else:  ## Anonymous
        form = AuthenticationForm()
        u_form = UserForm()
        t_form = TeacherForm()
        s_form = StudentForm()
        levels = Level.objects.all()
        try:
            cookie = request.session.get("cookie")
        except:
            pass

        rates = Rate.objects.all() #tarifs en vigueur 
        school_year = rates.first().year #tarifs pour l'année scolaire

        nb_teacher = Teacher.objects.all().count()
        nb_student = Student.objects.all().count()

        schools = School.objects.order_by("country__name")

        today_start = datetime.date(datetime.now())

        communications = Communication.objects.filter(active= 1).order_by("-today")


        nb_student_answers = Studentanswer.objects.filter(date__gte= today_start).count() + Customanswerbystudent.objects.filter(date__gte= today_start).count() + Writtenanswerbystudent.objects.filter(date__gte= today_start).count()
        
        exercise_nb = Exercise.objects.filter(supportfile__is_title=0).count()
        exercises = Exercise.objects.filter(supportfile__is_title=0, supportfile__is_ggbfile = 1 )

        i = random.randrange(0, len(exercises))
        exercise = exercises[i]

        context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, 'schools' : schools,'nb_teacher': nb_teacher, 'nb_student_answers': nb_student_answers,  'communications': communications,
                   'cookie': cookie, 'nb_exercise': exercise_nb, 'exercise': exercise,  'nb_student': nb_student, 'rates': rates, 'school_year': school_year, }



        return render(request, 'home.html', context)


def logout_view(request):
    try:
        connexion = Connexion.objects.get(user=user)
        connexion.delete()
    except:
        pass

    form = AuthenticationForm()
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()
    logout(request)
    levels = Level.objects.all()
    context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, 'cookie': False}
    return render(request, 'home.html', context)


def send_message(request):
    ''' traitement du formulaire de contact de la page d'accueil et du paiement de l'adhésion par virement bancaire '''
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject",None)
    message = request.POST.get("message")
    token = request.POST.get("token", None)

    if token :
        if int(token) == 7 :
            if message:
                school_datas = ""
                if not subject :
                    subject = "Adhésion SACADO - demande d'IBAN"
                    school_id = request.session.get("inscription_school_id",None)
                    if school_id :
                        school = School.objects.get(pk = school_id)
                        school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name
                send_mail(subject,
                          "Bonjour, vous venez d'envoyer le message suivant :\n\n" + message+" \n\n" + email +  school_datas +" \n\n Ceci est un mail automatique. Ne pas répondre.",
                          'info@sacado.xyz',
                          [email])
                send_mail(subject,
                            message+" \n\n" + email +  school_datas,
                          'info@sacado.xyz',
                          [email, "sacado.asso@gmail.com"])
        else :
            messages.error(request,"Erreur d'opération....")
    else :
        messages.error("Oubli de token.")

    return redirect("index")


def accounting_adhesion(school_exists, today , somme , acting, user, is_active  ):

    accounting, create = Accounting.objects.get_or_create( school = school_exists   ,  date = today ,  defaults={ 'amount' : somme, 'objet' : "Cotisation", 'beneficiaire' :  "SACADO ASSO" ,
                                                                                                                    'is_credit' : 1, 'address' : school_exists.address , 'complement' : school_exists.complement ,
                                                                                                                    'town' : school_exists.town , 'country' : school_exists.country , 'contact' : school_exists.address ,
                                                                                                                     'observation' : "Cotisation" ,'acting' : acting , 'user' : user ,'is_active' : is_active })
    if create :
        Detail.objects.create( accounting = accounting  ,  description = "Cotisation" , amount = somme)




def school_adhesion(request):

    rates = Rate.objects.all() #tarifs en vigueur 
    school_year = rates.first().year #tarifs pour l'année scolaire
    form = SchoolForm(request.POST or None)
    token = request.POST.get("token", None)
    today = datetime.now()
    

    if request.method == "POST" :
        if form.is_valid():
            if token :
                if int(token) == 7  :
                    school_commit = form.save(commit=False)
                    school_exists, created = School.objects.get_or_create(name = school_commit.name, town = school_commit.town , country = school_commit.country , code_acad = school_commit.code_acad , defaults={ 'nbstudents' : school_commit.nbstudents , 'address' : school_commit.address ,'complement' : school_commit.complement , }  )
                    if not created :
                        messages.error(request,"Etablissement existant.")
                        return redirect('index')

                    somme = request.POST.get("somme")

                    acting, user, is_active  = None , None , False 

                    accounting_adhesion(school_exists, today , somme , acting, user, is_active)

                    school_datas =  school_exists.name +"\n"+school_exists.code_acad +  " - " + str(school_exists.nbstudents) +  " élèves \n" + school_exists.address +  "\n"+school_exists.town+", "+school_exists.country.name
                    send_mail("Demande d'adhésion à la version établissement",
                              "Bonjour l'équipe SACADO, \nl'établissement suivant demande la version établissement :\n"+ school_datas +"\n\nCotisation : "+somme+" €.\n\nEnregistrement de l'étalissement dans la base de données https://sacado.xyz. Ne pas répondre.",
                              'info@sacado.xyz',
                              ['sacado.asso@gmail.com'])

                    request.session["name_admin"] = request.POST.get("name_admin")
                    request.session["mail_admin"] = request.POST.get("mail_admin")
                    request.session["somme"] = somme
                    request.session["inscription_school_id"] = school_exists.pk

                    return redirect('payment_school_adhesion')
        else :
            print(form.errors)


    context = { 'form' : form , 'rates': rates, 'school_year': school_year, }
    return render(request, 'setup/school_adhesion.html', context)



def payment_school_adhesion(request):
 
    somme = request.session.get("somme",None)
    if somme : 
        name_admin = request.session.get("name_admin")
        mail_admin = request.session.get("mail_admin")
        school_id = request.session.get("inscription_school_id")
        school = School.objects.get(pk = school_id)

        rate = Rate.objects.filter(quantity__gte=school.nbstudents).first()
        school_year = rate.year #tarifs pour l'année scolaire

        context = { 'school' : school , 'name_admin' : name_admin , 'mail_admin' : mail_admin , 'somme' : somme , 'rate' : rate ,  'school_year' : school_year ,  }

        return render(request, 'setup/payment_school_adhesion.html', context)

    else :
        return redirect('school_adhesion')     


def delete_school_adhesion(request):

    school_id = request.session.get("inscription_school_id")
    school = School.objects.get(pk = school_id)
    school.delete()
    messages.error(request,"Demande d'adhésion ssannulée")
    return redirect('index')



def renew_school_adhesion(request,school_id):
 
    school = School.objects.get(pk = school_id)

    today = datetime.now()
    if today < datetime(2021,7,1) :
        somme = Rate.objects.filter(quantity__gte=school.nbstudents).first().discount
    else :
        somme = Rate.objects.filter(quantity__gte=school.nbstudents).first().amount
    user = request.user
    accounting_adhesion(school, today , somme , None , user, False  )

    return redirect('admin_tdb') 






def print_proformat_school(request):

    school_year = Rate.objects.get(pk=1).year
    somme = request.session.get("somme",None) + 2
    name_admin = request.session.get("name_admin")
    mail_admin = request.session.get("mail_admin")
    school_id = request.session.get("inscription_school_id")
    school = School.objects.get(pk = school_id)

    now = datetime.now().date()

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="'+str(school.id)+"-"+str(datetime.now().strftime('%Y%m%d'))+".pdf"
    doc = SimpleDocTemplate(response,   pagesize=A4, 
                                        topMargin=0.3*inch,
                                        leftMargin=0.3*inch,
                                        rightMargin=0.3*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()

    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )

    elements = []                 
    title_black = ParagraphStyle('title', fontSize=20, )
    subtitle = ParagraphStyle('title', fontSize=16,  textColor=colors.HexColor("#00819f"),)
    normal = ParagraphStyle(name='Normal',fontSize=10,)
    normalr = ParagraphStyle(name='Normal',fontSize=12,alignment= TA_RIGHT)
 
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')  
    logo_tab = [[logo, "ASSOCIATION SACADO.XYZ \n2B avenue de la pinède \n83400 La Capte Hyères \nFrance" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])

    elements.append(logo_tab_tab)
    elements.append(Spacer(0, 0.2*inch))

    paragraph0 = Paragraph( "Adhésion Annuelle " + school_year  , sacado )
    elements.append(paragraph0)
    elements.append(Spacer(0, 0.5*inch))



    school_datas =  school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name
 
    demandeur =  school_datas+   "\n\nMontant de la cotisation : "+str(somme)+"€ (frais de port inclus)" +"\n\nNom du demandeur : " + name_admin +  "\nCourriel : " + mail_admin  




    demandeur_tab = [[demandeur, "ASSOCIATION SACADO.XYZ \n2B avenue de la pinède \n83400 La Capte Hyères \nFrance\n\n\n\n\n" ]]
    demandeur_tab_tab = Table(demandeur_tab, hAlign='LEFT', colWidths=[5*inch,2*inch])

    elements.append(demandeur_tab_tab)
    elements.append(Spacer(0, 0.2*inch))



    my_texte_ = "Sous réserve du bon fonctionnement de son hébergeur LWS, l'association SACADO met l'ensemble des fonctionnalités du site https://sacado.xyz à disposition des enseignants de l'établissement "+school.name+"."
    paragraph = Paragraph( my_texte_  , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))



    sy = school_year.split("-")
    my_texte = "Le présent contrat est valide pour la période scolaire du 1 Septembre " + sy[0]+" jusqu'au 30 juin "+sy[1]+" pour les établissements de rythme Nord. \nPour les établissements de rythme Sud, la validité de l'adhésion est valable sur l'année "+sy[1]+"."


    paragraph = Paragraph( my_texte  , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))



    signature_tab = [[ 'Signature précédée de la mention "Lu et approuvé" \n\n...........................................................\n\n\n ...........................................................',"" ]]
    signature_tab_tab = Table(signature_tab, hAlign='LEFT', colWidths=[4*inch,3*inch])

    elements.append(signature_tab_tab)
    elements.append(Spacer(0, 0.4*inch))

 
    doc.build(elements)

    return response



###############################################################################################################################################################################
###############################################################################################################################################################################
########  Inscription élève isolé
###############################################################################################################################################################################
###############################################################################################################################################################################

def inscription(request):
    context = {}
    return render(request, 'setup/register.html', context)


def test_display(request):
    context = {}
    return render(request, 'setup/test_display.html', context)


def student_to_association(request):

    frml = Formule.objects.get(pk=1)
    formule = Formule.objects.get(pk=4)
    context = { 'frml' : frml , 'formule' : formule }
    return render(request, 'setup/student_association.html', context)


def choice_menu(request,name):
    formules = Formule.objects.filter(name=name)
    end  = end_of_contract()
    context = { 'formules' : formules , 'end' : end , 'name' : name  }
    return render(request, 'setup/menu.html', context)   


def details_of_adhesion(request) :

    total_price = request.POST.get("total_price")    
    month_price = request.POST.get("month_price")
    nb_month = request.POST.get("nb_month")    
    date_end = request.POST.get("date_end")
    menu_id = request.POST.get("menu_id")

    data_post = request.POST
    levels = Level.objects.all()

    nb_child = int(request.POST.get("nb_child"))

    if nb_child == 0 :
        no_parent = True
    else :
        no_parent = False

    formule = Formule.objects.get(pk = int(menu_id))


    if request.user.is_authenticated :

        adhesion = Adhesion.objects.filter(user = request.user).last()
        context = {  'formule' : formule ,  'no_parent' : no_parent , 'data_post' : data_post , "nb_child" : nb_child ,  'levels' : levels ,  'adhesion' : adhesion, "renewal" : True }
        return render(request, 'setup/renewal_adhesion.html', context)   

    else : 

        userFormset = formset_factory(UserForm, extra = nb_child + 1, max_num= nb_child + 1, formset=BaseUserFormSet)
        context = {  'formule' : formule ,  'no_parent' : no_parent , 'data_post' : data_post ,  'levels' : levels ,  'userFormset' : userFormset, "renewal" : False }
        return render(request, 'setup/detail_of_adhesion.html', context)   


def commit_adhesion(request) :

    data_post = request.POST
    nb_child = int(request.POST.get("nb_child"))   
    menu_id = int(request.POST.get("menu_id"))    
    data_posted = {"total_price" : data_post.get('total_price'), "month_price" : data_post.get('month_price'), "nb_month" : data_post.get('nb_month'), "date_end" : data_post.get('date_end'), "menu_id" : menu_id , "nb_child" : nb_child }
 
    levels = request.POST.getlist("level")

    userFormset = formset_factory(UserForm, extra = nb_child + 1, max_num = nb_child + 1, formset=BaseUserFormSet)
    formset = userFormset(data_post)

    formule = Formule.objects.get(pk = menu_id )

    parents  , students = [] , []
    if formset.is_valid():
        i = 0
        for form in formset :
            user = dict()
            user["last_name"]  =  form.cleaned_data["last_name"]
            user["first_name"] =  form.cleaned_data["first_name"]
            user["username"]   =  form.cleaned_data["username"]
            user["password_no_crypted"]   =   form.cleaned_data["password1"] 
            user["password"]   =  make_password(form.cleaned_data["password1"])
            user["email"]      =  form.cleaned_data["email"]   
            if levels[i] : 
                level = Level.objects.get(pk = int(levels[i])).name
                user["level"]      = level 
                students.append(user)
            else :
                level = ""
                user["level"]      = level 
                parents.append(user)
            i += 1

        # mise en session des coordonnées des futurs membres  et  des détails de l'adhésion
 
        request.session["parents_of_adhesion"] = parents
        request.session["students_of_adhesion"] = students
        request.session["data_posted"] = data_posted 
 
        ############################################################
    else:
        print("formset.errors : ", formset.errors)



    context = {'formule' : formule ,  'data_post' : data_posted , 'parents' : parents  , 'students' : students  }
 
    return render(request, 'setup/commit_adhesion.html', context)   



def creation_facture(user,data_posted,code):
    ##################################################################################################################
    # Création de la facture de l'adhésion au format pdf
    ##################################################################################################################

    filename = str(user.id)+str(datetime.now().strftime('%Y%m%d'))+".pdf"
    now = datetime.now().date()

    outfilename = filename+".pdf"
    #outfiledir = "D:/uwamp/www/sacadogit/sacado/static/uploads/factures/{}/".format(user.id) # local
    outfiledir = "uploads/factures/{}/".format(user.id) # on a server
    if not os.path.exists(outfiledir):
        os.makedirs(outfiledir)

    store_path = os.path.join(outfiledir, filename)

    doc = SimpleDocTemplate(store_path,   pagesize=A4, 
                                        topMargin=0.3*inch,
                                        leftMargin=0.3*inch,
                                        rightMargin=0.3*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()

    sacado = ParagraphStyle('sacado', 
                            fontSize=26, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )

    elements = []                 
    title_black = ParagraphStyle('title', fontSize=20, )
    subtitle = ParagraphStyle('title', fontSize=16,  textColor=colors.HexColor("#00819f"),)
    normal = ParagraphStyle(name='Normal',fontSize=12,)
    normalr = ParagraphStyle(name='Normal',fontSize=12,alignment= TA_RIGHT)
     #### Mise en place du logo
    #logo = Image('D:/uwamp/www/sacadogit/sacado/static/img/sacadoA1.png') # local
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png') # on a server
    logo_tab = [[logo, "SACADO" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5*inch])
    logo_tab_tab.setStyle(TableStyle([ ('TEXTCOLOR', (0,0), (-1,0), colors.Color(0,0.5,0.62))]))
    
    elements.append(logo_tab_tab)
    elements.append(Spacer(0, 0.2*inch))

    paragraph0 = Paragraph( "Adhésion"   , sacado )
    elements.append(paragraph0)
    elements.append(Spacer(0, 1*inch))
    paragraph = Paragraph( "Réf : "+code   , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))

    paragraph = Paragraph( "Nom : "+user.last_name   , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.1*inch))
    paragraph1 = Paragraph( "Prénom : "+user.first_name   , normal )
    elements.append(paragraph1)
    elements.append(Spacer(0, 0.1*inch))
    paragraph2 = Paragraph( "Courriel : "+user.email   , normal )
    elements.append(paragraph2)
    elements.append(Spacer(0, 0.3*inch))

    date_end = data_posted.get("date_end")
    total_price = data_posted.get("total_price")
    month_price = data_posted.get("month_price")
    nb_month = data_posted.get("nb_month")
    nb_child = int(data_posted.get("nb_child"))   
    menu_id = int(data_posted.get("menu_id"))  
    formule = Formule.objects.get(pk = menu_id )

    para = Paragraph(  "Adhésion : "+formule.adhesion  , normal )
    elements.append(para)
    elements.append(Spacer(0, 0.1*inch))

    para1 = Paragraph( "Menu : "+formule.name  , normal )
    elements.append(para1)
    elements.append(Spacer(0, 0.3*inch))

    if nb_child > 0 : # enfant
        pluralise = ""
        if  nb_child > 1 :
            pluralise = "s" 
        para4 = Paragraph( "Nombre d'enfant"+pluralise+" inscrit"+pluralise+" : " +str(nb_child)  , normal )
        elements.append(para4)
        elements.append(Spacer(0, 0.1*inch))

        
        for student in user.parent.students.all() :

            paragraph_msg = Paragraph( "  -  "+ student.user.first_name+ " " + student.user.last_name  , normal )
            elements.append(paragraph_msg)
            elements.append(Spacer(0, 0.1*inch))

    elements.append(Spacer(0, 0.1*inch))
    para2 = Paragraph( "Fin d'adhésion : "+data_posted.get("date_end")  , normal )
    elements.append(para2)
    elements.append(Spacer(0, 0.1*inch))


    para3 = Paragraph( "Montant de l'adhésion : "+total_price+"€  soit "+nb_month +" x " + month_price+"€"  , normal )
    elements.append(para3)
    elements.append(Spacer(0, 0.1*inch))
 
    elements.append(Spacer(0, 2*inch))
    para0 = Paragraph(  "Soit un paiement de "+total_price+"€ payé le "+str(now) , normalr )
    elements.append(para0)
    elements.append(Spacer(0, 0.1*inch))

    doc.build(elements)

    return store_path
  



def save_adhesion(request) :

    parents_of_adhesion = request.session.get("parents_of_adhesion")
    students_of_adhesion = request.session.get("students_of_adhesion")
    data_posted = request.session.get("data_posted") # détails de l'adhésion

    date_end = data_posted.get("date_end")
    total_price = data_posted.get("total_price")
    month_price = data_posted.get("month_price")
    nb_month = data_posted.get("nb_month")
 
    users = []

    nb_child = int(data_posted.get("nb_child"))   
    menu_id = int(data_posted.get("menu_id"))  
    formule = Formule.objects.get(pk = menu_id )


    date_end_format = date_end.split(" ")
    months = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    date_end_month = months.index(date_end_format[1])+1 

    date_end_dateformat = str(date_end_format[2])+"-"+str(date_end_month)+"-"+str(date_end_format[0])+" 00:00:00" 



    ##################################################################################################################
    # Insertion dans la base de données
    ##################################################################################################################
    students_in = []
    code = str(uuid.uuid4())[:8]
    for s in students_of_adhesion :

        last_name, first_name, username , password , email , level =  s["last_name"]  , s["first_name"] , s["username"] , s["password"] , s["email"] , s["level"]  
        level = Level.objects.get(name = level)    
        user, created = User.objects.update_or_create(username = username, password = password , user_type = 0 , defaults = { "last_name" : last_name , "first_name" : first_name  , "email" : email , "closure" : date_end_dateformat })
        student,created_s = Student.objects.update_or_create(user = user, defaults = { "task_post" : 1 , "level" : level })

        group = Group.objects.get(level = level, teacher_id = 2480)
        group.students.add(student)


        parcourses = Parcours.objects.filter(level = level, teacher_id = 2480) # 2480 est SacAdoProf
        test = attribute_all_documents_to_student(parcourses, student)

        students_in.append(student) # pour associer les enfants aux parents

        if nb_child == 0 : # enfant émancipé ou majeur
            Adhesion.objects.update_or_create(user = user, amount = total_price , menu = menu_id, defaults = { "file"  : creation_facture(user,data_posted,code), "date_end" : date_end_dateformat,  "children" : nb_child, "duration" : nb_month })


    for p in parents_of_adhesion :

        last_name, first_name, username , password , email =  p["last_name"]  , p["first_name"] , p["username"] , p["password"] , p["email"] 
        user, created = User.objects.update_or_create(username = username, password = password , user_type = 1 , defaults = { "last_name" : last_name , "first_name" : first_name  , "email" : email , "closure" : date_end_dateformat })
        parent,create = Parent.objects.update_or_create(user = user, defaults = { "task_post" : 1 })
        
        for si in students_in :
            parent.students.add(si)

        adh, cr = Adhesion.objects.update_or_create(user = user, amount = total_price , menu = menu_id, defaults = { "file"  : creation_facture(user,data_posted,code), "date_end" : date_end_dateformat,  "children" : nb_child, "duration" : nb_month })

    ##################################################################################################################
    # Envoi du courriel
    ##################################################################################################################
    nbc = ""
    if nb_child > 1 :
        nbc = "s"

    for p in parents_of_adhesion :
        msg = "Bonjour "+p["first_name"]+" "+p["last_name"]+",\n\n vous venez de souscrire à une adhésion "+formule.adhesion +" SACADO avec le menu "+formule.name+". \n"
        msg += "votre référence d'adhésion est "+code+".\n\n"
        msg += "Votre adhésion est effective jusqu'au "+data_posted.get("date_end") +"\n"
        msg += "Votre identifiant est "+p["username"]+" et votre mot de passe est "+p["password_no_crypted"]+"\n"
        msg += "Vous avez inscrit "+str(nb_child)+" enfant"+nbc+" :\n"
        for s in students_of_adhesion :
            msg += "- "+s["first_name"]+" "+s["last_name"]+", identifiants de connexion : id "+s["username"]+" / mot de passe "+s["password_no_crypted"]+" \n"

        msg += "\n\n Il est possible de retrouver ces détails à partir de votre tableau de bord après votre connexion à https://sacado.xyz"

        msg += "L'équipe SACADO vous remercie de votre confiance.\n\n"

        send_mail("Inscription SACADO", msg, "info@sacado.xyz", [p["email"]])


    for s in students_of_adhesion :
        srcv = []        
        if s["email"] : 
            srcv.append(s["email"])
            smsg = "Bonjour "+s["first_name"]+" "+s["last_name"]+",\n\n vous venez de souscrire à une adhésion "+formule.adhesion +" SACADO avec le menu "+formule.name+". \n"
            smsg += "votre référence d'adhésion est "+code+".\n\n"
            smsg += "Votre identifiant est "+s["username"]+" et votre mot de passe est "+s["password_no_crypted"]+"\n\n"
            smsg += "Il est possible de retrouver ces détails à partir de votre tableau de bord après votre connexion à https://sacado.xyz"
            smsg += "L'équipe SACADO vous remercie de votre confiance.\n\n"

            send_mail("Inscription SACADO", smsg, "info@sacado.xyz", srcv)

    # Envoi à SACADO
    sacado_rcv = ["philippe.demaria83@gmail.com","brunoserres33@gmail.com","sacado.asso@gmail.com"]

    sacado_msg = "Une adhésion "+formule.adhesion +" SACADO avec le menu "+formule.name+" vient d'être souscrite pour "+str(nb_child)+" enfant"+nbc+" \n\n"
    sacado_msg += "Le montant de l'adhésion est : "+total_price+"€ soit "+nb_month+ " x "+month_price+"€\n\n"
    sacado_msg += "La date de fin de l'adhésion est : "+date_end+"\n\n"
    i,j = 1,1
    for p in parents_of_adhesion :
        sacado_msg += "Parent "+str(i)+" : "+p["first_name"]+" "+p["last_name"]+" adresse de courriel : "+p["email"]+". \n\n"
        i+=1
    for s in students_of_adhesion :
        if s["email"] :
            adr = ", adresse de courriel : "+s["email"] 
        sacado_msg += "Enfant "+str(j)+" : "+s["first_name"]+" "+s["last_name"]+" Niveau :" +s["level"]+adr+"\n\n"         
        j+=1

    send_mail("Inscription SACADO", sacado_msg, "info@sacado.xyz", sacado_rcv)

    #########################################################


    context = {      }

    return render(request, 'setup/save_adhesion.html', context)



def adhesions(request):
    """ liste des adhésions """
    adhesions = Adhesion.objects.filter(user = request.user ) 
    today = time_zone_user(request.user)
    last_week = today + timedelta(days = 7)
    context = { "adhesions" : adhesions,  "last_week" : last_week    }

    return render(request, 'setup/list_adhesions.html', context)




def calcul_remboursement(adhesion) :

    today = time_zone_user(adhesion.user)
    delta = adhesion.date_end - adhesion.date_start
    nb_days = delta.days 

    delta1 = today - adhesion.date_start
    nb_day1s = delta1.days

    ratio = 1 - round(nb_day1s/nb_days,2)

    formule = Formule.objects.get(pk= adhesion.menu)
    adhesion_tab = adhesion.amount.split(",")
    price = float(adhesion_tab[0]+"."+adhesion_tab[1])

    pluri = ""
    if nb_day1s > 1 :
        pluri =  "s"

    nd = str(nb_day1s)+" jour"+pluri

    return round(ratio*price - 5.99,2) , nd



def delete_adhesion(request):

    pk = int(request.POST.get("adh_id"))
    adhesion = Adhesion.objects.get(pk=pk)

    remb  = calcul_remboursement(adhesion)[0]

    msg = "Une demande d'annulation vient d'être formulée de la part de "+adhesion.user+". \n"
    msg += "La référence d'adhésion est "+adhesion.code+" et son id est "+adhesion.id+".\n\n"
    msg += "Le montant du remboursement est de "+remb+"€ au pro-rata des jours adhérés." 

    send_mail("Demande d'annulation d'adhésion SACADO", msg, "info@sacado.xyz", ["sacado.asso@gmail.com"])

    return redirect("adhesions")



##################################################################################################################
##################################################################################################################
##############################################  AJAX  ############################################################
##################################################################################################################
################################################################################################################## 

def ajax_get_price(request):

    nbr_students = request.POST.get("nbr_students",None)
    data = {}
    price = ""
    if nbr_students :
        if int(nbr_students) < 1500 : 
            adhesion = Rate.objects.filter(quantity__gte=int(nbr_students)).first()
            
            today = datetime.now()

            seuil = datetime(2021, 7, 1)

            if today < seuil :
                price = adhesion.discount
            else :
                price = adhesion.amount

    data["price"] = price

    return JsonResponse(data)



def ajax_remboursement(request):
    data_id = int(request.POST.get("data_id"))
    adhesion = Adhesion.objects.get(pk=data_id)
    data ={}
    data["remb"] , data["jour"] = calcul_remboursement(adhesion)
    return JsonResponse(data)


 
def ajax_changecoloraccount(request):
    """
    Appel Ajax pour afficher la liste des élèves du groupe sélectionné
    """
    if request.user.is_authenticated:
        code = request.POST.get('code')

    color = request.user.color
    filename1 = "static/css/navbar-fixed-left.min.css"
    filename2 = "static/css/AdminLTEperso.css"

    User.objects.filter(pk=request.user.id).update(color=code)

    change_color(filename1, color, code)
    change_color(filename2, color, code)

    return redirect("index")


def change_color(filename, color, code):
    # Read in the file
    with open(filename, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(color, code)
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)


@is_manager_of_this_school
def admin_tdb(request):

    school = request.user.school
    schools = request.user.schools.all()

    schools_tab = [school]
    for s in schools :
        schools_tab.append(s)


    teachers = Teacher.objects.filter(user__school=school, user__user_type=2)


    nb_teachers = teachers.count()
    nb_students = User.objects.filter(school=school, user_type=0).count()
    nb_groups = Group.objects.filter(Q(teacher__user__school=school)|Q(teacher__user__schools=school)).count()
    
    is_lycee = False
    if not school.get_seconde_to_comp :
        for t in teachers :
            if t.groups.filter(level__gte=10).count() > 0 :
                is_lycee = True
                break

    try:
        stage = Stage.objects.get(school=school)
        if stage:
            eca, ac, dep = stage.medium - stage.low, stage.up - stage.medium, 100 - stage.up
        else:
            eca, ac, dep = 20, 15, 15

    except:
        stage = {"low": 50, "medium": 70, "up": 85}
        eca, ac, dep = 20, 15, 15
    
    if len(schools_tab) == 1 :
        school_id = request.user.school.id
        request.session["school_id"] = school_id
    else :
        if request.session.get("school_id",None) :
            school_id = int(request.session.get("school_id",None))
        else :
            school_id = 0

    return render(request, 'dashboard_admin.html', {'nb_teachers': nb_teachers, 'nb_students': nb_students, 'school_id' : school_id , "school" : school , 
                                                    'nb_groups': nb_groups, 'schools_tab': schools_tab, 'stage': stage, 'is_lycee' : is_lycee , 
                                                    'eca': eca, 'ac': ac, 'dep': dep , 'communications' : [],
                                                    })


def gestion_files(request):
    levels = Level.objects.all()
    if request.method == "POST":

        level_id = request.POST.get("level")
        level = Level.objects.get(pk=level_id)
        supportfiles = Supportfile.objects.filter(level_id=level_id, is_title=0)
    else:
        level, level_id = None, 0
        supportfiles = []

    context = {'levels': levels, 'level': level, 'level_id': level_id, 'level_id': level_id,
               'supportfiles': supportfiles}

    return render(request, 'setup/gestion_files.html', context )


def get_cookie(request):
    request.session["cookie"] = "accept"
    return redirect('index')


def play_quizz(request):

    context = {}
    return render(request, 'tool/play_quizz.html', context)


 
 
def play_quizz_login(request):


    code = request.POST.get("code")
 
    if Quizz.objects.filter(code = code).count() == 1:

        quizz = Quizz.objects.get(code = code)
        groups = quizz.groups.all()
        student_set = set()
        for group in groups :
            student_set.update(group.students.all())
        students = list(student_set)
        random.shuffle(students)
 

        context = { "quizz" : quizz , "students" : students , }
        return render(request, 'tool/play_quizz_login.html', context)
    else :
        context = { 'error' : True}
        return render(request, 'tool/play_quizz.html', context)
    


def play_quizz_start(request):

    student_id = request.POST.get("student_id")
    student = Student.objects.get(pk = student_id)

    quizz_id = request.POST.get("quizz_id")
    quizz = Quizz.objects.get(pk = quizz_id)
    
    n = request.POST.get("n",0)

    quizz.students.add(student)
   
    questions = list(quizz.questions.order_by("ranking"))
    print(n)
    print(questions)
    question = questions[n]    
    n +=1
    context = {  "quizz" : quizz , "question" : question , "n" : n}
    return render(request, 'tool/play_quizz_start.html', context)
