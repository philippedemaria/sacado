from django.http import HttpResponse
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from socle.models import  Knowledge, Level, Theme
from socle.forms import  LevelForm, KnowledgeForm,  ThemeForm,MultiKnowledgeForm
from account.models import Teacher, Student
from django.contrib import messages
from account.decorators import user_can_create, user_is_superuser

import re


def cleanhtml(raw_html): #nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    cleantext = re.sub('\t', '', cleantext)
    return cleantext




def list_themes(request):
 
    themes = Theme.objects.all()

    return render(request, 'socle/list_themes.html', {'themes': themes})


def create_theme(request):

    form = ThemeForm(request.POST or None  )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le thème a été créé avec succès !')
        return redirect('themes')
    else:
        print(form.errors)

    context = {'form': form, 'theme': None  }

    return render(request, 'socle/form_theme.html', context)


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

    context = {'form': theme_form,  'theme': theme,   }

    return render(request, 'socle/form_theme.html', context )



def delete_theme(request, id):
    theme = Theme.objects.get(id=id)
    theme.delete()
    return redirect('themes')




def list_knowledges(request):
 
    knowledges = Knowledge.objects.all().select_related('theme', 'level').prefetch_related('exercises')

    return render(request, 'socle/list_knowledges.html', {'knowledges': knowledges})


def create_knowledge(request):

    form = KnowledgeForm(request.POST or None  )

    if form.is_valid():
        form.save()
        messages.success(request, 'Le savoir faire a été créé avec succès !')
        return redirect('knowledges')
    else:
        print(form.errors)

    context = {'form': form,  'knowledge': None  }

    return render(request, 'socle/form_knowledge.html', context)



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

    context = {'form': form,  'knowledge': None   }

    return render(request, 'socle/form_knowledge.html', context)




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

    context = {'form': knowledge_form,  'knowledge': knowledge,   }

    return render(request, 'socle/form_knowledge.html', context )


def delete_knowledge(request, id):
    knowledge = Knowledge.objects.get(id=id)
    knowledge.delete()
    return redirect('knowledges')



def list_levels(request):
 
    levels = Level.objects.all()

    return render(request, 'socle/list_levels.html', {'levels': levels})


def create_level(request):

    form = LevelForm(request.POST or None  )
    teacher = Teacher.objects.get(user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Le savoir faire a été créé avec succès !')
        return redirect('levels')
    else:
        print(form.errors)

    context = {'form': form,  'level': None , 'teacher': teacher }

    return render(request, 'socle/form_level.html', context)


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

    context = {'form': level_form,  'level': level, 'teacher': teacher  }

    return render(request, 'socle/form_level.html', context )


def delete_level(request, id):
    level = Level.objects.get(id=id)
    level.delete()
    return redirect('levels')
 
 

 