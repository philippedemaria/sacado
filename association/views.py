from django.shortcuts import render, redirect, get_object_or_404
from association.models import Accounting,Associate , Voting
from association.forms import AccountingForm,AssociateForm,VotingForm


from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from account.decorators import user_is_superuser
from templated_email import send_templated_mail
from django.db.models import Q
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
from cgi import escape
cm = 2.54
#################################################################################
import re
import pytz
from datetime import datetime 
from general_fonctions import *

 
 

#####################################################################################################################################
#####################################################################################################################################
####    accounting
#####################################################################################################################################
#####################################################################################################################################


@user_passes_test(user_is_superuser)
def association_index(request):
    return render(request, 'association/dashboard.html', {  })


@user_passes_test(user_is_superuser)
def list_accountings(request):
    accountings = Accounting.objects.all()
    return render(request, 'association/list_accounting.html', {'accountings': accountings  })


@user_passes_test(user_is_superuser) 
def create_accounting(request):
 
    form = AccountingForm(request.POST or None )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.author = request.user
        nf.save()
        messages.success(request, "Félicitations... Votre compte sacado est maintenant configuré et votre premier accountinge créé !")

        return redirect('association_index')
    else:
        print(form.errors)

    context = {'form': form, }

    return render(request, 'association/form_accounting.html', context)



@user_passes_test(user_is_superuser)
def update_accounting(request, id):

    teacher = Teacher.objects.get(user= request.user)
    accounting = Accounting.objects.get(id=id)
    
    form = accountingTeacherForm(request.POST or None, instance=accounting )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.author = request.user
        return redirect('association_index')
    else:
        print(form.errors)

    context = {'form': form,  'accounting': accounting, 'teacher': teacher,  }

    return render(request, 'accounting/form_accounting.html', context )



@user_passes_test(user_is_superuser)
def delete_accounting(request, id):

    accounting = Accounting.objects.get(id=id)
    accounting.delete()
    return redirect('association_index')
    

@user_passes_test(user_is_superuser)
def show_accounting(request, id ):

    accounting = Accounting.objects.get(id=id)
    context = {  'accounting': accounting,   }

    return render(request, 'association/show_accounting.html', context )





@user_passes_test(user_is_superuser)
def list_associate(request):
    user = request.user
    associates = Associate.objects.filter(is_active = 1)
    pending_associates = Associate.objects.filter(is_active = 0)

    return render(request, 'association/list_associate.html', {'associates': associates , 'pending_associates': pending_associates , 'user' : user })


@user_passes_test(user_is_superuser) 
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



@user_passes_test(user_is_superuser)
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



@user_passes_test(user_is_superuser)
def delete_associate(request, id):

    associate = Associate.objects.get(id=id)
    associate.delete()
    return redirect('list_associate')
    

 
@user_passes_test(user_is_superuser)
def accept_associate(request, id):
    Associate.objects.filter(id=id).update(is_active = 1)
    return redirect('list_associate')


 



@user_passes_test(user_is_superuser) 
def create_voting(request,id):
 
    form = VotingForm(request.POST or None )

    if form.is_valid():
        nf = form.save(commit = False)
        nf.user = request.user
        nf.associate_id = id
        nf.save()

        return redirect('list_associate')
    else:
        print(form.errors)

    context = {'form': form,   }

    return render(request, 'association/form_voting.html', context)


 


 

@user_passes_test(user_is_superuser)
def show_voting(request, id):

    voting = Voting.objects.get(id=id)
    context = {  'voting': voting,   }

    return render(request, 'association/show_voting.html', context)