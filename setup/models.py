import uuid
from django.db import models
from django_cron import CronJobBase, Schedule
from qcm.models import Parcours
from django.utils import formats, timezone
from datetime import datetime, timedelta       
    
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    today = timezone.now()

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = str(uuid.uuid4())[:64]    # a unique code

    def do(self):
        Parcours.objects.filter(stop__lt=today).update(is_publish=0)



class Formule(models.Model):

	name = models.CharField(max_length=255, verbose_name="Nom")
	adhesion = models.CharField(max_length=255, default ="" ,verbose_name="Adhesion")
	price = models.CharField(max_length=255, default ="" , verbose_name="Montant")

	is_family = models.BooleanField(default=0, verbose_name="Forfait famille ?") 
	nb_month = models.PositiveIntegerField(default=1, verbose_name="Nombre de mois")     

	def __str__(self):
	    return "{}".format(self.name)


	def data(self) :
		coeff_family = 1.7
		data = {}
		date = datetime.now()
		this_month = date.month

		price_tab = self.price.split(",")
		price = price_tab[0]+"."+price_tab[1]


		if this_month < 13 and this_month > 6 :
			left_month = 19 - int(this_month)
			end = datetime(date.year+1,6,30)
		else :
			left_month= 7 - int(this_month) 
			end = datetime(date.year,6,30)

		if self.nb_month == 1 :
			left_month= 1   
			end = date 	+ timedelta(days = 31)  

		else :
			if self.nb_month == 3 :

				if left_month > 2  :
					left_month = 3

				end = date 	+ timedelta(days = 31*left_month)  
 



		adh =  float(price) 
		adhf =  adh * coeff_family 


		data["left_month"] = left_month         
		data["total"] = round(left_month * adh,2)
		data["end"] = end
		data["totalF"] = round( left_month * adhf ,2) 
		data["priceF"] = round(adhf,2)
		return data