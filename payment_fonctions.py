from association.models import  Accounting, Detail
from datetime import  datetime

def accounting_adhesion(school, today , acting, user, is_active , observation ): #acting = date d'effet

    fee       = school.fee()
    today     = datetime.now()
    this_year = today.year
    next_year = int(this_year) + 1
    objet     = "Cotisation "+ str(this_year) +" - " +str(next_year)

    accounting, create = Accounting.objects.get_or_create( school = school   , is_active = 0 ,  defaults={ 'date' : today , 'amount' : fee , 'objet' : objet , 'beneficiaire' :  school.name ,
                                                                                                                    'is_credit' : 1, 'address' :  school.address , 'complement' : school.complement ,
                                                                                                                    'town' : school.town , 'country' : school.country , 'contact' : school.address ,
                                                                                                                     'observation' : observation ,'acting' : acting , 'user' : user  })
    if create :
        Detail.objects.create( accounting = accounting  ,  description = objet , amount = fee)
    else : 
        Accounting.objects.filter(pk=accounting.id).update(  date=today ,  amount = fee )

    return accounting.id