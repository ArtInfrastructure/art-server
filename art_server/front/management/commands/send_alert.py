# Copyright 2010 Office Nomads LLC (http://officenomads.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import time
import urllib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
	help = "Sends an alert to the art technician via the art instance's alert API"
	args = "[subject, message]"
	requires_model_validation = False

	def handle(self, *labels, **options):
		if not hasattr(settings, 'ALERT_SECRET'): raise CommandError('You must define ALERT_SECRET in your settings.py')
		if not hasattr(settings, 'ALERT_API_URL'): raise CommandError('You must define ALERT_API_URL in your settings.py')
		if not labels or len(labels) != 2: raise CommandError('Enter two arguments, a subject and a message.')
		subject = labels[0]
		message = labels[1]
		print urllib.urlopen(settings.ALERT_API_URL, urllib.urlencode({'secret':settings.ALERT_SECRET, 'subject':subject, 'message':message})).read()