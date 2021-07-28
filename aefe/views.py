from django.shortcuts import render
from django.conf import settings # récupération de variables globales du settings.py
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Testhistoric
from qcm.models import Parcours
import uuid

 

def aefe(request):

    teacher = request.user.teacher

    p_sixieme = [7367,7368,7369] #### A modifier en dur
    p_seconde = [7371,7372,7373,7374,7375] #### A modifier en dur

    parcours_sixieme = Parcours.objects.filter(id__in=p_sixieme) 
    parcours_seconde = Parcours.objects.filter(id__in=p_seconde)
 
    groupes_sixieme = request.user.teacher.groups.filter(level=6)
    groupes_seconde = request.user.teacher.groups.filter(level=10)

    context = {  'teacher' : teacher ,  'parcours_sixieme' : parcours_sixieme , 'parcours_seconde' : parcours_seconde , 'groupes_sixieme' : groupes_sixieme , 'groupes_seconde' : groupes_seconde }

    return render(request, 'aefe/aefe.html', context)




def get_this_parcours_aefe(request,id):

    parcours = Parcours.objects.get(pk=id)
 
    relationships = parcours.parcours_relationship.all() 
    teacher = request.user.teacher

    parcours.pk = None
    parcours.teacher = teacher
    parcours.is_publish = 1
    parcours.is_leaf = 0
    parcours.is_archive = 0
    parcours.is_share = 0
    parcours.is_favorite = 1
    parcours.code = str(uuid.uuid4())[:8]  
    parcours.save()

    level = parcours.level
    groups =  teacher.groups.filter(level=level)
 
    for g in groups :
        parcours.groups.add(g)
        student_list = list(g.students.all())
        parcours.students.add(*student_list)
        
 
        for r in relationships:
            try :
                r.pk = None
                r.parcours = parcours
                r.save()  
                r.students.add(*student_list)
            except :
                pass

    parcours_old = Parcours.objects.get(pk=id)
    Testhistoric.objects.get_or_create(teacher = teacher, clone = parcours , origin =  parcours_old )

    messages.success(request,"Parcours de remédiation attribué")

    return redirect ('aefe')

 
