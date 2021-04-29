from channels.generic.websocket import WebsocketConsumer
import json
from time import sleep
from django.db.models.signals import m2m_changed
#from asgiref.sync import async_to_sync
#from channels.layers import get_channel_layer
from django.dispatch import receiver
from tool.models import Generate_quizz

 

class RealConsumer(WebsocketConsumer):

    def connect(self,message):
        self.accept()


        # nb_students = gquizz.players.count()
        # self.send(json.dumps({ 'nb_students' : nb_students}))
    def get_new_player(sender, instance ,  **kwargs):
        if kwargs['created'] :
            nb_students = instance.students.count()
            self.send(json.dumps({ 'nb_students' : nb_students}))




    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json["message"] = "hello"
        self.send(json.dumps(message_json))



    def disconnect(self, message):
        pass


 
    m2m_changed.connect(get_new_player, sender=Generate_quizz.students)   


  

# from channels.generic.websocket import AsyncJsonWebsocketConsumer


# class RealConsumer(AsyncJsonWebsocketConsumer):

#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("gossip", self.channel_name)
#         print(f"Added {self.channel_name} channel to gossip")

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("gossip", self.channel_name)
#         print(f"Removed {self.channel_name} channel to gossip")

#     async def user_gossip(self, event):
#         await self.send_json(event)
#         print(f"Got message {event} at {self.channel_name}")