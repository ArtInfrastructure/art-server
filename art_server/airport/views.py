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
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

from lxml import etree

from art_server.hydration import dehydrate_to_list_xml
from models import *
from forms import *

class Snapshot:
	"""A simple wrapper which is dehydrated in the snapshot list view below"""
	def __init__(self, snapshot):
		self.timestamp = snapshot.created
		self.url = 'http://%s%s' % (Site.objects.get_current().domain, snapshot.get_absolute_url())
	class HydrationMeta:
		attributes = ['timestamp', 'url']

def explorer(request):
	return render_to_response('airport/explorer.html', { }, context_instance=RequestContext(request))

def snapshot_list(request):
	"""A list of all available snapshots"""
	if request.method == "POST":
		snapshot_form = AirportSnapshotForm(request.POST)
		if snapshot_form.is_valid():
			snapshot = snapshot_form.save()
	working_list = [Snapshot(snapshot) for snapshot in AirportSnapshot.objects.all()]
	return HttpResponse(dehydrate_to_list_xml(working_list, list_name='snapshotlist'))

def latest_snapshot(request):
	snap = AirportSnapshot.objects.latest()
	if snap == None: raise Http404
	return snapshot(request, snap.id)
	
def snapshot(request, id):
	"""The XML data from an individual snapshot"""
	snapshot = get_object_or_404(AirportSnapshot, pk=id)
	xpath = request.GET.get('xpath', None)

	if xpath == None:
		return HttpResponse(snapshot.xml_data, content_type="text/xml")

	element = etree.fromstring(snapshot.xml_data)
	result_elements = element.xpath(xpath)
	root = etree.Element('snapshot')
	for result_element in result_elements:
		root.append(result_element)
	return HttpResponse(etree.tostring(root, pretty_print=True), content_type="text/xml")


