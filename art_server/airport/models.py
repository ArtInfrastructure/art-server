# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import os.path
import Image
import httplib
import urllib
import datetime, calendar
import random
import time
import re
import feedparser
import unicodedata
import traceback
import logging
import pprint

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.utils.encoding import force_unicode
from django.db.models import Q

from lxml import etree

class AirportSnapshotManager(models.Manager):
	def latest(self):
		snaps = self.all()[:1]
		if len(snaps) == 1: return snaps[0]
		return None

class FlightLeg:
	TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'

	def __init__(self, fl_element):
		self.fl_element = fl_element
		self.update_time = self.get_attribute('.', 'update-time')
		self.stopover_index = self.get_attribute('Stopover', 'elementIndex')
		self.carrier = self.get_value('./FlightID/Carrier')
		self.flight_number = self.get_value('./FlightID/FlightNumber')
		self.scheduled_date_time = self.get_value('./FlightID/ScheduledDateTime')
		self.estimated = self.get_value('./Estimated')
		self.in_outbound = self.get_value('./FlightID/InOutbound')
		self.origin_destination_airport_code = self.get_value('./FlightID/OriginDestinationAirportCode')
		self.ac_type_code = self.get_value('./ACTypeCode')
		self.public_gate = self.get_value('./PublicGate')
		self.stand = self.get_value('./Stand')
		self.estimated = self.get_value('./Estimated')
		self.public_comment = self.get_value('./PublicComment')
		self.flight_status = self.get_value('./FlightStatus')
		self.gate_name = self.get_value('./GateInfo/GateName')
		self.sched_begin = self.get_value('./GateInfo/SchedBegin')
		self.sched_end = self.get_value('./GateInfo/SchedEnd')
		self.actual_begin = self.get_value('./GateInfo/ActualBegin')
		self.actual_end = self.get_value('./GateInfo/ActualEnd')
		self.bag_claim_name = self.get_value('./BagClaim/BagClaimName')
		self.bag_claim_status = self.get_value('./BagClaim/BagClaimStatus')
	
	@property
	def upcoming(self):
		if self.sched_end == None: return False
		return datetime.datetime(*(time.strptime(self.sched_end, self.TIMESTAMP_FORMAT)[0:6])) > datetime.datetime.now()

	def get_attribute(self, xPath, attribute_name, default=None):
		elements = self.fl_element.xpath(xPath)
		if len(elements) == 0: return default
		return elements[0].attrib.get(attribute_name)
	
	def get_value(self, xPath, default=None):
		elements = self.fl_element.xpath(xPath)
		if len(elements) == 0: return default
		return elements[0].text

	def __repr__(self): return "FlightLeg: %s %s" % (self.carrier, self.flight_number)

class AirportSnapshot(models.Model):
	"""An XML formatted snapshot of data from the airport."""
	xml_data = models.TextField(null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True)

	objects = AirportSnapshotManager()

	@property
	def flight_legs(self):
		root = etree.fromstring(self.xml_data)
		return sorted([FlightLeg(fl_element) for fl_element in root.xpath('//FlightLeg')], key=lambda fl: fl.scheduled_date_time)
				
	def __unicode__(self): return 'Snapshot %s' % self.created
	@models.permalink
	def get_absolute_url(self):
		return ('airport.views.snapshot', (), { 'id':self.id })
	class Meta:
		ordering = ['-created']
