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

class BACNetLight(models.Model):
	"""A lighting fixture which is controlled using the BACNet protocols.
	In BACNet speak: we're reading and writing Present-Value on Analog Outputs which range in value from 0 to 100."""
	name = models.CharField(max_length=1024, null=False, blank=False)
	device_id = models.PositiveIntegerField(null=False, blank=False, default=0)
	property_id = models.PositiveIntegerField(null=False, blank=False, default=0)
	@models.permalink
	def get_absolute_url(self): return ('lighting.views.bacnet_light', (), { 'id':self.id })
	def __unicode__(self): return '%s' % self.name
	class Meta:
		ordering = ['name']
		verbose_name = "BACNet Light"
		verbose_name_plural = "BACNet Lights"
	class HydrationMeta:
		attributes = ['id', 'name', 'device_id', 'property_id']

class Projector(models.Model):
	"""A light projection system which is controlled via the net."""
	name = models.CharField(max_length=1024, null=False, blank=False)
	@models.permalink
	def get_absolute_url(self): return ('lighting.views.projector', (), { 'id':self.id })
	def __unicode__(self): return '%s' % self.name
	class Meta:
		ordering = ['name']
	class HydrationMeta:
		attributes = ['id', 'name']
