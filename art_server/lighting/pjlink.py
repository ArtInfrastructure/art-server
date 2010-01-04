#!/usr/bin/python
"""Classes which are useful when controlling projectors using the PJLink protocol.
	Information on the PJLink protocol can be found here: http://pjlink.jbmia.or.jp/english/
"""
import socket
import pprint, traceback
import sys, time

class PJLinkProtocol:
	"""Holds the constants for the PJLink protocol"""
	# COMMAND LINE DATA
	ON = "1"
	OFF = "0"
	QUERY = "?"
	VIDEO_MUTE_ON = "11"
	VIDEO_MUTE_OFF = "10"
	AUDIO_MUTE_ON = "21"
	AUDIO_MUTE_OFF = "20"
	AUDIO_VIDEO_MUTE_ON = "31"
	AUDIO_VIDEO_MUTE_OFF = "30"
	
	# INPUT
	RGB_INPUT = "1"
	VIDEO_INPUT = "2"
	DIGITAL_INPUT = "3"
	STORAGE_INPUT = "4"
	NETWORK_INPUT = "5"
	INPUT_1 = "1"
	INPUT_2 = "2"
	INPUT_3 = "3"
	INPUT_4 = "4"
	INPUT_5 = "5"
	INPUT_6 = "6"
	INPUT_7 = "7"
	INPUT_8 = "8"
	INPUT_9 = "9"
	
	# COMMANDS
	POWER = "POWR"
	INPUT = "INPT"
	AVAILABLE_INPUTS = "INST"
	MUTE = "AVMT"
	ERROR_STATUS = "ERST"
	LAMP = "LAMP"
	NAME = "NAME"
	MANUFACTURE_NAME = "INF1"
	PRODUCT_NAME = "INF2"
	OTHER_INFO = "INFO"
	CLASS_INFO = "CLSS"
	AUTHENTICATE = "PJLINK"

	# RESPONSE
	OK = "OK"
	ERROR_1 = "ERR1"
	ERROR_2 = "ERR2"
	ERROR_3 = "ERR3"
	ERROR_4 = "ERR4"
	INVALID_PASSWORD_ERROR = 'ERRA'
	POWER_OFF_STATUS = "0"
	POWER_ON_STATUS = "1"
	COOLING_STATUS = "2"
	WARM_UP_STATUS = "3"
	UNAVAILABLE_STATUS = "ERR3"
	PROJECTOR_FAILURE_STATUS = "ERR4"
	ERROR_STATUS_OK = "0"
	ERROR_STATUS_WARNING = "1"
	ERROR_STATUS_ERROR = "2"

class PJLinkAuthenticationException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class PJLinkAuthenticationRequest:
	"""A codec for the PJLink request from the projector for authentication or an indicator that no authentication is required."""
	def __init__(self, password=None, seed=None):
		self.password = password
		self.seed = seed
		if self.seed == None and self.password != None: self.seed = PJLinkAuthenticationRequest.generate_seed()

	def encode(self):
		if self.seed:
			return '%s %s %s' % (PJLinkProtocol.AUTHENTICATE, PJLinkProtocol.ON, self.seed)
		else:
			return '%s %s' % (PJLinkProtocol.AUTHENTICATE, PJLinkProtocol.OFF)

	def authentication_hash_matches(self, auth_hash):
		if auth_hash == None: return self.seed == None
		if self.seed == None: return False
		correct_hash = PJLinkAuthenticationRequest.generate_hash(self.seed, self.password)
		return correct_hash == auth_hash

	@classmethod
	def decode(cls, encoded_request):
		tokens = encoded_request.split(' ')
		if tokens[1] == PJLinkProtocol.ON:
			return PJLinkAuthenticationRequest(seed=tokens[2])
		else:
			return PJLinkAuthenticationRequest()

	@classmethod
	def generate_hash(cls, seed, password):
		import random, hashlib
		m = hashlib.md5()
		m.update('%s %s' % (seed, password))
		return m.hexdigest()

	@classmethod
	def generate_seed(cls):
		import random
		"""Generate a random seed string which is four numbers, each in two character ASCII hex format"""
		return ''.join([('%x' % random.randint(0,255)) for i in range(4)])

class PJLinkCommandLine:
	"""Encoding and decoding methods for PJLink commands
		Encoded command lines are of the following format:
		<header><command><space><data><carriage return>
		Header: two bytes: the percent symbol followed by the number 1 (for version)
		Command: four bytes: something like POWR or LINE (see PJLinkProtocol) 
		Data: command specific data like "1" for on when using POWR, with 128 bytes or less
		
		An example: %%1POWR 1\\r
	"""
	def __init__(self, command, data, version=1, authentication_hash=None):
		self.command = command
		self.data = data
		self.version = version
		self.authentication_hash = authentication_hash

	def encode(self):
		"""Encode the command in the transmission format"""
		if self.authentication_hash:
			return '%s%%%s%s %s\r' % (self.authentication_hash, self.version, self.command, self.data)
		else:
			return '%%%s%s %s\r' % (self.version, self.command, self.data)

	@classmethod
	def decode(cls, encoded_command_line):
		"""Decode the raw data and return a PJLinkCommandLine instance."""
		auth_token, encoded_command = encoded_command_line.strip().split('%')
		if len(auth_token) == 0: auth_token = None
		version = int(encoded_command[0:1])
		command = encoded_command[1:5]
		data = encoded_command[6:len(encoded_command_line) - 1]
		return PJLinkCommandLine(command, data, version, auth_token)

class PJLinkResponse:
	"""Encoding and decoding methods for PJLink responses from the projector
		Encoded command lines are of the following format:
		<header><echo command><equal sign><data><carriage return>
		Header: two bytes: the percent symbol followed by the number 1 (for version)
		Command: four bytes: the command used in the command line, echoed back
		Data: response data like "OK", "ERR1", "ERR2", or "ERR3"
		
		An example:
			In response to a command line like: %%1POWR ?\\r
			The projector would send: %%1POWR=2\\r
			That would indicate that it is in state #2, which is lamp off but cooling
	"""
	def __init__(self, command, data, version=1):
		self.command = command
		self.data = data
		self.version = version

	def encode(self):
		"""Encode the command in the transmission format"""
		if self.version:
			return '%%%s%s=%s\r' % (self.version, self.command, self.data)
		else:
			return '%s=%s\r' % (self.command, self.data)

	@classmethod
	def decode(cls, encoded_command_line):
		"""Decode the raw data and return a PJLinkResponse instance"""
		if encoded_command_line[0] == '%': # It's a non-auth response
			version = int(encoded_command_line[1:2])
			command = encoded_command_line[2:6]
			data = encoded_command_line[7:len(encoded_command_line) - 1]
			return PJLinkResponse(command, data, version)
		if encoded_command_line.startswith('%s=%s' % (PJLinkProtocol.AUTHENTICATE, PJLinkProtocol.INVALID_PASSWORD_ERROR)):
			return PJLinkResponse(PJLinkProtocol.AUTHENTICATE, PJLinkProtocol.INVALID_PASSWORD_ERROR)

class PJLinkController:
	"""A command object for projectors which are controlled using the PJLink protocol"""
	def __init__(self, host, port=4352, password=None, version=1):
		self.host = host
		self.port = port
		self.password = password
		self.version = 1

	def power_on(self):
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.POWER, PJLinkProtocol.ON, self.version))
		return response.data == PJLinkProtocol.OK

	def power_off(self):
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.POWER, PJLinkProtocol.OFF, self.version))
		return response.data == PJLinkProtocol.OK
	
	def query_power(self):
		"""Return a power status constant from PJLinkProtocol or one of the Errors (directly from projector)"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.POWER, PJLinkProtocol.QUERY, self.version))
		return response.data

	def set_input(self, input_type, input_number):
		"""Set the projector type and input using PJLinkProtocol constants like PJLinkProtocol.RGB_INPUT and PJLinkProtocol.INPUT_3"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.INPUT, '%s%s' % (input_type, input_number), self.version))
		return response.data == PJLinkProtocol.OK

	def query_input(self):
		"""Return a tuple: <input type, input number> like (PJLinkProtocol.RGB_INPUT, PJLinkProtocol.INPUT_3)"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.INPUT, PJLinkProtocol.QUERY, self.version))
		if len(response.data) != 2: return (None, None)
		return (response.data[0], response.data[1])

	def query_available_inputs(self):
		"""Return an array of tuples: [<input type, input number>] similar to the results of query_input"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.AVAILABLE_INPUTS, PJLinkProtocol.QUERY, self.version))
		return [[input_type[0], input_type[1]] for input_type in response.data.split(' ')]

	def query_mute(self):
		"""Return a tuple of booleans: <audio is muted, video is muted>"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.MUTE, PJLinkProtocol.QUERY, self.version))
		if len(response.data) != 2: return (None, None)
		audio_is_muted = response.data == PJLinkProtocol.AUDIO_MUTE_ON or response.data == PJLinkProtocol.AUDIO_VIDEO_MUTE_ON
		video_is_muted = response.data == PJLinkProtocol.VIDEO_MUTE_ON or response.data == PJLinkProtocol.AUDIO_VIDEO_MUTE_ON
		return (audio_is_muted, video_is_muted)

	def set_mute(self, mute_state):
		"""Set the audio and video playback to mute or... unmute?  Use the PJLinkProtocol constants as the mute_state."""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.MUTE, mute_state, self.version))
		return response.data == PJLinkProtocol.OK

	def query_error_status(self):
		"""Return a set of error states: (fan status, lamp status, filter status, cover status, other status)"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.ERROR_STATUS, PJLinkProtocol.QUERY, self.version))
		if len(response.data) != 5: return (None, None, None, None, None)
		return (response.data[0], response.data[1], response.data[2], response.data[3], response.data[4])

	def query_lamps(self):
		"""Return an array of lamp lighting-hours and a boolean lamp-is-on value: [('100', True), ('142', False), (lighting-hours, is-on), ...]"""
		response = self._send_command_line(PJLinkCommandLine(PJLinkProtocol.LAMP, PJLinkProtocol.QUERY, self.version))

		results = [[int(lit_time)] for lit_time in response.data.split(' ')[::2]]
		for index, lamp_id in enumerate(response.data.split(' ')[1::2]):
			results[index].append(int(lamp_id) == 1)
		return results

	def query_name(self): return self._send_command_line(PJLinkCommandLine(PJLinkProtocol.NAME, PJLinkProtocol.QUERY, self.version)).data
	def query_manufacture_name(self): return self._send_command_line(PJLinkCommandLine(PJLinkProtocol.MANUFACTURE_NAME, PJLinkProtocol.QUERY, self.version)).data
	def query_product_name(self): return self._send_command_line(PJLinkCommandLine(PJLinkProtocol.PRODUCT_NAME, PJLinkProtocol.QUERY, self.version)).data
	def query_other_info(self): return self._send_command_line(PJLinkCommandLine(PJLinkProtocol.OTHER_INFO, PJLinkProtocol.QUERY, self.version)).data
	def query_class_info(self): return self._send_command_line(PJLinkCommandLine(PJLinkProtocol.CLASS_INFO, PJLinkProtocol.QUERY, self.version)).data

	def _send_command_line(self, command_line):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(15)
		sock.connect((self.host, self.port))
		encoded_auth_request = sock.recv(512)
		#print '\n\nauth request', encoded_auth_request
		auth_request = PJLinkAuthenticationRequest.decode(encoded_auth_request)
		if auth_request.seed:
			if self.password:
				command_line.authentication_hash = PJLinkAuthenticationRequest.generate_hash(auth_request.seed, self.password)
			else:
				sock.close()
				raise PJLinkAuthenticationException('The Projector requires a password, but we have none')
			
		#print 'sending', command_line.encode()
		sock.send(command_line.encode())
		encoded_response = sock.recv(512)
		#print 'received', encoded_response
		sock.close()
		if encoded_response == '': encoded_response = None
		response = PJLinkResponse.decode(encoded_response)
		if response.command == PJLinkProtocol.AUTHENTICATE and response.data == PJLinkProtocol.INVALID_PASSWORD_ERROR:
			raise PJLinkAuthenticationException('The projector rejected our password')
		return response

USAGE_MESSAGE = 'usage: pjlink [projector]'

def main():
	from django.core.management import setup_environ
	import settings
	setup_environ(settings)
	try:
		action = sys.argv[1]
	except IndexError:
		print USAGE_MESSAGE
		return
	if action == 'projector':
		from tests.test_lighting import MockPJLinkProjector
		projector = MockPJLinkProjector()
		projector.port = 4352
		projector.start()
		seconds_to_wait = 5
		while projector.running == False and seconds_to_wait > 0:
			time.sleep(1)
			seconds_to_wait -= 1
		if not projector.running:
			print 'Could not start the projector'
			return
		print 'Projector running: %s:%s' % (projector.server.getsockname()[0], projector.server.getsockname()[1])
		while True: time.sleep(100)
	else:
		print USAGE_MESSAGE
		return

if __name__ == "__main__":
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
