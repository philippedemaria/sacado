from association.models import Abonnement
from datetime import datetime ,  date
import requests



def date_abonnement(today):
    """Création d'un abonnement dans la base de données"""
    date_start = today.isoformat() # Année en cours
    if today < datetime( today.year,5,30) :
        date_stop  = datetime(today.year,7,14).isoformat() # Année en cours
    else :
        date_stop  = datetime(today.year+1,7,14).isoformat() # Année suivante

    return date_start, date_stop



def web_abonnement_xml(abonnement,id_abonnement , today):
    #Webservice du GAR

    date_start, date_stop = date_abonnement(today)

    body = "<idAbonnement>" + id_abonnement +"</idAbonnement>"
    body += "<commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement>"
    body += "<idDistributeurCom>832020065_000000000000000</idDistributeurCom>"
    body += "<idRessource>ark:/46173/00001.p</idRessource>"
    body += "<typeIdRessource>ark</typeIdRessource>"
    body += "<libelleRessource>SACADO</libelleRessource>"
    body += "<debutValidite>"+date_start+"</debutValidite>"
    body += "<finValidite>"+date_stop+"</finValidite>"
    body += "<uaiEtab>"+abonnement.school.code_acad+"</uaiEtab>"
    body += "<categorieAffectation>transferable</categorieAffectation>"
    body += "<typeAffectation>INDIV</typeAffectation>"
    body += "<nbLicenceEnseignant>500</nbLicenceEnseignant>"
    body += "<nbLicenceEleve>"+str(abonnement.school.nbstudents)+"</nbLicenceEleve>"
    body += "<nbLicenceProfDoc>100</nbLicenceProfDoc>"
    body += "<publicCible>ENSEIGNANT</publicCible>"
    body += "<publicCible>ELEVE</publicCible>"
    body += "</abonnement>"

    return body



 


def create_abonnement_gar(today,school,abonnement ,user):
    """Création d'un abonnement dans la base de données"""

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    return True 

    # id_abonnement = "ABO_SACADO_" + str(abonnement.school.code_acad)+"_"+str(timestamp) 
    # host   = "https://abonnement.partenaire.test-gar.education.fr/"+id_abonnement  # Adresse d'envoi
    # directory = '/home/sacado/'

    # header  =  { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' } 
    # body      = web_abonnement_xml(abonnement,id_abonnement, today) 
    # r         = requests.put(host, data=body, headers=header, cert=(directory + 'sacado.xyz-PFPART-2021.pem', directory + 'sacado.key'))

    # if r.status_code == 201 or r.status_code==200 :
    #     return True 
    # else :
    #     return False 
 
