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

import art_server.front.templatetags.imagetags as imagetags

class Artcam(models.Model):
	name = models.CharField(max_length=1024, null=True, blank=True)
	ip = models.IPAddressField(blank=False, null=True)
	def update_photo(self):
		url = 'http://%s:%s@%s/axis-cgi/jpg/image.cgi' % (settings.ARTCAM_PUBLIC_USERNAME, settings.ARTCAM_PUBLIC_PASSWORD, self.ip)
		filename, headers = urllib.urlretrieve(url)
		photo = ArtcamPhoto(artcam=self)
		image_file = file(filename, 'r')
		photo.image.save(filename + '.jpg', File(image_file), save=False)
		photo.save()
		
	def latest_photo(self):
		if ArtcamPhoto.objects.filter(artcam=self).count() > 0:
			return ArtcamPhoto.objects.filter(artcam=self)[0]
		return None
	def __unicode__(self):
		return self.name
	def get_update_url(self):
		return '%s?action=update' % reverse('artcam.views.artcam', kwargs={ 'id':self.id })
	@models.permalink
	def get_absolute_url(self):
		return ('artcam.views.artcam', (), { 'id':self.id })
	class Meta:
		ordering = ['name']
	

class ThumbnailedModel(models.Model):
	"""An abstract base class for models with an ImageField named "image" """
	def thumb(self):
		if not self.image: return ""
		try:
			file = settings.MEDIA_URL + self.image.path[len(settings.MEDIA_ROOT):]
			filename, miniature_filename, miniature_dir, miniature_url = imagetags.determine_resized_image_paths(file, "admin_thumb")
			if not os.path.exists(miniature_dir): os.makedirs(miniature_dir)
			if not os.path.exists(miniature_filename): imagetags.fit_crop(filename, 100, 100, miniature_filename)
			return """<img src="%s" /></a>""" % miniature_url
		except:
			traceback.print_exc()
			return None
	thumb.allow_tags = True
	class Meta:
		abstract = True

class ArtcamPhoto(ThumbnailedModel):
	image = models.ImageField(upload_to='artcam_photo', blank=False)
	artcam = models.ForeignKey(Artcam, blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True)
	def display_name(self): return os.path.basename(self.image.name)
	def __unicode__(self): return '%s' % self.display_name()
	@models.permalink
	def get_absolute_url(self):
		return ('artcam.views.artcam_photo', (), { 'artcam_id':self.artcam.id, 'photo_id':self.id })
	class Meta:
		ordering = ['-created']
	class HydrationMeta:
		attributes = ['id', 'created']
		nodes = ['image']
	def __unicode__(self):
		return str(self.image)
