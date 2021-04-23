from association.models import Abonnement
import requests



def web_abonnement_xml(abonnement,new):

	#Webservice du GAR
	host   = "https://abonnement.partenaire.test-gar.education.fr/"
	header = "<?xml version='1.0' encoding='UTF-8'?><abonnement xmlns='http://www.atosworldline.com/wsabonnement/v1.0/'>" + host

	header = { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' }


	dico   = dict()
	dico["idAbonnement"]          = "ABO" + str(abonnement.school.id)
	dico["commentaireAbonnement"] = "Abonnement à SacAdo"
	dico["idDistributeurCom"]     = "46173_832020065"
	dico["idRessource"]	          = "ark:/46173/00001.p"  
	dico["typeIdRessource"]       = "ark" 	   
	dico["libelleRessource"]      = "SACADO"
	dico["debutValidite"]	      = abonnement.date_start.isoformat()
	dico["finValidite"]	          = abonnement.date_stop.isoformat() #.strftime("%Y-%m-%d")
	if new :
		dico["uaiEtab"]	  	          = abonnement.school.code_acad 
	dico["categorieAffectation"]  = "transferable"
	dico["typeAffectation"]       = "ETABL"
	dico["nbLicenceGlobale"]      = "ILLIMITE"	   
	dico["publicCible"]           = "ELEVE"
	dico["publicCible"]           = "ENSEIGNANT"
	return dico




def create_abonnement(today,school,accounting_id,user):
    """Création d'un abonnement dans la base de données"""
	host   = "https://abonnement.partenaire.test-gar.education.fr/" 
    # Date d'abonnement du 1 septembre au 14 juillet
    if today < datetime.date(today.year(),5,30):
        date_start = today.isoformat() # Année en cours
        date_stop  = datetime.date(today.year(),7,14).isoformat() # Année en cours
    else :
        date_start = datetime.date(today.year(),9,1).isoformat() # Année en cours
        date_stop  = datetime.date(today.year()+1,7,14).isoformat() # Année suivante

    # Create Web abonnement d'un établissement
    abonnement, abo_created = Abonnement.objects.get_or_create(school = school, date_start = date_start, date_stop = date_stop,  accounting_id = accounting_id , defaults={ 'user' : user, 'gar_active' : 0}  )
    if not abo_created :
        headers={'host':host}
            params=web_abonnement_xml(abonnement,True)
            r=requests.post(str(abonnement.id),headers=headers,params=params)
            abonnement.gar_active=0
            abonnement.save()
            if r.status_code==200 :
                abonnement.gar_active=1
                abonnement.save()

	else : 
        headers={'host':host}
        params=web_abonnement_xml(abonnement,False)
        r=requests.put(str(abonnement.id),headers=headers,params=params)
        if r.status_code==201 :
            abonnement.gar_active=1
            abonnement.save()

    else :
        pass



def create_liste_etablissement_xml():
	pass
 