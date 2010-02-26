# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback
import logging
import urllib

from django.conf import settings
from django.db.models import Q
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.utils.html import strip_tags
import django.contrib.contenttypes.models as content_type_models
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import feedgenerator

from models import *
from art_server.hydration import dehydrate_to_list_xml, dehydrate_to_xml
from pjlink import PJLinkController, PJLinkProtocol

def bacnet_lights(request):
	return HttpResponse(dehydrate_to_list_xml(BACNetLight.objects.all()), content_type="text/xml")

def bacnet_light(request, id):
	light = get_object_or_404(BACNetLight, pk=id)
	return HttpResponse(dehydrate_to_xml(light), content_type="text/xml")

def bacnet_light_value(request, id):
	light = get_object_or_404(BACNetLight, pk=id)
	api_url = '%sdevice/%s/%s/' % (settings.BACNET_PROXY_URL, light.device_id, light.property_id)
	if request.method == 'POST' and request.POST.get('value', None):
		try:
			new_value = request.POST.get('value', None)
			result = urllib.urlopen(api_url, urllib.urlencode({'value':new_value})).read()
		except:
			logging.exception('Could not read the posted value for bacnet light %s' % request.POST.get('value', None))
	try:
		value = urllib.urlopen(api_url).read()
	except:
		logging.exception('Could not read the analog output for bacnet light %s' % light)
		value = -1
	return HttpResponse(value, content_type="text/plain")

def projectors(request):
	return HttpResponse(dehydrate_to_list_xml(Projector.objects.all()), content_type="text/xml")

def projector(request, id):
	projector = get_object_or_404(Projector, pk=id)
	return HttpResponse(dehydrate_to_xml(projector), content_type="text/xml")

class LampInfo:
	"""Wraps the projector's lamp info for dehydration"""
	def __init__(self, lighting_hours, is_on):
		self.lighting_hours = lighting_hours
		self.is_on = is_on
	class HydrationMeta:
		attributes = ['lighting_hours', 'is_on']


class ProjectorInfo:
	"""Used to wrap the projector information for dehydration"""
	def __init__(self, power_state, projector_name, manufacture_name, product_name, other_info):
		self.power_state = power_state
		self.projector_name = projector_name
		self.manufacture_name = manufacture_name
		self.product_name = product_name
		self.other_info = other_info
		self.lamps = []
	class HydrationMeta:
		attributes = ['power_state', 'projector_name', 'manufacture_name', 'product_name', 'other_info']
		nodes = ['lamps']

def projector_info(request, id):
	projector = get_object_or_404(Projector, pk=id)
	controller = PJLinkController(projector.pjlink_host, projector.pjlink_port, projector.pjlink_password)

	if request.method == 'POST':
		if request.POST.get('power', None) == PJLinkProtocol.POWER_ON_STATUS:
			controller.power_on()
		elif request.POST.get('power', None) == PJLinkProtocol.POWER_OFF_STATUS:
			controller.power_off()

	info = ProjectorInfo(controller.query_power(), controller.query_name(), controller.query_manufacture_name(), controller.query_product_name(), controller.query_other_info())
	for lamp in controller.query_lamps():
		info.lamps.append(LampInfo(lamp[0], lamp[1]))
	return HttpResponse(dehydrate_to_xml(info), content_type="text/xml")
