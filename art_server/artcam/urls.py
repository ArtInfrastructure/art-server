# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings

from models import *

class TestObj:
	def __init__(self):
		self.foo = 'bar'
		self.bar = 'baz'
	class HydrationMeta:
		attributes = ('foo', 'bar')

urlpatterns = patterns('',
	(r'^api/test/$', 'ground.views.podo', { 'podo':TestObj }),
	(r'^(?P<id>[\d]+)/$', 'artcam.views.artcam'),
	(r'^(?P<artcam_id>[\d]+)/photo/(?P<photo_id>[\d]+)/$', 'artcam.views.artcam_photo'),
	(r'^(?P<id>[\d]+)/video/$', 'artcam.views.artcam_video'),
	(r'^$', 'artcam.views.index'),
)
