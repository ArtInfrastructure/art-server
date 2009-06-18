import httplib, urllib

class StatusSender:
	def send_status(self, status, host):
		params = urllib.urlencode({'status':status})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = httplib.HTTPConnection(host)
		conn.request("POST", "/status/", params, headers)
		response = conn.getresponse()
		print response.status, response.reason, response.read()
		conn.close()

def main():
	sender = StatusSender()
	sender.send_status('normal', '127.0.0.1:8088')

if __name__ == '__main__':
	main()
