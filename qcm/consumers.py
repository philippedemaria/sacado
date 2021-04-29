from channels.generic.websocket import WebsocketConsumer
import json
from time import sleep
from random import randint 
 
 

class RealConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        for i in range(20):
            self.send(json.dumps({ 'message' : randint(1,100)}))
            sleep(1)

 
 