from django.conf import settings
from channels.generic.websocket import WebsocketConsumer , AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async


printc=print
#def printc(*a) :
#    pass

class TableauConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        printc("Tentative de connection, user=",self.scope["user"])
        if self.scope["user"].is_anonymous:
            printc("utilisateur anonyme, on le deconnecte")
            await self.close()
        else :    
            await self.accept()
            printc("L'utilisateur est loggé, on poursuit...")
            user=self.scope["user"]
            printc("type utilisateur :", user.user_type)
            if user.is_student :
               printc("c'est un élève")
               printc("nom de son channel :",self.channel_name)
               self.role=0
            if user.is_teacher :
               printc("c'est un enseignant")
               printc("nom du channel prof :",self.channel_name)
               printc("Le prof a ouvert la page RT du parcours, c'est ",self.scope['user'])
               self.connected_students=dict()
               self.role=2


    async def disconnect(self, close_code):
        printc(self.scope['user'], "se deconnecte")
        if self.role==0  :  #c'est un eleve qui se deconnecte
           await self.channel_layer.group_send("perso"+self.ugroupe,\
            {'type':"deconnexionEleve", 'user' : self.scope["user"], "ide":self.ide,"typexo":self.typexo})
           await self.channel_layer.group_discard(self.ugroupe,self.channel_name)
        elif self.role==2 :
           printc("c'est un prof, ",self.ugroupe)
           await self.channel_layer.group_send(self.ugroupe,{'type':"deconnexionProf", 'user':self.scope['user']})
           await self.channel_layer.group_discard(self.ugroupe,self.channel_name)

    async def receive_json(self,content) :
        command=content.get("command",None)
        dest=content.get("dest","")
        if self.role==0 and dest=="" :
            dest="p"
        printc("commande recue :", command, dest)

		# traitement de toutes les requetes spéciales, qui modifie les consumers        
        if 'c' in dest :  #le message s'adresse aussi au consumer... 
            if command=="connexionProf" :
               ugroupe="Salle"+str(content.get("parcours"))
               self.ugroupe=ugroupe
               printc("nom du layer de tout le groupe : '{}'".format(ugroupe))
               printc("on envoie l'info connexion du prof aux eleves connectés")
               await self.channel_layer.group_add(ugroupe,self.channel_name)
               printc("ajout du groupe ok")
               printc("creation du groupe ne contenant que le prof")
               await self.channel_layer.group_add("perso"+ugroupe, self.channel_name)
               await self.channel_layer.group_send(ugroupe,{'type':"connexionProf"})
                  
            elif command=="connexionEleve" :
               ugroupe="Salle"+str(content.get("parcours"))
               self.ugroupe=ugroupe
               self.ide=content.get("ide",None)
               self.typexo=content.get("typexo",None)
               await self.channel_layer.group_add(ugroupe,self.channel_name)
               await self.channel_layer.group_send("perso"+ugroupe, 
                   {'type' : "connexionEleve",
                    'user' : self.scope["user"],
                    'ide'  : self.ide,
                    'typexo' : self.typexo,
                    'channel' : self.channel_name})                   
        
        # messages standard, le consumer et channel ne font que transférer.       
        
        if ('e' in dest) and (self.role==2) : # du prof à un eleve particulier, 
            to=content.get("to",None)
            try :
                chan_to=self.connected_students[int(to)][0]
                printc("channel de l'élève trouvé")
                printc("content : ",content)
                await self.channel_layer.send(chan_to,
                   {'type': "profVersEleve",
                    'command':command,
                    'to'  : to,   #le destinataire à été envoyé par le client-prof
                    'ide' : content.get("ide",None),  #a priori inutile
                    'payload' : content.get("payload",None)
                    })
            except : 
                printc("eleve non trouvé ", self.connected_students)
                
        if ('a' in dest) and (self.role==2) : # du prof à tous les eleves, 
            payload=content.get("payload",None)
            print("message general du prof", payload)
            print("message ", payload)
            await self.channel_layer.group_send(self.ugroupe,
               {'type' : "profVersTous",
                'command' : command,
                'payload' : payload})
            printc("evenement declenché pour tout le groupe")
        if 'p' in dest :     # d'un eleve au prof
            printc("destination prof", content)
            printc(self.ide,self.typexo,self.scope['user'].username)
            await self.channel_layer.group_send("perso"+self.ugroupe,
                {'type':'eleveVersProf',
			     'command':command,
			     'from' : self.scope['user'].id,
			     'name' : self.scope['user'].username,
			     'ide'  : content.get("ide",self.ide),
			     'typexo': content.get("typexo",self.typexo),
			     'payload': content.get("payload",None)
			     })
            printc("ok")
    #----------- fonctions déclenchées par channel

    async def eleveVersProf(self,data):
        data['type']=data['command']
        printc("envoi standard",data)
        await self.send_json(data)

    async def profVersEleve(self,data):
          printc("entree dans profVersEleve, consumer de ",self.scope['user'])
          printc("data :",data)
          data['type']=data['command']
          data['from']=data.get("from","prof")
          await self.send_json(data)
          printc("ok")

    async def profVersTous(self,data) : #message envoyé par le prof à tous les eleves
          printc("entree profVersTous, data=",data)
          data['from']=data.get("from","prof")
          data['type']=data['command']
          await self.send_json(data)

    async def connexionProf(self,data):
            printc("entree dans la fonction connexion prof")
            printc("data=",data)
            printc("destinataire {} (role : {})".format(self.scope['user'], self.role))
            if self.role==0 :
                printc("destinataire : ",self.scope["user"].id, "exo :", self.ide)
                await self.send_json({'type' : 'connexionProf'})
                #chaque eleve renvoie une connexion au prof
                await self.channel_layer.group_send("perso"+self.ugroupe, 
                {'type' : "connexionEleve",
                 'user' : self.scope["user"],
                 'channel' : self.channel_name,
                 'ide':self.ide,
                 'typexo': self.typexo})

    async def deconnexionProf(self,data):
            printc("entree dans la fonction deconnexion prof")
            printc("data=",data)
            printc("destinataire {} (role : {})".format(self.scope['user'], self.role))
            if self.role==0 :
                printc("destinataire : ",self.scope["user"].id)
                await self.send_json({'type' : 'deconnexionProf', 'from' : data["user"].id})
                printc("deconnexion prof ok")
    async def connexionEleve(self,data):
            printc("entree dans la fonction connexion eleve")
            printc("data=",data)
            printc("destinataire {} (role : {})".format(self.scope['user'], self.role))
            if self.role==2 :
                printc("destinataire : le prof")
                self.connected_students[data['user'].id]=(data['channel'],data['user'])
                printc("connected_students : ", self.connected_students)
                await self.send_json({'type' : 'connexionEleve' , 'from' : data["user"].id, 'ide':data['ide'] , "typexo":data["typexo"] })
    async def deconnexionEleve(self,data):
            printc("entree dans la fonction deconnexion eleve")
            printc("data=",data)
            printc("destinataire {} (role : {})".format(self.scope['user'], self.role))
            if self.role==2 :
                printc("destinataire : le prof")
                if data['user'].id in self.connected_students :
                    self.connected_students.pop(data['user'].id)
                printc("connected_students : ", self.connected_students)
                await self.send_json({
                  'type' : 'deconnexionEleve' , 
                  'from' : data["user"].id, 
                   "ide":data['ide'],
                   "typexo":data['typexo']
                  })
                printc("deconnexion eleve ok")
