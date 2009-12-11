#!/usr/bin/python
"""Classes which are useful when controlling projectors using the PJLink protocol.
	Information on the PJLink protocol can be found here: http://pjlink.jbmia.or.jp/english/
"""
import socket
import pprint, traceback

class PJLinkProtocol:
	"""Holds the constants for the PJLink protocol"""
	# COMMAND LINE DATA CONSTANTS
	ON = "1"
	OFF = "2"
	QUERY = "?"
	VIDEO_MUTE_ON = "11"
	VIDEO_MUTE_OFF = "10"
	AUDIO_MUTE_ON = "21"
	AUDIO_MUTE_OFF = "20"
	AUDIO_VIDEO_MUTE_ON = "31"
	AUDIO_VIDEO_MUTE_OFF = "30"
	
	# COMMANDS
	POWER = "POWR"
	INPUT = "INPT"
	MUTE = "AVMT"
	ERROR_STATUS = "ERST"
	LAMP = "LAMP"
	NAME = "NAME"
	MANUFACTURE_NAME = "INF1"
	PRODUCT_NAME = "INF2"
	OTHER_INFO = "INFO"
	CLASS_INFO = "CLSS"

	# RESPONSE CONSTANTS
	OK = "OK"
	ERROR_1 = "ERR1"
	ERROR_2 = "ERR2"
	ERROR_3 = "ERR3"
	ERROR_4 = "ERR4"
	POWER_OFF_STATUS = "0"
	POWER_ON_STATUS = "1"
	COOLING_STATUS = "2"
	WARM_UP_STATUS = "3"
	UNAVAILABLE_STATUS = "ERR3"
	PROJECTOR_FAILURE_STATUS = "ERR4"
	
class PJLinkCommandLine:
	"""Encoding and decoding methods for PJLink commands
		Encoded command lines are of the following format:
		<header><command><space><data><carriage return>
		Header: two bytes: the percent symbol followed by the number 1 (for version)
		Command: four bytes: something like POWR or LINE (see PJLinkProtocol) 
		Data: command specific data like "1" for on when using POWR, with 128 bytes or less
		
		An example: %%1POWR 1\\r
	"""
	def __init__(self, command, data, version=1):
		self.command = command
		self.data = data
		self.version = version

	def encode(self):
		"""Encode the command in the transmission format"""
		return '%%%s%s %s\r' % (self.version, self.command, self.data)

	@classmethod
	def decode(cls, encoded_command_line):
		"""Decode the raw data and return a PJLinkCommandLine instance"""
		version = int(encoded_command_line[1:2])
		command = encoded_command_line[2:6]
		data = encoded_command_line[7:len(encoded_command_line) - 1]
		return PJLinkCommandLine(command, data, version)

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
		return '%%%s%s=%s\r' % (self.version, self.command, self.data)

	@classmethod
	def decode(cls, encoded_command_line):
		"""Decode the raw data and return a PJLinkResponse instance"""
		version = int(encoded_command_line[1:2])
		command = encoded_command_line[2:6]
		data = encoded_command_line[7:len(encoded_command_line) - 1]
		return PJLinkResponse(command, data, version)

class PJLinkController:
	"""A command object for projectors which are controlled using the PJLink protocol"""
	def __init__(self, host, port=4352, password=None, version=1):
		self.host = host
		self.port = port
		self.password = password
		self.version = 1

	def power_on(self):
		response = self.send_command_line(PJLinkCommandLine(PJLinkProtocol.POWER, PJLinkProtocol.ON, self.version))
	
	def send_command_line(self, command_line):
		print 'request:', command_line.encode()
		encoded_response = self.raw_round_trip(command_line.encode())
		print'response:', encoded_response
		return PJLinkResponse.decode(encoded_response)

	def raw_round_trip(self, data):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(15)
			sock.connect((self.host, self.port))
			sock.send(data)
			value = sock.recv(512)
			sock.close()
			if value == '': return None
			return value
		except:
			print pprint.pformat(traceback.format_exc()) 
			sock.close()
			return None

def main():
	pass

if __name__ == "__main__":
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
