# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings

from piston.resource import Resource

from handlers import BACnetObjectHandler, BACnetReadingHandler
from models import *

bacnet_object_handler = Resource(handler=BACnetObjectHandler)
bacnet_reading_handler = Resource(handler=BACnetReadingHandler)

urlpatterns = patterns('',
#	(r'^group/(?P<id>[\d]+)$', 'front.views.artist_group_detail'),
	(r'^api/object/$', bacnet_object_handler, { 'emitter_format': 'xml' }), 
	(r'^api/object/(?P<id>[\d]+)/$', bacnet_object_handler, { 'emitter_format': 'xml' }), 
	(r'^api/object/(?P<object_id>[\d]+)/(?P<property_name>[^/]+)/$', bacnet_reading_handler, { 'emitter_format': 'xml' }), 
	(r'^$', 'bacnet.views.index'),
)
