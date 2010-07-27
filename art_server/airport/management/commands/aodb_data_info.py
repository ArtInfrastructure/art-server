# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import time
import urllib
import traceback
from datetime import datetime, timedelta
from lxml import etree

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
	help = "Shows information about the AODB provided data files."
	args = "[start_date, end_date]"
	requires_model_validation = False

	def get_value(self, element, xPath, default=None):
		elements = element.xpath(xPath)
		if len(elements) == 0: return default
		return elements[0].text

	def handle(self, *labels, **options):
		from airport.models import FlightLeg
		from airport.tasks import FileMungerTask
		
		if not hasattr(settings, 'FILE_MUNGER_DIRECTORY'): raise CommandError('You must define FILE_MUNGER_DIRECTORY in your local_settings.py')
		if not os.path.isdir(settings.FILE_MUNGER_DIRECTORY): raise CommandError('The FILE_MUNGER_DIRECTORY does not exist: %s', settings.FILE_MUNGER_DIRECTORY)
		if len(labels) == 0:
			end_date = datetime.now()
			start_date = end_date - timedelta(days=1)
		elif len(labels) == 2:
			try:
				start_date = datetime(*(time.strptime(labels[0], FlightLeg.TIMESTAMP_FORMAT))[0:6])
				end_date = datetime(*(time.strptime(labels[1], FlightLeg.TIMESTAMP_FORMAT))[0:6])
			except:
				traceback.print_exc()
				example_start_date = (datetime.now() - timedelta(days=1)).isoformat().split('.')[0]
				example_end_date = datetime.now().isoformat().split('.')[0]
				raise CommandError('Could not parse those dates.  Enter them like so: %s %s' % (example_start_date, example_end_date))
		else:
			example_start_date = (datetime.now() - timedelta(days=1)).isoformat().split('.')[0]
			example_end_date = datetime.now().isoformat().split('.')[0]
			raise CommandError('Enter zero or two arguments, the start date and the end date like so: %s %s' % (example_start_date, example_end_date))

		files = FileMungerTask().files_to_munge()
		
		if len(files) == 0:
			print "No files were found in date range: %s %s" % (start_date, end_date)
		else:
			print "AODB File Time"
			print "\tCarrier Flight Scheduled-Time Estimated-Time Bag-Claim Bag-Status"
		for mdate, path in files:
			if mdate >= time.mktime(start_date.timetuple()) and mdate <= time.mktime(end_date.timetuple()):
				f = open(path)
				root = etree.fromstring(f.read())
				f.close()
				timestamp = datetime.fromtimestamp(mdate)
				print timestamp

				for flight_leg in root.xpath('//FlightLeg'): 
					carrier = self.get_value(flight_leg, './FlightID/Carrier', "-")
					flight_number = self.get_value(flight_leg, './FlightID/FlightNumber', "-")
					scheduled_date_time = self.get_value(flight_leg, './FlightID/ScheduledDateTime', '-')
					estimated = self.get_value(flight_leg, './Estimated', "-")
					bag_claim_name = self.get_value(flight_leg, './BagClaim/BagClaimName', "-")
					bag_claim_status = self.get_value(flight_leg, './BagClaim/BagClaimStatus', "-")
					print '\t%s %s %s %s %s %s' % (carrier, flight_number, scheduled_date_time, estimated, bag_claim_name, bag_claim_status)
					#print etree.tostring(flight_leg, pretty_print=True)
