import httplib, urllib
import traceback
import logging
import pprint
from stat import S_ISREG, ST_MTIME, ST_MODE
import os, sys, time

from lxml import etree
from scripts.scheduler import Task

class FileMungerTask(Task):
	"""The schedule task which updates the stored images for each of the artcams."""
	def __init__(self, loopdelay=30, initdelay=0):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		from django.contrib.sites.models import Site
		from models import AirportSnapshot
		site = Site.objects.get_current()
		files = self.files_to_munge()

		result_elements = {}
		for mdate, path in files:
			# if it's older than 24 hours ignore
			if mdate < int(time.time()) - 86400:
				print 'Too old: ', time.time(), mdate
				continue
			# if it's younger than 2 seconds it may not be complete, so ignore
			if mdate > int(time.time()) - 5:
				print 'Too young: ', time.time(), mdate
				continue
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
			logging.error('Created a snapshot with no flighlegs!')

		# start a new snapshot
		# for each file
		#  if file is older than 48 hours, delete
		#  if file is younger than 10 seconds, ignore
		#  else
		#    snip out the FlightLeg, add a timestamp attribute, add to snapshot
		# if snapshot has one or more flightlegs add snapshot to db
		# else email the art technician

	def files_to_munge(self):
		"""Returns an array of info about files in the form (creation_date, path), sorted in chronological order by modified date"""
		from settings import FILE_MUNGER_DIRECTORY
		entries = (os.path.join(FILE_MUNGER_DIRECTORY, fn) for fn in os.listdir(FILE_MUNGER_DIRECTORY))
		entries = ((os.stat(path), path) for path in entries)

		# leave only regular files, insert creation date
		return sorted(((stat[ST_MTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE])))
		
