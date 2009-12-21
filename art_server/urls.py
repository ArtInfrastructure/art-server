# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
	(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	(r'^api/artcam/$', 'artcam.api_views.artcams'),
	(r'^api/artcam/(?P<id>[\d]+)/$', 'artcam.api_views.artcam'),
	(r'^api/artcam/(?P<artcam_id>[\d]+)/photo/$', 'artcam.api_views.photos'),
	(r'^api/artcam/(?P<artcam_id>[\d]+)/photo/(?P<photo_id>[\d]+)/$', 'artcam.api_views.photo'),
	(r'^api/artcam/(?P<artcam_id>[\d]+)/photo/latest/$', 'artcam.api_views.latest_photo'),

	(r'^api/bnlight/$', 'lighting.api_views.bacnet_lights'),
	(r'^api/bnlight/(?P<id>[\d]+)/$', 'lighting.api_views.bacnet_light'),
	(r'^api/bnlight/(?P<id>[\d]+)/value/$', 'lighting.api_views.bacnet_light_value'),
	(r'^api/projector/$', 'lighting.api_views.projectors'),
	(r'^api/projector/(?P<id>[\d]+)/$', 'lighting.api_views.projector'),
	(r'^api/projector/(?P<id>[\d]+)/info/$', 'lighting.api_views.projector_info'),

	(r'^api/aodb/$', 'airport.views.snapshot_list'),
	(r'^api/aodb/latest\.xml$', 'airport.views.latest_snapshot'),
	(r'^api/aodb/(?P<id>[\d]+)/$', 'airport.views.snapshot'),
	(r'^airport/', include('airport.urls')),

	(r'^status/', include('flock.urls')),
	(r'^incus/', include('incus.urls')),
	(r'^iboot/', include('iboot.urls')),
	(r'^artcam/', include('artcam.urls')),
	(r'^lighting/', include('lighting.urls')),
	(r'^', include('front.urls')),
)
