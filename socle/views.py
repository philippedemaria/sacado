from django.http import HttpResponse
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from socle.models import  Knowledge, Level, Theme, Skill , Waiting
from socle.forms import  LevelForm, KnowledgeForm,  ThemeForm,MultiKnowledgeForm , SkillForm, MultiSkillForm , WaitingForm , MultiWaitingForm
from account.models import Teacher, Student
from django.contrib import messages
from account.decorators import user_can_create
from .decorators import user_is_superuser
from general_fonctions import *
import re


@user_is_superuser
def list_themes(request):
 
    themes = Theme.objects.all()

    return render(request, 'socle/list_themes.html', {'themes': themes, 'communications' : [] , })

@user_is_superuser 
def create_theme(request):

    form = ThemeForm(request.POST or None  )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le thème a été créé avec succès !')
        return redirect('themes')
    else:
        print(form.errors)

    context = {'form': form, 'communications' : [] , 'theme': None  }

    return render(request, 'socle/form_theme.html', context)

@user_is_superuser 
def update_theme(request, id):

    theme = Theme.objects.get(id=id)
    theme_form = ThemeForm(request.POST or None, instance=theme )
    if request.method == "POST" :
        if theme_form.is_valid():
            theme_form.save()
            messages.success(request, 'Le thème a été modifié avec succès !')
            return redirect('themes')
        else:
            print(theme_form.errors)

    context = {'form': theme_form, 'communications' : [] , 'theme': theme,   }

    return render(request, 'socle/form_theme.html', context )


@user_is_superuser 
def delete_theme(request, id):
    theme = Theme.objects.get(id=id)
    theme.delete()
    return redirect('themes')



@user_is_superuser 
def list_knowledges(request):
 
    knowledges = Knowledge.objects.all().select_related('theme', 'level').prefetch_related('exercises')

    return render(request, 'socle/list_knowledges.html', {'communications' : [] , 'knowledges': knowledges})

@user_is_superuser 
def create_knowledge(request):

    form = KnowledgeForm(request.POST or None  )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le savoir faire a été créé avec succès !')
        return redirect('knowledges')
    else:
        print(form.errors)

    context = {'form': form,  'communications' : [] , 'knowledge': None  }

    return render(request, 'socle/form_knowledge.html', context)

@user_is_superuser 
def create_multi_knowledge(request):

    form = MultiKnowledgeForm(request.POST or None  )
    if request.method == "POST" :
        if form.is_valid():
            theme = form.cleaned_data["theme"]
            level = form.cleaned_data["level"]
            names = form.cleaned_data["name"].split("\r")
            for name in names :
                Knowledge.objects.create(name=cleanhtml(name),theme=theme,level=level)
 
            messages.success(request, 'Les savoir faire ont été créés avec succès !')
            return redirect('knowledges')
        else:
            print(form.errors)

    context = {'form': form, 'communications' : [] ,  'knowledge': None   }

    return render(request, 'socle/form_knowledge.html', context)



@user_is_superuser
def update_knowledge(request, id):

    knowledge = Knowledge.objects.get(id=id)
    knowledge_form = KnowledgeForm(request.POST or None, instance=knowledge )
    if request.method == "POST" :
        if knowledge_form.is_valid():
            knowledge_form.save()
            messages.success(request, 'Le savoir faire a été modifié avec succès !')
            return redirect('knowledges')
        else:
            print(knowledge_form.errors)

    context = {'form': knowledge_form, 'communications' : [] , 'knowledge': knowledge,   }

    return render(request, 'socle/form_knowledge.html', context )

@user_is_superuser
def delete_knowledge(request, id):
    knowledge = Knowledge.objects.get(id=id)
    knowledge.delete()
    return redirect('knowledges')


@user_is_superuser
def list_levels(request):
 
    levels = Level.objects.all()

    return render(request, 'socle/list_levels.html', {'communications' : [] ,'levels': levels})

@user_is_superuser
def create_level(request):

    form = LevelForm(request.POST or None  )
    teacher = Teacher.objects.get(user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Le savoir faire a été créé avec succès !')
        return redirect('levels')
    else:
        print(form.errors)

    context = {'form': form,  'level': None , 'communications' : [] , 'teacher': teacher }

    return render(request, 'socle/form_level.html', context)

@user_is_superuser
def update_level(request, id):
    
    teacher = Teacher.objects.get(user=request.user)
    level = Level.objects.get(id=id)
    level_form = LevelForm(request.POST or None, instance=level )
    if request.method == "POST" :
        if level_form.is_valid():
            level_form.save()
            messages.success(request, 'Le savoir faire a été modifié avec succès !')
            return redirect('levels')
        else:
            print(level_form.errors)

    context = {'form': level_form,  'level': level, 'communications' : [] ,'teacher': teacher  }

    return render(request, 'socle/form_level.html', context )

@user_is_superuser
def delete_level(request, id):
    level = Level.objects.get(id=id)
    level.delete()
    return redirect('levels')
 
 

 


@user_is_superuser 
def create_multi_skill(request):

    form = MultiSkillForm(request.POST or None  )
    if request.method == "POST" :
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            names = form.cleaned_data["name"].split("\r")
            for name in names :
                Skill.objects.create(name=cleanhtml(name),subject=subject)
 
            messages.success(request, 'Les compétences ont été créées avec succès !')
            return redirect('skills')
        else:
            print(form.errors)

    context = {'form': form, 'communications' : [] ,  'skill': None   }

    return render(request, 'socle/form_skill.html', context)



@user_is_superuser
def update_skill(request, id):

    skill = Skill.objects.get(id=id)
    skill_form = SkillForm(request.POST or None, instance=skill )
    if request.method == "POST" :
        if skill_form.is_valid():
            skill_form.save()
            messages.success(request, 'Le savoir faire a été modifié avec succès !')
            return redirect('skills')
        else:
            print(skill_form.errors)

    context = {'form': skill_form, 'communications' : [] , 'skill': skill,   }

    return render(request, 'socle/form_skill.html', context )

@user_is_superuser
def delete_skill(request, id):
    skill = Skill.objects.get(id=id)
    skill.delete()
    return redirect('skills')


@user_is_superuser
def list_skills(request):
 
    skills = Skill.objects.order_by("subject")
    return render(request, 'socle/list_skills.html', {'communications' : [] ,'skills': skills})





@user_is_superuser 
def list_waitings(request):
 
    waitings = Waiting.objects.all().select_related('theme') 

    return render(request, 'socle/list_waitings.html', {'communications' : [] , 'waitings': waitings})

@user_is_superuser 
def create_waiting(request):

    form = WaitingForm(request.POST or None  )

    if form.is_valid():
        form.save()
        messages.success(request, "L'attendu a été créé avec succès !")
        return redirect('waitings')
    else:
        print(form.errors)

    context = {'form': form,  'communications' : [] , 'waiting': None  }

    return render(request, 'socle/form_waiting.html', context)

@user_is_superuser 
def create_multi_waiting(request):

    form = MultiWaitingForm(request.POST or None  )
    if request.method == "POST" :
        if form.is_valid():
            theme = form.cleaned_data["theme"]
            level = form.cleaned_data["level"]
            names = form.cleaned_data["name"].split("\r")
            for name in names :
                Waiting.objects.create( name=cleanhtml(name), theme=theme, level=level )
 
            messages.success(request, "Les attendu ont été créés avec succès !")
            return redirect('waitings')
        else:
            print(form.errors)

    context = {'form': form, 'communications' : [] ,  'waiting': None   }

    return render(request, 'socle/form_waiting.html', context)



@user_is_superuser
def update_waiting(request, id):

    waiting = Waiting.objects.get(id=id)
    waiting_form = WaitingForm(request.POST or None, instance=waiting )
    if request.method == "POST" :
        if waiting_form.is_valid():
            waiting_form.save()
            messages.success(request, "L'attendu a été créé avec succès !")
            return redirect('knowledges')
        else:
            print(waiting_form.errors)

    context = {'form': waiting_form, 'communications' : [] , 'waiting': waiting,   }

    return render(request, 'socle/form_waiting.html', context )

@user_is_superuser
def delete_waiting(request, id):
    waiting = Waiting.objects.get(id=id)
    waiting.delete()
    return redirect('waitings')



 
def ajax_chargewaitings(request):
    id_level =  request.POST.get("id_level")
    id_theme =  request.POST.get("id_theme")

    data = {}
    level =  Level.objects.get(pk = int(id_level))
    theme =  Theme.objects.get(pk = int(id_theme))

    waitings = Waiting.objects.values_list('id', 'name').filter(level=level, theme=theme)

    data['waitings'] = list(waitings)
 
    return JsonResponse(data)
