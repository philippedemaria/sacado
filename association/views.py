from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from account.decorators import user_is_board
from templated_email import send_templated_mail
from django.db.models import Q , Sum
from django.contrib.auth.decorators import  permission_required,user_passes_test
############### bibliothèques pour les impressions pdf  #########################
from association.models import *
from association.forms import *
from account.models import User, Student, Teacher, Parent ,  Response , Connexion
from bibliotex.models import Relationtex
from qcm.models import Exercise, Studentanswer , Customanswerbystudent , Writtenanswerbystudent
from school.models import School
from school.forms import SchoolForm
from group.models import Group
from school.gar import *
from setup.models import Formule
from setup.forms import FormuleForm
from socle.models import Level, Subject , Skill
from qcm.models import Supportfile
#################################################################################
import os
from django.utils import formats, timezone
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak,Frame , PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from html import escape
cm = 2.54
#################################################################################
import re
import pytz
from datetime import datetime  , timedelta , date
from general_fonctions import *
import xlwt
import uuid
import json 
from subprocess import run 



#################################################################
# Tex to BiblioTex
#################################################################



#################################################################
# Importation d'une fiche d'exos pour creer une bibliotex
#################################################################

tmpdir="ressources/fichesexos/tmp/"

def bloc(texte,commande):
    if "\\"+commande+"{" not in texte :
        return ""
    deb=texte[texte.index("\\"+commande+"{")+len(commande)+2:]  
    niv=1
    for i in range(1,len(deb)) :
        if deb[i]=='{' and deb[i-1]!='\\' : niv+=1
        if deb[i]=='}' and deb[i-1]!='\\' : niv-=1
        if niv==0 :
            return deb[0:i]

def conversion(tex) : 
    "prepare le fichier tex pour facililiter le boulot de mak4ht"
    f=open(tmpdir+"translitterations.txt")
    for l in f :
        [old,new]=l.split(r"%")
        old=old.strip()
        new=new.strip()
        if old[-1].isalpha() : # c'est une commande type \toto, il faut que le caractere
                                # suivant ne soit pas une lettre.
            p=re.compile(old.replace("\\",r"\\") +"([^a-zA-Z])")
            tex=p.sub(new.replace("\\",r"\\")+r"\1",tex)
        else :
            tex=tex.replace(old,new)
    return tex


def toHtml(tex) :
    if tex=="" : return ""
    f=open(tmpdir+"tmptex.tex","w",encoding="utf-8")
    f.write(r"\documentclass{article}")
    f.write(r"\begin{document}")
    f.write(conversion(tex))
    f.write("\n\n\end{document}")
    f.close()
    run(["make4ht","tmptex.tex","-u",'mathjax,charset=utf-8'],cwd=tmpdir)
    f=open(tmpdir+"tmptex.html","r")
    html=f.read() 
    f.close()
    return html
    #f=open(tmpdir+"tmptex.html","w")
    #f.write(conversion(html))
    #f.close()

def extraitBody(html) :
    deb=html.index("<body")+5 # pour un raison etrange, le > est parfois separé de <body
    while html[deb]!='>' :
        deb+=1
    fin=html.index("</body>")
    html=html[deb+1:fin].replace(r'\(','$').replace(r'\)','$')
    return html 


def create_bibliotex_from_tex(request) :

    levels = Level.objects.order_by("ranking")
    validate_save = request.POST.get("validate_save",None)
    post = False
    skills , knowledges = [], []
    context = { 'levels' : levels , 'post' : post } 

    if request.method == "POST" and not validate_save :
        post = True
        this_file  = request.FILES["this_file"]
        level_id   = request.POST.get("level")
        level      = Level.objects.get(pk=level_id)
        knowledges = level.knowledges.all()
        skills     = Skill.objects.filter(subject_id=1) 
 
        reader = this_file.read().decode('utf8')

        Lexos  = reader.split(r"\exo")

        exos=[]
        titreBiblio = bloc(reader,'fexos')
        for i,exo in enumerate(Lexos) :
            ex=dict()
            ex['titre'] = bloc(exo,'titreexo')
            ex['eno']   = bloc(exo,'eno')
            ex['cor']   = bloc(exo,'cor') 
            toHtml(ex['eno'])
            ex['enohtml']=extraitBody(open(tmpdir+"tmptex.html").read() )             
            if ex['cor']!="" :
                    toHtml(ex['cor'])
                    ex['corhtml']=extraitBody(open(tmpdir+"tmptex.html").read() )
            else :
                ex['corhtml']=""

            exos.append(ex)
        context.update( { 'level_id' : level.id ,   'post' : post , 'listeExos' : exos , 'knowledges' : knowledges , 'skills' : skills  , 'titreBiblio' : titreBiblio } )  

    elif request.method == "POST" and  validate_save :

        if validate_save :
            bibliotex,created = Bibliotex.objects.update_or_create( title = titreBiblio,
                                                            author_id   = 2480,
                                                            teacher_id  = 2480,
                                                            defaults={ 'is_favorite' : 1,
                                                                'is_share' : 1,
                                                                'is_archive'  : 0,
                                                                'is_publish' :1}
                                                          )
            if not created :
                messages.error(request,"Ce titre de biblioTex est déjà utilisé.")
                insert_exos = False
            else :
                subject = Subject.objects.get(pk=1) 
                group = Group.objects.filter(teacher_id=2480,subject=subject,level=level).first()
                bibliotex.levels.add(group.level)
                bibliotex.subjects.add(group.subject)
                bibliotex.groups.add(group)


        for i,exo in enumerate(Lexos) :

            ex=dict()
            ex['titre'] = bloc(exo,'titreexo')
            ex['eno']   = bloc(exo,'eno')
            ex['cor']   = bloc(exo,'cor') 
            toHtml(ex['eno'])
            ex['enohtml']=extraitBody(open(tmpdir+"tmptex.html").read() )             
            if ex['cor']!="" :
                    toHtml(ex['cor'])
                    ex['corhtml']=extraitBody(open(tmpdir+"tmptex.html").read() )
            else :
                ex['corhtml']=""

            if validate_save and insert_exos :

                knowledges = request.POST.getlist("knowledge"+str(i),None)
                knowledge  = Knowlege.objects.get(pk=knowledges[0])
                exotex, created = Exotex.objects.update_or_create(
                    title = ex['titre'],
                    content = ex['eno'] ,
                    content_html = request.POST.get("enohtml"+str(i),None) ,
                    author_id = 2480,
                    calculator = 0, 
                    duration = 15,
                    ###### Socle
                    subject       = group.subject ,
                    knowledge_id  = knowledges[0] ,
                    level         = group.level ,
                    theme         = knowledge.theme, 
                    point           = 0,
                    correction      = ex['cor'],
                    correction_html = request.POST.get("corhtml"+str(i),None),
                    ranking         = 0,
                    bloc_id = None,
                    is_read = 0)
                try : exotex.knowledges.set(knowledges[1:])
                except : pass 
                try : exotex.skills.set(request.POST.getlist("skill"+str(i)))
                except : pass 
                relationtex, created = Relationtex.objects.update_or_create(
                        exotex = exotex,
                        bibliotex = bibliotex,
                        teacher_id = 2480, 
                        calculator = 0,
                        duration = 15, 
                        )
                try : relationtex.knowledges.set(knowledges[1:])
                except : pass 
                try : relationtex.skills.set(request.POST.getlist("skill"+str(i)))
                except : pass 

            exos.append(ex)
        


    return render(request, 'association/create_bibliotex_from_tex.html', context )





#################################################################
# Suppression des fichiers non utilisés
#################################################################
@user_passes_test(user_is_board)
def to_clean_database(request,start):

    levels = Level.objects.exclude(pk=13).order_by('ranking')
    list_to_remove , list_to_keep = [] , []
    names = []
    
    ressources   = '/var/www/sacado/ressources/' 
    for level in levels :
        dico_level = {}
        dico_level['level'] = level.name
        supportfiles = Supportfile.objects.values_list('ggbfile',flat=True).filter(level=level)

        dirname      = ressources + 'ggbfiles/' + str(level.id)
        back_up_root = ressources + 'ggbfiles_backup/' + str(level.id) +"/" 

        list_level = []

        files = os.listdir(dirname)
        for file in files :
            dico_list_level = {}
            data_file = 'ggbfiles/'+ str(idl)+"/"+file
            dico_list_level['url'] = data_file
            list_level.append(dico_list_level)
        dico_level['urls'] = list_level  
        names.append(dico_level)    
 
    if start == 1 :
        to_keep_list()

    context = {'names' : names , }        
    return render(request, 'association/to_clean_database.html', context )


@user_passes_test(user_is_board)
def to_keep_list(request):

    levels = Level.objects.exclude(pk=13).order_by('ranking')

    list_to_keep = []

    dir_source     = '/var/www/sacado/ressources/ggbfiles/'

    for level in levels :
        idl = level.id
        supportfiles = Supportfile.objects.values_list('ggbfile',flat=True).filter(level=level)
        
        dirname      = dir_source + str(idl)

        files = os.listdir(dirname)
        for file in files :
            data_file = 'ggbfiles/'+ str(idl)+"/"+file
            if data_file in supportfiles :
                list_to_keep.append(str(idl)+"/"+file)

     
    #f =  open(dir_root + 'new_exos.txt', "w") 
    #for url in list_to_keep:
    #    print(url, file=f)
    #f.close()
    # Synchronisation des exercices de sacado vers academi                                                   
    # la liste des fichiers à modifier doit être                                                             
    # /var/www/sacado/ressources/ggbfiles/newExos.txt                                                      
    dir_dest="/var/www/sacado-academie/ressources/ggbfiles/"
    listeExos=open(dir_source+"newExos.txt","r")

    # creation de l'archive, on la place dans le même répertoire                                             
    commande = ["tar", "-C" , dir_source, "-czf", "newExos.tgz"] + list_to_keep
    run(commande)
    run( ["scp", dir_source+"newExos.tgz", "root@31.207.37.10:"+dir_dest+"newExos.tgz"])
    # Récupération de la liste, sur academie                                                                 
    commande = ["ssh", "-l", "root", "31.207.37.10", "tar -tf "+dir_dest+"newExos.tgz  > "+dir_dest+"newExos.txt"]
    run(commande)

    return

#################################################################
# Suppression des fichiers non utilisés
#################################################################

def get_active_year():
    """ renvoi d'un tuple sous forme 2021-2022  et d'un entier 2021 """
    active_year = Activeyear.objects.get(is_active=1)
    int_year = active_year.year
    return active_year, int_year


def get_active_abonnements(user):

    active_year, this_year = get_active_year() # active_year = 2020-2021 ALORS QUE this_year est 2020
    strt = datetime(this_year,6,1)
    start = dt_naive_to_timezone(strt,user.time_zone)


    abonnements = Abonnement.objects.filter(date_start__gte = start).exclude(accounting__date_payment = None).order_by("school__country__name")
    return abonnements


def get_pending_abonnements(user):

    active_year, this_year = get_active_year() # active_year = 2020-2021 ALORS QUE this_year est 2020
    strt = datetime(this_year,9,1)
    stp  = datetime(this_year+1,8,31)
    start = dt_naive_to_timezone(strt,user.time_zone)
    stop  = dt_naive_to_timezone(stp,user.time_zone)

    abonnements = Abonnement.objects.filter(date_start__gte = start , date_stop__lte = stop, accounting__date_payment = None).order_by("school__country__name")
    return abonnements




def get_accountings(user):

    active_year, this_year = get_active_year()
    if this_year == 2021 : 
        date_start   = datetime(2021, 1, 1) 
    else :
        date_start   = datetime(this_year, 9,1) 
    date_stop    = datetime(this_year+1, 9, 1) # gestion de l'année en cours début le 1er septembre

    start = dt_naive_to_timezone(date_start,user.time_zone)
    stop  = dt_naive_to_timezone(date_stop,user.time_zone)

    accountings = Accounting.objects.filter(date__gte = start , date__lt = stop )

    return accountings


def module_bas_de_page(elements, nb_inches,bas_de_page):

    elements.append(Spacer(0,nb_inches*inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : 903345569"  , bas_de_page )
    elements.append(asso3)
    asso30 = Paragraph( "siret : 903345569 00011"  , bas_de_page )
    elements.append(asso30)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères - FRANCE"  , bas_de_page )
    elements.append(asso4)
    return elements


def module_logo(elements):
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
    logo_tab = [[logo, "Association SacAdo\nhttps://sacado.xyz \nsacado.asso@gmail.com" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5.2*inch ])
    elements.append(logo_tab_tab)
    return elements

def module_style(elements):

    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page_blue = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    title = ParagraphStyle('title', 
                            fontSize=16,                             
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    subtitle = ParagraphStyle('title', 
                            fontSize=14, 
                            textColor=colors.HexColor("#00819f"),
                            )
    mini = ParagraphStyle(name='mini',fontSize=9 )  
    normal = ParagraphStyle(name='normal',fontSize=12,)   
    dateur_style = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style = ParagraphStyle('dateur_style', 
                            fontSize=11, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_mini = ParagraphStyle('dateur_style', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_blue = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            textColor=colors.HexColor("#00819f"),
                            )
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )
    offset = 0 # permet de placer le bas de page
    return sacado , bas_de_page, bas_de_page_blue, title , subtitle , mini , normal , dateur_style , signature_style , signature_style_mini, signature_style_blue , style_cell



#####################################################################################################################################
#####################################################################################################################################
####    statistiques
#####################################################################################################################################
#####################################################################################################################################
@user_passes_test(user_is_board)
def statistiques(request):


    date_start = time_zone_user(request.user) - timedelta(days=7)
    date_stop  = time_zone_user(request.user)

    inscriptions    = User.objects.filter(date_joined__lte=date_stop,date_joined__gt=date_start )
    nb_inscriptions = inscriptions.count()
    nb_students     = inscriptions.filter(user_type=0).count()
    nb_teachers     = inscriptions.filter(user_type=2).count()
    nb_connexions   = Connexion.objects.filter(date__lte=date_stop,date__gt=date_start ).aggregate(nb = Sum('nb'))["nb"]
    nb_answers      = Studentanswer.objects.filter(date__lte= date_stop,date__gt=date_start).count() + Customanswerbystudent.objects.filter(date__lte= date_stop,date__gt=date_start).count() + Writtenanswerbystudent.objects.filter(date__lte= date_stop,date__gt=date_start).count()

    nb_no_get_acces = Teacher.objects.values_list("user_id",flat=True).distinct().filter(user__date_joined__lte=date_stop,user__date_joined__gt=date_start , groups=None).count()

    #################################################################################################################################
    ##### Jour de la semaine étudiée
    #################################################################################################################################
    list_days = [ (time_zone_user(request.user) - timedelta(days=i) ).date() for i in range(7) ]
    run = 0
    string_days ,  sepn ,  sep   = "" , "" ,  "]" 
    nb_inscriptions_string = ""
    nb_students_string     = ""
    nb_teachers_string     = ""
    nb_connexions_string   = ""
    nb_answers_string      = ""

    months = [0,"janvier","février","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","décembre"]
    for d in list_days :
        nbans = Studentanswer.objects.filter(date__startswith = d ).count() + Customanswerbystudent.objects.filter(date__startswith = d ).count() + Writtenanswerbystudent.objects.filter(date__startswith = d ).count()
        if run > 0 and run < 8 : sep, sepn = "," , ","

        y ,  m , day = str(d).split("-")
        this_day = day + " " + months[int(m)] 
        string_days = this_day+sepn+string_days


        nb_inscriptions_string = str(User.objects.filter(date_joined__startswith = d ).count())+sep+nb_inscriptions_string
        nb_students_string     = str(User.objects.filter(date_joined__startswith = d ,user_type=0).count())+sep+nb_students_string
        nb_teachers_string     = str(User.objects.filter(date_joined__startswith = d ,user_type=2).count())+sep+nb_teachers_string
        if Connexion.objects.filter(date__startswith = d ).aggregate(nb = Sum('nb'))["nb"] : nbi = Connexion.objects.filter(date__startswith = d ).aggregate(nb = Sum('nb'))["nb"]
        else : nbi = 0    
        nb_connexions_string   = str(nbi)+sep+nb_connexions_string
        nb_answers_string      = str(nbans)+sep+nb_answers_string
        run += 1


    nb_inscriptions_string = "["+nb_inscriptions_string
    nb_students_string     = "["+nb_students_string
    nb_teachers_string     = "["+nb_teachers_string
    nb_connexions_string   = "["+nb_connexions_string
    nb_answers_string      = "["+nb_answers_string

    ################################################################################################################################# 
    #################################################################################################################################
    countries , all_countries = [] , []
    for u in inscriptions.order_by("country__name") :
        if u.country  and u.country.name not in countries :
            countries.append(u.country.name)
            all_countries.append({'country' : u.country.name , 'nb' : 1})
        elif u.country  :
            idx = countries.index(u.country.name)
            all_countries[idx]['nb'] +=1

    ################################################################################################################################# 
    #################################################################################################################################

    context = { 'string_days' : string_days, 'nb_inscriptions_string' : nb_inscriptions_string ,  'nb_students_string' : nb_students_string ,'nb_teachers_string' : nb_teachers_string ,
                'nb_connexions_string' : nb_connexions_string , 'nb_answers_string' : nb_answers_string , 'nb_inscriptions' : nb_inscriptions, 'nb_teachers' : nb_teachers, 'nb_students' : nb_students,
                'nb_answers': nb_answers , 'nb_connexions': nb_connexions , 'date_start': date_start ,   'date_stop': date_stop , 'all_countries' : all_countries , 'nb_no_get_acces' : nb_no_get_acces   }

    return render(request, 'association/statistiques.html', context) 

#####################################################################################################################################
#####################################################################################################################################
####    payment_accepted from Paypal
#####################################################################################################################################
#####################################################################################################################################

def payment_complete(request):
    body = json.loads(request.body)
 
    Accounting.objects.filter(pk = body['accounting_id']).update(is_active = 1)
    return JsonResponse('Payement completed !', safe = False)


#####################################################################################################################################
#####################################################################################################################################
####    Holidaybook
#####################################################################################################################################
#####################################################################################################################################
@user_passes_test(user_is_board)
def display_holidaybook(request):

    try :
        holidaybook = Holidaybook.objects.get(pk = 1)
        form = HolidaybookForm(request.POST or None, instance = holidaybook )

    except :
        form = HolidaybookForm(request.POST or None )
 
    if request.method == "POST":
        is_display = request.POST.get("is_display")
        if is_display == 'on' :
            is_display = 1
        else :
            is_display = 0 
        holidaybook, created = Holidaybook.objects.get_or_create(pk =  1, defaults={  'is_display' : is_display } )
        if not created :
            holidaybook.is_display = is_display
            holidaybook.save()
        
        return redirect('association_index')
 

    context = {'form': form  }

    return render(request, 'association/form_holidaybook.html', context)

@user_passes_test(user_is_board)
def update_formule(request, id):

    formule = Formule.objects.get(id=id)
    form = FormuleForm(request.POST or None, instance=formule )

    if request.method == "POST":
        if form.is_valid():
            form.save()
        else :
            print(form.errors)
        
        return redirect('list_rates')

    context = {'form': form, 'formule' : formule }

    return render(request, 'association/form_formule.html', context )


@user_passes_test(user_is_board)
def delete_formule(request, id):

    formule = Formule.objects.get(id=id)
    formule.delete()
    return redirect('list_rates')


#####################################################################################################################################
#####################################################################################################################################
####    accounting
#####################################################################################################################################
#####################################################################################################################################

# def school_to_customer():
#     today       = datetime.now()
#     abonnements = Abonnement.objects.values_list('school').distinct()
#     liste=[]
#     for school in abonnements :
#         if not school in liste :
#             liste.append(school)
#             Customer.objects.create(school_id = school[0],status=3 )
@user_passes_test(user_is_board)
def new_customer(request):
 

    if request.method == 'POST' :
        rne = request.POST.get('rne',None)
        if rne :
            this_user_id = request.POST.get('this_user_id',None)

            school = School.objects.filter(code_acad=rne).first()
            c ,cr = Customer.objects.get_or_create(school=school, defaults={ 'user_id' : this_user_id , 'phone' :  "0000000000" , 'status': 2, 'actual' : 1,
                                             'gestion' : 'En direct' , 'date_stop': None,   'date_start_gar': None, 'gar_abonnement_id': "", 'is_display_button': 0 } )

            print(school)
            return redirect('update_school_admin' , school.id)
    context = { }
    return render(request, 'association/new_customer.html', context ) 



@user_passes_test(user_is_board)
def all_schools(request):
 
    customers = Customer.objects.all()
    context = { 'customers': customers }

    return render(request, 'association/all_schools.html', context ) 


@csrf_exempt
def ajax_customer(request):

    status =  request.POST.get("status_id")
    status_tab = status.split("-")  
    Customer.objects.filter(pk=status_tab[1]).update(status=status_tab[0])
    data = {}

    return JsonResponse(data)

@csrf_exempt
def ajax_new_customer(request):

    rne =  request.POST.get("rne")
    school = School.objects.filter(code_acad=rne).first()
    data = {}
    data["html"] = school.name + ", "+school.town+ ", "+school.country.name
    data["users"] = list(school.users.filter(user_type=2).values_list("id",'last_name'))

    return JsonResponse(data)


@user_passes_test(user_is_board) 
def update_school_admin(request,id):

    today    = datetime.now()
    today_time = today -   timedelta(days = 15)
    school = School.objects.get(id=id)
    accountings = school.accountings.order_by("chrono")
    last_accounting = accountings.last()

    form = SchoolForm(request.POST or None, request.FILES  or None, instance=school)

    form_accounting = AccountingForm(request.POST or None )
    formSet  = inlineformset_factory( Accounting , Detail , fields=('accounting','description','amount',) , extra=0)
    form_ds  = formSet(request.POST or None)


    teachers = school.users.filter(user_type=2) 

    nb_total = school.users.filter(user_type=0).count()
    nb = 150
    if nb > nb_total:
        nb = nb_total

 
    customer = school.customer
    status = customer.status
    statusForm =  StatusForm(request.POST or None, instance=customer ) 

    form_abo = CustomAboForm(request.POST or None , instance=customer )   

    if request.POST.get("update_school",None)  :   
        if form.is_valid():
            school = form.save()
            school.is_active = 1
            school.save()
 
    context =  { 'accountings':accountings, 'form':form,  'last_accounting' : last_accounting ,'school':school ,'nb':nb ,'nb_total':nb_total ,
                 'customer' : customer , 'teachers' : teachers , 'status' : status ,'form_abo' : form_abo ,'statusForm' : statusForm ,
                 'form_accounting' : form_accounting , "form_abo" : form_abo , 'form_ds' : form_ds , 'school' : school , 
                 }
    return render(request,'association/update_school_admin.html' ,context )


@user_passes_test(user_is_board)
def customer_payment_from_modal(request,idc):

    customer = Customer.objects.get(pk=idc)
    today    = date.today()
    form_abo = CustomAboForm(request.POST or None , instance=customer )   
    if request.method == "POST"  :  
        if form_abo.is_valid():
            fa = form_abo.save(commit = False)
            if fa.actual == 1 :
                fa.status = 3 
            else :
                fa.status = 2
            if fa.school.gar: # appel de la fonction qui valide le Web Service
                if not customer.gar_abonnement_id :
                    test, raison , header , decode , ida = create_abonnement_gar( today , fa  , request.user )
                    if test :
                        fa.gar_abonnement_id = ida
                        messages.success(request,"Abonnement réussi. Activation du GAR réussie")
                    else :
                        messages.error(request,"Activation du GAR échouée..... Raison : {} \n\nHeader : {}\n\nDécodage : {} ".format(raison, header , decode ))
                else :
                    test, raison , header , decode , ida = update_abonnement_gar(  today , fa  )
                    if test :
                        messages.success(request,"Abonnement réussi. Modification du GAR réussie")
                    else :
                        messages.error(request,"Modification du GAR échouée..... Raison : {} \n\nHeader : {}\n\nDécodage : {} ".format(raison, header , decode ))

            else :
                messages.success(request,"Abonnement réussi. Le GAR n'est pas demandé.")
            
            fa.save()
        else :
            print(fa.errors) 
    return redirect("update_school_admin" , customer.school.id )




@user_passes_test(user_is_board)
def paiement_abonnement(request,idc):
    

    aid = request.POST.get('accounting_id')
    date_payment = request.POST.get('date_payment')

    customer =  Customer.objects.get(pk=idc)
    customer.date_payment = date_payment
    customer.status = 3
    customer.save()

    accounting = Accounting.objects.get(pk=aid)
    accounting.amount = customer.school.fee()
    accounting.date_payment = date_payment
    accounting.save()

    messages.success(request,"Modification du paiement réussi.")

    return redirect("update_school_admin" , customer.school.id )






@user_passes_test(user_is_board)
def association_index(request):

    today_start  = datetime.date(datetime.now())
    nb_teachers  = Teacher.objects.all().count()
    nb_students  = Student.objects.all().count()#.exclude(user__username__contains="_e-test_")
    nb_exercises = Exercise.objects.filter(supportfile__is_title=0).count()

    nb_schools   = Customer.objects.filter(status=3).count()

    months       = [1,2,3,4,5,6,7,8,9,10,11,12]
    days         = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_start  = today_start.month
    list_months  = months[month_start:12] + months[0:month_start]

    list_reals   = []
    for i in range(month_start,13+month_start) :
        list_reals.append(i)

    year   = today_start.year -1

    string = ""
    somme = 0
    run = 0
    for m in list_reals :        
        if m > 12 :
            year = today_start.year
            m = m-12
        sep = ""
        if run > 0 and run < 13 :
            sep = ","
        date_start   = datetime(year,m,1,0,0,0)
        date_stop    = datetime(year,m,days[m-1],23,59,59)

        n = Teacher.objects.filter(user__date_joined__lte=date_stop, user__date_joined__gte=date_start ).count()
        string += sep+str(n)
        somme += n
        run += 1


    nb_answers   = Studentanswer.objects.filter(date__gte= today_start).count() + Customanswerbystudent.objects.filter(date__gte= today_start).count() + Writtenanswerbystudent.objects.filter(date__gte= today_start).count()
    if Holidaybook.objects.all() :
        holidaybook  = Holidaybook.objects.values("is_display").get(pk=1)
    else :
        holidaybook = False


    customers_pending = Customer.objects.filter(status=0)

    active_year, this_year = get_active_year()

    context = { 'nb_teachers': nb_teachers , 'nb_students': nb_students , 'nb_exercises': nb_exercises, 'customers_pending' : customers_pending , 
                'nb_schools': nb_schools, 'nb_answers': nb_answers, 'holidaybook': holidaybook ,
                'list_months': list_months, 'string': string,  'month_start' : month_start , 'active_year' : active_year ,
                }

    return render(request, 'association/dashboard.html', context )



def customers_pending(request) :

    customers_pending = Customer.objects.filter(status=0)



    context = {  'customers_pending' : customers_pending   }

    return render(request, 'association/customers_pending.html', context )







@user_passes_test(user_is_board)
def create_activeyear(request):

    form       = ActiveyearForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        else :
            print(form.errors)
        
        return redirect('activeyears')

    return render(request, 'association/form_activeyear.html', {'form': form     })



@user_passes_test(user_is_board)
def update_activeyear(request,id):

    activeyear = Activeyear.objects.get(pk=id)
    form       = ActiveyearForm(request.POST or None , request.FILES or None , instance = activeyear)
 

    if request.method == "POST":
        if form.is_valid():
            form.save()
        else :
            print(form.errors)
        
        return redirect('activeyears')

    return render(request, 'association/form_activeyear.html', {'form': form     })


@user_passes_test(user_is_board)
def activeyears(request):

    years = Activeyear.objects.all()

    return render(request, 'association/list_activeyear.html', { 'years' :years   })



def total(first_date, last_date) :

    accountings =  Accounting.objects.filter(date_payment__gte=first_date, date_payment__lte=last_date).exclude(date_payment=None)
    total_amount = 0
    total_amount_active = 0
    for a in accountings :
        if a.is_credit :
            total_amount += a.amount
        else :
            total_amount -= a.amount
    return total_amount



@user_passes_test(user_is_board)
def adhesions(request):

    today = datetime.now()
    this_month = today.month
    this_year = today.year
    activeyear, year = get_active_year()
    first_date_month =  datetime(year, this_month, 1)
    first_date_year  = datetime(year, 1, 1)

    if this_month > 0 and this_month < 9 :
        this_year = this_year - 1
    first_date_schoolyear = datetime(year, 9, 1)

    total_month = total(first_date_month, today)
    total_year = total(first_date_year, today)
    total_shoolyear =  total(first_date_schoolyear, today)

    date_start = datetime(year, 8, 31)
    date_stop  = datetime(year+1, 8, 31)

    customers = Customer.objects.filter(status=3)

    context =  {'customers': customers , 'total_month': total_month, 'total_year': total_year, 'total_shoolyear': total_shoolyear ,'this_month' :this_month, 'activeyear' : activeyear ,'title_page' : 'abonnés' }
 
    return render(request, 'association/adhesions.html', context )




@user_passes_test(user_is_board)
def list_paypal(request):

    active_year, this_year    = get_active_year() 
    accountings = Accounting.objects.filter(is_paypal=1).exclude(date_payment=None)
    accounting_no_payment,  accounting_amount = 0, 0
    pay_accountings = accountings.exclude(date_payment=None)
    no_accountings = accountings.filter(date_payment=None)

    for a in pay_accountings :
        accounting_amount += a.amount
    for a in no_accountings :
        accounting_no_payment += a.amount


    active_year, this_year = get_active_year() # active_year = 2020-2021 ALORS QUE this_year est 2020
    today = datetime.now()
    this_month = today.month

    first_date_month =  datetime(this_year, this_month, 1)

    if this_month > 0 and this_month < 9 :
        this_year = this_year - 1
    first_date_schoolyear = datetime(this_year, 5, 1) ##### A CHANGER  

    total_month     = total(first_date_month, today)
    total_shoolyear = total(first_date_schoolyear, today)

    return render(request, 'association/list_accounting.html', { 'accounting_amount':accounting_amount,  'accounting_no_payment' : accounting_no_payment   , 'accountings': accountings ,  'active_year' : active_year ,  'tp' : 3 , 'total_month': total_month,  'total_shoolyear': total_shoolyear ,'this_month' :this_month })



@user_passes_test(user_is_board)
def bank_activities(request):
    context = { }

    return render(request, 'association/bank_activities.html', context )



@user_passes_test(user_is_board)
def calcule_bank_bilan(request):
    """ page d'accueil de la comptabilité"""

 
    this_year     = Activeyear.objects.get(is_active=1).year  
    plan_sale     = Plancomptable.objects.filter(code__gte=700,code__lt=800).order_by("code")
    plan_purchase = Plancomptable.objects.filter(code__gte=600,code__lt=700 ).order_by("code")
    plan_immo     = Plancomptable.objects.filter(code__in= [411,486,5121,5122] ).order_by("code")
    plan_resultat = Plancomptable.objects.filter(code__in=[110, 487] )

    my_dico = {}
    list_sales , list_purchases,plan_immos , plan_resultats = [] , [] , [] , []

    charges, products   = 0 , 0  
    for p in plan_sale :
        my_dico = {}
        accountings_sales = Accountancy.objects.filter(current_year = this_year  ,  plan_id = p.code   ).aggregate(Sum('amount'))
        my_dico["code"] = p.code 
        my_dico["name"] = p.name
        my_dico["solde"]= accountings_sales["amount__sum"]
        try :
            products +=accountings_sales["amount__sum"]
        except :
            pass
        list_sales.append( my_dico )


    for p in plan_purchase :
        my_dico = {}
        accountings_sales = Accountancy.objects.filter(current_year = this_year  ,  plan_id = p.code   ).aggregate(Sum('amount'))
        my_dico["code"] = p.code 
        my_dico["name"] = p.name
        my_dico["solde"]= accountings_sales["amount__sum"]
        try :
            charges +=accountings_sales["amount__sum"]
        except :
            pass
        list_purchases.append( my_dico )

    cs, ps   = 0 , 0 
 
    for p in plan_immo :
        my_dico = {}
        
        if p.code ==411 :

            my_dico = {}
            accountings_sales_debit = Accountancy.objects.filter(current_year = this_year  ,  plan_id = p.code, is_credit=1   ).aggregate(Sum('amount'))
            accountings_sales_credit = Accountancy.objects.filter(current_year = this_year  ,  plan_id = p.code, is_credit=0   ).aggregate(Sum('amount'))
            my_dico["code"] = p.code 
            my_dico["name"] = p.name
            try :
                solde = accountings_sales_credit["amount__sum"] - accountings_sales_debit["amount__sum"]
            except :
                solde = accountings_sales_credit["amount__sum"]
                
            my_dico["solde"]= solde

            if p.code > 5000 :
                try :
                    my_dico["solde"]= solde
                except :
                    pass
                try :
                    cs -= solde
                except :
                    pass
            else :
                my_dico["solde"]= solde
                try :
                    cs += solde
                except :
                    pass
            plan_immos.append( my_dico )


        else : 
            accountings_sales = Accountancy.objects.filter(current_year = this_year  ,  plan_id = p.code    ).aggregate(Sum('amount'))
            my_dico["code"] = p.code
            my_dico["name"] = p.name
            if p.code > 5000 :
                try :
                    my_dico["solde"]= -accountings_sales["amount__sum"]
                except :
                    pass
                try :
                    cs -= accountings_sales["amount__sum"]
                except :
                    pass
            else :
                my_dico["solde"]= accountings_sales["amount__sum"]
                try :
                    cs += accountings_sales["amount__sum"]
                except :
                    pass
            plan_immos.append( my_dico )


    for p in plan_resultat :
        my_dico = {}
        accountings_sales = Accountancy.objects.filter(current_year = this_year  ,  plan_id = p.code   ).aggregate(Sum('amount'))
        my_dico["code"] = p.code 
        my_dico["name"] = p.name
        my_dico["solde"]= accountings_sales["amount__sum"]
        try :
            ps += accountings_sales["amount__sum"]
        except :
            pass
        plan_resultats.append( my_dico )

    results = products - charges
    rs =  cs - ps


    return list_sales ,  list_purchases ,  plan_resultats ,  plan_immos , results , products , charges, rs , ps , cs   



@user_passes_test(user_is_board)
def bank_bilan(request):

    list_sales ,  list_purchases ,  plan_resultats ,  plan_immos , results , products , charges, rs , ps , cs   = calcule_bank_bilan(request)

    context = {  'list_sales' : list_sales ,  'list_purchases' : list_purchases ,  'plan_resultats' :  plan_resultats ,  'plan_immos' : plan_immos ,  'results' : results ,  'products' : products ,  'charges' :  charges ,  'rs' : rs  , 'ps' : ps, 'cs' : cs }  

    return render(request, 'association/bank_bilan.html', context )   

 
@user_passes_test(user_is_board)
def print_bank_bilan(request):

    list_sales ,  list_purchases ,  plan_resultats ,  plan_immos , results , products , charges, rs , ps , cs = calcule_bank_bilan(request)
    year_active = Activeyear.objects.get(is_active=1)
    #########################################################################################
    ### Instanciation
    #########################################################################################
    elements = []        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Compte_resultat_'+str(year_active.year)+'.pdf"'
    doc = SimpleDocTemplate(response,   pagesize=(landscape(letter)), 
                                        topMargin=0.5*inch,
                                        leftMargin=0.5*inch,
                                        rightMargin=0.5*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()
    OFFSET_INIT = 0.2
    #########################################################################################
    ### Style
    #########################################################################################
    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page_blue = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    title = ParagraphStyle('title', 
                            fontSize=16,                             
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    subtitle = ParagraphStyle('title', 
                            fontSize=14, 
                            textColor=colors.HexColor("#00819f"),
                            )
    mini = ParagraphStyle(name='mini',fontSize=9 )  
    normal = ParagraphStyle(name='normal',fontSize=12,)   
    dateur_style = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style = ParagraphStyle('dateur_style', 
                            fontSize=11, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_mini = ParagraphStyle('dateur_style', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_blue = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            textColor=colors.HexColor("#00819f"),
                            )
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )
    offset = 0 # permet de placer le bas de page
    return sacado , bas_de_page, bas_de_page_blue, title , subtitle , mini , normal , dateur_style , signature_style , signature_style_mini, signature_style_blue , style_cell


    #########################################################################################
    ### Logo Sacado
    #########################################################################################
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
    logo_tab = [[logo, "Association SacAdo\nhttps://sacado.xyz \nsacado.asso@gmail.com" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5.2*inch ])
    elements.append(logo_tab_tab)
    #########################################################################################
    ### Facture
    #########################################################################################
    elements.append(Spacer(0,0.3*inch))
    f = Paragraph( "Compte de résultat" , sacado )
    elements.append(f) 
    elements.append(Spacer(0,0.1*inch))
    fa = Paragraph( "Résultat : " + str(cr) + " €" , title )
    elements.append(fa) 
    details_list_sales , details_list_purchases = [] , [] 
    #########################################################################################
    ### Details_list_purchases
    #########################################################################################
    for a in accountings_list_purchases :
        if str(a["solde"]) != "0" :
            details_list_purchases.append(    ( str(a["code"])+". "+ str(a["name"]) , str(a["solde"])  )    )
           
    details_table_purchases = Table(details_list_purchases, hAlign='LEFT', colWidths=[4.2*inch,0.8*inch])
    details_table_purchases.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))
               ]))


    #########################################################################################
    ### Accountings_list_sales
    #########################################################################################
    for a in accountings_list_sales :
        if str(a["solde"]) != "0" :
            details_list_sales.append(  ( str(a["code"]) +". "+ str(a["name"]) , str(a["solde"])  )    )
           
    details_table_sales = Table(details_list_sales, hAlign='LEFT', colWidths=[4.2*inch,0.8*inch])
    details_table_sales.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))
               ]))

    #########################################################################################
    ### A mettre sur 2 colonnes
    #########################################################################################

    elements.append(Spacer(0,0.3*inch))
    g = Paragraph( "Charges : " + str(accountings_purchase) +"€", subtitle )
    elements.append(g)    
    elements.append(Spacer(0,0.1*inch))
    elements.append(details_table_purchases)

    elements.append(Spacer(0,0.3*inch))
    h = Paragraph( "Produits: " +str(accountings_sale) +"€" , subtitle )
    elements.append(h) 
    elements.append(Spacer(0,0.1*inch))
    elements.append(details_table_sales)
    #########################################################################################
    ### Bilan  
    #########################################################################################

    elements.append(Spacer(0,0.3*inch))
    b = Paragraph( "Bilan" , sacado )
    elements.append(b) 
 

    #########################################################################################
    ### Bilan actif
    #########################################################################################
    elements.append(Spacer(0,0.3*inch))
    actif = Paragraph( "Actif"  , subtitle )
    elements.append(actif)  
    elements.append(Spacer(0,0.1*inch))
    accountings_list_qc = [ ("411. Client", a_411 ) , ("411. Banque CA", accountings_ca ) , ("411. Banque Paypal", accountings_paypal )   ]

           
    accountings_list_qc_ = Table(accountings_list_qc, hAlign='LEFT', colWidths=[4.2*inch,0.8*inch])
    accountings_list_qc_.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))
               ]))
    elements.append(accountings_list_qc_)             

    #########################################################################################
    ### Bilan passif
    #########################################################################################

 
    elements.append(Spacer(0,0.3*inch))
    actif = Paragraph( "Passif"  , subtitle )
    elements.append(actif)  
    elements.append(Spacer(0,0.1*inch))
    accountings_list_qc = [ ("487 . Clients produits constatés d'avance", cpca["amount__sum"] ) , ( " Résultat", crf )   ]

           
    accountings_list_qc_ = Table(accountings_list_qc, hAlign='LEFT', colWidths=[4.2*inch,0.8*inch])
    accountings_list_qc_.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))
               ]))
    elements.append(accountings_list_qc_)  
    #########################################################################################
    ### Bas de page
    #########################################################################################
    nb_inches = 4.4 - offset
    elements.append(Spacer(0,nb_inches*inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : 903345569"  , bas_de_page )
    elements.append(asso3)
    asso30 = Paragraph( "siret : 903345569 00011"  , bas_de_page )
    elements.append(asso30)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères - FRANCE"  , bas_de_page )
    elements.append(asso4)


    doc.build(elements)

    return response    

@user_passes_test(user_is_board)
def print_balance(request):

    
 
    list_sales ,  list_purchases ,  plan_resultats ,  plan_immos , results , products , charges, rs , ps , cs = calcule_bank_bilan(request)
    year_active = Activeyear.objects.get(is_active=1)
    #########################################################################################
    ### Instanciation
    #########################################################################################
    elements = []        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Compte_Balance_Résultat_'+str(year_active.year)+'.pdf"'
    doc = SimpleDocTemplate(response,   pagesize=(landscape(letter)), 
                                        topMargin=0.5*inch,
                                        leftMargin=0.5*inch,
                                        rightMargin=0.5*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()
    OFFSET_INIT = 0.2
    #########################################################################################
    ### Style
    #########################################################################################
    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page_blue = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    title = ParagraphStyle('title', 
                            fontSize=16,                             
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    subtitle = ParagraphStyle('title', 
                            fontSize=14, 
                            textColor=colors.HexColor("#00819f"),
                            )
    mini = ParagraphStyle(name='mini',fontSize=9 )  
    normal = ParagraphStyle(name='normal',fontSize=12,)   
    dateur_style = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style = ParagraphStyle('dateur_style', 
                            fontSize=11, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_mini = ParagraphStyle('dateur_style', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_blue = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            textColor=colors.HexColor("#00819f"),
                            )
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ])
    offset = 0 # permet de placer le bas de page



    #########################################################################################
    ### Logo Sacado
    #########################################################################################
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
    logo_tab = [[logo, "Association SacAdo\nhttps://sacado.xyz \nsacado.asso@gmail.com" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5.2*inch ])
    elements.append(logo_tab_tab)
    #########################################################################################
    ### Facture
    #########################################################################################
    elements.append(Spacer(0,0.3*inch))
    f = Paragraph( "Balance" , sacado )
    elements.append(f) 
    elements.append(Spacer(0,0.1*inch))
    fa = Paragraph( str(year_active.year) +" " + str(year_active.year +1)  , title )
    elements.append(fa) 
    elements.append(Spacer(0,0.3*inch))

    #########################################################################################
    ### Details_list_purchases
    #########################################################################################
    plan = Plancomptable.objects.order_by("code")

    for p in plan :
        paragraph = Paragraph( str(p.code) +". "+ p.name , subtitle )
        details_list  = [(   "Débit","Crédit" , "Solde")] 
        p_code = p.code
        accountancies = Accountancy.objects.filter(plan_id=p_code)
        i = 1
        a_debit , a_credit = 0 , 0
        for a in accountancies :
            if a. is_credit:
                a_credit +=  a.amount
            else :
                a_debit +=  a.amount 
            i+=1
        if p_code > 5000 : 
            solde = abs(a_debit) - abs(a_credit) # les débits sont en négatifs
        elif p_code == 411 : 
            solde =   abs(a_debit) - abs(a_credit)
        else :
            solde =  abs(a_credit) - abs(a_debit) # les débits sont en négatifs

        if solde:
            solde =  abs(solde)
            elements.append(paragraph)
            elements.append(Spacer(0, 0.15*inch))
            details_list.append(   (   str( abs(a_debit ))+ " €" , str(a_credit)+ " €" ,  str(solde) + " €" )    )
     
            ##########################################################################
            ####  
            ##########################################################################
            details_tabs = [ ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray)  ,  ('BOX', (0,0), (-1,-1), 0.25, colors.gray)  ,   ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))  ]
            details_listing = Table(details_list, hAlign='LEFT', colWidths=[  1.2*inch,1.2*inch,1.2*inch])
            details_listing.setStyle(TableStyle(  details_tabs   ))
            elements.append(details_listing) 


    #########################################################################################
    ### Bas de page
    #########################################################################################

    elements.append(Spacer(0,inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : 903345569"  , bas_de_page )
    elements.append(asso3)
    asso30 = Paragraph( "siret : 903345569 00011"  , bas_de_page )
    elements.append(asso30)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères - FRANCE"  , bas_de_page )
    elements.append(asso4)
    doc.build(elements)

    return response 




@user_passes_test(user_is_board)
def create_accountancy(request):
    form = AccountancyForm(request.POST or None )
    plan = Plancomptable.objects.order_by("code")

    if request.method == "POST":    
        date = request.POST.get("date")
        year = date.split("-")[0]
        plan_id_c = request.POST.get("plan_id_c",None)
        plan_id_d = request.POST.get("plan_id_d",None)
        amount = request.POST.get("amount",None)
        Accountancy.objects.create(accounting_id = 0 , ranking = 2 , plan_id = int(plan_id_c) , is_credit = 1, amount = float(amount)  , current_year = year )             
        Accountancy.objects.create(accounting_id = 0 , ranking = 1 , plan_id = int(plan_id_d) , is_credit = 0, amount = -float(amount) , current_year = year )  
        return redirect('list_accountancy')

    return render(request, 'association/form_accountancy.html' , {'form': form , 'plan': plan })


 

@user_passes_test(user_is_board)
def list_accountancy(request):
    years = Activeyear.objects.all()
    # if request.method=='POST' :
    #     year_id = int(request.POST.get('this_year_id'))
    #     for a in years :
    #         a.is_active=0
    #         a.save()
    #     Activeyear.objects.filter(pk=year_id).update(is_active=1)
    #     ay = Activeyear.objects.get(pk=year_id)
    #     ay.is_active=1
    #     ay.save()
    #     year = ay.year
    #     messages.success(request,"L'année de visualisation est modifiée. L'année active est "+str(year)+"-"+str(year+1))
    # else :
    year    = Activeyear.objects.get(is_active=1)
    year_id = year.id
    #accontancies = Accountancy.objects.filter(current_year=year.year)
    accontancies = Accountancy.objects.filter(id__gte=1217).order_by("-id")
    return render(request, 'association/list_accountancy.html', {'accontancies' : accontancies , 'years' : years ,'year_id' : year_id })


 

@user_passes_test(user_is_board)
def print_big_book(request):
 
    list_sales ,  list_purchases ,  plan_resultats ,  plan_immos , results , products , charges, rs , ps , cs = calcule_bank_bilan(request)
    year_active = Activeyear.objects.get(is_active=1)
    #########################################################################################
    ### Instanciation
    #########################################################################################
    elements = []        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Compte_GrandLivre_resultat_'+str(year_active.year)+'.pdf"'
    doc = SimpleDocTemplate(response,   pagesize=(landscape(letter)), 
                                        topMargin=0.5*inch,
                                        leftMargin=0.5*inch,
                                        rightMargin=0.5*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()
    OFFSET_INIT = 0.2
    #########################################################################################
    ### Style
    #########################################################################################
    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page_blue = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    title = ParagraphStyle('title', 
                            fontSize=16,                             
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    subtitle = ParagraphStyle('title', 
                            fontSize=14, 
                            textColor=colors.HexColor("#00819f"),
                            )
    mini = ParagraphStyle(name='mini',fontSize=9 )  
    normal = ParagraphStyle(name='normal',fontSize=12,)   
    dateur_style = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style = ParagraphStyle('dateur_style', 
                            fontSize=11, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_mini = ParagraphStyle('dateur_style', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_blue = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            textColor=colors.HexColor("#00819f"),
                            )
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ])
    offset = 0 # permet de placer le bas de page



    #########################################################################################
    ### Logo Sacado
    #########################################################################################
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
    logo_tab = [[logo, "Association SacAdo\nhttps://sacado.xyz \nsacado.asso@gmail.com" ]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5.2*inch ])
    elements.append(logo_tab_tab)
    #########################################################################################
    ### Facture
    #########################################################################################
    elements.append(Spacer(0,0.3*inch))
    f = Paragraph( "Grand livre de compte" , sacado )
    elements.append(f) 
    elements.append(Spacer(0,0.1*inch))
    fa = Paragraph( str(year_active.year) +" " + str(year_active.year +1)  , title )
    elements.append(fa) 
    elements.append(Spacer(0,0.3*inch))

    #########################################################################################
    ### Details_list_purchases
    #########################################################################################
    plan = Plancomptable.objects.order_by("code")

    for p in plan :
        paragraph = Paragraph( str(p.code)+". "+ p.name , subtitle )
        details_list  = [(" "," ","Date","Id journal","Débit","Crédit")] 
        p_code = p.code
        accountancies = Accountancy.objects.filter(plan_id=p_code)
        i = 1
        a_debit , a_credit = 0 , 0
        for a in accountancies :
            if a. is_credit:
                details_list.append(   (i ,  str(a.plan_id)  , a.date.strftime("%d %m %Y")    , a.id , " " , str(abs(a.amount))+ " €" )    )
                a_credit +=  a.amount
            else :
                details_list.append(  ( i ,str(a.plan_id)  , a.date.strftime("%d %m %Y")    ,  a.id ,  str(abs(a.amount)) + " €", " ")    )
                a_debit +=  a.amount 
            i+=1 
        if p.code > 5000 :
            solde =  -(a_credit + a_debit) # les débits sont en négatifs
        elif p.code == 411 : 
            solde =  a_debit - a_credit 
        else : 
            solde =  a_credit + a_debit # les débits sont en négatifs

        if solde :
            elements.append(paragraph)
            elements.append(Spacer(0, 0.15*inch))
            details_list.append(   ( "" , ""  ,   "", "Soldes"    , str( abs(a_debit ))+ " €" , str(a_credit)+ " €" )    )
            details_list.append(   ( "" ,  ""    , " " ,  "Résultat"   ,  str(solde) + " €" , " " )    )
            ##########################################################################
            ####  
            ##########################################################################
            details_tabs = [ ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray)  ,  ('BOX', (0,0), (-1,-1), 0.25, colors.gray)  ,   ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))  ]
            details_listing = Table(details_list, hAlign='LEFT', colWidths=[  0.9*inch,  0.9*inch, inch,1.2*inch,1.2*inch,1.2*inch])
            details_listing.setStyle(TableStyle(  details_tabs   ))
          
            elements.append(details_listing) 

    #########################################################################################
    ### Bas de page
    #########################################################################################

    elements.append(Spacer(0,inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : 903345569"  , bas_de_page )
    elements.append(asso3)
    asso30 = Paragraph( "siret : 903345569 00011"  , bas_de_page )
    elements.append(asso30)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères - FRANCE"  , bas_de_page )
    elements.append(asso4)
    doc.build(elements)

    return response 




@user_passes_test(user_is_board)
def archive_accountancy(request):
    pass

 

 






@user_passes_test(user_is_board)
def accountings(request):
    """ page d'accueil de la comptabilité"""

    abonnements = get_active_abonnements(request.user)

    nb_schools        = abonnements.count()
    nb_schools_fr     = abonnements.filter(school__country_id = 5).count()
    nb_schools_no_fr  = abonnements.exclude(school__country_id =5).count() 
    nb_schools_no_pay = get_pending_abonnements(request.user).count()

 
    active_year, this_year    = get_active_year() 
 

    product , charge , actif  , commission_paypal, result_bank , result_paypal = 0 , 0 , 0 , 0 , 0 , 0
    accountings   = get_accountings(request.user).values_list("amount","is_credit","date_payment","objet","is_paypal") 


    charges_list = list()
    for a in accountings :
        if a[1] and a[2] != None and a[4] == 0: #Crédit encaissé en banque non paypal
            actif += a[0]
        elif a[1] and a[2] == None and a[4] == 0: #Crédit en attente non paypal
            product += a[0] 
        elif a[1]  and a[4] == 1: #Crédit encaissé en banque paypal
            result_paypal += a[0]
        elif a[1] == 0  and a[4] == 1: #Débit commission paypal
            commission_paypal += a[0]
        elif a[1] == 0 and a[4] == 0: #débit non paypal
            dico    = dict()
            dico["objet"]  = a[3]
            dico["amount"] = a[0]
            charges_list.append(dico)
            charge += abs(a[0])

    actif += result_paypal
    result       = actif - charge
    total        = actif + product

    today = datetime.now()

        
    context = { 'today' : today , 'charge': charge, 'product': product , 'result': result , 'actif': actif , 'total': total , 'result_paypal' : result_paypal ,  'nb_schools': nb_schools , 'abonnements': abonnements , 'charges_list' : charges_list ,
                'this_year' : this_year , 'active_year' : active_year , 'nb_schools': nb_schools , 'nb_schools_fr': nb_schools_fr , 'nb_schools_no_fr': nb_schools_no_fr ,  'nb_schools_no_pay': nb_schools_no_pay , 'commission_paypal' : commission_paypal }  



    return render(request, 'association/accountings.html', context )



def accounting_to_accountancy(request) :

    # Journal client
    active_year, this_year    = get_active_year() 
    accountings = Accounting.objects.filter(plan=18).exclude(date_payment=None)
    for accounting in accountings :
        is_credit1 = 0
        is_credit2 = 1
        if accounting.is_paypal : paypal = 5122
        else : paypal = 5121

        Accountancy.objects.create(accounting_id = accounting.id , ranking = 1 , plan_id = 411 , is_credit = 0, amount = -accounting.amount , current_year = this_year )  
        Accountancy.objects.create(accounting_id = accounting.id , ranking = 2 , plan_id = 706 , is_credit = 1, amount = accounting.amount  , current_year = this_year )  

        Accountancy.objects.create(accounting_id = accounting.id , ranking = 3 , plan_id = 411 , is_credit = 1, amount = accounting.amount , current_year = this_year  )  
        Accountancy.objects.create(accounting_id = accounting.id , ranking = 4 , plan_id = paypal , is_credit = 0, amount = -accounting.amount , current_year = this_year  ) 


    accountings = Accounting.objects.filter(plan=18,date_payment=None)
    for accounting in accountings :

        if accounting.amount >= 0 :
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 1 , plan_id = 411 , is_credit = 0, amount = accounting.amount , current_year = this_year  )  
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 2 , plan_id = 706 , is_credit = 1, amount = accounting.amount , current_year = this_year  ) 

        else : 
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 1 , plan_id = 411 , is_credit = 1, amount = accounting.amount , current_year = this_year  )  
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 2 , plan_id = 706 , is_credit = 0, amount = accounting.amount , current_year = this_year  )

    # Journal bancaire
    accountings = Accounting.objects.exclude(plan=18) 
    for accounting in accountings :
        amount = accounting.amount
        if accounting.is_paypal : paypal = 5122
        else : paypal = 5121


        if accounting.is_credit :
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 1 , plan_id = accounting.plan.code , is_credit = 1, amount = amount  , current_year = this_year )  
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 2 , plan_id = paypal , is_credit = 0, amount = amount , current_year = this_year  ) 

        else :
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 1 , plan_id = accounting.plan.code , is_credit = 0, amount = amount  , current_year = this_year )  
            Accountancy.objects.create(accounting_id = accounting.id , ranking = 2 , plan_id = paypal , is_credit = 1, amount = amount , current_year = this_year  )  

    return redirect('bank_bilan')
 


@user_passes_test(user_is_board)
def list_accountings(request,tp):

    active_year, this_year    = get_active_year() 
 

    # if tp == 0 :
    #     accountings = get_accountings(request.user).filter(plan__code__gte=700)
    # elif  tp == 1 :
    #     accountings = get_accountings(request.user).filter(plan__code__gte=600, plan__code__lt=700 )
    # else :
    #     accountings = get_accountings(request.user).exclude(is_paypal=1).exclude(date_payment=None)

    if tp == 0 :
        accountings = Accounting.objects.filter(plan__code__gte=700)
    elif  tp == 1 :
        accountings = Accounting.objects.filter(plan__code__gte=600, plan__code__lt=700 )
    else :
        accountings = Accounting.objects.exclude(is_paypal=1).exclude(date_payment=None)

    accounting_no_payment,  accounting_amount = 0, 0
    accountings_no_payments = accountings.filter(date_payment=None)

    for a in accountings :
        accounting_amount += a.amount
 
    for a in accountings_no_payments :
        accounting_no_payment += a.amount


    active_year, this_year = get_active_year() # active_year = 2020-2021 ALORS QUE this_year est 2020
    today = datetime.now()
    this_month = today.month

    first_date_month =  datetime(this_year, this_month, 1)

    if this_month > 0 and this_month < 9 :
        this_year = this_year - 1
    first_date_schoolyear = datetime(this_year, 1, 1) ##### A CHANGER  

    total_month     = total(first_date_month, today)
    total_shoolyear = total(first_date_schoolyear, today)

    return render(request, 'association/list_accounting.html', { 'accounting_amount':accounting_amount,  'accounting_no_payment' : accounting_no_payment   , 'accountings': accountings ,  'active_year' : active_year ,  'tp' : tp , 'total_month': total_month,  'total_shoolyear': total_shoolyear ,'this_month' :this_month })





@user_passes_test(user_is_board)
def ajax_total_month(request):
    data = {}
    month = int(request.POST.get("month"))

    today = datetime.now()
    active_year, this_year = get_active_year() # active_year = 2020-2021 ALORS QUE this_year est 2020
    first = datetime(this_year, month, 1)
    nb_days=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    first = datetime(this_year, month, 1)
    last = datetime(this_year, month, nb_days[month])


    data['html'] = "<label><b>"+str(total(first, last)).replace(".",",")+" € </b></label>"
    rows = Accounting.objects.values_list("id", flat = True).filter(date_payment__lte=last, date_payment__gte=first).exclude(date_payment=None)
    data['rows'] = list(rows)
    data['len']  = len(list(rows))
    return JsonResponse(data)


def str_to_date(date_str):
    dtab = date_str.split("-")
    m = str(dtab[1]).replace("0","")
    return datetime( int(dtab[0]) , int(dtab[1]) , int(dtab[2]) )



@user_passes_test(user_is_board)
def ajax_total_period(request):
    data = {}
    from_date = request.POST.get("from_date",None)
    to_date   = request.POST.get("to_date",None)

    if from_date and to_date :
        from_date = str_to_date(from_date)
        to_date = str_to_date(to_date)

        rows = Accounting.objects.values_list("id", flat = True).filter(date_payment__lte=to_date,date_payment__gte=from_date).exclude(date_payment=None)
        data['rows'] = list(rows)
        data['html'] = str(total(from_date, to_date)) +" €"
        data['len']  = len(list(rows))
    else :
        data['html'] = "Sélectionner deux dates"
        data['rows'] = False
        data['len']  = 0
    return JsonResponse(data)






@user_passes_test(user_is_board) 
def create_accounting(request,tp,ids):
 
    form     = AccountingForm(request.POST or None )
    formSet  = inlineformset_factory( Accounting , Detail , fields=('accounting','description','amount',) , extra=0)
    form_ds  = formSet(request.POST or None)
    today    = datetime.now()

    if ids > 0 :
        school = School.objects.get(pk=ids)
    else :
        school = None

    if tp == 0 :
        template = 'association/form_accounting.html'
    elif tp == 1 :
        template = 'association/form_accounting_depense.html'   
    else :
        template = 'association/form_accounting_bank.html'


    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.user = request.user
            nf.school = school
            forme = request.POST.get("forme",None)
            nf.chrono = str(uuid.uuid4())[:5]
            nf.is_active = 1
            if tp == 0 : 
                nf.chrono = create_chrono(Accounting, forme) # Create_chrono dans general_functions.py
            nf.tp = tp
            if tp == 0 :
                nf.plan_id = 18
                if forme == "FACTURE" :
                    nf.is_credit = 1
                else :
                    nf.is_credit = 0
            elif tp == 1 :
                if forme == "AVOIR" :
                    nf.is_credit = 0 
                else :
                    nf.is_credit = 1 
            else :
                nf.date_payment = today
            nf.save()


            form_ds = formSet(request.POST or None, instance = nf)
            for form_d in form_ds :
                if form_d.is_valid():
                    form_d.save()

            som = 0         
            details = nf.details.all()
            for d in details :
                som += d.amount

            active_year, this_year = get_active_year()


            if  tp == 1 :
                am =-som 
            else :
                am = som
            Accounting.objects.filter(pk = nf.id).update(amount=am)
            try :
                Accounting.objects.filter(pk = nf.id).update(country=nf.school.country)
            except :
                pass

            if tp == 0 :
                nb = 411
            elif nf.is_paypal :
                nb = 5122
            else :
                nb = 5121

            if tp == 0 :
                if nf.is_credit :
                    if not Accountancy.objects.filter(accounting_id = nf.id , plan_id = nf.plan.code , is_credit = 1, current_year = this_year):
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 1, amount = am ,current_year= this_year)  
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 0, amount = -am ,current_year= this_year) 
                    else :
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 1,current_year= this_year ).update(amount = am)  
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 0,current_year= this_year ).update(amount = -am)  
                else :
                   
                    if not Accountancy.objects.filter(accounting_id = nf.id , plan_id = nf.plan.code , is_credit = 0,current_year= this_year):
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 0, amount = -am ,current_year= this_year)  
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 1, amount = am ,current_year= this_year)
                    else :
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 0 ,current_year= this_year).update(amount = -am)  
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 1,current_year= this_year ).update(amount = am) 

            else :

                if nf.is_credit :
                    if not Accountancy.objects.filter(accounting_id = nf.id ,  plan_id = nf.plan.code , is_credit = 1,current_year= this_year):
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 1, amount = am,current_year= this_year )  
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 0, amount = -am,current_year= this_year ) 
                    else :
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 1,current_year= this_year ).update(amount = am)  
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 0,current_year= this_year ).update(amount = -am)  
                else :
                   
                    if not Accountancy.objects.filter(accounting_id = nf.id ,  plan_id = nf.plan.code , is_credit = 0,current_year= this_year):
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 0, amount = -am,current_year= this_year )  
                        Accountancy.objects.create(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 1, amount = am ,current_year= this_year)
                    else :
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 2 , plan_id = nf.plan.code , is_credit = 0,current_year= this_year ).update(amount = -am)  
                        Accountancy.objects.filter(accounting_id = nf.id , ranking = 1 , plan_id = nb , is_credit = 1,current_year= this_year ).update(amount = am)




        else :
            print(form.errors)
        
        if ids > 0 : return redirect('update_school_admin', ids )
        else : return redirect('list_accountings', 2 )
 

    context = {'form': form, 'form_ds': form_ds,  'tp' : tp , 'accounting' : None , 'school' : school }

    return render(request, template , context)



@user_passes_test(user_is_board) 
def renew_accounting(request,ids):
 

    school   = School.objects.get(pk=ids)
    form     = AccountingForm(request.POST or None , initial = { 'school' : school, })
    #form_abo = AbonnementForm(request.POST or None )
    formSet  = inlineformset_factory( Accounting , Detail , fields=('accounting','description','amount',) , extra=0)
    form_ds  = formSet(request.POST or None)
    today    = datetime.now()

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.user = request.user
            nf.beneficiaire = school.name
            forme = request.POST.get("forme",None)
            nf.chrono = str(uuid.uuid4())[:5]
            nf.chrono = create_chrono(Accounting, forme) # Create_chrono dans general_functions.py
            nf.plan_id = 18
            if forme == "FACTURE" :
                nf.is_credit = 1
            else :
                nf.is_credit = 0

            nf.save()

            form_ds = formSet(request.POST or None, instance = nf)
            for form_d in form_ds :
                if form_d.is_valid():
                    form_d.save()

            som = 0         
            details = nf.details.all()
            for d in details :
                som += d.amount

            customer = school.customer
            customer.actual = nf.mode
            customer.save()


            Accounting.objects.filter(pk = nf.id).update(amount=som)

            # if nf.is_abonnement :
            #     if form_abo.is_valid():
            #         fa = form_abo.save(commit = False)
            #         fa.user = request.user
            #         fa.accounting = nf
            #         fa.school = nf.school
            #         if nf.date_payment:
            #             fa.is_active = 1
            #         if fa.is_gar: # appel de la fonction qui valide le Web Service
            #             if not fa.gar_abonnement_id :
            #                 test, raison , header , decode , ida = create_abonnement_gar( today , nf  , request.user )
            #                 if test :
            #                     fa.gar_abonnement_id = ida
            #                     messages.success(request,"Activation du GAR réussie")
            #                 else :
            #                     messages.error(request,"Activation du GAR échouée..... Raison : {} \n\nHeader : {}\n\nDécodage : {} ".format(raison, header , decode ))
            #             else :
            #                 test, raison , header , decode , ida = update_abonnement_gar(  today , nf  )
            #                 if test :
            #                     messages.success(request,"Modification du GAR réussie")
            #                 else :
            #                     messages.error(request,"Modification du GAR échouée..... Raison : {} \n\nHeader : {}\n\nDécodage : {} ".format(raison, header , decode ))
            #         fa.save() 
        else :
            print(form.errors)
        
        return redirect('all_schools',)
 
    context = {'form': form, 'form_ds': form_ds, 'tp' : 0 , 'accounting' : None }

    return render(request, 'association/form_accounting.html', context)




@user_passes_test(user_is_board)
def update_accounting(request, id,tp):
    ###### Création d'accountancy

    today      = datetime.now()
    accounting = Accounting.objects.get(id=id)
    valeur     = accounting.amount
    school     = accounting.school

    form = AccountingForm(request.POST or None, instance=accounting )
    formSet = inlineformset_factory( Accounting , Detail , fields=('accounting','description','amount') , extra=0)
    form_ds = formSet(request.POST or None, instance = accounting)

    if tp == 0:
        template = 'association/form_accounting.html'
    else :
        template = 'association/form_accounting_bank.html'

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.user = request.user
            nf.school = school
            forme = request.POST.get("forme", None)
            nf.chrono = update_chrono(Accounting, accounting, forme)

            date_payment = request.POST.get("date_payment", None)
            if date_payment and tp == 0 :
                nf.tp = 2
                nf.is_credit = 1
            else :
                nf.tp = 2
            nf.save()
            
            for form_d in form_ds :
                if form_d.is_valid():
                    form_d.save()

            som = 0         
            details = nf.details.all()
            for d in details :
                som += d.amount

            Accounting.objects.filter(pk = accounting.id).update( amount = som)
            
            # Dans accountancy
            c_year       = Activeyear.objects.filter(is_active = 1).order_by("year").last()
            current_year = c_year.year

            Accountancy.objects.filter(accounting_id = accounting.id , ranking = 1 , plan_id = 411 , is_credit = 0 ).update(amount = som)  
            Accountancy.objects.filter(accounting_id = accounting.id , ranking = 2 , plan_id = 706 , is_credit = 1).update(amount = som) 


            if  nf.date_payment :
                if nf.is_paypal : bank = 5122
                else : bank = 5121  
                Accountancy.objects.update_or_create(accounting_id = accounting.id , ranking = 3 , plan_id = 411 , is_credit = 1 , defaults = {"amount" : som , 'current_year': current_year})  
                Accountancy.objects.update_or_create(accounting_id = accounting.id , ranking = 4 , plan_id = bank  , is_credit = 0 , defaults = {"amount" : -som , 'current_year': current_year}) 


            if not nf.school : # paiement par banque
                if nf.is_paypal : bank = 5122
                else : bank = 5121 
                if nf.is_credit :
                    Accountancy.objects.update_or_create(accounting_id = accounting.id  , plan_id = bank , is_credit = 0, amount = -som  , defaults = {"ranking" : 1 , 'current_year': current_year})   
                    Accountancy.objects.update_or_create(accounting_id = accounting.id ,  plan_id = nf.plan.code , amount = som , is_credit = 1, defaults = {"ranking" : 2 , 'current_year' : current_year})
                else :
                    Accountancy.objects.update_or_create(accounting_id = accounting.id  , plan_id = bank , is_credit = 1, amount = som  , defaults = {"ranking" : 1 , 'current_year': current_year})   
                    Accountancy.objects.update_or_create(accounting_id = accounting.id ,  plan_id = nf.plan.code , is_credit = 0, amount = -som , defaults = {"ranking" : 2 , 'current_year' : current_year})
 

            if int(tp) == 0 :
                return redirect('list_accountings', 0)
            elif int(tp) == 2 :
                return redirect('list_accountings', 2) 
            else :
                return redirect('list_paypal') 

        else :
            print(form.errors)
        

        if int(tp) == 0 :
            return redirect('list_accountings', 0)
        elif int(tp) == 2 :
            return redirect('list_accountings', 2) 
        else :
            return redirect('list_paypal') 
    
    context = {'form': form, 'form_ds': form_ds ,  'accounting': accounting,  'school' : school , 'tp' :tp }

    return render(request, template , context )


###############################################################################
#
#---------------------------------     GAR     --------------------------------
#
###############################################################################
 


def get_the_string_between(content,sub1,sub2) :
    # Récupère la valeur de la clé
    idx1 = content.index(sub1)
    idx2 = content.index(sub2)

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1) , idx2):
        res = res + content[idx]
    return res



 
@user_passes_test(user_is_board)
def abonnements_gar(request):


    #global_content = str('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><abonnements xmlns="http://www.atosworldline.com/wsabonnement/v1.0/"><abonnement><idAbonnement>AUTO_0350896J_26271_1619092961178</idAbonnement><commentaireAbonnement>Abonnement automatique</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ARK</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2021-04-22T14:02:41.000+02:00</debutValidite><finValidite>2024-08-15T00:00:01.000+02:00</finValidite><anneeFinValidite>2020-2021</anneeFinValidite><uaiEtab>0350896J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>ETABL</typeAffectation><nbLicenceGlobale>ILLIMITE</nbLicenceGlobale><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>AUTO_0350896J_26271_1629007368419</idAbonnement><commentaireAbonnement>Abonnement automatique</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ARK</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2021-08-15T08:02:48.000+02:00</debutValidite><finValidite>2023-08-15T00:00:00.000+02:00</finValidite><anneeFinValidite>2021-2022</anneeFinValidite><uaiEtab>0350896J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>ETABL</typeAffectation><nbLicenceGlobale>ILLIMITE</nbLicenceGlobale><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0291103S_1659621068</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-04T14:51:08.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0291103S</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0291103S_1659631645</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-04T17:47:25.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0291103S</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0350029S_1660732089</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-17T11:28:09.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0350029S</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0350029S_1660732189</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-17T11:29:49.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0350029S</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0350896J_1659614436</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-04T13:00:36.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0350896J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0350896J_1659638763</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-04T19:46:03.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0350896J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0561622J_1660732409</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-17T11:33:30.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0561622J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0561622J_1660732443</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-17T11:34:02.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0561622J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement><abonnement><idAbonnement>SACADO_0561622J_1660732461</idAbonnement><commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement><idDistributeurCom>832020065_0000000000000000</idDistributeurCom><idRessource>ark:/46173/00001.p</idRessource><typeIdRessource>ark</typeIdRessource><libelleRessource>SACADO</libelleRessource><debutValidite>2022-08-17T11:34:21.000+02:00</debutValidite><finValidite>2023-07-14T00:00:00.000+02:00</finValidite><uaiEtab>0561622J</uaiEtab><categorieAffectation>transferable</categorieAffectation><typeAffectation>INDIV</typeAffectation><nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant><nbLicenceEleve>500</nbLicenceEleve><nbLicenceProfDoc>100</nbLicenceProfDoc><nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel><publicCible>ELEVE</publicCible><publicCible>ENSEIGNANT</publicCible><publicCible>DOCUMENTALISTE</publicCible><publicCible>AUTRE PERSONNEL</publicCible></abonnement></abonnements>')
 

    test, raison , header , cont   = these_abonnements_gar()

    if test :
        global_content = str(cont)

        content_tab = global_content.split("<abonnement>")

        balises_values = ["idAbonnement" , "commentaireAbonnement" ,"idDistributeurCom" , "debutValidite" ,"finValidite" ,  "uaiEtab" , "categorieAffectation" ,"nbLicenceEnseignant" ,"nbLicenceEleve" , "nbLicenceAutrePersonnel" , "nbLicenceProfDoc"]
        balises_start  = ["<idAbonnement>" , "<commentaireAbonnement>" ,"<idDistributeurCom>" , "<debutValidite>" ,"<finValidite>" ,  "<uaiEtab>" , "<categorieAffectation>" ,"<nbLicenceEnseignant>" ,"<nbLicenceEleve>" , "<nbLicenceAutrePersonnel>" , "<nbLicenceProfDoc>" ]
        balises_close  = ["</idAbonnement>" , "</commentaireAbonnement>" ,"</idDistributeurCom>" , "</debutValidite>" ,"</finValidite>" ,  "</uaiEtab>" , "</categorieAffectation>" ,"</nbLicenceEnseignant>" ,"</nbLicenceEleve>" , "</nbLicenceAutrePersonnel>" , "</nbLicenceProfDoc>" ]
        dataset        = []

        for content in content_tab :
            dico = {}
            for i in range(len(balises_values)) :
                try :
                    result = get_the_string_between(content , balises_start[i] , balises_close[i])
     
                    if balises_values[i] == 'uaiEtab' :
                        school = School.objects.filter(code_acad = result).first()
                        dico["name"] = school.name
                    elif balises_values[i] == 'debutValidite' or balises_values[i] == 'finValidite' :
                        dico[balises_values[i]]  = result.split("T")[0]
                    else :
                        dico[balises_values[i]] = result

                except :
                    pass
            if len(dico)  :
                dataset.append(dico)
        context = {'dataset': dataset, 'error' :False  }

    else :
        context = {'dataset': [] , 'error' :True  }

    return render(request, "association/abonnements_gar.html" , context )




@user_passes_test(user_is_board)
def delete_abonnement_gar(request,idg):
  

    abonnement = Abonnement.objects.get(gar_abonnement_id = idg)
    school_id  = abonnement.school.id

    test, raison , header , decode   = delete_gar_abonnement(idg)

    if test :
        school = School.objects.get(pk = school_id)
        School.objects.filter(pk = school.id).update(gar = 1)
        messages.success(request,"Suppression de l'abonnement du GAR réussie")
    else :
        messages.error(request,"Suppression de l'abonnement du GAR échouée : {} \n\n {} \n\n {} ".format(raison, header , decode ))


    return redirect("abonnements_gar"  )


@user_passes_test(user_is_board)
def direct_update_abonnement_gar(request):


  
    id_abonnement  = request.POST.get("idAbonnement")
    debutValidite  = request.POST.get("debutValidite")+"T00:00:00.000000"
    finValidite    = request.POST.get("finValidite")+"T00:00:00.000000"
    nbLicenceEleve = request.POST.get("nbLicenceEleve")
    is_primaire    = request.POST.get("is_primaire",None)

    header  =  { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' } 
    body = "<?xml version='1.0' encoding='UTF-8'?>"
    body += "<abonnement xmlns='http://www.atosworldline.com/wsabonnement/v1.0/'>"
    body += "<idAbonnement>" + id_abonnement +"</idAbonnement>"
    body += "<commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement>"
    body += "<idDistributeurCom>832020065_0000000000000000</idDistributeurCom>"
    body += "<idRessource>ark:/46173/00001</idRessource>" #/46173/00001.p
    body += "<typeIdRessource>ark</typeIdRessource>"
    body += "<libelleRessource>SACADO</libelleRessource>"
    body += "<debutValidite>"+debutValidite+"</debutValidite>"
    body += "<finValidite>"+finValidite+"</finValidite>"
    body += "<categorieAffectation>transferable</categorieAffectation>"
    body += "<typeAffectation>INDIV</typeAffectation>"
    body += "<nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant>"
    body += "<nbLicenceEleve>"+nbLicenceEleve+"</nbLicenceEleve>"
    if is_primaire :
        body += "<nbLicenceProfDoc>100</nbLicenceProfDoc>"
        body += "<nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel>"
        body += "<publicCible>DOCUMENTALISTE</publicCible>"
        body += "<publicCible>AUTRE PERSONNEL</publicCible>"
    body += "<publicCible>ENSEIGNANT</publicCible>"
    body += "<publicCible>ELEVE</publicCible>"
    body += "</abonnement>"


    try :
        f = open('/var/www/sacado/logs/gar_connexions.log','a')
        print("================  MODIFICATION GAR ================", file=f)
        print("===> date_start : ", file=f)
        print(date_start, file=f)
        print("===> date_stop : ", file=f)
        print(date_stop, file=f)
        print("===> id_abonnement : ", file=f)
        print(id_abonnement, file=f)
        print("===> body : ", file=f)
        print(body, file=f)
        f.close()
    except :
        pass 


    host   = "https://abonnement.gar.education.fr/"+id_abonnement  # Adresse d'envoi
    directory = '/home/sacado/'
    r   = requests.post(host, data=body, headers=header, cert=(directory + 'sacado.xyz-PROD-2021.pem', directory + 'sacado_prod.key'))

    if r.status_code == 201 or r.status_code==200 :
        messages.success(request,"Modification réussie") 
    else :
        messages.success(request,r.content.decode('utf-8'))
    return redirect("abonnements_gar"  )


 




 
@user_passes_test(user_is_board)
def purge_gar(request,user_type):

    nb_teachers = User.objects.filter(user_type=2 , school__gar=1).exclude(is_superuser=1).count()
    nb_students = User.objects.filter(user_type=0 , school__gar=1).count()


    if user_type < 3 :
        User.objects.filter(user_type=user_type , school__gar=1).delete()[:2000]
 
    context = {  'nb_teachers' : nb_teachers , 'nb_students' : nb_students }

    return render(request, 'association/purge_gar.html', context)





@user_passes_test(user_is_board)
def create_avoir(request, id):
 
    accounting = Accounting.objects.get(id=id)
    amount     = accounting.amount
    chronof    = accounting.chrono

    this_id    = accounting.id


    accounting.pk = None
    accounting.amount = -amount
    accounting.is_credit = 0

    accounting.forme = "AVOIR"
    chrono = create_chrono(Accounting, "AVOIR")
    accounting.chrono = chrono
    texte = " Avoir sur facture " + chronof
    accounting.objet = texte
    accounting.observation = texte
    accounting.mode = " Avoir sur facture " + chronof
    acc = accounting.save()
    
    c_year       = Activeyear.objects.filter(is_active = 1).order_by("year").last()
    current_year = c_year.year
    # Création des avoirs
    Accountancy.objects.create(accounting_id = this_id , ranking = 3 , plan_id = 411 , is_credit = 1, amount = amount , current_year = current_year)  
    Accountancy.objects.create(accounting_id = this_id , ranking = 4 , plan_id = 706 , is_credit = 0, amount = amount , current_year = current_year)  
 
    accounti = Accounting.objects.get(id=id) 
    accounti.objet += " Avoir sur " + chronof
    accounti.observation += " Avoir sur " + chronof
    accounti.is_active = 0
    accounti.is_abonnement = 0
    accounti.save()

    return redirect('list_accountings', 0)
    

 



@user_passes_test(user_is_board)
def show_accounting(request, id ):

    accounting = Accounting.objects.get(id=id)
    details = Detail.objects.filter(accounting=accounting)


    context = {  'accounting': accounting, 'details': details,  }

    return render(request, 'association/show_accounting.html', context )





def print_accounting(request, id ):

    accounting = Accounting.objects.get(id=id)

    if not request.user.is_superuser :
        if request.user.school != accounting.school :
            return redirect ("index")

    #########################################################################################
    ### Instanciation
    #########################################################################################
    elements = []        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+str(accounting.chrono)+'.pdf"'
    doc = SimpleDocTemplate(response,   pagesize=A4, 
                                        topMargin=0.5*inch,
                                        leftMargin=0.5*inch,
                                        rightMargin=0.5*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()
    OFFSET_INIT = 0.2
    #########################################################################################
    ### Style
    #########################################################################################
    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page_blue = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )

    title = ParagraphStyle('title', 
                            fontSize=16, 
                            )

    subtitle = ParagraphStyle('title', 
                            fontSize=14, 
                            textColor=colors.HexColor("#00819f"),
                            )
 
    mini = ParagraphStyle(name='mini',fontSize=9 )  

    normal = ParagraphStyle(name='normal',fontSize=12,)   

    dateur_style = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style = ParagraphStyle('dateur_style', 
                            fontSize=11, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_mini = ParagraphStyle('dateur_style', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_blue = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            textColor=colors.HexColor("#00819f"),
                            )

    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )
    offset = 0 # permet de placer le bas de page
    #########################################################################################
    ### Logo Sacado
    #########################################################################################
    dateur = "Date : " + accounting.date.strftime("%d-%m-%Y")
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
    logo_tab = [[logo, "Association SacAdo\nhttps://sacado.xyz \nsacado.asso@gmail.com", dateur]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5.2*inch,inch])
    elements.append(logo_tab_tab)
    #########################################################################################
    ### Facture
    #########################################################################################
    elements.append(Spacer(0,0.3*inch))
    f = Paragraph( accounting.forme , sacado )
    elements.append(f) 
    #########################################################################################
    ### Bénéficiaire ou Etablissement
    #########################################################################################
    if accounting.school :
        beneficiaire = accounting.school.name
        address = accounting.school.address
        complement = accounting.school.complement
        town = accounting.school.town 
        country = accounting.school.country.name
        zip_code = accounting.school.zip_code
        contact = ""
        name_contact = ""
        for u in accounting.school.users.filter(is_manager=1) :
            contact += u.email +" "
            name_contact += u.last_name +" " + u.first_name +" - "
    else :    
        beneficiaire = accounting.beneficiaire
        address = accounting.address
        complement = accounting.complement
        zip_code = accounting.school.zip_code
        town = accounting.town 
        country = accounting.country.name
        contact = accounting.contact
        name_contact = ""

    beneficiaire = Paragraph( beneficiaire  , signature_style )
    elements.append(beneficiaire)
    elements.append(Spacer(0,0.1*inch))
    if address :
        address = Paragraph( address , signature_style_mini )
        elements.append(address)
        offset += OFFSET_INIT

    if complement :
        compl = Paragraph( complement , signature_style_mini )
        elements.append(compl)
        offset += OFFSET_INIT

    if zip_code :
        complementz = Paragraph( zip_code , signature_style_mini )
        elements.append(complementz)
        offset += OFFSET_INIT

    town = Paragraph( town + " - " + country , signature_style_mini )
    elements.append(town)


    #########################################################################################
    ### Code de facture
    #########################################################################################
 
    elements.append(Spacer(0,0.5*inch))
    code = Paragraph( accounting.forme+" "+accounting.chrono , normal )
    elements.append(code)
    elements.append(Spacer(0,0.1*inch))
    objet = Paragraph(  "Objet : "+accounting.objet , normal )
    elements.append(objet) 
    elements.append(Spacer(0,0.1*inch))
    licence = Paragraph(  "Licence : "+str(accounting.school.nbstudents)+" élèves" , normal )
    elements.append(licence) 
    elements.append(Spacer(0,0.2*inch))


    #########################################################################################
    ### Description de facturation
    #########################################################################################
    details_tab = [("Description", "Qté", "Px unitaire HT" ,  "Px Total HT" )]

    details = Detail.objects.filter(accounting = accounting)

    for d in details :
        details_tab.append((d.description, "1" , d.amount ,  d.amount ))
        offset += OFFSET_INIT
                
    details_table = Table(details_tab, hAlign='LEFT', colWidths=[4.1*inch,1*inch,1*inch,1*inch])
    details_table.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))
               ]))
    elements.append(details_table)

    #########################################################################################
    ### Total de facturation
    #########################################################################################
    elements.append(Spacer(0,0.1*inch))
    details_tot = Table([("Total HT", str( accounting.amount) +"€" ), ("Net à payer en euros", str( accounting.amount) +"€" )], hAlign='RIGHT', colWidths=[2.8*inch,1*inch])
    details_tot.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(0.9,0.9,0.9))
               ]))
    elements.append(details_tot)

    #########################################################################################
    ### TVA non applicable
    #########################################################################################

    elements.append(Spacer(0,0.1*inch)) 
    tva = Paragraph(  "« TVA non applicable, suivant article 293-b du CGI. »"  , signature_style_mini )
    elements.append(tva)


    #########################################################################################
    ### Observation
    #########################################################################################
    offs = 0
    if accounting.observation  :
        elements.append(Spacer(0,0.4*inch)) 

        
        for text in cleantext(accounting.observation) :
            observation = Paragraph( text , normal )
            elements.append(observation)
            elements.append(Spacer(0,0.1*inch))
            offs +=0.15 




 
    #########################################################################################
    ### Reglement facture
    #########################################################################################
    elements.append(Spacer(0,1*inch)) 
    label_facture = ""
    if accounting.date_payment  :
        label_facture = "Facture réglée le " + str(accounting.date_payment.strftime("%d-%m-%Y")) +" "+accounting.mode

    facture = Paragraph(  label_facture  , normal )
    elements.append(facture)
    offs +=1

    offset = offs + OFFSET_INIT


    #########################################################################################
    ### Bas de page
    #########################################################################################
    nb_inches = 4.4 - offset
    elements.append(Spacer(0,nb_inches*inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : 903345569"  , bas_de_page )
    elements.append(asso3)
    asso30 = Paragraph( "siret : 903345569 00011"  , bas_de_page )
    elements.append(asso30)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères - FRANCE"  , bas_de_page )
    elements.append(asso4)

    doc.build(elements)

    return response
 


def print_bilan(request):

    date_start = request.POST.get("date_start")
    date_end   = request.POST.get("date_end")
    envoi      = request.POST.get("envoi") 
    date_start_obj = datetime.strptime(date_start, '%Y-%m-%d')
    date_end_obj   = datetime.strptime(date_end, '%Y-%m-%d')
    OFFSET_INIT = 0.2

    accountings = Accounting.objects.filter(date__gte=date_start_obj, date__lte=date_end_obj)
    #########################################################################################
    ### Instanciation
    #########################################################################################
    elements = []        
    response = HttpResponse(content_type='application/pdf')


    response['Content-Disposition'] = 'attachment; filename="Bilans.pdf"'
    doc = SimpleDocTemplate(response,   pagesize=A4, 
                                        topMargin=0.5*inch,
                                        leftMargin=0.5*inch,
                                        rightMargin=0.5*inch,
                                        bottomMargin=0.3*inch     )

    sample_style_sheet = getSampleStyleSheet()
    #########################################################################################
    ### Style
    #########################################################################################
    sacado = ParagraphStyle('sacado', 
                            fontSize=20, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    sacado_mini = ParagraphStyle('sacado', 
                            fontSize=14, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            )
    bas_de_page_blue = ParagraphStyle('sacado', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_CENTER,
                            textColor=colors.HexColor("#00819f"),
                            )
    title = ParagraphStyle('title', 
                            fontSize=16, 
                            )
    subtitle = ParagraphStyle('title', 
                            fontSize=14, 
                            textColor=colors.HexColor("#00819f"),
                            )
    mini = ParagraphStyle(name='mini',fontSize=9 )  
    normal = ParagraphStyle(name='normal',fontSize=12,)   
    dateur_style = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            leading=26,
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style = ParagraphStyle('dateur_style', 
                            fontSize=11, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_mini = ParagraphStyle('dateur_style', 
                            fontSize=9, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            )
    signature_style_blue = ParagraphStyle('dateur_style', 
                            fontSize=12, 
                            borderPadding = 0,
                            alignment= TA_RIGHT,
                            textColor=colors.HexColor("#00819f"),
                            )
    style_cell = TableStyle(
            [
                ('SPAN', (0, 1), (1, 1)),
                ('TEXTCOLOR', (0, 1), (-1, -1),  colors.Color(0,0.7,0.7))
            ]
        )

    offset = 0 # permet de placer le bas de page
    #########################################################################################
    ### Logo Sacado
    #########################################################################################
    logo = Image('https://sacado.xyz/static/img/sacadoA1.png')
    logo_tab = [[logo, "Association SacAdo \nContact : assocation@sacado.xyz"]]
    logo_tab_tab = Table(logo_tab, hAlign='LEFT', colWidths=[0.7*inch,5.52*inch])
    logo_tab_tab.setStyle(TableStyle([ ('TEXTCOLOR', (0,0), (-1,0), colors.Color(0,0.5,0.62))]))
    elements.append(logo_tab_tab)
    #########################################################################################
    ### Facture
    #########################################################################################
    elements.append(Spacer(0,0.3*inch))
    bilan = Paragraph( "Bilans" , sacado )
    elements.append(bilan) 
    #########################################################################################
    ### Bénéficiaire ou Etablissement
    #########################################################################################
    date_s = Paragraph(  date_start + " - " + date_end , sacado_mini )
    elements.append(date_s)
    elements.append(Spacer(0,0.2*inch))  

    details_tab = []
    som = 0 
    i = 0
    for a in accountings :
        if a.beneficiaire :
            bene = a.beneficiaire
        else :
            bene = a.school.name
        details_tab.append((a.date.strftime("%d %b %Y")+ ": "+bene +" "+a.objet,  a.amount ))
        offset += OFFSET_INIT
        som += a.amount
        i+=1
        if i == 30 :
            elements.append(PageBreak())
                
    details_table = Table(details_tab, hAlign='LEFT', colWidths=[6.3*inch,1*inch])
    details_table.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(1,1,1))
               ]))
    elements.append(details_table)
    #########################################################################################
    ### Total de facturation
    #########################################################################################
    elements.append(Spacer(0,0.1*inch))
    details_tot = Table([("Total TTC en euros", som  )], hAlign='LEFT', colWidths=[6.3*inch,1*inch])
    details_tot.setStyle(TableStyle([
               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,0), (-1,0), colors.Color(0.9,0.9,0.9))
               ]))
    elements.append(details_tot)
    #########################################################################################
    ### Signature Bruno
    #########################################################################################

    elements.append(Spacer(0,inch)) 
    signature = Paragraph(  "_______________________________"  , signature_style_blue )
    elements.append(signature)
    elements.append(Spacer(0,0.1*inch)) 
    signature2 = Paragraph( "Bruno Serres                     "  , signature_style )
    elements.append(signature2)
    signature2 = Paragraph( "Trésorier de l'association SacAdo"  , signature_style_mini )
    elements.append(signature2)
    #########################################################################################
    ### Bas de page
    #########################################################################################
    nb_inches = 4.6 - offset
    elements.append(Spacer(0,nb_inches*inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : 903345569"  , bas_de_page )
    elements.append(asso3)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères"  , bas_de_page )
    elements.append(asso4)

    doc.build(elements)

    return response


def export_bilan(request):

    date_start = request.POST.get("date_start")
    date_end   = request.POST.get("date_end")
    envoi      = request.POST.get("envoi")
    date_start_obj = datetime.strptime(date_start, '%Y-%m-%d')
    date_end_obj   = datetime.strptime(date_end, '%Y-%m-%d')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bilans.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(date_start+'-'+date_end)

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date', 'Date de valeur',  'Crédit/Débit', 'Objet', "Bénéficiaire", 'Etablissement', 
                'Address','Complément', 'Ville', 'Pays', 'Contact', 
                'Observation', 'Montant', 'Emetteur']

 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    accountings = Accounting.objects.filter(date_payment__gte=date_start_obj, date_payment__lte=date_end_obj).values_list('date', 'date_payment', 'is_credit' , 'objet', 'beneficiaire','school', 'address', 'complement',  'town', 'country', 'contact', 'observation', 'amount', 'user' ).order_by("date")
    ############  Gestion des selects multiples #####################################
    row_n = 0
    for accounting in accountings :
        row_n += 1
 
 
        for col_num in range(len(accounting)):
            
            if col_num == 0 : 
                content =  accounting[col_num].strptime(date_start, '%Y-%m-%d')
            elif col_num == 1 :
                content =  accounting[col_num].strptime(date_start, '%Y-%m-%d')
            elif col_num == 2 :
                if  accounting[2] :
                    content = "Crédit"
                else :
                    content = "Débit"
            elif col_num == 11 :         
                content =  cleanhtml(str(unescape_html(accounting[col_num]))) 
            elif col_num == 13 :  
                user = User.objects.get(pk=accounting[col_num])       
                content =  user.last_name+ " "+  user.first_name 
            else :
                content =  accounting[col_num]
 
            if content  :           
                ws.write(row_n, col_num, content , font_style)
 
    wb.save(response)
    return response
 


#####################################################################################################################################
#####################################################################################################################################
####    Relance
#####################################################################################################################################
#####################################################################################################################################

@user_passes_test(user_is_board)
def relance_accounting(request, id ):

    accounting = Accounting.objects.get(pk=id)
    managers = accounting.school.users.filter(is_manager=1)
    dest = [user.email for user in managers]

    chrono = accounting.chrono


    msg = "Bonjour Madame, Monsieur,\n\nRéférence : "+chrono+ "\n\nComme suite à la demande d'abonnement SACADO de votre établissement " + accounting.school.name +", nous n'avons pas reçu votre cotisation durant la période d'essai qui vient de se terminer.\n\nPourriez-vous nous confirmer le règlement de ladite cotisation ? \n\nCordialement."

    send_mail("Rappel Abonnement SACADO", msg , settings.DEFAULT_FROM_EMAIL , dest)
    send_mail("Rappel Abonnement SACADO", msg , settings.DEFAULT_FROM_EMAIL , [settings.DEFAULT_FROM_EMAIL])

    messages.success(request,"Message de relance envoyé aux administrateurs SACADO de "+ accounting.school.name )
    return redirect("update_school_admin" , accounting.school.id )



#####################################################################################################################################
#####################################################################################################################################
####    Associate
#####################################################################################################################################
#####################################################################################################################################


@user_passes_test(user_is_board)
def list_associate(request):
    user = request.user
    associates = Associate.objects.filter(is_active = 1)
    pending_associates = Associate.objects.filter(is_active = 0)

    nb_total = User.objects.filter(user_type=0).exclude(username__contains="_e-test_").count()

    return render(request, 'association/list_associate.html', {'associates': associates , 'pending_associates': pending_associates , 'user' : user  , 'nb_total':nb_total  })


@user_passes_test(user_is_board) 
def create_associate(request):
 
    form = AssociateForm(request.POST or None )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.author = request.user
        nf.save()


        return redirect('list_associate')

    else:
        
        print(form.errors)

    context = {'form': form, }

    return render(request, 'association/form_associate.html', context)



@user_passes_test(user_is_board)
def update_associate(request, id):

    associate = Associate.objects.get(id=id)
    
    form = AssociateForm(request.POST or None, instance=associate )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.author = request.user
        return redirect('list_associate')
    else:
        print(form.errors)

    context = {'form': form,  'associate': associate,  }

    return render(request, 'association/form_associate.html', context )



@user_passes_test(user_is_board)
def delete_associate(request, id):

    associate = Associate.objects.get(id=id)
    associate.delete()
    return redirect('list_associate')
    

 
@user_passes_test(user_is_board)
def accept_associate(request, id):
    Associate.objects.filter(id=id).update(is_active = 1)
    return redirect('list_associate')


@user_passes_test(user_is_board)
def mails_parents(request):
    users = User.objects.filter(user_type=1) 
    context = {'users': users,   }

    return render(request, 'association/mails_parents.html', context)


#####################################################################################################################################
#####################################################################################################################################
####    Voting
#####################################################################################################################################
#####################################################################################################################################
 



@user_passes_test(user_is_board) 
def create_voting(request,id):
 
    form = VotingForm(request.POST or None )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.user = request.user
        nf.associate_id = id
        nf.save()
        try : 
            rcv = ["sacado.asso@gmail.com"]
            msg = "Une proposition de membre est postée par "+str(request.user)+". Rendez-vous sur https://sacado.xyz"
            send_mail("Proposition de membre", msg , settings.DEFAULT_FROM_EMAIL , rcv)
        except :
            pass
        return redirect('list_associate')

    else:
        print(form.errors)

    context = {'form': form,   }

    return render(request, 'association/form_voting.html', context)


 


 

@user_passes_test(user_is_board)
def show_voting(request, id):

    voting = Voting.objects.get(id=id)
    context = {  'voting': voting,   }

    return render(request, 'association/show_voting.html', context)




#####################################################################################################################################
#####################################################################################################################################
####    Section
#####################################################################################################################################
#####################################################################################################################################
 

@user_passes_test(user_is_board) 
def create_section(request):

    sections = Section.objects.all()
    form = SectionForm(request.POST or None )

    if form.is_valid():
        form.save()

        return redirect('create_document')
    else:
        print(form.errors)

    context = {'form': form, 'sections' : sections }

    return render(request, 'association/form_section.html', context)



@user_passes_test(user_is_board)
def update_section(request, id):

    sections = Section.objects.all()
    section = Section.objects.get(id=id)
    
    form = SectionForm(request.POST or None, instance=section )

    if form.is_valid():
        form.save()
        return redirect('list_documents')
    else:
        print(form.errors)

    context = {'form': form,  'section': section, 'sections' : sections   }

    return render(request, 'association/form_section.html', context )



@user_passes_test(user_is_board)
def delete_section(request, id):

    section = Section.objects.get(id=id)
    section.delete()
    return redirect('create_section')
    
 





@user_passes_test(user_is_board)
def list_documents(request):
    documents = Document.objects.order_by("section", "date_modified")
    document =  documents.first()
    return render(request, 'association/show_document.html', { 'documents': documents , 'document': document  })


@user_passes_test(user_is_board) 
def create_document(request):
 
    form = DocumentForm(request.POST or None )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.user = request.user
        nf.save()

        return redirect('list_documents')
    else:
        print(form.errors)

    context = {'form': form, }

    return render(request, 'association/form_document.html', context)



@user_passes_test(user_is_board)
def update_document(request, id):

 
    document = Document.objects.get(id=id)
    
    form = DocumentForm(request.POST or None, instance=document )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.user = request.user
        nf.save()
        return redirect('list_documents')
    else:
        print(form.errors)

    context = {'form': form,  'document': document,  }

    return render(request, 'association/form_document.html', context )



@user_passes_test(user_is_board)
def delete_document(request, id):

    document = Document.objects.get(id=id)
    document.delete()
    return redirect('list_documents')


 
def ajax_shower_document(request):
    document_id =  int(request.POST.get("document_id"))
    document =  Document.objects.get(pk=document_id)
    data = {}
 
    context = {  'document': document   }
 
    data['html'] = render_to_string('association/ajax_shower_document.html', context)

    return JsonResponse(data)


#####################################################################################################################################
#####################################################################################################################################
####    Rate
#####################################################################################################################################
#####################################################################################################################################
@user_passes_test(user_is_board)
def list_rates(request):
    formules = Formule.objects.all()
    rates = Rate.objects.all()
    return render(request, 'association/list_rate.html', {'rates': rates , 'formules': formules   })


@user_passes_test(user_is_board)
def show_rate(request):

    rates = Rate.objects.filter(is_active = 1).order_by("quantity")
    return render(request, 'association/list_rate.html', {'rates': rates ,     })


@user_passes_test(user_is_board) 
def create_rate(request):
 
    form = RateForm(request.POST or None )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.author = request.user
        nf.save()


        return redirect('list_rates')

    else:
        
        print(form.errors)

    context = {'form': form, }

    return render(request, 'association/form_rate.html', context)



@user_passes_test(user_is_board)
def update_rate(request, id):

    rate = Rate.objects.get(id=id)
    
    form = RateForm(request.POST or None, instance=rate )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.author = request.user
        return redirect('list_rates')
    else:
        print(form.errors)

    context = {'form': form,  'rate': rate,  }

    return render(request, 'association/form_rate.html', context )



@user_passes_test(user_is_board)
def delete_rate(request, id):

    rate = Rate.objects.get(id=id)
    rate.delete()
    return redirect('list_rates')
    
 



@user_passes_test(user_is_board)
def reset_all_students_sacado(request):

    Parent.objects.all().delete()
    Response.objects.all().delete() 
    User.objects.filter(user_type=0).exclude(username__contains= "_e-test").delete()
    messages.success(request,"Ré-initialisation effectuée avec succès.")


    return redirect('association_index')




@user_passes_test(user_is_board)
def pending_adhesions(request):

    today       = time_zone_user(request.user)
    date_limit  = today - timedelta(days=15)

    customers     = Customer.objects.filter(status=2)
    context     = { 'customers': customers,  'prosp' : True  ,'title_page' : 'en attente'   }

    return render(request, 'association/adhesions.html', context )



@user_passes_test(user_is_board)
def prospec_schools(request):

    schools     = Accounting.objects.values_list("school").distinct().exclude(school=None) 
    user_no_adh = User.objects.filter(user_type=2).exclude(school__in= schools).order_by("-last_login")
    context     = { 'user_no_adh': user_no_adh,  'prosp' : True  }

    return render(request, 'association/list_prospec_schools.html', context )



@user_passes_test(user_is_board)
def prospec_to_adhesions(request):

    customers     = Customer.objects.filter(status=1)
    context     = { 'customers': customers,  'prosp' : False ,'title_page' : 'anciens clients'    }

    return render(request, 'association/adhesions.html', context )
 


@user_passes_test(user_is_board)
def contact_prosp(request):

    week_prev   = time_zone_user(request.user) - timedelta(days=7)

    teachers    = Teacher.objects.filter(Q(groups=None)|Q(teacher_parcours=None)).filter( user__date_joined__gt= week_prev)
    nb_teachers = teachers.count()
    som = 0
    if request.method == "POST":
        teacher_ids = request.POST.getlist("teacher_ids", None)
        for teacher_id in teacher_ids :
            user = User.objects.get(pk = teacher_id )
            msg  = request.POST.get("message", None).replace("***","\n")
            msg  = "Bonjour "+user.first_name+" " +user.last_name+",\n"+msg
            objet = request.POST.get("objet", None)
            send_mail( objet, msg , settings.DEFAULT_FROM_EMAIL , [ user.email ]  )
            Prospection.objects.create(user=user)
            som +=1



    context     = { 'teachers': teachers, 'som' : som   }

 

    return render(request, 'association/contact_prosp.html', context )

 

def ajax_display_button(request):    

    customer_id =  int(request.POST.get("customer_id"))
    customer =  Customer.objects.get(pk=customer_id)
    data = {}
    if customer.is_display_button :
        customer.is_display_button = 0
        html = "<i class='bi bi-database-dash text-danger' title='Le bouton d\'adhésion est caché. Afficher le bouton d\'adhésion'></i>"
    else :
        customer.is_display_button = 1
        html = "<i class='bi bi-database-fill-down text-success' title='Le bouton d\'adhésion est affiché. Cacher le bouton d\'adhésion'></i>"
    customer.save()

    data['html'] = html

    return JsonResponse(data)

 
def ajax_display_all_buttons(request):    

    Customer.objects.all().update(is_display_button=1)
    data = {}
    data['html'] =  "<i class='bi bi-database-fill-down text-success' title='Le bouton d\'adhésion est affiché. Cacher le bouton d\'adhésion'></i>"

    return JsonResponse(data)

 