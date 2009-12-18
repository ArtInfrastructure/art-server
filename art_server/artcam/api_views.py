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
from art_server.hydration import dehydrate_to_list_xml, dehydrate_to_xml

IMAGE_COMMENT = '<!-- tack the image name onto http://%s/media/ to get the full URL -->' % Site.objects.get_current().domain

def artcams(request):
	return HttpResponse(dehydrate_to_list_xml(Artcam.objects.all()), content_type="text/xml")

def artcam(request, id):
	artcam = get_object_or_404(Artcam, pk=id)
	return HttpResponse(dehydrate_to_xml(artcam), content_type="text/xml")

def photos(request, artcam_id):
	artcam = get_object_or_404(Artcam, pk=artcam_id)
	return HttpResponse(dehydrate_to_list_xml(ArtcamPhoto.objects.filter(artcam__id=artcam_id)) + IMAGE_COMMENT, content_type="text/xml")

def photo(request, artcam_id, photo_id):
	photo = get_object_or_404(ArtcamPhoto, pk=photo_id)
	if photo.artcam.id != int(artcam_id): raise Http404
	return HttpResponse(dehydrate_to_xml(photo) + IMAGE_COMMENT, content_type="text/xml")

def latest_photo(request, artcam_id):
	photos = ArtcamPhoto.objects.filter(artcam__id=artcam_id)
	if len(photos) == 0: raise Http404
	return HttpResponse(dehydrate_to_xml(photos[0]) + IMAGE_COMMENT, content_type="text/xml")
