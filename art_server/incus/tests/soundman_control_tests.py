import socket, select
import threading

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from incus.soundman_control import SoundManControl

class MockSoundManServer(threading.Thread):
	"""This creates a single threaded localhost server socket which speaks the SoundMan protocol"""

	GREETING = """OK                      *********************************\r\nOK                      ** Welcome to SoundMan-Server! **\r\nOK                      *********************************\r\n.\r\n"""

	def __init__(self):
		self.backlog = 5 
		self.timeout = 2
		self.buffer_size = 1024
		self.server = None
		self.running = False

		self.port = 0 # 0 indicates that the server should use any open socket
		
		threading.Thread.__init__(self)

	def stop_server(self):
		self.running = False
		if self.server: self.server.close()
	
	def run(self): 
		if self.running: return
		self.server = socket.socket()
		self.server.settimeout(self.timeout)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind(('127.0.0.1',self.port)) 
		self.server.listen(self.backlog)
		self.running = True
		while self.running:
			try:
				client, address = self.server.accept()
				client.setblocking(1)
				client.send(MockSoundManServer.GREETING)
				data = client.recv(self.buffer_size) 
				if not data:
					client.close()
					continue
				data = data.strip()
				#print 'Received ', data
				response = None
				if data.startswith('ECHO '): # A fake command that we use for testing the parser
					response = '%s;' % data[len('ECHO '):]
				else:
					response = 'ERROR 1234'
				client.send(('%s\r\n' % response).encode())
				client.close()
			except (socket.timeout):
				continue
		self.server.close()

class SoundManControlTest(TestCase):
	
	def setUp(self):
		self.sm_server = MockSoundManServer()
		self.sm_server.start()

	def tearDown(self):
		self.sm_server.stop_server()
	
	def test_control(self):
		sm_control = SoundManControl(self.sm_server.server.getsockname()[0], self.sm_server.server.getsockname()[1])
		test_message = 'FOOF FOR THOUGHT'
		result = sm_control.send_command('ECHO %s' % test_message)
		self.failUnlessEqual(result, test_message)
		result = sm_control.send_command('MAKE_AN_ERROR')
		self.failUnless(result.startswith('ERROR '))
		
