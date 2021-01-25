from channels.generic.websocket import WebsocketConsumer
import json
from time import sleep


class RealConsumer(WebsocketConsumer):

	def connect(self):
		self.accept()


		for i in range (20):
			self.send(json.dumps({ 'value' : i}))
			sleep(1)



     def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        self.send(text_data="Hello world!")
        # Or, to send a binary frame:
        self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        self.close()
        # Or add a custom WebSocket error code!
        self.close(code=4123)

    def disconnect(self, close_code):
        # Called when the socket closes