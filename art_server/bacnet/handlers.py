import re

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from models import *

MAX_LIST_LENGTH = 100

class BACnetObjectHandler(BaseHandler):
	methods_allowed = ('GET',)
	model = BACnetObject
	def read(self, request, id=None):
		if id: return BACnetObject.objects.get(id=id)
		return BACnetObject.objects.all()[:MAX_LIST_LENGTH]

class BACnetReadingHandler(BaseHandler):
	methods_allowed = ('GET',)
	def read(self, request, object_id, property_name):
		return BACnetPropertyReading.objects.filter(bacnet_property__bacnet_object__id=object_id, bacnet_property__name=property_name)[:MAX_LIST_LENGTH]


