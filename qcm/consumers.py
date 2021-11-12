from django.conf import settings
from channels.generic.websocket import WebsocketConsumer , AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async


class TableauConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        print("Tentative de connection, user=",self.scope["user"])
        if self.scope["user"].is_anonymous:
            print("utilisateur anonyme, on le deconnecte")
            await self.close()
        else :    
            await self.accept()
            print("L'utilisateur est loggé, on poursuit...")
            
         # Store which rooms the user has joined on this connection
            user=self.scope["user"]
            print("type utilisateur :", user.user_type)
            if user.is_student :
               print("c'est un élève")
               print("nom de son channel :",self.channel_name)

            if user.is_teacher :
               print("c'est un enseignant")
               print("nom du channel prof :",self.channel_name)

               

    async def disconnect(self, close_code):
        print(self.scope['user'], " se deconnecte")
        # Leave room group
        self.channel_layer.group_discard(self.channel_name)

    async def receive_json(self,content) :
        command=content.get("command",None)
        print("commande recue :", command)
        if command=="teacher_join" :
               #-------création de la salle de realtime
            print("Le prof a ouvert la page RT du parcours, c'est ",self.scope['user'])
			   #------on ouvre le groupe       
            print("le prof a initié le real time", self.scope['user'])
            # on stockera dans la variable de session le groupe d'élèves
            self.connected_students=dict()
            self.role=2
            us=self.scope["user"].id
            print("user=",us)
            
            ugroupe="Salle"+str(content.get("parcours"))
            self.ugroupe=ugroupe
            print("nom du layer de tout le groupe : '{}'".format(ugroupe))
            await self.channel_layer.group_add(ugroupe,self.channel_name)
            print("ajout du groupe ok")
            
            await self.send_json({"type": "autojoin","salle": ugroupe})
            print("renvoie de ok au prof : ok")
        if command=="student_join" :
            print("l'élève a ouvert un exo")
            print("parcours : ", content.get("parcours"))
            us=self.scope["user"].id
            self.role=0 
            print("id de l'élève :",us) 
            ugroupe="Salle"+str(content.get("parcours"))
            self.ugroupe=ugroupe
            print("champ user recu ",content.get("user"))
            print("il est ajouté au layer de tout le groupe, qui se nomme '{}'".format(ugroupe))
            await self.channel_layer.group_add(ugroupe,self.channel_name)
            uperso=ugroupe+'perso'+str(us)
            #print("il est aussi ajouté à un layer contenant juste lui et le prof, qui se nomme",uperso)
            #await self.channel_layer.group_add(uperso,self.channel_name)
     
            #print("on envoie les infos au layer général pour que le prof soit informé")
            await self.channel_layer.group_send(ugroupe, 
                {'type' : "connexion.eleve",
                 'user' : self.scope["user"],
                 'channel' : self.channel_name})
            print("envoi ok")
        if command=="student_message"  :
            message=content.get("message",None)
            print("on va déclencher l'évènement message eleve au groupe '{}'".format(self.ugroupe))
            print("message : '{}'".format(message))
            await self.channel_layer.group_send(self.ugroupe,
               {'type' : "student.message",
                'from' : self.scope['user'].id, #expéditeur
                'message' : message,
                'name' : self.scope['user'].first_name +" "+  self.scope['user'].last_name ,
                })
            print("évènement student_message déclenché à tout le groupe")
        if command=="teacher_message" :
            print("command teacher_message recue" ,content)
            message=content.get("message",None)
            
            #print("on va déclencher l'évènement teacher_message à tout le groupe '{}'".format(self.ugroupe))
            print("message : '{}'".format(message))
            await self.channel_layer.group_send(self.ugroupe,
               {'type' : "teacher.message",
                'to' : content.get('to',None),   #le destinataire à été envoyé par le client-prof
                'message' : message})
            print("évènement déclenché à tout le groupe")
        if command=="teacher_message_general" :
             print("message general du prof")
             message=content.get("message",None)
             print("message ", message)
             print("ugroupe ", self.ugroupe)
             await self.channel_layer.group_send(self.ugroupe,
                {'type' : "teacher.message.general",
                 'message' : message})
             print("evenement declenché pour tout le groupe")	





    async def student_message(self,data) : #message envoyé par l'élève au prof
        print("entree dans la fonction student_message")
        print('user : ', self.scope['user'], self.role)
        if self.role==2 :   #c'est le prof qui reçoit, il faut donc lui envoyer
            print("Envoyé par l'élève {}".format(data["from"]))
            print("message :", data['message'])
            await self.send_json({'type':'message','from': str(data["from"]),"message" : str(data['message']) , 'name' : data["name"]  })
    
    async def teacher_message(self,data) : #message envoyé par le prof à un eleve
        print("entree dans la fonction teacher_message")
        print('user : ', self.scope['user'], self.scope['user'].id,self.role)
        print("self", self.scope['user'].id, "de type", type(self.scope['user'].id))
        print("destinataire", data['to'],type(data['to']))
        if  self.scope['user'].id == data['to'] : #on est dans l'instance de l'élève destinataire
            print("Envoyé à l'élève {}".format(data["to"]))
            print("message :", data['message'])
            await self.send_json({'type':'message','to': data["to"],"message" : data['message']})
            print("ok")
        else :
            print("self n'est pas le destinataire du message, rien à faire")

    async def teacher_message_general(self,data) : #message envoyé par le prof à tous les eleves
          print("entree dans teacher message general")
          await self.send_json({'type':'message','from': "prof", "name": "moi", "message" : str(data['message'])})


    async def connexion_eleve(self,data):
            print("entree dans la fonction connexion eleve")
            print("data=",data)
            print("destinataire {} (role : {})".format(self.scope['user'], self.role))
            if self.role==2 :
                print("destinataire : le prof")
                self.connected_students[data['user'].id]=(data['channel'],data['user'])
                print("connected_students : ", self.connected_students)
                await self.send_json({'type' : 'connexion' , 'from' : data["user"].id })



