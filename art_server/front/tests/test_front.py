from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from front.models import *

APP_PATH = '/'

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_ui(self):
		response = self.client.get(APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless('front/index.html' in [template.name for template in response.template])

	def test_status_listeners(self):
		self.failUnless(StatusListener.objects.all().count() == 0)

		response = self.client.post(APP_PATH + 'status/', {'register':8088})
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless('front/status.html' in [template.name for template in response.template])
		self.failUnless(StatusListener.objects.all().count() == 1)
		sl = StatusListener.objects.all()[0]
		self.failUnlessEqual(sl.host, '127.0.0.1:8088')
		
		response = self.client.post(APP_PATH + 'status/', {'unregister':8088})
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless('front/status.html' in [template.name for template in response.template])
		self.failUnless(StatusListener.objects.all().count() == 0)

		


