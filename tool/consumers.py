from django.conf import settings
from channels.generic.websocket import WebsocketConsumer , AsyncJsonWebsocketConsumer
import json
import base64
import random

def ran() :
	return str(random.randint(1000,9999))
		


#def printc(*a) :
#	pass
printc=print
class VisioConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        printc("Tentative de connection")
        printc("user=",self.scope["user"])
        if self.scope["user"].is_anonymous :
            printc("utilisateur anonyme")
            await self.close()
        else :    
            await self.accept()
            printc("L'utilisateur est loggé, on poursuit...")
            
    async def disconnect(self, close_code):
        printc(self.scope['user'], " se deconnecte")
        # Leave room group
        if "nconn" in self.scope :
           printc("le destinataire se deconnecte")
        else :
            printc("une fenetre expediteur se ferme", self.scope['code'])
            await self.channel_layer.group_send("groupe"+self.scope["code"],{"type":"deconnexion"})
			
        self.channel_layer.group_discard(self.channel_name)    
    async def receive_json(self,content) :
        command=content.get("command",None)
        printc("commande recue ",command)
        
        if command=="joinExpediteur" :
           code=content.get("code",None);
           printc("joinExpediteur recu, avec le code",code)
           if code !=None :
              await self.channel_layer.group_send("groupe"+str(code),{"type":"joinExpediteur"})
              
              self.scope['code']=str(code)
        if command=="joinDestinataire" :
            self.scope["code"]=ran() #une chaine aléatoire de 4 caractères
            self.scope["nconn"]=0    #nombre de fenêtres d'envoi ouvertes  
            self.scope["groupe"]="groupe"+self.scope["code"]
            printc("groupe : ",self.scope["groupe"])
            await self.channel_layer.group_add(self.scope["groupe"],self.channel_name)
            await self.send_json({"command":"joinDestinataire","code":self.scope['code']})
            printc("joinDestinataire traité")
        if command=="cast" :
            printc("fichier envoyé par l'expediteur")
            printc(content.get("name"))
            await self.channel_layer.group_send("groupe"+self.scope["code"],
                {"type" : "cast",
                 "user" : self.scope['user'],
                 "Imgb64" : content.get("Imgb64"), # l'image encodée base64
                 "fileType" : content.get("fileType")
                 })  		
            printc("envoie au channel ok")
            printc(content.get("Imgb64"))
    #------------  fonctions de tratiement des évènements---------------------
    
    async def joinExpediteur(self,data):
        printc("je suis ",self.scope["user"], "entree dans joinExpediteur")
        self.scope["nconn"]+=1
        await self.send_json({"command":"joinExpediteur"})				

    async def deconnexion(self,data) :
        printc("fermeture d'une fenetre")
        printc(" il en reste", self.scope["nconn"]-1)
        self.scope["nconn"]-=1
        if self.scope["nconn"]<=0 :
            await self.send_json({"command":"tousDeco"})
			
    async def cast(self,data):
        printc("entree dans cast")
        await self.send_json({"command":"cast", "Imgb64":data['Imgb64'], "fileType":data['fileType']})
        print("envoie ok")

   
   
