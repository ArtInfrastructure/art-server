import telnetlib
import pprint
import traceback

class IBootControl:
	"""A control object for Dataprobe's iBoot network attached remote power controller"""
	def __init__(self, host, port, password):
		"""The port should be the telnet port, not the http or heartbeat port"""
		self.host = host
		self.port = port
		self.password = password

	def query_iboot_state(self):
		"""Returns True if it is on, False if it is off, None if it could not be reached"""
		result = self.send_command('q')
		if result == None: return None
		return result == 'ON'

	def turn_on(self): return send_command('n') == 'ON'

	def turn_off(self): return send_command('f') == 'OFF'

	def cycle_power(self): return send_command('c') == 'CYCLE'

	def send_command(self, command):
		"Sends a command to the device.  Returns the result code or None if it can't control the device."
		telnet = telnetlib.Telnet()
		try:
			telnet.open(self.host, self.port)
			telnet.write(self.format_command(command))
			value = telnet.read_until('\n', 2)
			if value == '': return None
			return value
		except:
			print pprint.pformat(traceback.format_exc()) 
		finally:
			telnet.close()
		return None

	def format_command(self, action):
		return '\x00\x1d%s\x00\x1d%s\x00\x0d' % (self.password, action)

