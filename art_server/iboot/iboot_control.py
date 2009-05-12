import telnetlib
import pprint
import traceback
import socket

class IBootControl:
	"""A control object for Dataprobe's iBoot network attached remote power controller"""
	def __init__(self,  password, host, port=80):
		"""The port should be the telnet port, not the http or heartbeat port"""
		self.password = password
		self.host = host
		self.port = port

	def query_iboot_state(self):
		"""Returns True if it is on, False if it is off, None if it could not be reached"""
		result = self.send_command('q')
		if result == None: return None
		return result == 'ON'

	def toggle(self):
		if self.query_iboot_state():
			return self.turn_off()
		else:
			return self.turn_on()

	def turn_on(self): return self.send_command('n') == 'ON'

	def turn_off(self): return self.send_command('f') == 'OFF'

	def cycle_power(self): return self.send_command('c') == 'CYCLE'

	def send_command(self, command):
		"Sends a command to the device.  Returns the result code or None if it can't control the device."
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)
		try:
			sock.connect((self.host, self.port))
			msg = self.format_command(command)
			sock.send(msg)
			value = sock.recv(20)
			if value == '': return None
			return value
		except:
			print pprint.pformat(traceback.format_exc()) 
		finally:
			sock.close()
		return None

	def format_command(self, action):
		return '\x1b%s\x1b%s\x0d' % (self.password, action)

