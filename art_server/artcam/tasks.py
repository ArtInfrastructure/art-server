from scripts.scheduler import Task
import httplib, urllib
import traceback
import logging
import pprint
import sys

class ArtcamTask(Task):
	"""The schedule task which updates the stored images for each of the artcams."""
	def __init__(self, loopdelay=300, initdelay=1):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		from django.contrib.sites.models import Site
		from models import Artcam
		site = Site.objects.get_current()
		for artcam in Artcam.objects.all():
			try:
				artcam.update_photo()
			except:
				print 'error in artcam task: '
				self.send_alert("ArtCam Failure: %s" % artcam, "Could not update %s: %s %s" % (artcam, sys.exc_info()[0], sys.exc_info()[1]))
				logging.debug("Could not update %s: %s %s", artcam, sys.exc_info()[0], sys.exc_info()[1])


