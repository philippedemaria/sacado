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
            await self.close()
        else :    
            await self.accept()
            user=self.scope["user"]
            if user.is_student :
               self.role=0
            if user.is_teacher :
               self.connected_students=dict()
               self.role=2


    async def disconnect(self, close_code):
        if self.role==0  :  #c'est un eleve qui se deconnecte
           await self.channel_layer.group_send("perso"+self.ugroupe,\
            {'type':"deconnexionEleve", 'user' : self.scope["user"], "ide":self.ide,"typexo":self.typexo})
           await self.channel_layer.group_discard(self.ugroupe,self.channel_name)
        elif self.role==2 :
           await self.channel_layer.group_send(self.ugroupe,{'type':"deconnexionProf", 'user':self.scope['user']})
           await self.channel_layer.group_discard(self.ugroupe,self.channel_name)

    async def receive_json(self,content) :
        command=content.get("command",None)
        dest=content.get("dest","")
        if self.role==0 and dest=="" :
            dest="p"

		# traitement de toutes les requetes spéciales, qui modifie les consumers        
        if 'c' in dest :  #le message s'adresse aussi au consumer... 
            if command=="connexionProf" :
               ugroupe="Salle"+str(content.get("parcours"))
               self.ugroupe=ugroupe
               await self.channel_layer.group_add(ugroupe,self.channel_name)
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
            await self.channel_layer.group_send(self.ugroupe,
               {'type' : "profVersTous",
                'command' : command,
                'payload' : payload})
        if 'p' in dest :     # d'un eleve au prof
            await self.channel_layer.group_send("perso"+self.ugroupe,
                {'type':'eleveVersProf',
			     'command':command,
			     'from' : self.scope['user'].id,
			     'name' : self.scope['user'].username,
			     'ide'  : content.get("ide",self.ide),
			     'typexo': content.get("typexo",self.typexo),
			     'payload': content.get("payload",None)
			     })

    #----------- fonctions déclenchées par channel

    async def eleveVersProf(self,data):
        data['type']=data['command']
        await self.send_json(data)

    async def profVersEleve(self,data):
          data['type']=data['command']
          data['from']=data.get("from","prof")
          await self.send_json(data)

    async def profVersTous(self,data) : #message envoyé par le prof à tous les eleves
          data['from']=data.get("from","prof")
          data['type']=data['command']
          await self.send_json(data)

    async def connexionProf(self,data):
            if self.role==0 :
                await self.send_json({'type' : 'connexionProf'})
                #chaque eleve renvoie une connexion au prof
                await self.channel_layer.group_send("perso"+self.ugroupe, 
                {'type' : "connexionEleve",
                 'user' : self.scope["user"],
                 'channel' : self.channel_name,
                 'ide':self.ide,
                 'typexo': self.typexo})

    async def deconnexionProf(self,data):
            if self.role==0 :
                await self.send_json({'type' : 'deconnexionProf', 'from' : data["user"].id})

    async def connexionEleve(self,data):
            if self.role==2 :
                self.connected_students[data['user'].id]=(data['channel'],data['user'])
                await self.send_json({'type' : 'connexionEleve' , 'from' : data["user"].id, 'ide':data['ide'] , "typexo":data["typexo"] })
    
    async def deconnexionEleve(self,data):
            if self.role==2 :
                if data['user'].id in self.connected_students :
                    self.connected_students.pop(data['user'].id)
                await self.send_json({
                  'type' : 'deconnexionEleve' , 
                  'from' : data["user"].id, 
                   "ide":data['ide'],
                   "typexo":data['typexo']
                  })
