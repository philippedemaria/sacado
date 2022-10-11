
from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.db.models import Q , Sum 
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string
from qcm.models import  *
from socle.models import  Theme, Knowledge , Level , Skill , Waiting , Subject

import uuid
import time
import math
import json
import random
from datetime import datetime , timedelta
from collections import Counter 
################################################################################################################################
################################################################################################################################
############################### KNN fonctions
################################################################################################################################
################################################################################################################################



def get_distance(data1,data2):
    """Calcule la distance"""
    distance = 0.0
    for i in range(len(data1)): 
        distance += (data1[i] - data2[i])**2
    return math.sqrt(distance)


def get_list_distances(dataset,data0):
    """Liste des distances calculées"""
    distances = []
    for data in dataset:
        dist = get_distance(data0, data)
        distances.append((data[2], dist))
    distances.sort(key=lambda tup: tup[1])
    return distances
     
 
def get_final_list(list_distances,k):
    """Liste des k distances conservées"""
    final_list = list()
    for i in range (k) :
        a = list_distances[i][0]
        final_list.append(a)
    return final_list


def prediction(dataset, data0, k):
    """Liste des k distances conservées"""
    list_distances = get_list_distances(dataset,data0)
    final_list = get_final_list(list_distances,k)
    
    pattern = final_list[0]
    i = 0
    for mot in final_list :
        if mot == pattern :
            i+=1
    if i > len(final_list)/2 :
        u_a = pattern
    else :
       u_a = final_list[-1] 
    return u_a

################################################################################################################################
################################################################################################################################
############################### KNN fonctions
################################################################################################################################
################################################################################################################################


def get_knowledges_to_knowledge(k_id):

    # parcours contenant k_id
    parcours_ids = Relationship.objects.values_list("parcours_id", flat=True).filter(exercise__knowledge_id = k_id).distinct()
    list_ex_ids = list(Relationship.objects.values_list("exercise_id", flat=True).filter(parcours_id__in = parcours_ids).order_by("ranking"))

    parcours = Parcours.objects.filter(level_id = 10 , teacher__user_id=2480)
    for  p in parcours :    
        print(p)



    # listing  = {}
    # for ex_id in list_ex_ids :
    #     if ex_id not in listing :
    #         listing[ex_id] =  1
    #     else :
    #         listing[ex_id] +=  1

    # listing = sorted(listing.items(), key=lambda t: t[1])
    # print("k_id" , "exercise.knowledge.id" , " exercise.knowledge.name" , "exercise.id" , "nbo" )
    # for e_id , nbo in listing :
    #     exercise = Exercise.objects.get(pk=e_id)
    #     print(k_id , exercise.knowledge.id , exercise.knowledge.name , exercise.id ,   nbo )

    return parcours_ids # liste des parcours





def get_e_list(parcourses,all_exercise_ids):
    """Convertit des parcours en liste de bytes dont un 1 représente un exo commun""" 

    list_positions={}
    for i,e_id in enumerate(all_exercise_ids) :
        list_positions[e_id]=i

    i = 0    
    e_list = [[0]*len(all_exercise_ids)]*len(parcourses)
    for p in parcourses :
        this_list = [0]*len(all_exercise_ids)
        p_exercise_ids = p.parcours_relationship.values_list("exercise_id",flat=True).filter(exercise__supportfile__is_title=0)# liste des ids des exos du parcours p
        for e_id in p_exercise_ids :
            if e_id in list_positions :
                this_list[list_positions[e_id]]=e_id
   
        e_list[i] = this_list
        i+=1

    return e_list
 

def compare(parcours0,parcourses):
    """Convertit des parcours en liste de bytes dont un 1 représente un exo commun""" 

    pattern = set(parcours0.parcours_relationship.values_list("exercise_id",flat=True).filter(exercise__supportfile__is_title=0).order_by("exercise_id"))
    dp = int(len(pattern)*0.8)
    e_list = []




    for p in parcourses :
        p_exercise_ids = p.parcours_relationship.values_list("exercise_id",flat=True).filter(exercise__supportfile__is_title=0).order_by("exercise_id")
        inter = set(p_exercise_ids).intersection(pattern)

        if len(inter) > dp :
            e_list+= list(p_exercise_ids)
 
    counter = Counter(e_list)

    print( counter.most_common() )  
    print( list(parcours0.parcours_relationship.values_list("exercise_id",flat=True).filter(exercise__supportfile__is_title=0).order_by("exercise_id") )) 
    return e_list




def get_parcourses_to_parcours(p_id):

    parcours         = Parcours.objects.get(pk = p_id)
    all_parcours     = Parcours.objects.filter(level=parcours.level, subject=parcours.subject).exclude(teacher=parcours.teacher)
    all_exercise_ids = Exercise.objects.values_list("id",flat=True).filter(level=parcours.level, theme__subject=parcours.subject, supportfile__is_title=0).order_by("id")
    
    # parcours_list = get_e_list(all_parcours,all_exercise_ids)# liste des parcours ayant au moins 1 exo en commun avec le parcours de réf
    # parcours0     = get_e_list([parcours],all_exercise_ids)[0]

    compare(parcours, all_parcours)

    # for p in parcours_list :
    #     difflib.SequenceMatcher(None, parcours_list, parcours0).ratio()




    # final_parcours_list = [] 
    # for fp in parcours_list :
    #     for i in range(len(fp)) :
    #         if fp not in final_parcours_list and  parcours0[i]==fp[i] and fp[i] == 1 :
    #             final_parcours_list.append(fp) # liste des parcours ayant au moins 1 exo au même endroit avec le parcours de réf

    # last_exo_ids = [0]*len(final_parcours_list[0])

    # for fpl in final_parcours_list :
    #     for i in range(len(fpl)) :
    #         last_exo_ids[i] += fpl[i]

    # list_exercises_ids = []
    # for i in range(len(all_exercise_ids))  :
    #     if last_exo_ids[i] > 10 :
    #         list_exercises_ids.append(all_exercise_ids[i])

    # print(list_exercises_ids, len(list_exercises_ids))

    return #list_exercises_ids # liste des parcours

