"""This sets the values of the projector dimming control panel via the network"""
import sys
import socket
import traceback

class CrestonControl(object):
	"""The Crestron controller class. 
	NOTE: This is not thread safe so use a controller in each thread."""
	def __init__(self, host, port=1313, timeout=15):
		self.host = host
		self.port = port
		self.timeout = timeout
		self.sock = None
		
	def can_connect(self): return self.ping() == 'Pong'

	def ping(self): return self.send_command('Ping')

	def raise_high(self): return self.send_command('HighLvlUp')
	def lower_high(self): return self.send_command('HighLvlDown')

	def raise_low(self): return self.send_command('DimLvlUp')
	def lower_low(self): return self.send_command('DimLvlDown')

	def query_status(self):
		"""
		Returns a map of status values like so:
		{'High': '55000', 'Current': '62965', 'Wake': '5:00 AM', 'Low': '62965', 'Lamp1': '2-1468', 'Sleep': '1:00 AM', 'Lamp2': '2-1469'}
		"""
		lines = self.send_command('Update', lines=9)
		results = {}
		for line in lines:
			key, sep, val = line.partition('-')
			results[key] = val
		return results


	def toggle_dim(self):
		"""Returns True if enabled, False if disabled, and None if there is an error"""
		result = self.send_command('EnableDim')
		if result == None: return None
		return result == 'DimEnabled'

	def close(self):
		if self.sock:
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()
			self.sock = None

	def format_command(self, command): return '%s%s' % (command, '\r\n')

   	def send_command(self, command, lines=1):
		"""
		Sends a command to the device.
		If lines == 1: it returns a string
		if lines > 1: it returns an array of strings
		Returns None if it can't control the device.
		"""
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(self.timeout)
		try:
			self.sock.connect((self.host, self.port))
			welcome = self.sock.recv(1024)
			msg = self.format_command(command)
			self.sock.send(msg)
			results = []
			for i in range(lines):
				value = self.sock.recv(2048)
				if len(value.strip()) == 0: continue
				results.append(value.strip())
			if len(results) == 0:
				self.close()
				return None
			self.close()
			if lines == 1: return results[0]
			return results
		except:
			traceback.print_exc()
		self.close()
		return None

def main(control):
	while True:
		sys.stdout.write('COMMAND >> ')
		line = raw_input()
		if line == None: break
		line = line.strip()
		if len(line) == 0: continue
		if line == '\i':
			print control.query_status()
		else:
			response = control.send_command(line)
			if response: print response

def print_help():
	print 'python creston_control.py <host>'
	print 'Raw control commands can be entered.'
	print '\i queries the status'

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print_help()
		sys.exit(2)
	control = None
	try:
		control = CrestonControl(sys.argv[1])
		if not control.can_connect(): raise(Exception('Could not connect to %s' % sys.argv[1]))
		main(control)
	except EOFError:
		pass				
	except KeyboardInterrupt:
		pass
	if control: control.close()
	print

# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
