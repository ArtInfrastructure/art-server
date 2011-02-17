import socket, select, time, traceback
import threading

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from incus.soundman_control import SoundManControl

class MockChannel:
	def __init__(self, id, channel_type='i', gain=0, mute=False):
		self.channel_type = channel_type
		self.id = id
		self.gain = gain
		self.mute = mute

	@property
	def name(self): return '%s%s' % (self.channel_type, self.id)

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
		
		self.inputs = [MockChannel(i, 'i') for i in range(15)]
		self.outputs = [MockChannel(i, 'o') for i in range(15)]
		self.playbacks = [MockChannel(i, 'p') for i in range(5)]

		threading.Thread.__init__(self)

	def strip_int(self, raw): return int(''.join([c for c in raw if c.isdigit()]))

	def get_channel(self, name):
		id = self.strip_int(name)
		if name.lower().startswith('i') and id < len(self.inputs): return self.inputs[id]
		if name.lower().startswith('o') and id < len(self.outputs): return self.outputs[id]
		if name.lower().startswith('p') and id < len(self.playbacks): return self.playbacks[id]
		return None
		
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
				elif data.lower().startswith('get chan '):
					channel_names, attributes = self.parse_chan_list(data)
					response = attributes[0]
					if attributes[0] == 'gain':
						for channel_name in channel_names:
							channel = self.get_channel(channel_name)
							response += ' %s=%s' % (channel.name, channel.gain)
					elif attributes[0] == 'mute':
						for channel in channels: response += ' %s=OFF' % channel
					else:
						response = 'ERROR 4444'
				elif data.lower().startswith('set chan '):
					channel_names, attributes = self.parse_chan_list(data, end_token_count=2)
					for channel_name in channel_names:
						channel = self.get_channel(channel_name)
						if attributes[0] == 'gain':
							channel.gain = float(attributes[1])
							response = 'OK'
						else:
							response = 'ERROR 3333'
				else:
					response = 'ERROR 1234'
				client.send(('%s\r\n' % response).encode())
				client.close()
			except (socket.timeout):
				continue
			except:
				traceback.print_exc()
		self.server.close()

	def parse_chan_list(self, data, end_token_count=1):
		tokens = data.split(' ')
		channels = []
		for token in tokens[2:-1 * end_token_count]: channels.append(token)
		return (channels, [token.lower() for token in tokens[-1 * end_token_count:]])
		
class SoundManControlTest(TestCase):
	
	def setUp(self):
		self.sm_server = MockSoundManServer()
		self.sm_server.start()
		time.sleep(1)

	def tearDown(self):
		self.sm_server.stop_server()
	
	def test_control(self):
		sm_control = SoundManControl(self.sm_server.server.getsockname()[0], self.sm_server.server.getsockname()[1])
		test_message = 'FOOF FOR THOUGHT'
		result = sm_control.send_command('ECHO %s' % test_message)
		self.failUnlessEqual(result, test_message)
		result = sm_control.send_command('MAKE_AN_ERROR')
		self.failUnless(result.startswith('ERROR '))
		
		data, response = sm_control.get_gains('o1 o2 o3 p4')
		self.failUnlessEqual(data['o1'], 0)
		self.failUnlessEqual(data['o2'], 0)
		self.failUnlessEqual(data['o3'], 0)
		self.failUnlessEqual(data['p4'], 0)
		
		sm_control.set_gains({'o1':2, 'o2':4, 'p3':6})
		data, response = sm_control.get_gains('o1 o2 p3 p4')
		#print 'set', data, response
		self.failUnlessEqual(data['o1'], 2)
		self.failUnlessEqual(data['o2'], 4)
		self.failUnlessEqual(data['p3'], 6)
		self.failUnlessEqual(data['p4'], 0)

		sm_control.set_gains({'o1':0, 'o2':0, 'p3':0})
		data, response = sm_control.get_gains('o1 o2 p3 p4')
		self.failUnlessEqual(data['o1'], 0)
		self.failUnlessEqual(data['o2'], 0)
		self.failUnlessEqual(data['p3'], 0)
		self.failUnlessEqual(data['p4'], 0)

