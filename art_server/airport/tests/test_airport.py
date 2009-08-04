from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from airport.models import *
from airport.airport_client import SnapshotList

from lxml import etree

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
		snapshot.xml_data = """<funky_snapshot>
				<sub_element>Hey</sub_element>
				<sub_element foo="bar">
					<sub_sub_element />
				</sub_element>
			</funky_snapshot>"""
		snapshot.save()
		self.failUnless(AirportSnapshot.objects.all().count() == 1)

		# check that we can read the snapshot
		response = self.client.get('%s%s/' % (APP_PATH, snapshot.id))
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnlessEqual(response.content, snapshot.xml_data)

		# check that we can fetch an element via XPath
		response = self.client.get('%s%s/?xpath=//sub_element[@foo=%%22bar%%22]' % (APP_PATH, snapshot.id))
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		element = etree.fromstring(response.content)
		self.failUnlessEqual(len(element), 1)
		self.failUnlessEqual(element[0].get('foo'), 'bar')

		# make certain that we get a list with one element
		response = self.client.get('%s' % APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 1)
		self.failUnless(snapshot_list[0][1].endswith(snapshot.get_absolute_url()))

		# create a snapshot via form
		response = self.client.post('%s' % APP_PATH, { 'xml_data': '<spunky><sub_element>Ahoi</sub_element></spunky>' })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(AirportSnapshot.objects.all().count() == 2)
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 2)

		# make certain that new lists have the form-created snapshot
		response = self.client.get('%s' % APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		snapshot_list = SnapshotList(response.content)
		self.failUnless(len(snapshot_list) == 2)

		# make certain that the latest url returns the latest snapshot
		response = self.client.get('%slatest.xml' % APP_PATH)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		element = etree.fromstring(response.content)
		self.failUnlessEqual(element.tag, 'spunky')
