from association.models import Abonnement
import requests


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
    abonnement, abo_created = Abonnement.objects.get_or_create(school = school, date_start = date_start, date_stop = date_stop,  accounting_id = accounting_id , defaults={ 'user' : user}  )
 
    host += str(abonnement.id)
	r = requests.put(host, params)
	r.status_code
	r.headers['content-type']
	r.encoding
	r.text
	r.json()




def create_web_abonnement_xml(abonnement):

	#Webservice du GAR
	host   = "https://abonnement.partenaire.test-gar.education.fr/"
	header = "<?xml version='1.0' encoding='UTF-8'?><abonnement xmlns='http://www.atosworldline.com/wsabonnement/v1.0/'>" + host

	dico   = dict()
	dico["idAbonnement"]          = "ABO" + str(abonnement.school.id)
	dico["commentaireAbonnement"] = "Abonnement à SacAdo"
	dico["idDistributeurCom"]     = "46173_832020065"
	dico["idRessource"]	          = "ark:/46173/00001.p"  
	dico["typeIdRessource"]       = "ark" 	   
	dico["libelleRessource"]      = "SACADO"
	dico["debutValidite"]	      = abonnement.date_start.isoformat()
	dico["finValidite"]	          = abonnement.date_stop.isoformat() #.strftime("%Y-%m-%d")
	dico["uaiEtab"]	  	          = abonnement.school.code_acad 
	dico["categorieAffectation"]  = "transferable"
	dico["typeAffectation"]       = "ETABL"
	dico["nbLicenceGlobale"]      = "ILLIMITE"	   
	dico["publicCible"]           = "ELEVE"

	return dico




def create_liste_etablissement_xml():
	pass


	# school   = dict()
	# school["numero_uaiuai"]            = abonnement.school.code_acad
	# school["nature_uai"]               =  
	# school["nature_uai_libe"]          =  
	# school["type_uai"]	             =  
	# school["type_uai_libe"]            =  
	# school["commune"]                  =  
	# school["commune_libe"]	         = abonnement.school.town 
	# school["academie"]	             = 
	# school["academie_libe"]	  	     =  
	# school["departement_insee_3"]      = abonnement.school.code_acad[1:4]
	# school["departement_insee_3_libe"] = 
	# school["appellation_officielle"]   =     
	# school["patronyme_uai"]            = ""
	# school["code_postal_uai"]          = abonnement.school.zip_code
	# school["localite_acheminement_uai"]= abonnement.school.town.upper()
 
 


 

#    <etablissement>
#       <numero_uaiuai>0010428K</numero_uaiuai>
#       <nature_uai>151</nature_uai>
#       <nature_uai_libe>Ecole élémentaire</nature_uai_libe>
#       <type_uai>1ORD</type_uai>
#       <type_uai_libe>Ecoles du premier degré ordinaires</type_uai_libe>
#       <commune>1083</commune>
#       <commune_libe>Chaneins</commune_libe>
#       <academie>10</academie>
#       <academie_libe>Lyon</academie_libe>
#       <departement_insee_3>01</departement_insee_3>
#       <departement_insee_3_libe>Ain</departement_insee_3_libe>
#       <appellation_officielle>Ecole primaire</appellation_officielle>
#       <patronyme_uai></patronyme_uai>
#       <code_postal_uai>01110</code_postal_uai>
#       <localite_acheminement_uai>CHANEINS</localite_acheminement_uai>
#    </etablissement>

# </listEtablissement>

