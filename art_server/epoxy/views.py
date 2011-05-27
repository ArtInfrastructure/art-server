import traceback
import httplib2

from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from models import ProxyDestination

def go(request, id):
	"""Proxy incoming API calls to the appropriate ProxyDestination or 404 if it doesn't exist."""
	destination = get_object_or_404(ProxyDestination, pk=id)

	if not destination.is_valid_remote_address(request.META.get('HTTP_X_EPOXY_REMOTE', None)):
		return HttpResponseForbidden('The requesting IP# is not permitted to call this API')

	remote_path = request.path[len(reverse('epoxy.views.go', kwargs={'id':id})):]
	if request.method == 'GET':
		url = '%s%s?%s' % (destination.url, remote_path, request.GET.urlencode())
		response, content = httplib2.Http().request(url, request.method)
	elif request.method == 'POST':
		url = '%s%s' % (destination.url, remote_path)
		response, content = httplib2.Http().request(url, request.method, request.POST.urlencode())
	return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])

# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
