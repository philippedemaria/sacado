from channels.generic.websocket import WebsocketConsumer
import json
from time import sleep


class RealConsumer(WebsocketConsumer):

	def connect(self):
		self.accept()


		for i in range (20):
			self.send(json.dumps({ 'value' : i }))
			sleep(1)


