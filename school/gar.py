from association.models import Abonnement
from datetime import datetime ,  date
import requests


def web_abonnement_xml(abonnement,new):

	#Webservice du GAR
	#header = "<?xml version='1.0' encoding='UTF-8'?><abonnement xmlns='http://www.atosworldline.com/wsabonnement/v1.0/'>"
	#header = { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' }

	dico   = dict()
	dico["idAbonnement"]          = "ABO_SACADO_" + str(abonnement.school.code_acad)
	dico["commentaireAbonnement"] = "Abonnement à SacAdo"
	dico["idDistributeurCom"]     = "46173_832020065"
	dico["idRessource"]	          = "ark:/46173/00001.p" # En production, il faut enlever le p 
	dico["typeIdRessource"]       = "ark" 	   
	dico["libelleRessource"]      = "SACADO"
	dico["debutValidite"]	      = abonnement.date_start.isoformat()
	dico["finValidite"]	          = abonnement.date_stop.isoformat() #.strftime("%Y-%m-%d")
	if new :
		dico["uaiEtab"]	  	      = abonnement.school.code_acad 
	dico["categorieAffectation"]  = "transferable"
	dico["typeAffectation"]       = "ETABL"
	dico["nbLicenceGlobale"]      = "ILLIMITE"	   
	dico["publicCible"]           = "ELEVE"
	dico["publicCible"]           = "ENSEIGNANT"
	return dico




def date_abonnement(today):
    """Création d'un abonnement dans la base de données"""
    date_start = today.isoformat() # Année en cours
    if today < datetime( today.year,5,30) :
        date_stop  = datetime(today.year,7,14).isoformat() # Année en cours
    else :
        date_stop  = datetime(today.year+1,7,14).isoformat() # Année suivante

    return date_start, date_stop



def create_abonnement(today,school,accounting_id,user):
    """Création d'un abonnement dans la base de données"""
    host   = "https://abonnement.partenaire.test-gar.education.fr/" # Adresse d'envoi
    # Date d'abonnement du 1 septembre au 14 juillet
    date_start, date_stop = date_abonnement(today)

    # Create Web abonnement d'un établissement
    abonnement, abo_created = Abonnement.objects.get_or_create(school = school, date_start = date_start, date_stop = date_stop,  accounting_id = accounting_id , is_gar = 1, defaults={ 'user' : user,  'is_active' : 0}  )
    if not abo_created :
        headers = {'host':host}
        params  = web_abonnement_xml(abonnement,True)
        r       = requests.post(str(abonnement.id),headers=headers,params=params)
        abonnement.is_active=0
        abonnement.save()
        if r.status_code==200 :
            abonnement.is_active = 1
            abonnement.save()

    else : 
        headers = {'host':host}
        params  = web_abonnement_xml(abonnement,False)
        r = requests.put(str(abonnement.id),headers=headers,params=params)
        if r.status_code==201 :
            abonnement.is_active = 1
            abonnement.save()

 