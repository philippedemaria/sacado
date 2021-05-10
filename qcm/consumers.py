from channels.generic.websocket import WebsocketConsumer , AsyncJsonWebsocketConsumer
import json
from time import sleep
from random import randint 

 




# class RealConsumer(WebsocketConsumer):

#     def connect(self):
#         self.accept()

#         for i in range(20):
#             self.send(json.dumps({ 'message' : randint(1,100)}))
#             sleep(1)






 
class RealConsumer(WebsocketConsumer):

    def connect(self):
        print("Connected")
        # self.parcours_id = self.scope['url_route']['kwargs']['parcours_id']
        # self.room_parcours_id = 'room_%s' % self.parcours_id

        # # Join room group
        # self.channel_layer.group_add(
        #     self.room_parcours_id,
        #     self.channel_name
        # )
        self.accept()


    def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        self.channel_layer.group_discard(
            self.room_parcours_id,
            self.channel_name
        )




    # async def receive(self, text_data):
    #     """
    #     Receive message from WebSocket.
    #     Get the event and send the appropriate event
    #     """
    #     response = json.loads(text_data)
    #     event = response.get("event", None)
    #     message = response.get("message", None)
    #     if event == 'MOVE':
    #         # Send message to room group
    #         await self.channel_layer.group_send(self.room_parcours_id, {
    #             'type': 'send_message',
    #             'message': message,
    #             "event": "MOVE"
    #         })

    #     if event == 'START':
    #         # Send message to room group
    #         await self.channel_layer.group_send(self.room_parcours_id, {
    #             'type': 'send_message',
    #             'message': message,
    #             'event': "START"
    #         })

    #     if event == 'END':
    #         # Send message to room group
    #         await self.channel_layer.group_send(self.room_parcours_id, {
    #             'type': 'send_message',
    #             'message': message,
    #             'event': "END"
    #         })


    # async def send_message(self, res):
    #     """ Receive message from room group """
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         "payload": res,
    #     }))