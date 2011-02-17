"""A network control library for Richmond Sound Design's SoundMan software.

This code connects over TCP to the SoundMan server and communicates using the "SoundMan-Script" protocol.
Information on the protocol is here: http://www.richmondsounddesign.com/soundman-script.html

NOTE: The SoundMan server allows only 16 concurrent connections, so all clients should judiciously close connections.

- this library only uses TCP (Richmond charges extra for UDP)

Commands, responses, and tokens:

- commands are ended by semi-colons or CR (they accept \\n or \\r\\n)
- everything between a semi-colon and a CR is a comment and ignored
- tokens can be separated by multiple spaces or tabs
- some tokens have optional spaces (e.g. I5 == I 5)
- command responses begin with "OK" or "ERROR <undocumented 4 digit error code>"
- command responses are upper case and always end with \\r\\n
- all single line responses (command or query) are terminated by semi-colon except OK and ERROR
- if the first line isn't OK or ERROR and it doesn't end with a semi-color, it's a multiline response
- multiline responses are terminated by a line containing just a period: ".\\r\\n"
- inquiry command responses are not always upper case and may be multiple lines
- command tokens are not case sensitive, allowing all up or down or mixes
- responses may be multiple lines
- command control responses are first-come-first-served and synchronous
- except for the periodic responses to commands like GET VU

Opening welcome:

When the connection is made the server will send a welcome that is three OK lines followed by a period terminator:
OK some text\\r\\n
OK some more text\\r\\n
OK even more text\\r\\n
.\\r\\n


Basic syntax:

GET <item type> <item identifier> <item property>

- each GET references a single item

SET <item type> <item identifiers> <item property> <property value>

- each SET can reference multiple items

Synonyms:

- I == IN == INPUT
- O == OUT == OUTPUT
- CHAN == CHANNEL
- X == XPOINT == CROSSPOINT
- PX == PBXPOINT == PLAYBACKCROSSPOINT
- "-" == TO

IDs: 

- Single: I5, OUTPUT 5, PB 23, X1.1 (input.output)
- Ranges: INPUT4-11, O 3-9, PB1 TO 6, X1.2-16
- Mixes: I6-23 26 30-43, 
- commas can be used instead of spaces: I 6-23,26,30-43 (but not for X or PX, which it looking for periods)

Gains:

- 1 is full
- .5 is -6db
- 2 is double normal, so be careful about clipping

"""
import telnetlib
import pprint
import traceback
import socket
import sys

class SoundManControl:
	def __init__(self, host, port=20000):
		self.host = host
		self.port = port
		self.receive_size = 1024 * 5
	
	def play(self):
		pass
	
	def is_playing(self):
		pass
	
	def get_gains(self, channel_list):
		response = self.send_command('GET CHAN %s GAIN' % channel_list)
		return (self.parse_gains(response), response)

	def parse_gains(self, response):
		print response
		tokens = response.split(' ')
		if tokens[0].lower() != 'gain': return None
		results = {}
		for token in tokens[1:]:
			key, val = token.split('=')
			print token, key, val
			results[key] = float(val)
		return results

	def is_an_error_response(self, response): return response == None or len(response) == 0 or response.startswith('ERROR')

	def read_result(self, sock):
		result = ''
		finished_header = False
		while True:
			value = sock.recv(self.receive_size)
			print 'RECV: %s' % repr(value)
			if value == None or len(value) == 0: break
			if not finished_header:
				header_end = value.find("\r\n.\r\n")
				if header_end != -1:
					finished_header = True
					value = value[header_end + 5:]

			if finished_header:	
				result = result + value
				print 'RESULT %s' % repr(result)
				if result.endswith("\r\n.\r\n") or result.endswith("OK\r\n") or result == 'OK' or result.startswith('ERROR ') or result.endswith(';\r\n'): break

		if not finished_header: raise Exception("Did not find the end of the SoundMan greeting: %s" % value)
		result = result.strip()
		if result.endswith(';'):result = result[0:-1]
		return result

	def send_command(self, command):
		"Sends a command to the device.  Returns the result code or None if it can't control the device."
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(15)
		try:
			sock.connect((self.host, self.port))
			sock.send('%s\r\n' % command)
			value = self.read_result(sock)
			if value == '': 
				sock.close()
				return None
			sock.close()
			return value
		except:
			value = None
			traceback.print_exc() 
			sock.close()
			return value

def main(sm_control):
	while True:
		sys.stdout.write('SOUNDMAN COMMAND >>')
		line = raw_input()
		if line == None: break
		line = line.strip()
		if len(line) == 0: continue
		response = sm_control.send_command(line)
		if response: print response

def print_help():
	print 'soundmain_control <host>'

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print_help()
		sys.exit(2)
	try:
		sm_control = SoundManControl(sys.argv[1])
		main(sm_control)
	except EOFError:
		pass				
	except KeyboardInterrupt:
		pass
	print

# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
