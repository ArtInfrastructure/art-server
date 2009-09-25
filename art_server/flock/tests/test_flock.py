from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from flock.models import *

APP_PATH = '/status/'

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_status_listeners(self):
		self.failUnless(StatusListener.objects.all().count() == 0)

		response = self.client.post(APP_PATH, {'register':8088})
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless('flock/status.html' in [template.name for template in response.template])
		self.failUnless(StatusListener.objects.all().count() == 1)
		sl = StatusListener.objects.all()[0]
		self.failUnlessEqual(sl.host, '127.0.0.1:8088')
		self.failUnlessEqual(len(sl.tests.all()), 0)
		
		response = self.client.post(APP_PATH, {'unregister':8088})
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless('flock/status.html' in [template.name for template in response.template])
		self.failUnless(StatusListener.objects.all().count() == 0)

		response = self.client.post(APP_PATH, {'register':8088, 'tests':'test1,test2,test3'})
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless('flock/status.html' in [template.name for template in response.template])
		self.failUnless(StatusListener.objects.all().count() == 1)
		sl = StatusListener.objects.all()[0]
		self.failUnlessEqual(len(sl.tests.all()), 3)
		self.failUnless('test2' in [test.name for test in sl.tests.all()])

