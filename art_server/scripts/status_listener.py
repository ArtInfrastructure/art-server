"""
	This script runs a server which listens for status messages from the art server.
	To connect it to your system, edit the handle_status function.
	To run external scripts for each status level, uncomment the lines including "os.system(...)"
	and replace the dummy path with the path to your scripts.
	
	To run this script you must have Python 2.4 or later.
	From the command line: python status_listener.py
	Press crtl-c to abort the script.
"""
import string
import cgi
import os
import time
import logging
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib

# The IP and port of the art server in the form 'host:port'.
ART_SERVER_HOST = '127.0.0.1:8000'

# The port on which the status listener will sit
# Change this if you receive a error like 'Address already in use'
WEB_PORT = 8090

def handle_status(status):
	"""Put your status handling implementation here.
	The possible values for the status parameter are: normal, emergency
	"""
	if status == 'normal':
		print 'Status is normal'
		# os.system('/full/path/to/script/reactToNormalStatus.sh')
	elif status == 'emergency':
		print 'Status is emergency'
		# os.system('/full/path/to/script/reactToEmergencyStatus.sh')
	else:
		print 'Unknown status'

STATUS_PARAMETER_NAME = 'status'

class StatusWebHandler(BaseHTTPRequestHandler):
	"""The http handler which reads the status parameter and hands it to the handle_status function."""
	def do_GET(self):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('This is an art cloud status handler.')
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			length = int(self.headers.getheader('content-length'))
			if ctype == 'application/x-www-form-urlencoded':
				try:
					qs = self.rfile.read(length)
					body = cgi.parse_qs(qs, keep_blank_values=1)
					handle_status(body[STATUS_PARAMETER_NAME][0])
				except (KeyError, IndexError):
					logging.exception('Received a POST with no status parameter: %s' % ctype)
			else:
				logging.error('Received a POST of unexpected type: %s' % ctype)
			self.send_response(200)
			self.end_headers()
			self.wfile.write("<HTML>POST OK.<BR><BR>");
		except:
			logging.exception("Error in POST")
			pass

def register_listener():
	try:
		params = urllib.urlencode({ 'register':WEB_PORT })
		f = urllib.urlopen("http://%s/status/" % ART_SERVER_HOST, params)
		f.read()
		return True
	except:
		return False

def unregister_listener():
	try:
		params = urllib.urlencode({ 'unregister':WEB_PORT })
		f = urllib.urlopen("http://%s/status/" % ART_SERVER_HOST, params)
		f.read()
		return True
	except:
		return False

def main():
	try:
		server = HTTPServer(('', WEB_PORT), StatusWebHandler)
		if not register_listener():
			print 'Could not register with %s' % ART_SERVER_HOST
			return
		print 'started status listener...'
		server.serve_forever()
	except KeyboardInterrupt:
		print ' Shutting down status listener'
		if not unregister_listener(): print 'Could not unregister with %s' % ART_SERVER_HOST
		server.socket.close()

if __name__ == '__main__':
	main()
