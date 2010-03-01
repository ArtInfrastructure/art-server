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
from forms import *

@staff_member_required
def status_listener(request, host):
	message = None
	try:
		status_listener = get_object_or_404(StatusListener, host=host)
		
		if request.method == 'POST' and request.POST.get('test_name', None):
			test_name = request.POST.get('test_name')
			try:
				status_listener.send_status(test_name)
				message = 'Triggered the test: %s' % test_name
			except:
				message = 'Could not trigger that test, probably because the status listener was not listening'
		return render_to_response('flock/status_listener.html', {'page_message': message, 'status_listener':status_listener}, context_instance=RequestContext(request))
	except:
		logging.exception('Error in status listener')
		raise

def index(request):
	page_message = None
	try:
		if request.method == 'POST' and request.POST.get('register', None):
			host = '%s:%s' % (request.META.get('REMOTE_ADDR', '127.0.0.1'), int(request.POST['register']))
			sl, created = StatusListener.objects.get_or_create(host=host)
			for test in sl.tests.all(): test.delete()
			if request.POST.get('tests', None):
				test_names = request.POST.get('tests').split(',')
				for test_name in test_names:
					sl_test = StatusListenerTest(name=test_name)
					sl_test.save()
					sl.tests.add(sl_test)
		elif request.method == 'POST' and request.POST.get('unregister', None):
			host = '%s:%s' % (request.META.get('REMOTE_ADDR', '127.0.0.1'), int(request.POST['unregister']))
			try:
				sl = StatusListener.objects.get(host=host)
				for test in sl.tests.all(): test.delete()
				sl.delete()
			except StatusListener.DoesNotExist:
				logging.debug('Tried to unregister an unknown host: %s' % host)
				
		return render_to_response('flock/status.html', { 'page_message':page_message, 'status_listeners':StatusListener.objects.all() }, context_instance=RequestContext(request))
	except:
		logging.exception('Could not set the status')
		raise


