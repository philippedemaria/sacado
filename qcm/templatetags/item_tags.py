import random
import re
import html
from django import template
register = template.Library()



@register.filter
def index(sequence, position):
    return sequence[position]




@register.simple_tag ## retourne le  score d'un même exercice par élève.
def get_score(obj,student): 
    return obj.send_score(student) 

@register.simple_tag ## retourne les scores d'un même exercice par élève.
def get_scores(obj,student): 
    return obj.send_scores(student)

@register.simple_tag ## retourne  l'heure d'un exerice fait par élève.
def get_timer(obj,student): 
    return obj.timer(student) 

@register.simple_tag ## retourne la liste des scores et l'heure d'un exercice fait par élève.
def get_score_and_time(obj,student): 
    return obj.score_and_time(student) 


@register.simple_tag ## retourne le dernier score et l'heure d'un exercice fait par élève.
def get_last_score_and_time(obj,parcours,student): 
    return obj.last_score_and_time(parcours,student) 




@register.simple_tag ## retourne si un exercice est choisi dans un parcours.
def get_is_selected(obj,parcours): 
    return obj.is_selected(parcours) 

@register.simple_tag ## retourne le pourcentage d'exercices fait sur un parcours.
def get_percent(obj,student): 
    return obj.is_percent(student) 


@register.simple_tag ## teste le nombre d'exercices faits sur un parcours.
def get_done(obj,student): 
    return obj.is_done(student) 


@register.simple_tag ## teste le nombre d'exercices faits sur un parcours.
def get_affect(obj,student): 
    return obj.is_affect(student) 

# @register.simple_tag ##  Renvoie les exercices selon thème d'un élève 
# def get_exercises_by_theme(obj,theme): 
#     return obj.exercises_by_theme(theme) 


@register.simple_tag ##  Renvoie les exercices selon thème d'un élève 
def get_resultexercises_by_theme(obj,theme): 
    return obj.resultexercises_by_theme(theme) 


@register.simple_tag ##  Renvoie les exercices selon thème d'un élève 
def get_resultknowledge_by_theme(obj,theme): 
    return obj.resultknowledge_by_theme(theme) 


@register.filter
def contrast_color(color):
    try :
        color_test = 0.299 * int(color[1:3],16) + 0.587 * int(color[3:5],16) + 0.114 * int(color[5:7],16)
    except :
        try :
            if 'rgba' in color :
                color_tab = color[5:].split(",")
                color_test = 0.299 * int(color[0]) + 0.587 * int(color[1]) + 0.114 * int(color[2])
            else :
                color_test = 10
        except :
            color_test = 10
    if color_test > 200 :
        return "#271942"
    else :
        return "#FFFFFF"



@register.filter
def cleanhtml(arg):
    cleantext = re.sub('<.*?>', '', arg)
    cleantext = re.sub('\n', '', cleantext)
    cleantext = html.unescape(cleantext)
    return cleantext


@register.filter
def time_done(arg): #convertit 1 entier donné  (en secondes) en durée h:m:s
    if arg == "" :
        return arg
    else :
        arg = int(arg)
        if arg < 60 :
            s = arg
            if s < 10 :
                s = "0"+str(s)
            else :
                s = str(s)
            r = s +"s"          
            return r
        if arg < 3600 :
            m = int(arg/60)
            if m<10 :
                m = "0"+str(m)
            else :
                m = str(m)
            s = arg%60
            if s < 10 :
                s = "0"+str(s)
            else :
                s = str(s)
            r = m+"min. "+s +"s"          
            return r
        else :
            h = int(arg/3660)
            if h<10 :
                h = "0"+str(h)
            else :
                h = str(h)
            m = int(arg%60 /60)
            if m<10 :
                m = "0"+str(m)
            else :
                m = str(m)
            s = int((int(arg%3600) - int(arg%60))/100)
            if s < 10 :
                s = "0"+str(s)
            else :
                s = str(s)
            r = str(h)+"h. "+m+"min. "+s +"s"     
            return r



@register.filter
def int_minutes(arg): #convertit 1 entier donné (en minutes) en durée
    if arg == "" :
        r = ""
    else :
        arg = int(arg)
        if arg < 60 :
            h = "00"
            m = arg
        else :
            h = int(arg/60)
            m = arg%60
            if m<10 :
                m = "0"+str(m)
        r = str(h)+"h."+str(m)           

    return r



@register.simple_tag ##  
def get_relationship(obj,parcours): 
    return obj.is_relationship(parcours) 
 
@register.simple_tag ##  
def get_used_in_parcours(obj,teacher): 
    return obj.used_in_parcours(teacher) 

 
@register.simple_tag ##  résultats d'un savoir faire par élève
def get_scorek(obj,student): 
    return obj.send_scorek(student)



@register.simple_tag  
def get_exercises_by_knowledge(obj,student,group): ##  
    return obj.exercices_by_knowledge(student,group)



@register.simple_tag ##  teste si un exerice est uitlisé dans un groupe
def get_exercise_used(obj,group,teacher,theme): 
    return obj.nb_exercise_used(group,teacher,theme)


@register.simple_tag  ##  retourne le score par thème d'un groupe par élève
def get_score_by_theme(obj,student,group): 
    return obj.as_score_by_theme(student,group)


@register.simple_tag ##  retourne le score moyen des exercices par élève d'un groupe
def get_knowledge_average(obj,group): 
    return obj.knowledge_average(group)


@register.simple_tag ##  
def get_knowledge_worked(obj,student): 
    return obj.nb_knowledge_worked(student)


@register.simple_tag ##  retroune le nombre de taches données par groupe
def get_nb_task_done(obj,group): 
    return obj.nb_task_done(group)


@register.simple_tag ## retourne une liste des élèves du groupes qui ont fait l'exercice.
def get_who_are_done(obj,group): 
    return obj.who_are_done(group)


@register.simple_tag ##  retroune le nombre de taches données par parcours
def get_nb_task_parcours_done(obj,parcours): 
    return obj.nb_task_parcours_done(parcours)


@register.simple_tag ## retourne une liste des élèves du parcours qui ont fait l'exercice.
def get_who_are_done_parcours(obj,parcours): 
    return obj.who_are_done_parcours(parcours)



@register.simple_tag ## booleen si l'élève appartient ou pas à un parcours
def get_exercise(obj, exercise): 
    return obj.has_exercise( exercise)

@register.simple_tag ## retourne le nombre d'exercices par parcours publiés.
def get_all_details(obj,parcours): 
    return obj.all_details(parcours)




@register.simple_tag ## booleen si l'élève appartient ou pas à un parcours
def get_in_parcours(obj, parcours): 
    return obj.is_in_parcours( parcours)


 
@register.simple_tag ## donne le score par knowledge 
def get_score_student_parcours(obj,student, parcours): 
    return obj.score_student_parcours(student, parcours)

 
@register.simple_tag ## donne le score par knowledge 
def get_score_student_parcours(obj,student, parcours): 
    return obj.score_student_parcours(student, parcours)


@register.simple_tag ## donne le score par knowledge 
def get_percent_student_done_parcours_exercice(obj, parcours,group_id): 
    return obj.percent_student_done_parcours_exercice(parcours,group_id)




@register.simple_tag ## donne le score par relation 
def get_score_student_for_this(obj, student): 
    return obj.score_student_for_this(student)



@register.simple_tag ## teste si la relationship est sous constrainte pour cet élève
def get_constraint_to_this_relationship(obj, student): 
    return obj.constraint_to_this_relationship(student)



@register.simple_tag ## donne le score par relation
def get_an_association_knowledge_supportfile(obj, supportfile): 
    return obj.association_knowledge_supportfile(supportfile)

@register.simple_tag ## donne le score par relation
def get_parcours_group_students_count(obj, group): 
    return obj.parcours_group_students_count(group)


@register.simple_tag ## 
def get_details(obj,  parcours): 
    return obj.details(parcours)



@register.simple_tag ## donne le score par knowledge 
def get_tasks(obj,  parcours): 
    return obj.is_task_exists(parcours)



@register.simple_tag ## donne le score par knowledge 
def get_result_skills(obj,  skill): 
    return obj.result_skills(skill)