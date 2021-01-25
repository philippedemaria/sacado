# from channels.generic.websocket import WebsocketConsumer
# import json
# from time import sleep


# class RealConsumer(WebsocketConsumer):

# 	def connect(self):
# 		self.accept()


# 		for i in range (20):
# 			self.send(json.dumps({ 'value' : i}))
# 			sleep(1)


from channels.generic.websocket import AsyncJsonWebsocketConsumer


class RealConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("gossip", self.channel_name)
        print(f"Added {self.channel_name} channel to gossip")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gossip", self.channel_name)
        print(f"Removed {self.channel_name} channel to gossip")

    async def user_gossip(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")