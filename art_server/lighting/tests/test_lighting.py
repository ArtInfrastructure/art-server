from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
import socket, select
import threading
import pprint

from lighting.models import *
from lighting.pjlink import PJLinkCommandLine, PJLinkResponse, PJLinkProtocol, PJLinkController

APP_PATH = '/lighting/'

class MockPJLinkProjector(threading.Thread):
	def __init__(self):
		self.backlog = 5 
		self.buffer_size = 1024
		self.server = None
		self.running = False
		threading.Thread.__init__(self)

	def stop_server(self):
		self.running = False
	
	def run(self): 
		if self.running: return
		self.running = True
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		#self.server.settimeout(5)
		self.server.bind(('127.0.0.1',0)) 
		self.server.listen(self.backlog)
		print 'running'
		while self.running: 
			client, address = self.server.accept() 
			print dir(client)
			data = client.recv(self.buffer_size) 
			if data: 
				command_line = PJLinkCommandLine.decode(data)
				response = PJLinkResponse(PJLinkProtocol.POWER, PJLinkProtocol.POWER_ON_STATUS)
				client.send(response.encode())
			client.close() 
		self.server.close()
		
class PJLinkTest(TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	def test_controller(self):
		projector = MockPJLinkProjector()
		projector.start()
		
		controller = PJLinkController(projector.server.getsockname()[0], projector.server.getsockname()[1])
		controller.power_on()
		
		projector.server.close()
		
	def test_codecs(self):
		command1 = PJLinkCommandLine(PJLinkProtocol.POWER, PJLinkProtocol.ON)
		self.failUnlessEqual(command1.version, 1)
		self.failUnlessEqual(command1.command, PJLinkProtocol.POWER)
		self.failUnlessEqual(command1.data, PJLinkProtocol.ON)
		
		command2 = PJLinkCommandLine.decode(command1.encode())
		self.failUnlessEqual(command1.encode(), command2.encode())
		self.failUnlessEqual(command1.command, command2.command)
		self.failUnless(command1.data, command2.data)
		self.failUnless(command1.version, command2.version)
		
		response1 = PJLinkResponse(PJLinkProtocol.POWER, "1")
		self.failUnlessEqual(response1.version, 1)
		self.failUnlessEqual(response1.command, PJLinkProtocol.POWER)
		self.failUnlessEqual(response1.data, "1")
		
		response2 = PJLinkResponse.decode(response1.encode())
		self.failUnlessEqual(response1.encode(), response2.encode())
		self.failUnlessEqual(response1.version, response2.version)
		self.failUnlessEqual(response1.command, response2.command)
		self.failUnlessEqual(response1.data, response2.data)
