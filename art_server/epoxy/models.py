import os
import traceback
import logging
from IPy import IP

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

class ProxyDestination(models.Model):
	"""A remote HTTPd which will determine how to proxy incoming requests to epoxy.views.go()"""
	url = models.CharField(max_length=1000, null=False, blank=False, help_text='The full URL to the HTTPd which will handle the proxied API call')
	ips = models.CharField(max_length=1000, null=True, blank=True, help_text='The space separated IP#s or masks (e.g. "127.0.0.1/8 10.0.2.2") which are allowed to make this API call.')

	def is_valid_remote_address(self, remote_address):
		if not self.ips: return True
		if not remote_address: return False
		for ip in self.ips.split(' '):
			if remote_address in IP(ip): return True
		return False

	def clean(self):
		if self.ips:
			try:
				for ip in self.ips.split(' '): IP(ip)
			except:
				traceback.print_exc()
				raise ValidationError('Not a valid IP entry: "%s"' % self.ips)

	def save(self, *args, **kwargs):
		self.clean()
		super(ProxyDestination, self).save(*args, **kwargs)

	
	def __unicode__(self): return self.url

	class Meta:
		ordering = ['id']

# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
