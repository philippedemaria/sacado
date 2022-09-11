from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render,redirect
from django.forms import formset_factory
 
from django.contrib.auth import   logout , login, authenticate
from django.contrib.auth.forms import  UserCreationForm,  AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.utils import formats, timezone
from django.contrib import messages
 
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from django.db.models import Count, Q

from account.decorators import is_manager_of_this_school
from account.forms import  UserForm, TeacherForm, StudentForm , BaseUserFormSet , NewpasswordForm
from account.models import  User, Teacher, Student  , Parent , Adhesion , Facture
from association.models import Accounting , Detail , Rate , Abonnement , Holidaybook, Customer
from group.models import Group, Sharing_group
from group.views import student_dashboard
from qcm.models import Folder , Parcours, Exercise,Relationship,Studentanswer, Supportfile, Customexercise, Customanswerbystudent,Writtenanswerbystudent
from sendmail.models import Communication
from setup.forms import WebinaireForm , TweeterForm
from setup.models import Formule , Webinaire , Tweeter 
from school.models import Stage , School, Country , Town
from school.forms import  SchoolForm, SchoolUpdateForm  
from school.gar import *
from socle.models import Level, Subject 
from tool.models import Quizz, Question, Choice
from bibliotex.models import Exotex
from datetime import date, datetime , timedelta

from itertools import chain
from general_fonctions import *
from payment_fonctions import *

import random
import pytz
import uuid
import time
import os
import fileinput 
import random
import json

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
        index_tdb = True  # Permet l'affichage des tutos Youtube dans le dashboard
  
        today = time_zone_user(request.user)

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

            teacher = request.user.teacher
            grps = teacher.groups.all() 
            shared_grps_id = Sharing_group.objects.filter(teacher=teacher).values_list("group_id", flat=True) 
            # sgps = []
            # for sg_id in shared_grps_id :
            #     grp = Group.objects.get(pk=sg_id)
            #     sgps.append(grp)

            sgps    = Group.objects.filter(pk__in=shared_grps_id)
            groupes =  grps | sgps
            groups  = groupes.order_by("level__ranking") 
            this_user = request.user
            nb_teacher_level = teacher.levels.count()
            relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today).order_by("date_limit").order_by("parcours")
            folders_tab = teacher.teacher_folders.filter(students=None, is_favorite=1, is_archive=0 ,is_trash=0 )#.exclude(teacher__user__username__contains="_e-test") ## Dossiers  favoris non affectés
            teacher_parcours = teacher.teacher_parcours
            parcours_tab = teacher_parcours.filter(students=None, is_favorite=1, is_archive=0 ,is_trash=0 ).order_by("is_evaluation")#.exclude(teacher__user__username__contains="_e-test") ## Parcours / évaluation favoris non affecté
            
            #Menu_right
            #parcourses = teacher_parcours.filter(is_evaluation=0, is_favorite =1, is_archive=0,  is_trash=0 ).order_by("-is_publish")
            #communications = Communication.objects.values('id', 'subject', 'texte', 'today').filter(active=1).order_by("-id")

            request.session["tdb"] = True

            webinaire = Webinaire.objects.filter(date_time__gte=today,is_publish=1).first()

            # Pour la GAR et le Primaire
            group_prims = []
            if request.user.school and request.user.school.is_primaire :   
                group_prims = request.user.school.school_group.filter(teacher=None)




            template = 'dashboard.html'
            context = {'this_user': this_user, 'teacher': teacher, 'groups': groups,  'parcours': None, 'today' : today , 'timer' : timer , 'nb_teacher_level' : nb_teacher_level , 
                       'relationships': relationships,  'index_tdb' : index_tdb, 'folders_tab' : folders_tab , 'group_prims' : group_prims , 
                       'parcours_tab': parcours_tab, 'webinaire': webinaire, #'parcourses': parcourses,'communications': communications, 
                       }
        
        elif request.user.is_student:  ## student

            if request.user.closure : 
                if request.user.closure < today :
                    messages.error(request,"Votre adhésion est terminée.")  
                    return redirect("logout")

            template, context = student_dashboard(request, 0)

        elif request.user.is_parent:  ## parent
            parent = Parent.objects.get(user=request.user)
            students = parent.students.order_by("user__first_name")
            context = {'parent': parent, 'students': students, 'today' : today , 'index_tdb' : index_tdb, }
            template = 'dashboard.html'

        return render(request, template , context)
    
    else:  ## Anonymous
        #########
        ###################
        form    = AuthenticationForm()
        u_form  = UserForm()
        t_form  = TeacherForm()
        s_form  = StudentForm()
        np_form = NewpasswordForm()
        levels  = Level.objects.filter(is_active=1).exclude(pk=13).order_by("ranking")

        try :
            holidaybook = Holidaybook.objects.get(pk=1)
            sacado_voyage = holidaybook.is_display
        except :
            sacado_voyage = False

        rates = Rate.objects.all() #tarifs en vigueur 
        school_year = rates.first().year #tarifs pour l'année scolaire

        nb_teacher = Teacher.objects.all().count()
        nb_student = Student.objects.all().count()
        
        subjects = Subject.objects.filter(pk__in=[1,2,3])
        #abonnements = Abonnement.objects.filter(is_active =1).prefetch_related("school__country").order_by("school__country__name")
        #abonnements  = Abonnement.objects.filter(is_active = 1).order_by("school__country__name")
        customers    = Customer.objects.filter(status__gte=2).exclude(school_id=50).exclude(school_id=88).order_by("school__country__name")
 
        today_start = datetime.date(datetime.now())

        communications = Communication.objects.filter(active= 1).order_by("-today")


        nb_student_answers = Studentanswer.objects.filter(date__gte= today_start).count() + Customanswerbystudent.objects.filter(date__gte= today_start).count() + Writtenanswerbystudent.objects.filter(date__gte= today_start).count()
        
        exercises = Exercise.objects.select_related("supportfile").filter(supportfile__is_title=0 )
        exercise_nb = exercises.count() - 1

        nb_exotex = Exotex.objects.count() 
 
        i = random.randrange(0, exercise_nb)
        exercise = exercises[i]


        cookie_rgpd_accepted = request.COOKIES.get('cookie_rgpd_accepted',None)
        cookie_rgpd_accepted = not ( cookie_rgpd_accepted  == "True" )

        context = { 'cookie_rgpd_accepted' : cookie_rgpd_accepted , 'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'np_form': np_form, 'levels': levels,  'nb_teacher': nb_teacher, 'nb_student_answers': nb_student_answers,  'communications': communications,
                    'nb_exotex': nb_exotex, 'nb_exercise': exercise_nb, 'exercise': exercise,  'nb_student': nb_student, 'rates': rates, 'school_year': school_year, 'subjects': subjects,  'sacado_voyage' : sacado_voyage,  'customers' : customers}

        response = render(request, 'home.html', context)
        return response
 

 
# def ajax_reponse_to_rgpd(request) :

#     data     = {}
#     context  = {}
#     response = render(request, 'home.html', context)
#     if request.POST.get("response") == "yes" :
#         date = datetime.now()+timedelta(days=180)
#     else :
#         date = datetime.now()+timedelta(days=181)
    
#     response.set_cookie('bandeau_rgpd', date )
#     return JsonResponse(data)

 


def logout_view(request):
    try:
        connexion = Connexion.objects.get(user=user)
        connexion.delete()
    except:
        pass

    try :
        is_gar_check = request.session.get("is_gar_check",None)
        # récupérer le nameId qui permet de récupérer l'IDO puis déconnecter avec l'IDO
    except :
        pass

    form = AuthenticationForm()
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()
    logout(request)
    levels = Level.objects.all()
    context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, 'cookie': False}
    return render(request, 'home.html', context)


def all_routes(request,adresse):
    return redirect("index")


def logout_academy(request):
    logout(request)
    return redirect("academy")



def singleLogoutGar(request):

    # création du dictionnaire qui avec les données du GAR  
    data_xml = request.headers["X-Gar"]
    gars = json.loads(data_xml)
    dico_received = dict()
    for gar in gars :
        dico_received[gar['key']] = gar['values']
    username   = dico_received["IDO"]
    logout(request)


def ressource_sacado(request): #Protection saml pour le GAR

    # création du dictionnaire qui avec les données du GAR  
    ###########################################################################################
    ###########################################################################################
    request.session["is_gar_check"] = True # permet de savoir si l'utilisateur passe par le GAR
    ###########################################################################################
    ###########################################################################################

    data_xml = request.headers["X-Gar"]
    gars = json.loads(data_xml)

    dico_received = dict()
    for gar in gars :
        dico_received[gar['key']] = gar['values']
    ##########################################################
    today = datetime.now()

    uai        = dico_received["UAI"][0] 
    school     = School.objects.filter(code_acad = uai).last()
    last_name  = dico_received["NOM"][0] 
    first_name = dico_received["PRE"][0]
    email = str(today.timestamp()) + "@sacado.xyz"

    if 7 < today.month < 13  :
        closure  = datetime(today.year + 1, 6 , 30 , 0 , 0 , 0)
    else :
        closure  = datetime(today.year, 6 , 30 , 0 , 0 , 0)

    time_zone  = "Europe/Paris"
    is_extra   = 0
    is_manager = 0 
    cgu        = 1
    is_testeur = 0
    country    = school.country
    is_board   = 0

    username   = dico_received["IDO"][0]
    password   = make_password("sacado_gar")
    civilite   = dico_received["CIV"][0]


    # context = {"dico_received" : dico_received , 'data_xml' : data_xml }
    # return render(request, 'setup/test_gar.html', context)


    if Abonnement.objects.filter( school__code_acad = uai ,  date_stop__gte = today , date_start__lte = today , is_active = 1 ) :    
     

        if 'elv' in dico_received["PRO"][0] : # si ELEVE 
            user_type  = 0 

            div   = dico_received["DIV"][0]
            name  = div.split("##")[0]

            user, created = User.objects.get_or_create(username = username, defaults = {  "school" : school , "user_type" : user_type , "password" : password , "time_zone" : time_zone , "last_name" : last_name , "first_name" : first_name  , "email" : email , "closure" : closure ,  "country" : country , })
            
            if not school.is_primaire :
                group, c_g        = Group.objects.get_or_create(school = school, name = name )
                student,created_s = Student.objects.get_or_create(user = user, defaults = { "task_post" : 0 , "level" : group.level }) 
            else :
                level = Level.objects.get(pk=1)
                group, c_g        = Group.objects.get_or_create(school = school, name = name , defaults = { 'level' : level }  )
                student,created_s = Student.objects.get_or_create(user = user, defaults = { "task_post" : 0 , "level" : level })
            try :
                group.students.add(student)
            except: 
                pass
 
        else : # si ENSEIGNANT 'ens' in dico_received["PRO"][0] 
            user_type   = 2    
            code_levels = dico_received["P_MS4"] 
            if "P_MEL" in dico_received.keys() : 
                email = dico_received["P_MEL"][0]
                if not email :
                    email = str(today.timestamp()) + "@sacado.xyz"

            user, created     = User.objects.get_or_create(username = username, defaults = {  "school" : school , "user_type" : user_type , "password" : password , "time_zone" : time_zone , "last_name" : last_name , "first_name" : first_name  , "email" : email , "closure" : closure ,  "country" : country , })
            teacher,created_t = Teacher.objects.get_or_create(user = user, defaults = { "notification" : 0 , "exercise_post" : 0    })

            if not school.is_primaire :
                for code_level in code_levels  : 
                    if code_level == 2111 : level_id = 6
                    elif code_level == 2112 : level_id = 7
                    elif code_level == 2115 : level_id = 8
                    elif code_level == 2216 : level_id = 9
                    elif code_level== 2211 : level_id = 10
                    elif code_level == 2212 : level_id = 11
                    else : level_id = 12
                    level = Level.objects.get(pk=level_id)
                    teacher.levels.add(level)

                try :    
                    groups = dico_received["DIV"]
                    for group in groups :
                        name = group.split("##")[0]
                        teacher = user.teacher
                        if name[0] == 6 : level_id = 6
                        elif name[0] == 5 : level_id = 7
                        elif name[0] == 4 : level_id = 8
                        elif name[0] == 3 : level_id = 9
                        elif name[0] == 2 : level_id = 10
                        elif name[0] == 1 : level_id = 11
                        else : level_id = 12

                        Group.objects.get_or_create(name = name , teacher = teacher ,  school = school , defaults = {  'level_id' : level_id , "lock" : 0  })
                except :
                    pass
        #########################################################


        user_authenticated = authenticate( username= username, password= "sacado_gar")
 
        if user_authenticated is not None:
            login(request, user_authenticated,  backend='django.contrib.auth.backends.ModelBackend' )
            request.session["user_id"] = user.id
        else : 
            messages.error(request,"Votre compte n'est pas connu par SACADO.")

    else :
        messages.error(request,"Votre établissement n'est pas abonné à SACADO.")
    return index(request)
 


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
                #### Si c'est un établissement qui fait une demande 
                school_datas = ""
                if not subject :
                    subject = "Adhésion SACADO - demande d'IBAN"
                    school_id = request.session.get("inscription_school_id",None)
                    if not school_id:
                        school_id = request.POST.get("inscription_school_id",None)
                    if school_id :
                        school = School.objects.get(pk = school_id)
                        school_datas = "\n"+school.name +"\n"+school.code_acad +  " - " + str(school.nbstudents) +  " élèves \n" + school.address +  "\n"+school.town+", "+school.country.name
                ############################################################  

                send_mail(subject,
                            message+" \n\n Ce mail est envoyé à partir de l'adresse : " + email + "\n\n" + school_datas,
                          settings.DEFAULT_FROM_EMAIL,
                          ["sacado.asso@gmail.com" ])
                messages.success(request,"Message envoyé..... Merci. L'équipe Sacado.")

        else :
            messages.error(request,"Erreur d'opération....")
    else :
        messages.error(request,"Oubli de token.")

    if request.POST["info_academy"] == "yes" :
        return redirect("academy")
    else :
        return redirect("index")




@csrf_exempt
def ajax_charge_town(request):

    id_country =  request.POST.get("id_country")
    data = {}
    if id_country == 5 :
        data['towns'] = None
    else : 
        towns = Town.objects.values_list('name','name').filter(country_id=id_country).order_by("name") 
        data['towns'] = list(towns)
    data['id_country'] = id_country
    return JsonResponse(data)



@csrf_exempt
def ajax_charge_school(request):

    id_country =  request.POST.get("id_country")
    town       =  request.POST.get("id_town")

    data = {}
    schools = School.objects.values_list('id', 'name').filter(country_id=id_country, town = town).order_by("name")  
    data['schools'] = list(schools)
    return JsonResponse(data)


@csrf_exempt
def ajax_charge_school_by_rne(request):

    id_rne       =  request.POST.get("id_rne")
    data = {}
    schools = School.objects.values_list('id', 'name').filter(country_id=5,code_acad=id_rne)
    data['schools'] = list(schools)

    school = School.objects.filter(country_id=5,code_acad=id_rne).first()
    is_active = False

    customer = Customer.objects.get(pk=school.id)
    if customer.status > 1 : 
        is_active = True 

    data["is_active"] = is_active

    return JsonResponse(data)




def school_adhesion(request):

    rates = Rate.objects.all() #tarifs en vigueur 
    school_year = rates.first().year #tarifs pour l'année scolaire

    countries = Country.objects.order_by("name")

    token = request.POST.get("token", None)
    today = time_zone_user(request.user)
    u_form = UserForm(request.POST or None)

    school_id = request.POST.get("school",None)
    if request.POST.get("school",None):
        school  = School.objects.get(pk=school_id)
        form = SchoolUpdateForm(request.POST or None, request.FILES  or None, instance = school)
    else :
        form = SchoolUpdateForm(request.POST or None, request.FILES  or None)
 

    if request.method == "POST" :
        if  all((u_form.is_valid(), form.is_valid())):   

            if token :
                if int(token) == 7 :
                    school_commit = form.save()
                    school_exists, created = School.objects.get_or_create(name = school_commit.name, town = school_commit.town , country = school_commit.country , 
                        code_acad = school_commit.code_acad , defaults={ 'nbstudents' : school_commit.nbstudents , 'logo' : school_commit.logo , 'address' : school_commit.address ,'complement' : school_commit.complement , 'gar' : school_commit.gar }  )
                    try :
                        if not created :
                            Customer.objects.create(school=school_exists,status= 0,town = school_exists.town , country = school_exists.country )
                    except :
                        pass

                    #    nbstudents = school_commit.nbstudents , address = school_commit.address , complement = school_commit.complement, logo = school_commit.logo )
                        # si l'établisseent est déjà créé, on la modifie et on récupère son utilisateur.
                    #School.objects.filter(pk = school_exists.id).update(town = school_commit.town , country = school_commit.country , code_acad = school_commit.code_acad , 
                    #    nbstudents = school_commit.nbstudents , address = school_commit.address , complement = school_commit.complement, logo = school_commit.logo )
                    new_user_id = request.session.get("new_user_id", None)
                    if new_user_id :
                        user = User.objects.get(pk = new_user_id )
                    else :
                        user = u_form.save(commit=False)
                        user.user_type = User.TEACHER
                        user.school = school_exists # on attribue l'établissement à la personne qui devient référence
                        user.is_manager = 1 # on attribue l'établissement à la personne qui devient administratrice de sacado.
                        user.set_password(u_form.cleaned_data["password1"])
                        user.country = school_exists.country
                        user.save()
                        username = u_form.cleaned_data['username']
                        password = u_form.cleaned_data['password1']
                        teacher = Teacher.objects.create(user=user)
                        request.session["new_user_id"] = user.id    
                    # else :
                    #     # si l'établissement vient d'être créé on crée aussi la personne qui l'enregistre.
                    #     user = u_form.save(commit=False)
                    #     user.user_type = User.TEACHER
                    #     user.school = school_exists # on attribue l'établissement à la personne qui devient référence
                    #     user.is_manager = 1 # on attribue l'établissement à la personne qui devient administratrice de sacado.
                    #     user.set_password(u_form.cleaned_data["password1"])
                    #     user.country = school_exists.country
                    #     user.save()
                    #     username = u_form.cleaned_data['username']
                    #     password = u_form.cleaned_data['password1']
                    #     teacher = Teacher.objects.create(user=user)
                    #     request.session["new_user_id"] = user.id 
                    #     ##########
                    #     ##########
                    #     # Si on vient de créer un établissement, on lui crée un abonnement.
                    #     ##########


                    is_active   = False # date d'effet, user, le paiement est payé non ici... doit passer par la vérification
                    observation = "Paiement en ligne"             
 
                    accounting_id = accounting_adhesion(school_exists, today , None, user, is_active , observation) # création de la facturation

                    ########################################################################################################################
                    #############  Abonnement
                    ########################################################################################################################
                    date_start, date_stop = date_abonnement(today)

                    abonnement, abo_created = Abonnement.objects.get_or_create( accounting_id = accounting_id  , defaults={'school' : school_exists, 'is_gar' : school_exists.gar, 'date_start' : date_start, 'date_stop' : date_stop,  'user' : user, 'is_active' : 0}  )
 
                    asking_gar = "Pas d'accès au GAR demandé."
                    if school_exists.gar: # appel de la fonction qui valide le Web Service
                        asking_gar = "Accès au GAR demandé."
                        
                        #create_abonnement_gar(today, abonnement,request.user)

                    ########################################################################################################################
                    #############  FIN  Abonnement
                    ########################################################################################################################

                    school_datas =  school_exists.name +"\n"+school_exists.code_acad +  " - " + str(school_exists.nbstudents) +  " élèves \n" + school_exists.address +  "\n"+school_exists.town+", "+school_exists.country.name
                    send_mail("Demande d'adhésion à la version établissement",
                              "Bonjour l'équipe SACADO, \nl'établissement suivant demande la version établissement :\n"+ school_datas +"\n"+asking_gar+"\n\nCotisation : "+str(school_exists.fee())+" €.\n\nEnregistrement de l'établissement dans la base de données.\nEn attente de paiement. \nhttps://sacado.xyz. Ne pas répondre.",
                              settings.DEFAULT_FROM_EMAIL,
                              ['sacado.asso@gmail.com'])

                    send_mail("Demande d'adhésion à la version établissement",
                              "Bonjour "+user.first_name+" "+user.last_name +", \nVous avez demandé la version établissement pour :\n"+ school_datas +"\n"+asking_gar+"\n\nCotisation : "+str(school_exists.fee())+" €. \nEn attente de paiement. \nL'équipe SACADO vous remercie de votre confiance. \nCeci est un mail automatique. Ne pas répondre. ",
                               settings.DEFAULT_FROM_EMAIL,
                               [user.email])


                    # Mise en session de l'ide de l'établissement et de l'id de la facture.
                    request.session["accounting_id"] = accounting_id
                    request.session["inscription_school_id"] = school_exists.pk  # inscription_school_id != school_id... On pourrait imaginer qu'un établissement en inscrive un autre sinon.
                    request.session["contact"] = user.first_name+" "+user.last_name 

                    return redirect('payment_school_adhesion')
        else :
            print(form.errors)
            print(u_form.errors)

    context = { 'form' : form , 'rates': rates, 'school_year': school_year, 'u_form' : u_form , 'countries' : countries }
    return render(request, 'setup/school_adhesion.html', context)




def payment_school_adhesion(request):
 

    school_id     = request.session.get("inscription_school_id", None)
    accounting_id = request.session.get("accounting_id", None)
    contact       = request.session.get("contact", None)
    new_user_id   = request.session.get("new_user_id", None)

 
    if school_id and new_user_id :
        user = User.objects.get(pk = new_user_id )
        school     = School.objects.get(pk = school_id)
        accounting = Accounting.objects.get(pk=accounting_id) 

        context = { 'school' : school , 'contact' : contact ,   'accounting' : accounting ,   'user' : user , }

        return render(request, 'setup/payment_school_adhesion.html', context)

    else :
        return redirect('school_adhesion')     



def iban_asking(request,school_id,user_id):

    school = School.objects.get(pk = school_id)
    user = User.objects.get(pk = user_id)
    send_mail("Demande d'IBAN",
                "Bonjour l'équipe SACADO, \nJe souhaiterais recevoir un IBAN de votre compte pour procéder à un virement bancaire en faveur de mon établissement :\nIdentifiant : "+ str(school.id) +"\nUAI : "+ school.code_acad +"\n"+ school.name +"\n"+ school.town +","+ school.country.name +"\n\nNe pas répondre.",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email,'sacado.asso@gmail.com'])

    messages.success(request,"Demande d'IBAN envoyée")
    return redirect('index')



def delete_school_adhesion(request):

    school_id = request.session.get("inscription_school_id")
    school = School.objects.get(pk = school_id)

    if school.users.count() == 0 :
        school.delete()
        messages.success(request,"Demande d'adhésion annulée")  

        try :
            send_mail("Suppression d'adhésion",
                    "Bonjour l'équipe SACADO, \nJe souhaite annuler la demande d'adhésion :\n\n"+ school.name +"\n"+ school.town +","+ school.country.name +"\n\nNe pas répondre.",
                        settings.DEFAULT_FROM_EMAIL,
                        ['sacado.asso@gmail.com'])
        except :
            pass

    elif school.users.count() == 1 :
        for u in school.users.all():
            u.teacher.delete()
            u.delete()

        school.delete()
        messages.success(request,"Demande d'adhésion annulée")  

        try :
            send_mail("Suppression d'adhésion",
                    "Bonjour l'équipe SACADO, \nJe souhaite annuler la demande d'adhésion :\n\n"+ school.name +"\n"+ school.town +","+ school.country.name +"\n\nNe pas répondre.",
                        settings.DEFAULT_FROM_EMAIL,
                        ['sacado.asso@gmail.com'])
        except :
            pass            

    else :  
        messages.error(request,"La demande d'annulation ne peut être validée. Des utilisateurs de votre établissement restent inscrits.")  

    return redirect('index')


 
def print_proformat_school(request):

    school_year = Rate.objects.get(pk=1).year
 

    new_user_id   = request.session.get("new_user_id", None)
    if new_user_id :
        user = User.objects.get(pk = new_user_id )
    else :
        user = request.user
 
    school_id = request.session.get("inscription_school_id", None)
    if school_id :
        school = School.objects.get(pk = school_id)
    else :
        school = request.user.school

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
    demandeur =  school_datas+   "\n\nMontant de la cotisation : "+str(school.fee()+2)+"€ (frais de port inclus)" +"\n\nNom du demandeur : " + user.first_name + " "  + user.last_name + "\nCourriel : " + user.email  


    demandeur_tab = [[demandeur, "ASSOCIATION SACADO.XYZ \n2B avenue de la pinède \n83400 La Capte Hyères \nFrance\n\n\n\n\n" ]]
    demandeur_tab_tab = Table(demandeur_tab, hAlign='LEFT', colWidths=[5*inch,2*inch])

    elements.append(demandeur_tab_tab)
    elements.append(Spacer(0, 0.2*inch))



    my_texte_ = "Sous réserve du bon fonctionnement de son hébergeur LWS, l'association SACADO met l'ensemble des fonctionnalités du site https://sacado.xyz à disposition des enseignants de l'établissement "+school.name+"."
    paragraph = Paragraph( my_texte_  , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))

    sy = school_year.split("-")
    my_texte = "Le présent contrat est valide pour la période scolaire du 1 Septembre " + sy[0]+" jusqu'au 7 juillet "+sy[1]+" pour les établissements de rythme Nord. \nPour les établissements de rythme Sud, la validité de l'adhésion est valable sur l'année "+sy[1]+"."

    paragraph = Paragraph( my_texte  , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))

    signature_tab = [[ 'Signature précédée de la mention "Lu et approuvé" \n\n...........................................................\n\n\n ...........................................................',"" ]]
    signature_tab_tab = Table(signature_tab, hAlign='LEFT', colWidths=[4*inch,3*inch])

    elements.append(signature_tab_tab)
    elements.append(Spacer(0, 0.4*inch))

    doc.build(elements)

    return response


def tutos_video_sacado(request):
    context = {}
    return render(request, 'setup/tutos_video_sacado.html', context)



def ajax_get_subject(request):
    subject_id =  request.POST.get("subject_id")
    data = {}
    level_ids = Exercise.objects.values_list("level__id", flat= True).filter(theme__subject_id = subject_id).distinct()
    levels =  Level.objects.filter(pk__in=level_ids).order_by("ranking")
    data['html'] = render_to_string('ajax_get_subject.html', { 'levels' : levels , 'subject_id' :  subject_id })

    return JsonResponse(data)


###############################################################################################################################################################################
###############################################################################################################################################################################
########  Interface Python
###############################################################################################################################################################################
###############################################################################################################################################################################

def python(request):
    context = {}
    return render(request, 'basthon/interface_python.html', context)


###############################################################################################################################################################################
###############################################################################################################################################################################
########  Inscription élève isolé
###############################################################################################################################################################################
###############################################################################################################################################################################


def academy(request):

    nb_exercises = Exercise.objects.filter(supportfile__is_title=0 ).count()
    nb_students  = Student.objects.count()
    formules = Formule.objects.filter(pk__lte=3)
 

    form = AuthenticationForm()
    np_form = NewpasswordForm()

    levels = Level.objects.order_by("ranking")
    context = { 'nb_exercises' : nb_exercises , 'form' : form , 'np_form' : np_form , 'levels' : levels , 'nb_students' : nb_students , 'formules'  :  formules  }
    return render(request, 'setup/academy_index.html', context)



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
    nb_month    = request.POST.get("nb_month")    
    date_end    = request.POST.get("date_end")
    menu_id     = request.POST.get("menu_id")

    data_post = request.POST
    levels = Level.objects.all()

    try :
        nb_child = int(request.POST.get("nb_child"))
    except :
        nb_child = 1

    if nb_child == 0 :
        no_parent = True
    else :
        no_parent = False
  
    formule = Formule.objects.get(pk = 1)

    try :
        if request.user.is_in_academy :
            formules = Formule.objects.filter(pk__lte=3)
            adhesion = Adhesion.objects.filter(user = request.user).last()
            context = {  'formule' : formule , 'formules'  : formules ,   'no_parent' : no_parent , 'data_post' : data_post , "nb_child" : nb_child ,  'levels' : levels ,  'adhesion' : adhesion, "renewal" : True,   }
            return render(request, 'setup/renewal_adhesion.html', context)   
        else : 
            userFormset = formset_factory(UserForm, extra = nb_child + 1, max_num= nb_child + 2, formset=BaseUserFormSet)
            context = {  'formule' : formule ,  'no_parent' : no_parent , 'data_post' : data_post ,  'levels' : levels ,  'userFormset' : userFormset, "renewal" : False }
            return render(request, 'setup/detail_of_adhesion.html', context)   
    except :
        userFormset = formset_factory(UserForm, extra = nb_child + 1, max_num= nb_child + 2, formset=BaseUserFormSet)
        context = {  'formule' : formule ,  'no_parent' : no_parent , 'data_post' : data_post ,  'levels' : levels ,  'userFormset' : userFormset, "renewal" : False }
        return render(request, 'setup/detail_of_adhesion.html', context)   




def renewal_adhesion(request) :

    levels = Level.objects.order_by("ranking")
    formules = Formule.objects.filter(pk__lte=3)
    context = {    'formules'  : formules,  'levels'  : levels }
    return render(request, 'setup/renewal_adhesion.html', context)   






def creation_facture(facture):
 
    ##################################################################################################################
    # Création de la facture de l'adhésion au format pdf
    ##################################################################################################################

    #filename = str(user.id)+str(datetime.now().strftime('%Y%m%d'))+".pdf"
    filename= facture.chrono+".pdf"
    now = datetime.now().date()

    #outfiledir = "D:/uwamp/www/sacadogit/sacado/static/uploads/factures/{}/".format(user.id) # local
    outfiledir = "uploads/factures/{}/".format(facture.user.id) # on a server
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
    paragraph = Paragraph( "Réf : "+facture.chrono   , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.2*inch))

    paragraph = Paragraph( "Nom : "+facture.user.last_name   , normal )
    elements.append(paragraph)
    elements.append(Spacer(0, 0.1*inch))
    paragraph1 = Paragraph( "Prénom : "+facture.user.first_name   , normal )
    elements.append(paragraph1)
    elements.append(Spacer(0, 0.1*inch))
    paragraph2 = Paragraph( "Courriel : "+facture.user.email   , normal )
    elements.append(paragraph2)
    elements.append(Spacer(0, 0.3*inch))

 
    
    #para = Paragraph(  "Adhésion : "+formule.adhesion  , normal )
    #elements.append(para)
    #elements.append(Spacer(0, 0.1*inch))

    #para1 = Paragraph( "Menu : "+formule.name  , normal )
    #elements.append(para1)
    #elements.append(Spacer(0, 0.3*inch))
 
 
    total_price = 0     
    for adhesion in facture.adhesions.all() :

        delta    = adhesion.stop - adhesion.start
        duration = int(round(delta.days/30,0))

        paragraph_msg = Paragraph( "  -  {} {}, montant : {:.2f}€, durée : {:d} mois ".\
                  format(adhesion.student.user.first_name,adhesion.student.user.last_name,adhesion.amount,duration)  , normal )
        elements.append(paragraph_msg)
        elements.append(Spacer(0, 0.1*inch))
        total_price += adhesion.amount

    elements.append(Spacer(0, 0.5*inch))
    para3 = Paragraph( "Montant de l'adhésion : {:6.2f}€".format(total_price)  , normal )
    elements.append(para3)
    elements.append(Spacer(0, 0.1*inch))
 
        
    elements.append(Spacer(0, 2*inch))
    para3 = Paragraph( "Date de paiement : "+ facture.date.strftime('%d/%m/%Y') +" "  , normal )
    elements.append(para3)
    elements.append(Spacer(0, 0.1*inch))
 

    doc.build(elements)
    print("pdf facture ok")
    return store_path
  


def all_from_parent_user(user) :
    students = user.parent.students.all()
    u_parents = []
    for s in students :
        for  p in s.students_parent.all() : 
            if p not in u_parents :
                u_parents.append(p.user)
    return u_parents





def save_renewal_adhesion(request) :
    """page de paiement paypal
    request.POST contient une liste student_ids, une liste level, et des
    listes "engagement"+student_ids"""
    #----- on met les informations concernant le paiment dans session
    #------------- extraction des infos pour les passer au template
    somme = 0
    students = []
    for student_id in request.POST.getlist('student_ids') :
 
        try :
            engagement_si_tab = request.POST.get('engagement'+student_id)
            student_id,duration,amount = engagement_si_tab.split("-")
            amount=amount.replace(",",".")
            somme +=  float(amount)
            level_si = request.POST.get('level'+student_id)
            student  = Student.objects.get(pk = student_id)
            level    = Level.objects.get(pk = level_si)
            students.append({
                'duration' : duration, 
                'name' : student.user.first_name +" " +student.user.last_name ,
                'level_name' : level.name } 
                )



        except :	
            pass
    somme = "{:.2f}".format(somme).replace(".",",")
    context = { 'somme' : somme , 'students' : students }

    return render(request, 'setup/save_renewal_adhesion.html', context)  


@csrf_exempt
def accept_renewal_adhesion(request) :
   
	body=json.loads(request.body)
	#---------- Vérification du paiement auprès de paypal
	orderID = body['orderID'] 
	#print("https://api-m.sandbox.paypal.com/v2/checkout/orders/"+orderID)
	#r = requests.post("https://api-m.sandbox.paypal.com/v2/checkout/orders/"+orderID )
	#print(r.content)
	#print(request.session.keys())
	#print(request.session['paypal_payment'])
	ok=True
	if ok :
		parent=request.user
		adh=request.session['detail_adhesions']
		
		code = str(uuid.uuid4())[:8]
		chrono = create_chrono(Facture,"F")
		#-----------creation d'une nouvelle facture
		new_fact=Facture()
		new_fact.chrono=chrono
		new_fact.user=parent
		new_fact.orderID=orderID
		new_fact.date=datetime.now()
		new_fact.save() #il faut sauver avant de pouvoir ajouter les adhesions 
		#-------- modification de la closure des students
		for i,student_id in enumerate(adh['student_ids']) :
			student_user = User.objects.get(pk = student_id)
			eng = adh['engagements'][i].split("-")  # mois-prix 
			duration = int(eng[0]) * 31
			closure = student_user.closure
		
			if closure :    #il y a deja un abonnement en cours : le debut
							#du nouvel abonnement commence le lendemain de la fin
				debut=closure+timedelta(days=1)
			else : 
				debut=datetime.now()
				
			new_closure = debut + timedelta(days = duration)
			User.objects.filter(pk = student_id).update(closure=new_closure)
		
			#-----------creation d'une nouvelle adhésion
			new_adh=Adhesion()
			new_adh.amount=float(eng[1].replace(",","."))
			#new_adh.formule_id = eng[0]
			new_adh.start      = debut
			new_adh.stop       = new_closure
			new_adh.level      = Level.objects.filter(id=adh['level'][i])[0]
			new_adh.student    = Student.objects.get(user_id=student_id)
			new_adh.save()
			new_fact.adhesions.add(new_adh)
			#for pid in paypal_payment.getlist("user") :
			#Adhesion.objects.filter(user_id = pid).update(date_end=new_closure)
			#Adhesion.objects.filter(user_id = pid).update(file = creation_facture(user,data_posted,code))
		new_fact.save()
		new_fact.file=creation_facture(new_fact)

		#     user = User.objects.get(pk = pid)

		#     ##################################################################################################################
		#     # Envoi du courriel
		#     ##################################################################################################################
		#     msg = "Bonjour "+ user.first_name +" "+ user.last_name +",\n\n vous venez de souscrire à un prolongement de l'abonnement à la SACADO Académie. \n"
		#     msg += "votre référence d'adhésion est "+chrono+".\n\n"
		#     msg += "Les identifiants de connexion n'ont pas changé.\n"
		#     msg += "L'équipe de SACADO Académie vous remercie de votre confiance.\n\n"
		#     send_mail("Inscription SACADO Académie", msg, settings.DEFAULT_FROM_EMAIL, [ user.email ]
		# # Envoi à SACADO
		# sacado_rcv = ["philippe.demaria83@gmail.com","brunoserres33@gmail.com","sacado.asso@gmail.com"]
		# sacado_msg = "Renouvellement d'adhésion après période d'essai : user_id"+ user.id +" : "+ user.first_name +" "+ user.last_name 
		# send_mail("Renouvellement d'adhésion après période d'essai", sacado_msg, settings.DEFAULT_FROM_EMAIL, sacado_rcv)
		data={"ok":True} 
		#return JsonResponse(data,safe=True)
		return HttpResponse("ok")


def attribute_all_documents_to_student_by_level(level,student) :
    try :
        group = Group.objects.filter(level = level, school_id = 50, name__contains="SacAdo").first()
        group.students.add(student)
        groups = [group]
        test = attribute_all_documents_of_groups_to_a_new_student(groups, student)
        success = True
    except :
        success = False
    return success




def add_adhesion(request) :

    form =  UserForm(request.POST or None)
    formule = Formule.objects.get(pk = 1)
    levels = Level.objects.order_by("ranking")
    today = time_zone_user(request.user)

    if request.method == "POST" :
        if form.is_valid():
            #end = today + timedelta(days=7)
            end = datetime(2022,8,31) 
            form_user = form.save(commit=False)
            form_user.closure = end
            form_user.school_id = 50
            form_user.cgu = 1
            form_user.country_id = 4
            form_user.user_type = 0
            form_user.save()
            level_id = request.POST.get("level")
            student = Student.objects.create(user=form_user, level_id = level_id)
            level   = Level.objects.get(pk = level_id)
            u_parents = all_from_parent_user(request.user)

            u_p_mails = []
            for u_p in u_parents : 
                u_p.parent.students.add(student)
                u_p_mails.append(u_p.email)

            chrono = create_chrono(Facture,"F")
            success = attribute_all_documents_to_student_by_level(level,student)
  
            adhesion = Adhesion.objects.create(start = today, stop = end, student = student , level_id = level_id  , amount = 0  , formule_id = None ) 
            facture = Facture.objects.create(chrono = chrono, file = "" , user = request.user , date = today     ) 
            facture.adhesions.add(adhesion)

            msg = "Bonjour,\n\nVous venez de souscrire à une adhésion à la SACADO Académie. \n"
            msg += "Votre référence d'adhésion est "+chrono+".\n\n"
            msg += "Vous avez inscrit : \n"
            msg += "- "+student.user.first_name+" "+student.user.last_name+", l'identifiant de connexion est : "+student.user.username +" \n"
            msg += "\n\nRetrouvez ces détails à partir de votre tableau de bord après votre connexion à https://sacado.xyz/academy\n\n"
            msg += "L'équipe de SACADO Académie vous remercie de votre confiance.\n\n"



            msg += "Voici quelques conseils pour votre enfant :\n\nConnecte toi sur https://sacado.xyz/academy\n\n"
            msg += "Indique ton Nom d’utilisateur et ton Mot de passe\n\n"
            msg += "Clique sur le bouton « connexion »   -> Tu arrives ensuite sur ton profil. \n\n"   
            msg += "Le menu est à gauche :\n\n"
            msg += "« Compte » permet de changer ton mot de passe, te déconnecter et choisir ton avatar.\n\n"
            msg += "« Matières » te permet d’accéder à tes parcours d’exercices. Tu cliques sur « accéder » pour entrer dans le dossier, puis tu choisis un thème."
            msg += "A l’intérieur, tu auras tous les exercices.\n\n"
            msg += "Tu vas à ton rythme, tu choisis les exercices que tu as besoin de travailler, de réviser…\n\n"
            msg += "Tu enregistres quand tu as fait au moins 5 situations (parfois 10), si tu as fait des erreurs, c’est normal parce que tu apprends, essaie de bien comprendre la correction proposée, puis continue les exercices suivants pour améliorer ton score."
            msg += "Une pastille de couleur sur un exercice permet de voir que tu l’as déjà fait (% de réussite).\n\n"
            msg += "« Suivi » permet de voir ton évolution. Clique en bas sur les différents bilans et en haut à droite pour la synthèse.\n\n"
            msg += "« Flashpack » : permet de créer des propres cartes de révision, pour entraîner ta mémoire.\n\n"

                
            send_mail("Inscription SACADO Académie", msg, settings.DEFAULT_FROM_EMAIL, u_p_mails )

            return redirect("index")
 
    context = {  "renewal" : True, "form" : form, "formule" : formule  ,   'levels' : levels , }
    return render(request, 'setup/add_adhesion.html', context)   
 
        




def commit_adhesion(request) :

    data_post   = request.POST
    try :
        nb_child = int( data_post.get("nb_child") )
    except :
        nb_child = 1     

    menu_id     = int(data_post.get("menu_id"))    
    data_posted = {"total_price" : data_post.get('total_price'), "month_price" : data_post.get('month_price'), "nb_month" : data_post.get('nb_month'), "date_end" : data_post.get('date_end'), "menu_id" : menu_id , "nb_child" : nb_child }
 
    levels      = request.POST.getlist("level")

    max_num     = nb_child + 2
    userFormset = formset_factory(UserForm, extra = nb_child + 1, max_num = max_num , formset=BaseUserFormSet)
    formset     = userFormset(data_post)

    if int(menu_id) > 0 : formule = Formule.objects.get(pk = int(menu_id))
    else :  
        formule= None

    parents  , students = [] , []
    if formset.is_valid():
        i = 0
        for form in formset :
            user = dict()
            user["last_name"]  =  form.cleaned_data["last_name"]
            user["first_name"] =  form.cleaned_data["first_name"]
            user["username"]   =  form.cleaned_data["username"]
            user["password_no_crypted"]  =  form.cleaned_data["password1"] 
            user["password"]   =  make_password(form.cleaned_data["password1"])
            user["email"]      =  form.cleaned_data["email"]   
            if 1<= i <= nb_child : 
                level          = Level.objects.get(pk = int(levels[i])).name
                user["level"]  = level 
                students.append(user)
            else :
                user["level"]      = "" 
                parents.append(user)
            i += 1

        # mise en session des coordonnées des futurs membres  et  des détails de l'adhésion
 
        request.session["parents_of_adhesion"] = parents
        request.session["students_of_adhesion"] = students
        request.session["data_posted"] = data_posted 
 
        ############################################################
    else:
        messages.error(request,formset.errors)
        messages.error(request,"Confirmation du mot de passe erronée. Merci de revenir à la page précédente.")



    context = {'formule' : formule ,  'data_post' : data_posted , 'parents' : parents  , 'students' : students  }
 
    return render(request, 'setup/commit_adhesion.html', context)   







def save_adhesion(request) :

    parents_of_adhesion = request.session.get("parents_of_adhesion")
    students_of_adhesion = request.session.get("students_of_adhesion")
    data_posted = request.session.get("data_posted") # détails de l'adhésion
    total_price = data_posted.get("total_price")
    nb_child = int(data_posted.get("nb_child"))

    users = []

    total_price = 0
    formule          = None
    formule_adhesion = " période d'essai "
    formule_name     = " Essai "
    today = time_zone_user(request.user)
    #date_end_dateformat = today + timedelta(days=7)
    date_end_dateformat = datetime(2022,8,15)  
    date_end = str(date_end_dateformat)
    nb_month = 0
    menu_id = 1
    ##################################################################################################################
    # Insertion dans la base de données
    ##################################################################################################################
    students_in , adhesions_in = [] , []
    code = str(uuid.uuid4())[:8]
    chrono = create_chrono(Facture,"F")
    for s in students_of_adhesion :

        last_name, first_name, username , password , email , level =  s["last_name"]  , s["first_name"] , s["username"] , s["password"] , s["email"] , s["level"]  
        level = Level.objects.get(name = level)    
        user, created = User.objects.update_or_create(username = username, password = password , user_type = 0 , defaults = { "last_name" : last_name , "first_name" : first_name  , "email" : email , "country_id" : 4 ,  "school_id" : 50 , "closure" : date_end_dateformat })
        student,created_s = Student.objects.update_or_create(user = user, defaults = { "task_post" : 1 , "level" : level })

        success = attribute_all_documents_to_student_by_level(level,student)

        folders = Folder.objects.filter(level = level, teacher_id = 2480 , is_trash=0) # 2480 est SacAdoProf
        for f in folders :
            f.students.add(student)

        if created_s : 
            students_in.append(student) # pour associer les enfants aux parents 

 
        adhesion = Adhesion.objects.create( student = student , level = level , start = today , amount = total_price , stop = date_end_dateformat , formule_id  = None )
        adhesions_in.append(adhesion)

    i = 0
    for p in parents_of_adhesion :

        # if nb_child == 0 : # enfant émancipé ou majeur
        #     Adhesion.objects.update_or_create(user = user, amount = total_price , menu = menu_id, defaults = { "file"  : creation_facture(user,data_posted,code), "date_end" : date_end_dateformat,  "children" : nb_child, "duration" : nb_month })
        last_name, first_name, username , password , email =  p["last_name"]  , p["first_name"] , p["username"] , p["password"] , p["email"] 
        user, created = User.objects.update_or_create(username = username, password = password , user_type = 1 , defaults = { "last_name" : last_name , "first_name" : first_name  , "email" : email , "country_id" : 4 ,  "school_id" : 50 ,  "closure" : date_end_dateformat })
        parent,create = Parent.objects.update_or_create(user = user, defaults = { "task_post" : 1 })

        if i == 0 :
            facture = Facture.objects.create(chrono = chrono , user = user, date = today ,    file = None )
            new_facture = facture
        else :
            facture = new_facture

        i += 1
        

        for adh in adhesions_in :
            facture.adhesions.add(adh)

        for si in students_in :
            parent.students.add(si)


        ##################################################################################################################
        # Envoi du courriel
        ##################################################################################################################
        nbc = ""
        if nb_child > 1 :
            nbc = "s"
            
        msg = "Bonjour "+p["first_name"]+" "+p["last_name"]+",\n\nVous venez de souscrire à une adhésion "+formule_adhesion +" à la SACADO Académie avec le menu "+formule_name+". \n"
        msg += "Votre référence d'adhésion est "+chrono+".\n\n"
        msg += "Votre identifiant est "+p["username"]+" et votre mot de passe est "+p["password_no_crypted"]+"\n"
        msg += "Vous avez inscrit : \n"
        for s in students_of_adhesion :
            msg += "- "+s["first_name"]+" "+s["last_name"]+", l'identifiant de connexion est : "+s["username"]+", le mot de passe est "+s["password_no_crypted"]+" \n"

        msg += "\n\nRetrouvez ces détails à partir de votre tableau de bord après votre connexion à https://sacado.xyz/academy\n\n"

        msg += "L'équipe de SACADO Académie vous remercie de votre confiance.\n\n"

        ###### Quelques recommandations pour les parents

        msg += "Voici quelques conseils pour votre enfant :\n\nConnecte toi sur https://sacado.xyz/academy\n\n"
        msg += "Indique ton Nom d’utilisateur et ton Mot de passe\n\n"
        msg += "Clique sur le bouton « connexion »   -> Tu arrives ensuite sur ton profil. \n\n"   
        msg += "Le menu est à gauche :\n\n"
        msg += "« Compte » permet de changer ton mot de passe, te déconnecter et choisir ton avatar.\n\n"
        msg += "« Matières » te permet d’accéder à tes parcours d’exercices. Tu cliques sur « accéder » pour entrer dans le dossier, puis tu choisis un thème."
        msg += "A l’intérieur, tu auras tous les exercices.\n\n"
        msg += "Tu vas à ton rythme, tu choisis les exercices que tu as besoin de travailler, de réviser…\n\n"
        msg += "Tu enregistres quand tu as fait au moins 5 situations (parfois 10), si tu as fait des erreurs, c’est normal parce que tu apprends, essaie de bien comprendre la correction proposée, puis continue les exercices suivants pour améliorer ton score."
        msg += "Une pastille de couleur sur un exercice permet de voir que tu l’as déjà fait (% de réussite).\n\n"
        msg += "« Suivi » permet de voir ton évolution. Clique en bas sur les différents bilans et en haut à droite pour la synthèse.\n\n"
        msg += "« Flashpack » : permet de créer des propres cartes de révision, pour entraîner ta mémoire.\n\n"

        #########
        email=EmailMessage("Inscription SACADO Académie",msg,settings.DEFAULT_FROM_EMAIL,[p["email"]])

        image=MIMEBase('application','octet-stream')
        nomImage="instruction.png"
        fichierImage=open(settings.STATIC_ROOT+"/img/"+nomImage,'rb')
        image.set_payload((fichierImage).read())
        encoders.encode_base64(image)
        image.add_header('Content-Disposition', "inline ; filename= %s" % nomImage)
        
        email.attach(image)
        
        email.send()
        #####################"
        # fin envoi du courriel 2e version, bêta
        ##################################################
       

    for s in students_of_adhesion :
        srcv = []        
        if s["email"] : 
            srcv.append(s["email"])
            smsg = "Bonjour "+s["first_name"]+" "+s["last_name"]+",\n\n vous venez de souscrire à une adhésion "+formule_adhesion +" à SACADO Académie avec le menu "+formule_name+". \n"
            smsg += "votre référence d'adhésion est "+chrono+".\n\n"
            smsg += "Votre identifiant est "+s["username"]+" et votre mot de passe est "+s["password_no_crypted"]+"\n\n"
            smsg += "Il est possible de retrouver ces détails à partir de votre tableau de bord après votre connexion à https://sacado.xyz/academy"
            smsg += "L'équipe SACADO vous remercie de votre confiance.\n\n"

            send_mail("Inscription SACADO académie", smsg, settings.DEFAULT_FROM_EMAIL, srcv)

    # Envoi à SACADO
    sacado_rcv = ["sacado.asso@gmail.com"]
    sacado_msg = "Une adhésion "+formule_adhesion +" SACADO vient d'être souscrite. \n\n"

    i,j = 1,1
    for p in parents_of_adhesion :
        sacado_msg += "Parent "+str(i)+" : "+p["first_name"]+" "+p["last_name"]+" adresse de courriel : "+p["email"]+". \n\n"
        i+=1
    for s in students_of_adhesion :
        if s["email"] :
            adr = ", adresse de courriel : "+s["email"]
        else :
            adr = "" 
        sacado_msg += "Enfant "+str(j)+" : "+s["first_name"]+" "+s["last_name"]+" Niveau :" +s["level"]+adr+"\n\n"         
        j+=1

    send_mail("Inscription SACADO Académie", sacado_msg, settings.DEFAULT_FROM_EMAIL, sacado_rcv)

    #########################################################

    username = parents_of_adhesion[0]["username"]
    password = parents_of_adhesion[0]["password_no_crypted"]

    user = authenticate(username=username, password=password)
    login(request, user,  backend='django.contrib.auth.backends.ModelBackend' )


    return redirect( 'index' )



def adhesions_academy(request):
    """ liste des adhésions """
    user = request.user

    u_parents = all_from_parent_user(user)

    factures =  Facture.objects.filter(user__in=u_parents) 


    today = time_zone_user(request.user)
    last_week = today + timedelta(days = 7)
    context = { "factures" : factures,  "last_week" : last_week    }

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

    send_mail("Demande d'annulation d'adhésion SACADO", msg, settings.DEFAULT_FROM_EMAIL, ["sacado.asso@gmail.com"])

    return redirect("adhesions")


 

def csrf_failure(request, reason=""):
    ctx = {'message': 'some custom messages'}
    return render(request,"csrf_failure.html", ctx) 




def list_exercises_academy(request , id):

    level = Level.objects.get(pk=id)    
    exercises = Exercise.objects.filter(level=level,supportfile__is_title=0,theme__subject_id=1).order_by("theme","knowledge__waiting","knowledge","ranking")

    pk_ids = [0,1762,1651,1427,984,2489,2035,4842,8087,5802,1120,3891,3233,0,6107]

    exercise = Exercise.objects.get(pk=pk_ids[id])

    return render(request, 'setup/list_exercises_academy.html', {'exercises': exercises, 'level':level, 'exercise':exercise  })




def envoie_rapport(fichiers,destinataires):
    """envoie les rapports à une seule famille.
    Fichiers contient une liste de noms de fichiers pdf à envoyer
    destinataires : une liste de chaines contenant les destinataires"""
    #------------
    if destinataires==[] :
        return "aucun destinataire"
    
    msg=MIMEMultipart()
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = destinataires[0]
    for i in range(1,len(destinataires)):
        msg['to']+=","+destinataires[i]
        
    liste_eleves=[]  #liste des eleves dont on joint les rapports

    for fichier in fichiers :
        try :
            pdf=open(fichier,'rb')
            fpdf = MIMEBase('application','octet-stream')
            fpdf.set_payload(pdf.read())
            pdf.close()
            encoders.encode_base64(fpdf)
            fpdf.add_header('content-disposition', 'attachment; filename ='+ fichier)
            msg.attach(fpdf)
            liste_eleves.append("eleve"+fichier)
        except :
            print("""fonction envoie_pdf de setup : 
le fichier {} qui doit être envoyé à {} est introuvable""".format(fichier,msg['To']))
    npdf=len(liste_eleves)  #nombre de fichiers à envoyer
    if npdf==0 :
        print("""fonction envoie_pdf de setup : 
aucun fichier pdf à envoyer""")
        return "aucun fichier pdf à envoyer"

    # preparation du joli texte du corps du message
    eleves=liste_eleves[0]
    if npdf==1 :
        pluriel=""
    else :
        pluriel="s"
        for i in range(1,npdf-1) :
            eleves+=", "+liste_eleves[i]
        eleves+=" et "+liste_eleves[-1]
    #-------------------------------
    msg['Subject'] = "Rapport{} d'activité de ".format(pluriel)+eleves
    
    msg.attach(MIMEText("""Bonjour,
veuillez trouver en pièce jointe le{} rapport{} d'activité{} de {}.

Très cordialement,

L'équipe Sacado Académie""".format(pluriel,pluriel,pluriel,eleves),'plain'))

    server = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
    server.set_debuglevel(False) # show communication with the server
    try:
       server.ehlo()
       if server.has_extn('STARTTLS'):
          server.starttls()
          server.ehlo() 
       server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
       server.sendmail(settings.DEFAULT_FROM_EMAIL, destinataires,msg.as_string() )
    finally:
        server.quit()
    return "mails envoyés avec succès"



    
def send_reports(request) :
    """envoie tous les rapports à toutes les familles"""
    fichiers=["toto1.pdf","toto2.pdf", "toto1.pdf"]
    destinataires=["stephan.ceroi@mailo.com","stephan.ceroi@gmail.com"]
    r=envoie_rapport(fichiers, destinataires)
    return HttpResponse(r)



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
    nb_students = User.objects.filter(school=school, user_type=0).exclude(username__contains="_e-test_").count()
    nb_groups   = Group.objects.filter(Q(teacher__user__school=school)|Q(teacher__user__schools=school)).count()
    
    is_lycee = False
    try :
        if not school.get_seconde_to_comp :
            for t in teachers :
                if t.groups.filter(level__gte=10).count() > 0 :
                    is_lycee = True
                    break
    except :
        pass

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

    rates       = Rate.objects.all() #tarifs en vigueur 
    school_year = rates.first().year #tarifs pour l'année scolaire
    only_admin_can_manage = school.is_managing

    renew_propose = renew(school)

 
    return render(request, 'dashboard_admin.html', {'nb_teachers': nb_teachers, 'nb_students': nb_students, 'school_id' : school_id , "school" : school ,  'renew_propose' : renew_propose ,
                                                    'nb_groups': nb_groups, 'schools_tab': schools_tab, 'stage': stage, 'is_lycee' : is_lycee , 'school_year' : school_year ,  'rates' : rates , 
                                                    'eca': eca, 'ac': ac, 'dep': dep , 'only_admin_can_manage' : only_admin_can_manage
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
    question = questions[n]    
    n +=1
    context = {  "quizz" : quizz , "question" : question , "n" : n}
    return render(request, 'tool/play_quizz_start.html', context)

############################################################################################
#######  WEBINAIRE
############################################################################################


def webinaire_register(request):

    today = time_zone_user(request.user) 
    webinaire = Webinaire.objects.filter(date_time__gte=today,is_publish=1).first()
    nb_places = 20 - webinaire.users.count()
    return render(request, 'setup/form_webinaire_register.html', {'webinaire': webinaire , 'nb_places' : nb_places })


def webinaire_registrar(request,id,key):

    if request.user.is_superuser :
        webinaire = Webinaire.objects.get(id=id)
        if key == 1:
            webinaire.users.add(request.user)
        else :
            webinaire.users.remove(request.user)

    return redirect('index') 



def webinaire_show(request,id):
    if request.user.is_superuser :
        webinaire = Webinaire.objects.get(id=id)
        return render(request, 'setup/show_webinaire.html', {'webinaire': webinaire })
    else :
        return redirect('index') 



def webinaire_list(request):
    if request.user.is_superuser :
        webinaires = Webinaire.objects.all()
        return render(request, 'setup/list_webinaires.html', {'webinaires': webinaires })
    else :
        return redirect('index') 



def webinaire_create(request):

    if request.user.is_superuser :
        form = WebinaireForm(request.POST or None ,  request.FILES or None  )
        if form.is_valid():
            form.save()
            messages.success(request, 'Le webinaire a été créé avec succès !')
            return redirect('webinaires')
        else:
            print(form.errors)
        context = {'form': form, 'communications' : [] , 'webinaire': None  }

        return render(request, 'setup/form_webinaire.html', context)
    else :
        return redirect('index') 



def webinaire_update(request, id):

    if request.user.is_superuser :
        webinaire = Webinaire.objects.get(id=id)
        form = WebinaireForm(request.POST or None, request.FILES or None, instance=webinaire )
        if request.method == "POST" :
            if form.is_valid():
                form.save()
                messages.success(request, 'Le webinaire a été modifié avec succès !')
                return redirect('webinaires')
            else:
                print(theme_form.errors)

        context = {'form': form,  'webinaire': webinaire,   }

        return render(request, 'setup/form_webinaire.html', context )
    else :
        return redirect('index')  


def webinaire_delete(request, id):
    if request.user.is_superuser :
        webinaire = Webinaire.objects.get(id=id)
        webinaire.delete()

        return redirect('webinaires')
    else :
        return redirect('index') 



def rgpd(request):
    context = {  }
    return render(request, 'setup/rgpd_gar.html', context)  

def gar_rgpd(request):
    context = {  }
    return render(request, 'setup/rgpd_gar.html', context)  


def cgu(request):
    context = {  }
    return render(request, 'setup/cgu.html', context)  


def cgv(request):
    context = {  }
    return render(request, 'setup/cgv.html', context)  


def mentions(request):
    context = {  }
    return render(request, 'setup/mentions.html', context)  

def mentions_academy(request):
    context = {  }
    return render(request, 'setup/mentions_academy.html', context)  


def tweeters(request):
    if request.user.is_superuser :
        tweeters = Tweeter.objects.all().order_by("-date_created")
        return render(request, 'setup/tweeters.html', {'tweeters': tweeters })
    else :
        return redirect('index') 


def tweeters_public(request):
    tweeters = Tweeter.objects.all().order_by("-date_created")
    return render(request, 'setup/tweeters_public.html', {'tweeters': tweeters })
 


def tweeter_create(request):

    if request.user.is_superuser :
        form = TweeterForm(request.POST or None  )
        if form.is_valid():
            form.save()
            messages.success(request, 'Le tweet a été créé avec succès !')
            return redirect('tweeters')
        else:
            print(form.errors)
        context = {'form': form, 'tweeter': None  }

        return render(request, 'setup/form_tweeter.html', context)
    else :
        return redirect('index') 



def tweeter_update(request, id):

    if request.user.is_superuser :
        tweeter = Tweeter.objects.get(id=id)
        form = TweeterForm(request.POST or None,  instance=tweeter )
        if request.method == "POST" :
            if form.is_valid():
                form.save()
                messages.success(request, 'Le tweet a été modifié avec succès !')
                return redirect('tweeters')
            else:
                print(form.errors)

        context = {'form': form,  'tweeter': tweeter,   }

        return render(request, 'setup/form_tweeter.html', context )
    else :
        return redirect('index')  


def tweeter_delete(request, id):
    if request.user.is_superuser :
        tweeter = Tweeter.objects.get(id=id)
        tweeter.delete()

        return redirect('tweeters')
    else :
        return redirect('index') 
