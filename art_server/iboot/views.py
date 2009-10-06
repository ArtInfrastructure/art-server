# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback

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
from iboot_control import IBootControl

@staff_member_required
def index(request):
	return render_to_response('iboot/index.html', { 'iboots':IBootDevice.objects.all() }, context_instance=RequestContext(request))

@staff_member_required
def iboot(request, id):
	iboot = get_object_or_404(IBootDevice, pk=id)
	control = IBootControl(settings.IBOOT_POWER_PASSWORD, iboot.ip)
	if request.method == 'POST':
		if request.POST.get('action', None) == 'toggle': control.toggle()
	status = control.query_iboot_state()
	return render_to_response('iboot/iboot.html', { 'iboot':iboot, 'status':status }, context_instance=RequestContext(request))
