from association.models import  Accounting, Detail
from datetime import  datetime
from datetime import  datetime
from general_fonctions import *

def accounting_adhesion(school, today , date_payment, user, is_active , observation ):  

    fee       = school.fee()
    today     = datetime.now()
    this_year = today.year
    next_year = int(this_year) + 1
    objet     = "Adhésion "+ str(this_year) +" - " +str(next_year)

    accounting, create = Accounting.objects.get_or_create( school = school   , is_active = 0 ,  defaults={ 'date' : today , 'amount' : fee , 'objet' : objet , 'beneficiaire' :  school.name , 'chrono' : create_chrono(Accounting,"FACTURE") ,
                                                                                                                    'is_credit' : 1 , 'address' :  school.address , 'complement' : school.complement , 'is_abonnement' : True ,
                                                                                                                    'town' : school.town , 'country' : school.country , 'contact' : school.address , 'forme' : "FACTURE", 'plan_id' :  18 ,
                                                                                                                     'observation' : observation ,'date_payment' : date_payment , 'user' : user  })
    if create :

        Detail.objects.create( accounting = accounting  ,  description = objet , amount = fee)
    else : 
        Accounting.objects.filter(pk=accounting.id).update(  date=today ,  amount = fee )


    return accounting.id