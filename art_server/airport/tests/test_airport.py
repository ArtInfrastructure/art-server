from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from airport.models import *
from airport.airport_client import SnapshotList

APP_PATH = '/api/aodb/'

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_snapshot_api(self):
		self.failUnless(AirportSnapshot.objects.all().count() == 0)

		# make certain that we can get an empty list
		response = self.client.get('%s' % APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 0)

		# manually create a snapshot
		snapshot = AirportSnapshot()
		snapshot.xml_data = '<funky_snapshot><sub_element>Hey</sub_element></funkysnapshot>'
		snapshot.save()
		self.failUnless(AirportSnapshot.objects.all().count() == 1)

		# check that we can read the snapshot
		response = self.client.get('%s%s/' % (APP_PATH, snapshot.id))
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnlessEqual(response.content, snapshot.xml_data)

		# make certain that we get a list with one element
		response = self.client.get('%s' % APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 1)
		self.failUnless(snapshot_list[0][1].endswith(snapshot.get_absolute_url()))

		# create a snapshot via form
		response = self.client.post('%s' % APP_PATH, { 'xml_data': '<funky_snapshot><sub_element>Ahoi</sub_element></funkysnapshot>' })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(AirportSnapshot.objects.all().count() == 2)
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 2)

		# make certain that new lists have the form created snapshot
		response = self.client.get('%s' % APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 2)
