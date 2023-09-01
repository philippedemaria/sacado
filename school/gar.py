from association.models import Abonnement
from datetime import datetime ,  date
import requests



def date_abonnement(today):
    """Création d'un abonnement dans la base de données"""
    date_start = today.isoformat() # Année en cours
    date_stop  = datetime(today.year+1,7,14)  # Année suivante

    suf = "T00:00:00.000000"
    date_start, date_stop = str(today), str(date_stop.isoformat())

    return date_start, date_stop



def web_abonnement_xml(accounting,id_abonnement , today):
    #Webservice du GAR
    date_start, date_stop = date_abonnement(today)

    body = "<?xml version='1.0' encoding='UTF-8'?>"
    body += "<abonnement xmlns='http://www.atosworldline.com/wsabonnement/v1.0/'>"
    body += "<idAbonnement>" + id_abonnement +"</idAbonnement>"
    body += "<commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement>"
    body += "<idDistributeurCom>832020065_0000000000000000</idDistributeurCom>"
    body += "<idRessource>ark:/46173/00001</idRessource>" #/46173/00001.p
    body += "<typeIdRessource>ark</typeIdRessource>"
    body += "<libelleRessource>SACADO</libelleRessource>"
    body += "<debutValidite>"+date_start+"</debutValidite>"
    body += "<finValidite>"+date_stop+"</finValidite>"
    body += "<uaiEtab>"+accounting.school.code_acad+"</uaiEtab>"
    body += "<categorieAffectation>transferable</categorieAffectation>"
    body += "<typeAffectation>INDIV</typeAffectation>"
    body += "<nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant>"
    body += "<nbLicenceEleve>"+str(accounting.school.nbstudents)+"</nbLicenceEleve>"

    if not accounting.school.is_primaire :
        body += "<nbLicenceProfDoc>100</nbLicenceProfDoc>"
        body += "<nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel>"
        body += "<publicCible>DOCUMENTALISTE</publicCible>"
        body += "<publicCible>AUTRE PERSONNEL</publicCible>"
        
    body += "<publicCible>ENSEIGNANT</publicCible>"
    body += "<publicCible>ELEVE</publicCible>"
    
    try :
        f = open('/var/www/sacado/logs/gar_connexions.log','a')
        print("===> date_start : ", file=f)
        print(date_start, file=f)
        print("===> date_stop : ", file=f)
        print(date_stop, file=f)
        print("===> id_abonnement : ", file=f)
        print(id_abonnement, file=f)
        print("===> body : ", file=f)
        print(body, file=f)
        f.close()
    except :
        pass 




    body += "</abonnement>"
    return body



def web_update_abonnement_xml(customer,id_abonnement):
    #Webservice du GAR
    suf = "T00:00:00.000000"
    date_start, date_stop = str(customer.date_start_gar)+suf, str(customer.date_stop)+suf

    #date_start, date_stop = str(customer.date_start_gar).isoformat(), str(customer.date_stop).isoformat()


    body = "<?xml version='1.0' encoding='UTF-8'?>"
    body += "<abonnement xmlns='http://www.atosworldline.com/wsabonnement/v1.0/'>"
    body += "<idAbonnement>" + id_abonnement +"</idAbonnement>"
    body += "<commentaireAbonnement>AbonnementSacAdo</commentaireAbonnement>"
    body += "<idDistributeurCom>832020065_0000000000000000</idDistributeurCom>"
    body += "<idRessource>ark:/46173/00001</idRessource>" #/46173/00001.p
    body += "<typeIdRessource>ark</typeIdRessource>"
    body += "<libelleRessource>SACADO</libelleRessource>"
    body += "<debutValidite>"+date_start+"</debutValidite>"
    body += "<finValidite>"+date_stop+"</finValidite>"
    body += "<categorieAffectation>transferable</categorieAffectation>"
    body += "<typeAffectation>INDIV</typeAffectation>"
    body += "<nbLicenceEnseignant>ILLIMITE</nbLicenceEnseignant>"
    body += "<nbLicenceEleve>"+str(customer.school.nbstudents)+"</nbLicenceEleve>"



    try :
        f = open('/var/www/sacado/logs/gar_connexions.log','a')
        print("===> date_start : ", file=f)
        print(date_start, file=f)
        print("===> date_stop : ", file=f)
        print(date_stop, file=f)
        print("===> id_abonnement : ", file=f)
        print(id_abonnement, file=f)
        print("===> body : ", file=f)
        print(body, file=f)
        f.close()
    except :
        pass 

    if not customer.school.is_primaire :
        body += "<nbLicenceProfDoc>100</nbLicenceProfDoc>"
        body += "<nbLicenceAutrePersonnel>50</nbLicenceAutrePersonnel>"
        body += "<publicCible>DOCUMENTALISTE</publicCible>"
        body += "<publicCible>AUTRE PERSONNEL</publicCible>"
        
    body += "<publicCible>ENSEIGNANT</publicCible>"
    body += "<publicCible>ELEVE</publicCible>"
    
    body += "</abonnement>"
    return body




def create_abonnement_gar(today,customer ,user): 
    """Création d'un abonnement dans la base de données"""
 
    id_abonnement = "SACADO_" + str(customer.school.code_acad)+"_"+str(today)
    #host   = "https://abonnement.partenaire.test-gar.education.fr/"+id_abonnement  # Adresse d'envoi

    host   = "https://abonnement.gar.education.fr/"+id_abonnement  # Adresse d'envoi
    directory = '/home/sacado/'

    header  =  { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' } 

    body      = web_abonnement_xml(customer,id_abonnement, today) 
    r         = requests.put(host, data=body, headers=header, cert=(directory + 'sacado.xyz-PROD-2021.pem', directory + 'sacado_prod.key'))

    if r.status_code == 201 or r.status_code==200 :
        return True , "ok" , "ok" , "ok"  , id_abonnement 
    else :
        return False, r.status_code , r.headers , r.content.decode('utf-8') , None



def update_abonnement_gar(today,customer):
    """update d'un abonnement dans la base de données"""

    #host   = "https://abonnement.partenaire.test-gar.education.fr/"+id_abonnement  # Adresse d'envoi

    id_abonnement = customer.school.customer.gar_abonnement_id

    host   = "https://abonnement.gar.education.fr/"+id_abonnement  # Adresse d'envoi
    directory = '/home/sacado/'

    header  =  { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' } 

    body      = web_update_abonnement_xml(customer,id_abonnement) 

    r         = requests.post(host, data=body, headers=header, cert=(directory + 'sacado.xyz-PROD-2021.pem', directory + 'sacado_prod.key'))

    if r.status_code == 201 or r.status_code==200 :
        return True , "ok" , "ok" , "ok"  , id_abonnement 
    else :
        return False, r.status_code , r.headers , r.content.decode('utf-8') , None




def delete_gar_abonnement(id_abonnement):
    """Supression d'un abonnement dans la base de données"""

    host      = "https://abonnement.gar.education.fr/"+id_abonnement  # Adresse d'envoi
    directory = '/home/sacado/'

    header    =  { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' } 

    r         = requests.delete(host, headers=header, cert=(directory + 'sacado.xyz-PROD-2021.pem', directory + 'sacado_prod.key'))

    if r.status_code == 204 :
        return True , "ok" , "ok" , "ok"  
    else :
        return False, r.status_code , r.headers , r.content.decode('utf-8')  



def these_abonnements_gar():
    """récupération des abonnements dans la base de données"""

    host          = "https://abonnement.gar.education.fr/abonnements"  # Adresse d'envoi
    directory     = '/home/sacado/'

    header        =  { 'Content-type': 'application/xml;charset=utf-8' , 'Accept' : 'application/xml' } 

    body          = '<filtres xmlns="http://www.atosworldline.com/wsabonnement/v1.0/"><filtre><filtreNom>idDistributeurCom</filtreNom>'
    body          += '<filtreValeur>832020065_0000000000000000</filtreValeur>'
    body          += '</filtre></filtres>'

    r             = requests.get(host, data=body, headers=header, cert=(directory + 'sacado.xyz-PROD-2021.pem', directory + 'sacado_prod.key'))

    if r.status_code == 201 or r.status_code==200 :
        return True , "ok" , "ok" ,  r.content.decode('utf-8') # open('responses/subs.xml', 'w').write(str(response.content.decode('utf-8'))) 
    else :
        return False, r.status_code , r.headers , r.content.decode('utf-8')

