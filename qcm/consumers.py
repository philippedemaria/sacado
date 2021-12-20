from django.conf import settings
from channels.generic.websocket import WebsocketConsumer , AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async

printc=print

class TableauConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        printc("Tentative de connection, user=",self.scope["user"])
        if self.scope["user"].is_anonymous:
            printc("utilisateur anonyme, on le deconnecte")
            await self.close()
        else :    
            await self.accept()
            printc("L'utilisateur est loggé, on poursuit...")
            
         # Store which rooms the user has joined on this connection
            user=self.scope["user"]
            printc("type utilisateur :", user.user_type)
            if user.is_student :
               printc("c'est un élève")
               printc("nom de son channel :",self.channel_name)

            if user.is_teacher :
               printc("c'est un enseignant")
               printc("nom du channel prof :",self.channel_name)
               printc("Le prof a ouvert la page RT du parcours, c'est ",self.scope['user'])


    async def disconnect(self, close_code):
        printc(self.scope['user'], " se deconnecte")
        # Leave room group
        self.channel_layer.group_discard(self.ugroupe,self.channel_name)

    async def receive_json(self,content) :
        command=content.get("command",None)
        printc("commande recue :", command)
        if command=="teacher_join" :
               self.connected_students=dict()
               self.role=2
               us=self.scope["user"].id 
               ugroupe="Salle"+str(content.get("parcours"))
               self.ugroupe=ugroupe
               
               printc("nom du layer de tout le groupe : '{}'".format(ugroupe))
               await self.channel_layer.group_add(ugroupe,self.channel_name)
               printc("ajout du groupe ok")
               printc("creation du groupe de contenant que le prof")
               await self.channel_layer.group_add("perso"+ugroupe, self.channel_name)
               await self.send_json({"type": "autojoin","salle": ugroupe})
               printc("renvoie de ok au prof : ok")
        if command=="student_join" :
            printc("l'élève a ouvert un exo")
            printc("parcours : ", content.get("parcours"))
            printc("exo",content.get("exo",None))
            us=self.scope["user"].id
            self.role=0 
            printc("id de l'élève :",us) 
            ugroupe="Salle"+str(content.get("parcours"))
            self.ugroupe=ugroupe
            printc("champ user recu ",content.get("user"))
            printc("il est ajouté au layer de tout le groupe, qui se nomme '{}'".format(ugroupe))
            await self.channel_layer.group_add(ugroupe,self.channel_name)
            await self.channel_layer.group_send("perso"+ugroupe, 
                {'type' : "connexion.eleve",
                 'user' : self.scope["user"],
                 'channel' : self.channel_name})
            printc("envoi ok")
        if command=="student_message"  :
            message=content.get("message",None)
            printc("on va déclencher l'évènement message eleve au groupe '{}'".format("perso"+self.ugroupe))
            printc("message : '{}'".format(message))
            await self.channel_layer.group_send("perso"+self.ugroupe,
               {'type' : "student.message",
                'from' : self.scope['user'].id, #expéditeur id
                'name'  : self.scope['user'].username,
                'message' : message})
            printc("évènement student_message déclenché au groupe-singleton")
        if command=="ExoDebut" :
           await self.channel_layer.group_send("perso"+self.ugroupe,
			    {'type' : "ExoDebut",
			     'from' : self.scope['user'].id, #expéditeur id
                'name'  : self.scope['user'].username,
                'ide' : content.get("ide"),  #identifiant d'exo
                })
        if command=="SituationFinie" :
           await self.channel_layer.group_send("perso"+self.ugroupe,
			    {'type' : "SituationFinie",
			     'from' : self.scope['user'].id, #expéditeur id
                'name'  : self.scope['user'].username,
                'resultat' : content.get("resultat"),
                'ide' : content.get("ide"),  #identifiant d'exo
                "grade" : content.get("grade"),
                "situation" : content.get("situation"),
                "numexo"    : content.get("numexo")
                
               })
        if command=="teacher_message" :
            printc("command teacher_message recue" ,content)
            message=content.get("message",None)
            to=content.get('to')
            try :
                chan_to=self.connected_students[int(to)][0]
                
            except : 
                printc("eleve non trouvé ", self.connected_students)
                chan_to="toto"
            printc("message : '{}', to : {} channel : {}".format(message,to,chan_to))
            await self.channel_layer.send(chan_to,
               {'type' : "teacher.message",
                'to' : content.get('to',None),   #le destinataire à été envoyé par le client-prof
                'message' : message})
            printc("évènement déclenché au seul eleve destinataire")
        if command=="teacher_message_general" :
            print("message general du prof")
            message=content.get("message",None)
            print("message ", message)
            await self.channel_layer.group_send(self.ugroupe,
               {'type' : "teacher.message.general",
                'message' : message})
            printc("evenement declenché pour tout le groupe")
						

    async def student_message(self,data) : #message envoyé par l'élève au prof
        printc("entree dans la fonction student_message")
        printc('user : ', self.scope['user'], self.role)
        if self.role==2 :   #c'est le prof qui reçoit, il faut donc lui envoyer
            printc("Envoyé par l'élève {}".format(data["from"]))
            printc("message :", data['message'])
            await self.send_json({'type':'message','from': str(data["from"]),"message" : str(data['message']) , 'name' : data["name"]  })
    
    
    async def ExoDebut(self,data) :  #l'eleve commence un exo, le consumer du prof averti le client du prof
        #printc("entree ExoDebut")
        if self.role==2 :
            await self.send_json(data)
    async def SituationFinie(self,data) :  #l'eleve a termine une situation, le consumer du prof averti le client du prof
        #printc("entree dans SituationFinie")
        if self.role==2 :
            await self.send_json(data)

    async def teacher_message(self,data) : #message envoyé par le prof à un eleve
        printc("entree dans la fonction teacher_message")
        printc('user : ', self.scope['user'], self.scope['user'].id,self.role)
        printc("self", self.scope['user'].id, "de type", type(self.scope['user'].id))
        printc("destinataire", data['to'],type(data['to']))
        if  self.scope['user'].id == data['to'] : #on est dans l'instance de l'élève destinataire
            printc("Envoyé à l'élève {}".format(data["to"]))
            printc("message :", data['message'])
            await self.send_json({'type':'message','to': data["to"],"message" : data['message']})
            printc("ok")
        else :
            printc("self n'est pas le destinataire du message, rien à faire")

    async def teacher_message_general(self,data) : #message envoyé par le prof à tous les eleves
          printc("entree dans teacher message general, message="+data['message'])
          await self.send_json({'type':'message','from': "prof", "name": "moi", "message" : str(data['message'])})


    async def connexion_eleve(self,data):
            printc("entree dans la fonction connexion eleve")
            printc("data=",data)
            printc("destinataire {} (role : {})".format(self.scope['user'], self.role))
            if self.role==2 :
                printc("destinataire : le prof")
                self.connected_students[data['user'].id]=(data['channel'],data['user'])
                printc("connected_students : ", self.connected_students)
                await self.send_json({'type' : 'connexion' , 'from' : data["user"].id })


