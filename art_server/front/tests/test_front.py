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
