# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import httplib, urllib
import traceback
import logging
import pprint
from stat import S_ISREG, ST_MTIME, ST_MODE
import os, sys, time
import datetime

from lxml import etree
from scripts.scheduler import Task
from settings import FILE_MUNGER_DIRECTORY

class FileMungerTask(Task):
	"""The schedule task which updates the airport snapshot data from a known directory of AODB data files.
	THIS WILL DELETE FILES MORE THAN TWO DAYS OLD AND SNAPSHOTS MORE THAN 5 DAYS OLD"""
	def __init__(self, loopdelay=120, initdelay=0):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		from django.contrib.sites.models import Site
		from models import AirportSnapshot
		site = Site.objects.get_current()
		files = self.files_to_munge()
		
		result_elements = {}
		for mdate, path in files:
			# if it's older than 26 hours (in seconds) ignore
			if mdate < int(time.time()) - 100800:
				#print 'Too old: ', time.time(), mdate
				# if it's older than two days, delete it
				if mdate < int(time.time()) - 172800: os.unlink(path)
				continue
			
			# if it's younger than a few seconds it may not be complete, so ignore
			if mdate > int(time.time()) - 5: continue
			
			data_file = open(path)
			element = etree.fromstring(data_file.read())
			flightleg_elements = element.xpath('//FlightLeg')
			for flightleg_element in flightleg_elements:
				flightleg_element.set('update-time', time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(mdate)))
				carrier = flightleg_element.xpath('//Carrier')[0].text
				flight_number = flightleg_element.xpath('//FlightNumber')[0].text
				result_elements[(carrier, flight_number)] = flightleg_element
		
		root = etree.Element('snapshot')
		for key in result_elements: root.append(result_elements[key])
		if len(root.xpath('//FlightLeg')) > 0:
			snapshot = AirportSnapshot.objects.create(xml_data=etree.tostring(root, pretty_print=True))
		else:
			logging.error('Munged a snapshot with no flighlegs!')

      	# Delete snapshots which are five or more days old
		expiration_datetime = datetime.datetime.now() - datetime.timedelta(days=5)
		old_snapshots = AirportSnapshot.objects.filter(created__lt=expiration_datetime)
		for snapshot in old_snapshots: snapshot.delete()
	
	def files_to_munge(self):
		"""Returns an array of info about files in the form (creation_date, path), sorted in chronological order by modified date"""
		entries = (os.path.join(FILE_MUNGER_DIRECTORY, fn) for fn in os.listdir(FILE_MUNGER_DIRECTORY))
		entries = ((os.stat(path), path) for path in entries)
		
		# leave only regular files, insert creation date
		return sorted(((stat[ST_MTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE])))
		
