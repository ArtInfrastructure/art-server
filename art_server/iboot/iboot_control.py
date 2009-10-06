# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""A control library for Dataprobe iBoot Network Attached Remote Power Controllers.
	The TCP protocol is passed over the same port as the iBoot uses for HTTP, which defaults to 80."""
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
			if value == '': 
				sock.close()
				return None
			return value
		except:
			print pprint.pformat(traceback.format_exc()) 
		sock.close()
		return None

	def format_command(self, action):
		return '\x1b%s\x1b%s\x0d' % (self.password, action)

