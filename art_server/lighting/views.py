# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import sys
import datetime
import calendar
import traceback
import simplejson as json

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

from bacnet_control import BacnetControl
from creston_control import CrestonControl
from pjlink import PJLinkController, PJLinkProtocol
from api_views import ProjectorInfo, LampInfo

from models import *
from forms import *

@staff_member_required
def index(request):
	return render_to_response('lighting/index.html', { 'bacnet_lights':BACNetLight.objects.all(), 'projectors':Projector.objects.all() }, context_instance=RequestContext(request))

@staff_member_required
def creston(request):
	control = CrestonControl(settings.CRESTON_CONTROL_HOST)
	message = None
	control_info = None
	return_json = False
	try:
		if request.method == 'POST':
			command_form = CrestonCommandForm(request.POST)
			if request.POST.get('action', None): 
				action = request.POST.get('action')
				if action == 'high-up':
					control.raise_high()
				elif action == 'high-down':
					control.lower_high()
				elif action == 'low-up':
					control.raise_low()
				elif action == 'low-down':
					control.lower_low()
				else:
					print "Error: unknown action: %s" % action
					raise HttpResponseServeError('unknown action: %s' % action)
				return_json = True
			elif request.POST.get('command', None):
				if command_form.is_valid():
					command = command_form.cleaned_data['command']
					if command == 'Update':
						lines = 9
					else:
						lines = 1
					result = control.send_command(command, lines)
					return HttpResponse(str(result or "Error"), mimetype='text/plain')
				else:
					print 'is not valid', command_form
			else:
				print 'no POST', request.POST
		else:
			command_form = CrestonCommandForm()
			
		try:
			control_info = control.query_status()
			#control_info = {'High': '55000', 'Current': '63098', 'Wake': '5:00 AM', 'Low': '63098', 'Lamp1': '2-1468', 'Sleep': '1:00 AM', 'Lamp2': '2-1469'}
		except:
			message = 'Could not communicate with the controller.'
		if return_json: return HttpResponse(json.dumps(control_info), mimetype='application/json')
		return render_to_response('lighting/creston.html', {'command_form':command_form, 'control_info':control_info}, context_instance=RequestContext(request))
	except:
		traceback.print_exc()
		
@staff_member_required
def bacnet_light(request, id):
	light = get_object_or_404(BACNetLight, pk=id)
	control = BacnetControl(settings.BACNET_BIN_DIR)
	if request.method == 'POST':
		light_control_form = LightControlForm(request.POST)
		if light_control_form.is_valid():
			new_value = light_control_form.cleaned_data['light_value']
			try:
				control.write_analog_output_int(light.device_id, light.property_id, new_value)
			except:
				logging.exception('Could not write the posted value (%s) for bacnet device %s property %s' % (new_value, light.device_id, light.property_id))
				return HttpResponseServerError('Could not write the posted value (%s) for bacnet device %s property %s\n\n%s' % (new_value, light.device_id, light.property_id, sys.exc_info()[1]))
	try:
		light_value = control.read_analog_output(light.device_id, light.property_id)[1]
		light_control_form = LightControlForm(data={'light_value':light_value})
	except:
		logging.exception('Could not read the analog output for bacnet device %s property %s' % (light.device_id, light.property_id))
		light_value = None
		light_control_form = LightControlForm()
	return render_to_response('lighting/bacnet_light.html', {'light_value':light_value, 'light_control_form':light_control_form, 'light':light }, context_instance=RequestContext(request))

@staff_member_required
def projector(request, id):
	projector = get_object_or_404(Projector, pk=id)
	controller = PJLinkController(projector.pjlink_host, projector.pjlink_port, projector.pjlink_password)
	try:
		if request.method == 'POST':
			new_event_form = ProjectorEventForm(request.POST)
			if request.POST.get('power', None) == PJLinkProtocol.POWER_ON_STATUS:
				controller.power_on()
				new_event_form = ProjectorEventForm(initial={ 'device':projector.id })
			elif request.POST.get('power', None) == PJLinkProtocol.POWER_OFF_STATUS:
				controller.power_off()
				new_event_form = ProjectorEventForm(initial={ 'device':projector.id })
			elif request.POST.get('action', None) == 'delete' and request.POST.get('event_id', None):
				event = ProjectorEvent.objects.get(pk=int(request.POST.get('event_id', None)))
				event.delete()
				new_event_form = ProjectorEventForm(initial={ 'device':projector.id })
			elif new_event_form.is_valid():
				new_event_form.save()
				new_event_form = ProjectorEventForm(initial={ 'device':projector.id })
		else:
			new_event_form = ProjectorEventForm(initial={ 'device':projector.id })
			
		audio_mute, video_mute = controller.query_mute()
		info = ProjectorInfo(controller.query_power(), controller.query_name(), controller.query_manufacture_name(), controller.query_product_name(), controller.query_other_info(), audio_mute, video_mute)
		for lamp in controller.query_lamps(): info.lamps.append(LampInfo(lamp[0], lamp[1]))
	except:
		logging.exception('Could not communicate with the projector')
		info = None

	return render_to_response('lighting/projector.html', { 'events':ProjectorEvent.objects.filter(device=projector), 'new_event_form':new_event_form, 'projector':projector, 'projector_info':info }, context_instance=RequestContext(request))
