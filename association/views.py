from django.shortcuts import render, redirect, get_object_or_404
from association.models import Accounting,Associate , Voting , Document, Section , Detail , Rate  , Holidaybook, Abonnement
from association.forms import AccountingForm,AssociateForm,VotingForm, DocumentForm , SectionForm, DetailForm , RateForm , AbonnementForm , HolidaybookForm
from account.models import User, Student, Teacher, Parent ,  Response
from qcm.models import Exercise, Studentanswer , Customanswerbystudent , Writtenanswerbystudent
from school.models import School
from setup.models import Formule
from setup.forms import FormuleForm
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
import uuid
import json
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from account.decorators import user_is_board
from templated_email import send_templated_mail
from django.db.models import Q , Sum
from django.contrib.auth.decorators import  permission_required,user_passes_test
############### bibliothèques pour les impressions pdf  #########################
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
from datetime import datetime 
from general_fonctions import *
import xlwt
 
 


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


@user_passes_test(user_is_board)
def association_index(request):

    today_start  = datetime.date(datetime.now())
    nb_teachers  = Teacher.objects.all().count()
    nb_students  = Student.objects.all().count()#.exclude(user__username__contains="_e-test_")
    nb_exercises = Exercise.objects.filter(supportfile__is_title=0).count()
    nb_schools   = School.objects.all().count()

    nb_answers   = Studentanswer.objects.filter(date__gte= today_start).count() + Customanswerbystudent.objects.filter(date__gte= today_start).count() + Writtenanswerbystudent.objects.filter(date__gte= today_start).count()
    if Holidaybook.objects.all() :
        holidaybook  = Holidaybook.objects.values("is_display").get(pk=1)
    else :
        holidaybook = False

    context = { 'nb_teachers': nb_teachers , 'nb_students': nb_students , 'nb_exercises': nb_exercises, 
                'nb_schools': nb_schools, 'nb_answers': nb_answers, 'holidaybook': holidaybook ,
                }

    return render(request, 'association/dashboard.html', context )


def total(first_date, last_date) :

    accountings = Accounting.objects.filter(acting__lte=last_date, acting__gte=first_date).exclude(acting=None)
    total_amount = 0
    total_amount_active = 0
    for a in accountings :
        if a.is_credit :
            total_amount += a.amount
        else :
            total_amount -= a.amount
    return total_amount



@user_passes_test(user_is_board)
def list_accountings(request,tp):
    if tp == 0 :
        accountings = Accounting.objects.filter(tp=tp,acting=None).exclude(is_paypal=1).order_by("-date")
    elif tp == 1 :
        accountings = Accounting.objects.filter(tp=tp,acting=None).order_by("-date")
    else :
        accountings = Accounting.objects.exclude(acting=None).order_by("-date")

    today = datetime.now()
    this_month = today.month
    this_year = today.year

    first_date_month =  datetime(this_year, this_month, 1)
    first_date_year = datetime(this_year, 1, 1)

    if this_month > 0 and this_month < 8 :
        this_year = this_year - 1
    first_date_schoolyear = datetime(this_year, 9, 1)

    total_month = total(first_date_month, today)
    total_year = total(first_date_year, today)
    total_shoolyear =  total(first_date_schoolyear, today)

    return render(request, 'association/list_accounting.html', {'accountings': accountings , 'tp' : tp , 'total_month': total_month, 'total_year': total_year, 'total_shoolyear': total_shoolyear ,'this_month' :this_month })





@user_passes_test(user_is_board)
def ajax_total_month(request):
    data = {}
    month = int(request.POST.get("month"))

    today = datetime.now()
    this_year = datetime.now().year
    first = datetime(this_year, month, 1)
    nb_days=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    first = datetime(this_year, month, 1)
    last = datetime(this_year, month, nb_days[month])


    data['html'] = "<label><b>"+str(total(first, last)).replace(".",",")+" € </b></label>"
    rows = Accounting.objects.values_list("id", flat = True).filter(acting__lte=last, acting__gte=first).exclude(acting=None)
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
    to_date = request.POST.get("to_date",None)

    if from_date and to_date :
        from_date = str_to_date(from_date)
        to_date = str_to_date(to_date)

        rows = Accounting.objects.values_list("id", flat = True).filter(acting__lte=to_date,acting__gte=from_date).exclude(acting=None)
        data['rows'] = list(rows)
        data['html'] = str(total(from_date, to_date)) +" €"
        data['len']  = len(list(rows))
    else :
        data['html'] = "Sélectionner deux dates"
        data['rows'] = False
        data['len']  = 0
    return JsonResponse(data)






@user_passes_test(user_is_board) 
def create_accounting(request,tp):
 
    form     = AccountingForm(request.POST or None )
    form_abo = AbonnementForm(request.POST or None )
    formSet = inlineformset_factory( Accounting , Detail , fields=('accounting','description','amount',) , extra=0)
    form_ds = formSet(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.user = request.user
            forme = request.POST.get("forme",None)
            nf.chrono = create_chrono(Accounting, forme) # Create_chrono dans general_functions.py
            nf.tp = tp
            if tp == 0 :
                nf.tp = 18
                if forme == "FACTURE" :
                    nf.is_credit = 1
                else :
                    nf.is_credit = 0
            elif tp == 1 :
                if forme == "AVOIR" :
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

            Accounting.objects.filter(pk = nf.id).update(amount=som)

            if nf.is_abonnement :
                if form_abo.is_valid():
                    fa = form_abo.save(commit = False)
                    fa.user = request.user
                    fa.accounting = nf
                    fa.school = nf.school
                    if nf.acting:
                        fa.active = 1
                    fa.save()
        else :
            print(form.errors)
        
        return redirect('list_accountings',tp)
 

    context = {'form': form, 'form_ds': form_ds, 'form_abo' : form_abo , 'tp' : tp  }

    return render(request, 'association/form_accounting.html', context)



@user_passes_test(user_is_board)
def update_accounting(request, id):

    accounting = Accounting.objects.get(id=id)
    is_credit =  accounting.is_credit
    try :
        abonnement = accounting.abonnement 
        form_abo = AbonnementForm(request.POST or None, instance=accounting.abonnement  )
    except :
        abonnement = False
        form_abo = AbonnementForm(request.POST or None )

    form = AccountingForm(request.POST or None, instance=accounting )
    formSet = inlineformset_factory( Accounting , Detail , fields=('accounting','description','amount') , extra=0)
    form_ds = formSet(request.POST or None, instance = accounting)

    if request.method == "POST":
        if form.is_valid():
            nf = form.save(commit = False)
            nf.user = request.user
            forme = request.POST.get("forme", None)
            nf.chrono = update_chrono(Accounting, accounting, forme)
            nf.save()

            for form_d in form_ds :
                if form_d.is_valid():
                    form_d.save()

            som = 0         
            details = nf.details.all()
            for d in details :
                som += d.amount

            Accounting.objects.filter(pk = accounting.id).update(amount=som,is_credit=is_credit)
 

            if nf.is_abonnement :
                if form_abo.is_valid():
                    fa = form_abo.save(commit = False)
                    fa.user = request.user
                    fa.accounting = accounting
                    fa.school = nf.school
                    if nf.acting:
                        fa.is_active = 1
                        Accounting.objects.filter(pk = accounting.id).update(is_active = 1)
                        Accounting.objects.filter(pk = accounting.id).update(tp = 3)
                    fa.save()
                else :
                    accounting.abonnement.delete()

        else :
            print(form.errors)
        
        return redirect('list_accountings', accounting.tp)

    context = {'form': form, 'form_ds': form_ds ,  'accounting': accounting,  'form_abo': form_abo, 'abonnement' : abonnement  }

    return render(request, 'association/form_accounting.html', context )



@user_passes_test(user_is_board)
def delete_accounting(request, id):

    accounting = Accounting.objects.get(id=id)
    accounting.delete()
    return redirect('list_accountings', accounting.tp)
    

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
    logo_tab = [[logo, "Association SacAdo\nhttps://sacado.xyz \nassociation@sacado.xyz", dateur]]
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
        contact = ""
        name_contact = ""
        for u in accounting.school.users.filter(is_manager=1) :
            contact += u.email +" "
            name_contact += u.last_name +" " + u.first_name +" - "
    else :    
        beneficiaire = accounting.beneficiaire
        address = accounting.address
        complement = accounting.complement
        town = accounting.town 
        country = accounting.country.name
        contact = accounting.contact
        name_contact = ""

    beneficiaire = Paragraph( beneficiaire , signature_style )
    elements.append(beneficiaire)
    elements.append(Spacer(0,0.1*inch))
    if address :
        address = Paragraph( address , signature_style_mini )
        elements.append(address)
        offset += OFFSET_INIT

    if complement :
        complement = Paragraph( complement , signature_style_mini )
        elements.append(complement)
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
    if accounting.acting  :
        label_facture = "Facture réglée le " + str(accounting.acting.strftime("%d-%m-%Y")) +" "+accounting.mode

    facture = Paragraph(  label_facture  , normal )
    elements.append(facture)
    offs +=1

    offset = offs + OFFSET_INIT


    #########################################################################################
    ### Bas de page
    #########################################################################################
    nb_inches = 4.6 - offset
    elements.append(Spacer(0,nb_inches*inch)) 
    asso = Paragraph(  "___________________________________________________________________"  , bas_de_page_blue )
    elements.append(asso)
    asso2 = Paragraph( "Association SacAdo"  , bas_de_page )
    elements.append(asso2)
    asso3 = Paragraph( "siren : W832020065 - Préfecture du Var"  , bas_de_page )
    elements.append(asso3)
    asso4 = Paragraph( "2B Avenue de la pinède, La Capte, 83400 Hyères"  , bas_de_page )
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
    asso3 = Paragraph( "siren : W832020065"  , bas_de_page )
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


    accountings = Accounting.objects.filter(acting__gte=date_start_obj, acting__lte=date_end_obj).values_list('date', 'acting', 'is_credit' , 'objet', 'beneficiaire','school', 'address', 'complement',  'town', 'country', 'contact', 'observation', 'amount', 'user' ).order_by("date")
    ############  Gestion des selects multiples #####################################
    row_n = 0
    for accounting in accountings :
        row_n += 1
        print(accounting)
 
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
            send_mail("Proposition de membre", msg , 'info@sacado.xyz', rcv)
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
def accountings(request):


    this_day     = datetime.now() 
    this_year    = this_day.year

    nb_schools        = Abonnement.objects.filter(date_start__lte = this_day  , date_stop__gte = this_day).count()
    nb_schools_fr     = Abonnement.objects.filter(date_start__lte = this_day  , date_stop__gte = this_day, is_active = 1, school__country_id = 5).count()
    nb_schools_no_fr  = Abonnement.objects.filter(date_start__lte = this_day  , date_stop__gte = this_day, is_active = 1).exclude(school__country_id =5).count() 
    nb_schools_no_pay = Abonnement.objects.filter(date_start__lte = this_day  , date_stop__gte = this_day, is_active = 0).count()
  
    start_date   = datetime(this_year, 1, 1)
    end_date     = datetime(this_year, 12, 31)

    product , charge , actif = 0 , 0 , 0
    accountings   = Accounting.objects.values_list("amount","is_credit","acting").filter(date__gte = start_date  , date__lte = end_date)

    for a in accountings :
        if a[1] and a[2] != None:
            actif += a[0]
        elif a[1] and a[2] == None:
            product += a[0] 
        else :
            charge += a[0]

    result       = actif - charge
    total        = actif + product
        
    context = { 'charge': charge, 'product': product , 'result': result , 'actif': actif , 'total': total ,  'nb_schools': nb_schools ,  
                'nb_schools': nb_schools , 'nb_schools_fr': nb_schools_fr , 'nb_schools_no_fr': nb_schools_no_fr ,  'nb_schools_no_pay': nb_schools_no_pay }  



    return render(request, 'association/accountings.html', context )





@user_passes_test(user_is_board)
def adhesions(request):
    accountings = Accounting.objects.exclude(user_id=None).order_by("-date")
    today = datetime.now()
    this_month = today.month
    this_year = today.year

    first_date_month =  datetime(this_year, this_month, 1)
    first_date_year = datetime(this_year, 1, 1)

    if this_month > 0 and this_month < 8 :
        this_year = this_year - 1
    first_date_schoolyear = datetime(this_year, 9, 1)

    total_month = total(first_date_month, today)
    total_year = total(first_date_year, today)
    total_shoolyear =  total(first_date_schoolyear, today)


    context =  {'accountings': accountings , 'total_month': total_month, 'total_year': total_year, 'total_shoolyear': total_shoolyear ,'this_month' :this_month }
 
    return render(request, 'association/adhesions.html', context )







@user_passes_test(user_is_board)
def list_paypal(request):
    accountings = Accounting.objects.filter(is_paypal=1).order_by("-date")


    today = datetime.now()
    this_month = today.month
    this_year = today.year

    first_date_month =  datetime(this_year, this_month, 1)
    first_date_year = datetime(this_year, 1, 1)

    if this_month > 0 and this_month < 8 :
        this_year = this_year - 1
    first_date_schoolyear = datetime(this_year, 9, 1)

    total_month = total(first_date_month, today)
    total_year = total(first_date_year, today)
    total_shoolyear =  total(first_date_schoolyear, today)


    context =  {'accountings': accountings , 'total_month': total_month, 'total_year': total_year, 'total_shoolyear': total_shoolyear ,'this_month' :this_month }
 
    return render(request, 'association/list_accounting.html', context )



@user_passes_test(user_is_board)
def bank_activities(request):
    context = { }

    return render(request, 'association/bank_activities.html', context )



@user_passes_test(user_is_board)
def bank_bilan(request):
    context = {  }

    return render(request, 'association/bank_bilan.html', context )   

 
 