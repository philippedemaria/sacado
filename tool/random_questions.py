from tool.models import * 
from random import  randint, shuffle
import math



def additionne_str(a,b,c=0,d=0,e=0):
	if a and b and c and d and e :
		title  = "Additionne les nombres "+str(a)+", "+str(b)+", "+str(c)+", "+str(d)+" et "+str(e)
		answer = a + b + c + d + e
	elif a and b and c and d  :
		title  = "Additionne les nombres "+str(a)+", "+str(b)+", "+str(c)+" et "+str(d)
		answer = a + b + c + d
	elif a and b and c :
		title  = "Additionne les nombres "+str(a)+", "+str(b)+" et "+str(c)
		answer = a + b + c 
	elif a and b :
		title  = "Additionne les nombres "+str(a)+" et "+str(b)
		answer = a + b
	return title, answer

def goto_str(a,b):
	title  = "Combien pour aller de "+str(a)+" à "+str(b)+" ?" 
	answer =  b-a
	return title, answer


def soustraire_str(a,b,c=0,d=0,e=0):
	if a and b and c and d and e :
		title  = "Soustrais  les nombres "+str(a)+", "+str(b)+", "+str(c)+", "+str(d)+" et "+str(e)
		answer = a + b + c + d + e
	elif a and b and c and d  :
		title  = "Soustrais les nombres "+str(a)+", "+str(b)+", "+str(c)+" et "+str(d)
		answer = a + b + c + d
	elif a and b and c :
		title  = "Soustrais les nombres "+str(a)+", "+str(b)+" et "+str(c)
		answer = a + b + c 
	elif a and b :
		title  = "Soustrais les nombres "+str(a)+" et "+str(b)
		answer = a + b 
	return title, answer


def multiplie_str(n,m) :
	title  = "Multiplie les nombres "+str(n)+" et "+str(m)
	answer = n*m
	return title, answer

def fraction_add(n,m,p,q=0,e=0):
	if q==0 : q=m
	title  = "Calcule $\frac{"+str(n)+"}{"+str(m)+"} + \frac{"+str(p)+"}{"+str(q)+"}$"  
	if e==1 : answer = round(n/m + p/q,1)
	else : answer = str(n)+"##"+str(m)+"##"+str(p)+"##"+str(q)
	return title, answer

def fraction_sub(n,m,p,q=0,e=0):
	if q==0 : q=m
	title  = "Calcule $\frac{"+str(n)+"}{"+str(m)+"} + \frac{"+str(p)+"}{"+str(q)+"}$"  
	if e==1 : answer = round(n/m + p/q,1)
	else : answer = str(n)+"##"+str(m)+"##"+str(p)+"##"+str(q)
	return title, answer


def frac(n,m):
	frac_str  = "\frac{"+str(n)+"}{"+str(m)+"}"  
	return frac_str

def fraction_irreductible(n,m,p,q=0,e=0):
	if q==0 : q=m
	title  = "Calcule $\frac{"+str(n)+"}{"+str(m)+"} + \frac{"+str(p)+"}{"+str(q)+"}$"  
	if e==1 : answer = round(n/m + p/q,1)
	else : answer = str(n)+"##"+str(m)+"##"+str(p)+"##"+str(q)
	return title, answer



def create_questions_flash_random_variable(m_ids,quizz) :

	nb_slide    = quizz.nb_slide
	list_of_ids = [0]*nb_slide
	length = len(m_ids)
	i , j = 0 , 0
	while i < nb_slide :
		for j in range (length) :
			list_of_ids[i] = int(m_ids[j])
			i+=1
			if i == nb_slide  : break
				
	shuffle(list_of_ids) # la liste des ids des questions flash

	for mental_id in list_of_ids :
		mental = Mental.objects.get(pk=mental_id)
		#title, answer = mental.script alea_content(mental_id)
		variables  = dict()
		exec(mental.script,globals(),variables)
		title    = variables['title']
		answer   = variables['answer']
		wanswer  = variables['wans']
		question = Question.objects.create(title = title, answer = answer, mental_id = mental_id, qtype=2 , size = 48, writinganswer = wanswer)
		quizz.questions.add(question)


 


