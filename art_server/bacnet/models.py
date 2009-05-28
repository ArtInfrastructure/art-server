# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import os.path
import Image
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
from django.core.files import File
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.utils.encoding import force_unicode
from django.db.models import Q
from django.db.models.fields.files import ImageFieldFile
from django.core.urlresolvers import reverse

class BacnetProperty(models.Model):
	name = models.CharField(max_length=1024, null=True, blank=True)
	type_name = models.CharField(max_length=1024, null=True, blank=True)
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		return ('bacnet.views.bacnet_property', (), { 'id':self.id })
	class Meta:
		ordering = ['name']
	
class BacnetPropertyReading(models.Model):
	bacnet_property = models.ForeignKey(BacnetProperty, blank=False, null=False)
	reading = models.CharField(max_length=1024, blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		return ('bacnet.views.property_reading', (), { 'id':self.id })
	class Meta:
		ordering = ['-created']

class BacnetObject(models.Model):
	name = models.CharField(max_length=1024, null=False, blank=False)
	address = models.CharField(max_length=1024, null=False, blank=False)
	type_name = models.CharField(max_length=1024, null=False, blank=False)
	bacnet_properties = models.ManyToManyField(BacnetProperty, blank=True, null=True)
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		return ('bacnet.views.object_detail', (), { 'id':self.id })
	class Meta:
		ordering = ['name']
