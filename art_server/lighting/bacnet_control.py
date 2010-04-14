#!/usr/bin/python

"""These functions wrap the bacnet command line apps from http://bacnet.sourceforge.net/
In your django settings you'll need a BACNET_BIN_DIR with the full path to the directory containing the compiled apps.
Like so (no slash on the end, please):
BACNET_BIN_DIR = '/usr/local/src/bacnet-stack-0.5.3/bin'
"""

import os, sys, subprocess
import settings
import logging

USAGE_MESSAGE = 'usage: bacnet_control <read-ao|write-ao> <device id> <property id> [<value>]'

def clean_rp_result(read_result):
	"""The read_result is something like (0, '100.000000\r\n'), so we slice out the number."""
	quote_index = read_result.find("'")
	slash_index = read_result.find("\\", start=quote_index)
	return read_result[quote_index + 1:slash_index]


class BacnetControl:
	def __init__(self, bin_dir_path, bacnet_port=47809):
		self.bin_dir_path = bin_dir_path
		self.bacnet_port = bacnet_port
	def run_command(self, args):
		os.environ['BACNET_IP_PORT'] = '%s' % self.bacnet_port
		proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=self.bin_dir_path)
		output = ''
		while True:
			next_line = proc.stdout.readline()
			if next_line == '' and proc.poll() != None: break
			output = '%s%s' % (output, next_line)
		proc.wait()
		return (proc.returncode, output)

	def get_bin_path(self, bin_name):
		bin_name = '%s%s' % (bin_name, settings.BACNET_EXECUTABLE_EXTENSION)
		bin_path = os.path.join(self.bin_dir_path, bin_name)
		if not os.path.exists(bin_path):
			raise IOError('Bacnet bin does not exist: %s' % bin_path)
		return bin_path

	def read_analog_output(self, device_id, property_id):
		"""Returns the Present-Value of an Analog Output property"""
		bin_path = self.get_bin_path('bacrp')
		# bacrp device-instance object-type object-instance property [index]
		# bacrp 100 1 23 1 85
		args = [bin_path, '%s' % int(device_id), '2', '%s' % int(property_id), '85']
		return self.run_command(args)

	def write_analog_output_int(self, device_id, property_id, value):
		"""Returns the Present-Value of an Analog Output property"""
		bin_path = self.get_bin_path('bacwp')
		# bacwp device-instance object-type object-instance property priority index tag value [tag value...]
		args = [bin_path, '%s' % int(device_id), '2', '%s' % int(property_id), '85', '16', '-1', '2', '%s' % int(value)]
		return self.run_command(args)

def main():
	try:
		action = sys.argv[1]
		device_id = sys.argv[2]
		property_id = sys.argv[3]
	except IndexError:
		print USAGE_MESSAGE
		return

	control = BacnetControl(settings.BACNET_BIN_DIR)
	if action == 'read-ao':
		print control.read_analog_output(device_id, property_id)
	elif action == 'write-ao':
		try:
			value = sys.argv[4]
		except IndexError:
			print USAGE_MESSAGE
			return
		control.write_analog_output_int(device_id, property_id, value)
	else:
		print USAGE_MESSAGE
		return

if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
