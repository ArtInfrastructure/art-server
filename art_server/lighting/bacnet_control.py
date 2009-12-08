#!/usr/bin/python

"""These functions wrap the bacnet command line apps from http://bacnet.sourceforge.net/
In your django settings you'll need a BACNET_BIN_DIR with the full path to the directory containing the compiled apps.
Like so (no slash on the end, please):
BACNET_BIN_DIR = '/usr/local/src/bacnet-stack-0.5.3/bin'
"""

import os, sys, subprocess
import settings

USAGE_MESSAGE = 'usage: bacnet_control <read-ao|write-ao> <device id> <property id> [<value>]'

def read_analog_output(device_id, property_id):
	"""Returns the Present-Value of an Analog Output property"""
	# bacrp device-instance object-type object-instance property [index]
	args = ['%s/bacrp' % settings.BACNET_BIN_DIR, '%s' % int(device_id), '1', '%s' % int(property_id), '85']
	print 'Reading with args: %s' % args
	retval = subprocess.call(args)
	print retval
	return 0

def write_analog_output_int(device_id, property_id, value):
	"""Returns the Present-Value of an Analog Output property"""
	# bacwp device-instance object-type object-instance property priority index tag value [tag value...]
	args = ['%s/bacwp' % settings.BACNET_BIN_DIR, '%s' % int(device_id), '1', '%s' % int(property_id), '85', '16', '-1', '2', '%s' % int(value)]
	print 'Writing with args: %s' % args
	retval = subprocess.call(args)
	print retval
	return 0

def main():
	try:
		action = sys.argv[1]
		device_id = sys.argv[2]
		property_id = sys.argv[3]
	except IndexError:
		print USAGE_MESSAGE
		return

	if action == 'read-ao':
		print read_analog_output(device_id, property_id)
	elif action == 'write-ao':
		try:
			value = sys.argv[4]
		except IndexError:
			print USAGE_MESSAGE
			return
		write_analog_output_int(device_id, property_id, value)
	else:
		print USAGE_MESSAGE
		return

if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
