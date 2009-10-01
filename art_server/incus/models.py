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

class ABDevice(models.Model):
	"""Represents an AudioBox device."""
	name = models.CharField(max_length=1024, null=False, blank=False)
	ip = models.IPAddressField(blank=False, null=False)
	port = models.IntegerField(blank=False, null=False, default=55128)
	def channel_groups(self):
		return ABChannelGroup.objects.filter(audio_channels__audioBoxDevice=self).distinct()
	class Meta:
		verbose_name = 'AudioBox device'
		verbose_name_plural = 'AudioBox devices'
	def __unicode__(self): return self.name
	@models.permalink
	def get_absolute_url(self): return ('incus.views.device', (), { 'id':self.id })

class ABChannelGroup(models.Model):
	"""A set of channels whose gain can be controlled as a group, each with relative gain changes."""
	name = models.CharField(max_length=1024, null=False, blank=False)
	master_gain = models.FloatField(null=False, default=0)
	class Meta:
		verbose_name = 'channel group'
		verbose_name_plural = 'channel groups'
	def __unicode__(self): return self.name
	@models.permalink
	def get_absolute_url(self): return ('incus.views.channel_group', (), { 'id':self.id })

class ABChannel(models.Model):
	"""An audio channel on the AudioBox device."""
	audioBoxDevice = models.ForeignKey(ABDevice, blank=False, null=False)
	number = models.IntegerField(blank=False, null=False)
	channel_group = models.ForeignKey(ABChannelGroup, blank=True, null=True, related_name="channels")
	gain = models.FloatField(null=False, default=0)
	class Meta:
		verbose_name = 'channel'
		verbose_name_plural = 'channels'
		ordering = ['number']
	def __unicode__(self): return '%s - channel %s' % (self.audioBoxDevice.__unicode__(), self.number)
