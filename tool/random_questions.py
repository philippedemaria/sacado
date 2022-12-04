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


def alea_content(mental_id):
	if mental_id == 1 : #1) Additionner sans retenue deux nombres de 2 chiffres plus petits que 30
		a = randint(0,9)
		b = randint(0,9 - a)
		c = randint(1,2)*10
		d = randint(1,2)*10
		n = c+a
		m = d+b
		title, answer  = additionne_str(n,m)

	elif mental_id == 2 : #2) Additionner des dizaines entières
		n = randint(1,9)*10
		m = randint(1,9)*10
		title, answer  = additionne_str(n,m)

	elif mental_id == 3 :#3) Calculer des sommes : ajouter 9 (nombres inférieurs à 100)
		n      = randint(1,100)
		title, answer  = additionne_str(n,9)

	elif mental_id == 4 :#4) Additionner 3 nombres à 1 chiffre
		n = randint(1,9)
		m = randint(1,9)
		p = randint(1,9)
		title, answer  = additionne_str(n,m,p)

	elif mental_id == 5 :#5) Calculer mentalement des sommes de deux nombres de dizaines et unités, sans retenue, et au résultat plus petit que 100
		pass
		
	elif mental_id == 6 :#6) Additionner 2 nombres à 1 chiffre avec 1 nombre à 2 chiffres
		n = randint(1,9)
		m = randint(1,9)
		p = randint(10,99)
		title, answer  = additionne_str(n,m,p)

	elif mental_id == 7 :#7) Additionner 2 nombres à 2 chiffres
		n = randint(10,99)
		m = randint(10,99)
		title, answer  = additionne_str(n,m)

	elif mental_id == 8 :#8) Additionner 1 nombre à 2 chiffres avec 1 nombre à 1 chiffre
		n = randint(10,99)
		m = randint(1,9)
		title, answer  = additionne_str(n,m)
		
	elif mental_id == 9 :#9) Additionner 3 nombres à 2 chiffres
		n = randint(10,99)
		m = randint(10,99)
		p = randint(10,99)
		title, answer  = additionne_str(n,m,p) 

	elif mental_id == 10 :#10) Additionner un nombre se terminant par 8 avec 1 nombre à 2 chiffres pris au hasard
		n = randint(1,9)*10 + 8
		m = randint(10,20)
		title, answer  = additionne_str(n,m ) 

	elif mental_id == 11 :#11) Additionner un nombre se terminant par 9 avec 1 nombre à 2 chiffres pris au hasard
		n = randint(1,9)*10 + 9
		m = randint(10,20)
		title, answer  = additionne_str(n,m ) 

	elif mental_id == 12 : #12) Additionner 2 nombres à 2 chiffres avec 1 nombre à 1 chiffre
		n = randint(10,99)
		m = randint(10,99)
		p = randint(1,9)
		title, answer  = additionne_str(n,m,p) 

	elif mental_id == 13 : #13) Additionner 2 nombres à 2 chiffres avec 2 nombre à 1 chiffre
		n = randint(10,99)
		m = randint(10,99)
		p = randint(1,9)
		q = randint(1,9)
		title, answer  = additionne_str(n,m,p,q) 

	elif mental_id == 14 : #14) Additionner 3 nombres à 2 chiffres avec 1 nombre à 1 chiffre
		n = randint(10,99)
		m = randint(10,99)
		p = randint(10,99)
		q = randint(1,9)
		title, answer  = additionne_str(n,m,p,q) 

	elif mental_id == 15 : #15) Additionner 3 nombres à 2 chiffres
		n = randint(10,99)
		m = randint(10,99)
		p = randint(10,99)
		title, answer  = additionne_str(n,m,p) 

	elif mental_id == 16 : #16) Additionner 2 nombres < 100 à 1 décimale chacun
		n = randint(1,99) + randint(1,9)*0.1
		m = randint(1,99) + randint(1,9)*0.1
		title, answer  = additionne_str(n,m ) 

	elif mental_id == 17 : #17) Additionner 2 nombres < 100 à 2 décimale chacun
		n = randint(1,99) + randint(11,99)*0.01
		m = randint(1,99) + randint(11,99)*0.01
		title, answer  = additionne_str(n,m ) 

	elif mental_id == 18 : #18) Trouver le complément à 10
		n = randint(1,9)
		title, answer  = goto_str(n,10)  

	elif mental_id == 19 : #19) Trouver le complément à 100
		n = randint(1,99)
		title, answer  = goto_str(n,100) 

	elif mental_id == 20 :#20) Connaitre les compléments à la dizaine supérieure
		d = randint(0,9)*10 
		n = d + randint(0,9)
		m = d + 10
		title, answer  = goto_str(n,m) 
		print(title, answer)

	elif mental_id == 21 :#21) Trouver le complément à 1000
		n = randint(1,999)
		title, answer  = goto_str(n,1000) 

	elif mental_id == 22 :#22) Compléter un nombre à 1 décimale < 100 à l'unité supérieure
		u = randint(1,99) 
		n = u + randint(1,9)*0.1
		m = u + 1
		title, answer  = goto_str(n,m) 

	elif mental_id == 23 :#23) Compléter un nombre à 1 décimale < 100 à la dizaine supérieure
		d = randint(0,9)*10
		n = d + randint(1,9) + randint(1,9)*0.1
		m = d + 10
		title, answer  = goto_str(n,m) 

	elif mental_id == 24 :#24) Compléter un nombre à 1 décimale < 100 à la centaine supérieure
		c = randint(0,9)*100
		n = d + randint(1,99) + randint(1,9)*0.1
		m = c + 100
		title, answer  = goto_str(n,m) 

	elif mental_id == 25 :#25) Compléter un nombre à 2 décimales < 100 à l'unité supérieure
		u = randint(1,99) 
		n = u + randint(1,99)*0.01
		m = u + 1
		title, answer  = goto_str(n,m) 

	elif mental_id == 26 :#26) Compléter un nombre à 2 décimales < 100 à la dizaine supérieure
		d = randint(0,9)*10
		n = d + randint(1,9) + randint(1,99)*0.01
		m = d + 10
		title, answer  = goto_str(n,m) 

	elif mental_id == 27 :#27) Compléter un nombre à 2 décimales < 100 à la centaine supérieure
		c = randint(0,9)*100
		n = d + randint(1,99) + randint(1,99)*0.01
		m = c + 100
		title, answer  = goto_str(n,m)

	elif mental_id == 28 :#28) Calculer des différences entre des nombres inférieurs à 10
		n = randint(0,9)
		m = randint(n,9)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 29 :#29) Soustraire des dizaines entières (inférieur à 100)
		n = randint(0,9)*10
		m = randint(n,9)*10
		title, answer  = soustraire_str(m,n)

	elif mental_id == 30 :#30) Calculer des différences : retirer 9 (nombres inférieurs à 100)
		n = randint(9,99)
		title, answer  = soustraire_str(n,9)

	elif mental_id == 31 :#31) Soustraire 1 nombre à 1 chiffre d'1 nombre à 2 chiffres
		n = randint(1,9)
		m = randint(10,99)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 32 :#32) Soustraire 2 nombres à 2 chiffres
		n = randint(0,9)*10  + randint(1,9)
		m = randint(n,99)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 33 :#33) Soustraire un nombre se terminant par 8 et un nombre à 2 chiffres
		if randint(0,1)==0 :
			m = randint(0,9)*10  + 8
			n = randint(1,m)
		else :
			n = randint(0,9)*10  + 8
			m = randint(n,99)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 34 :#34) Soustraire un nombre se terminant par 9 d' un nombre à 2 chiffres
		if randint(0,1)==0 :
			m = randint(0,9)*10  + 9
			n = randint(1,m)
		else :
			n = randint(0,9)*10  + 9
			m = randint(n,99)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 35 :#35) Soustraire 1 nombre à 1 chiffre d'un nombre à 3 chiffres
		m = randint(100,999)
		n = randint(1,9)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 36 :#36) Soustraire 1 nombre à 2 chiffres d'un nombre à 3 chiffres
		m = randint(100,999)
		n = randint(10,99)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 37 :#37) Soustraire 1 nombre à 3 chiffres d'un nombre à 3 chiffres
		n = randint(100,999)
		m = randint(n,999)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 38 :#38) Soustraire un nombre se terminant par 8 d'un nombre à 3 chiffres
		n = randint(0,9)*100  + randint(0,9)*10  + 8
		m = randint(n,999)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 39 :#39) Soustraire un nombre se terminant par 9 d'un nombre à 3 chiffres
		n = randint(0,9)*100  + randint(0,9)*10  + 9
		m = randint(n,999)
		title, answer  = soustraire_str(m,n)

	elif mental_id == 40 :#40) Connaitre les doubles des nombres inférieurs à 10
		n = randint(0,9)
		title  = "Donne le double de " +str(n)
		answer = 2*n

	elif mental_id == 41 :#41) Connaître les tables de multiplication par 2, 3, 4 et 5, 6, 7, 8, 9, 10
		n = randint(2,4)
		m = randint(5,10)
		title, answer  = multiplie_str(m,n)

	elif mental_id == 42 :#42) Connaitre les doubles des nombres d’usage courant inférieurs à 100 et se terminant par 0 ou 5
		if randint(0,1)==0:u=0
		else :u=5
		n = randint(1,9)*10 + u
		title  = "Donne le double de "+str(n)
		answer = 2*n

	elif mental_id == 43 :#43) Connaitre les doubles des nombres inférieurs à 100
		n = randint(1,99)
		title  = "Donne le double de "+str(n)
		answer = 2*n

	elif mental_id == 44:#44) Etre interrogé(e) sur les tables jusqu'à 11
		n = randint(2,11)
		m = randint(2,10)
		title, answer  = multiplie_str(m,n)

	elif mental_id == 45 :#45) Etre interrogé(e) sur la table de 2
		m = randint(2,10)
		title, answer  = multiplie_str(m,2)

	elif mental_id == 46 :#46) Etre interrogé(e) sur la table de 3
		m = randint(2,10)
		title, answer  = multiplie_str(m,3)

	elif mental_id == 47 :#47) Etre interrogé(e) sur la table de 4
		m = randint(2,10)
		title, answer  = multiplie_str(m,4)

	elif mental_id == 48 :#48) Etre interrogé(e) sur la table de 5
		m = randint(2,10)
		title, answer  = multiplie_str(m,5)

	elif mental_id == 48 :#49) Etre interrogé(e) sur la table de 6
		m = randint(2,10)
		title, answer  = multiplie_str(m,6)

	elif mental_id == 50 :#50) Etre interrogé(e) sur la table de 7
		m = randint(2,10)
		title, answer  = multiplie_str(m,7)

	elif mental_id == 51 :#51) Etre interrogé(e) sur la table de 8
		m = randint(2,10)
		title, answer  = multiplie_str(m,8)

	elif mental_id == 52 :#52) Etre interrogé(e) sur la table de 9
		m = randint(2,10)
		title, answer  = multiplie_str(m,9)

	elif mental_id == 53 :#53) Etre interrogé(e) sur la table de 10
		m = randint(2,10)
		title, answer  = multiplie_str(m,10)

	elif mental_id == 54 :#54) Etre interrogé(e) sur la table de 11
		m = randint(2,10)
		title, answer  = multiplie_str(m,11)

	elif mental_id == 55 :#55) Trouver le double ou le triple d'un nombre à 2 chiffres
		n = randint(10,99)
		if randint(0,1)==0: 
			m = 3*n
			title, answer  =  "Calcule le le triple de "+ n , m
		else : 
			m = 2*n
			title, answer  =  "Calcule le double de "+ n , m
	
	elif mental_id == 56 :#56) Etre interrogé(e) sur les tables jusqu'à 12, les nombres pouvant etre terminés par des zéros
		n = randint(2,12)
		m = randint(2,10)
		title, answer  = multiplie_str(m,n)

	elif mental_id == 57 :#57) Etre interrogé(e) sur les tables jusqu'à 12 et tables de 15,25; les nombres pouvant etre terminés par des zéros
		r = randint(0,12)
		liste = [2,3,4,5,6,7,8,9,10,11,12,15,25]
		n = liste[r]
		m = randint(2,10)
		title, answer  = multiplie_str(m,n)

	elif mental_id == 58 :#58) Etre interrogé(e) sur la table de 15
		m = randint(2,10)
		title, answer  = multiplie_str(m,15)
	
	elif mental_id == 59 :#59) Etre interrogé(e) sur la table de 25
		m = randint(2,10)
		title, answer  = multiplie_str(m,15)

	elif mental_id == 60 :#60) Trouver le quotient et le reste d'un nombre à 2 ou 3 chiffres divisé par un nombre inférieur ou égal à 11
		n = randint(10,999)
		d = randint(2,11)
		q = n//d
		r = n%d
		title, answer  = "Calcule le quotient et le reste de "+str(n)+" divisé par "+str(d), str(q)+"##"+str(r)
	
	elif mental_id == 61 :#61) Trouver le quotient et le reste d'un nombre à 2 ou 3 chiffres divisé par un nombre inférieur ou égal à 11, le reste étant nul
		d = randint(2,11)
		q = randint(5,90)
		title, answer  = "Calcule le quotient et le reste de "+str(d*q)+" divisé par "+str(d), q

	elif mental_id == 62 :#62) Trouver le quotient et le reste d'un nombre à 2 chiffres divisé par un nombre à 1 chiffre
		n = randint(10,99)
		d = randint(2,9)
		q = n//d
		r = n%d
		title, answer  = "Calcule le quotient et le reste de "+str(n)+" divisé par "+str(d), str(q)+"##"+str(r)

	elif mental_id == 63 :#63) Trouver le quotient d'un nombre à 2 chiffres divisé par un nombre à 1 chiffre, le reste étant nul
		d = randint(2,11)
		q = randint(2,9)
		title, answer  = "Calcule le quotient et le reste de "+str(d*q)+" divisé par "+str(d), q

	elif mental_id == 64 :#64) Connaitre les moitiés de nombres d'usage courant inférieurs à 100 et se terminant par 0 ou 5
		if randint(0,1)==0: 
			a = 2*(n+5)
			title, answer  =  "Calcule le moitié de "+ str(a) , n + 5
		else :  
			a = 2*n 
			title, answer  =  "Calcule le moitié de "+ str(a) , n

	elif mental_id == 65 : # Additionner 2 fractions de même dénominateur 
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		j = randint(0,9)
		p = liste[j]
		title, answer  = fraction_add(n,m,p)

	elif mental_id == 66 : # Additionner 2 fractions de même dénominateur (puissance de 10)
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		pui = 10**randint(1,3)
		j = randint(0,9)
		p = liste[j]*pui
		title, answer  = fraction_add(n,m,p)

	elif mental_id == 67 : # Additionner 2 fractions de dénominateur mutiple
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		j = randint(0,9)
		p = liste[j]
		q = liste[j] * randint(2,9)
		title, answer  = fraction_add(n,m,p,q)

	elif mental_id == 68 : # Additionner 2 fractions de dénominateur différent
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		j = randint(0,9)
		k = randint(0,9)
		p = liste[j]
		q = liste[k] 
		title, answer  = fraction_add(n,m,p,q)

	elif mental_id == 69 : # Soustraire 2 fractions de même dénominateur
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		j = randint(0,9)
		p = liste[j]
		title, answer  = fraction_sub(n,m,p)

	elif mental_id == 70 : # Soustraire 2 fractions de même dénominateur(puissance de 10)
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		pui = 10**randint(1,3)
		j = randint(0,9)
		p = liste[j]*pui
		title, answer  = fraction_sub(n,m,p)

	elif mental_id == 71 : # Soustraire 2 fractions de dénominateur mutiple
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		j = randint(0,9)
		p = liste[j]
		q = liste[j] * randint(2,9)
		title, answer  = fraction_sub(n,m,p,q)

	elif mental_id == 72 : # soustraire 2 fractions de dénominateur différent
		n = randint(1,20)
		m = randint(1,20)
		liste = [i for i in range(1,10)]
		j = randint(0,9)
		k = randint(0,9)
		p = liste[j]
		q = liste[k] 
		title, answer  = fraction_sub(n,m,p,q)

	elif mental_id == 73 : # simplifier une fraction inférieure dont les numérateurs et dénominateurs sont inférieurs à 100  
		nume = [i for i in range(2,100)]
		deno = [i for i in range(2,100)]
		j = randint(0,97)
		k = randint(0,97)
		n = nume[j]
		m = deno[k] 
		pgcd = math.gcd(n, m)
		title, answer  = "Simplifie la fraction "+frac(n,m), str(n//pgcd)+"##"+str(m//pgcd)

	elif mental_id == 74 : # Rendre une fraction irréductible 
		nume = [i for i in range(2,1000)]
		deno = [i for i in range(2,1000)]
		j = randint(0,97)
		k = randint(0,97)
		n = nume[j]
		m = deno[k] 
		pgcd = math.gcd(n, m)
		title, answer  = "Simplifie la fraction "+frac(n,m), str(n//pgcd)+"##"+str(m//pgcd)

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
		loc  = dict()
		exec(mental.script,globals(),loc)
		title  = loc['title']
		answer = loc['answer']
		question = Question.objects.create(title = title, answer = answer, mental_id = mental_id, qtype=2 , size = 48)
		quizz.questions.add(question)


 


