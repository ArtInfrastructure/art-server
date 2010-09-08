from scripts.scheduler import Task
import httplib, urllib
import traceback
import logging
import pprint
from stat import S_ISREG, ST_MTIME, ST_MODE
import sys, os, time

class ArtcamTask(Task):
	"""The schedule task which updates the stored images for each of the artcams."""
	def __init__(self, loopdelay=300, initdelay=1):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		from django.contrib.sites.models import Site
		from django.conf import settings
		from models import Artcam
		
		site = Site.objects.get_current()
		for artcam in Artcam.objects.all():
			try:
				artcam.update_photo()
			except:
				print 'error in artcam task: '
				self.send_alert("ArtCam Failure: %s" % artcam, "Could not update %s: %s %s" % (artcam, sys.exc_info()[0], sys.exc_info()[1]))
				logging.debug("Could not update %s: %s %s", artcam, sys.exc_info()[0], sys.exc_info()[1])

		# delete the old resized images
		files = self.resized_files()
		youngest_date = int(time.time()) - 604800 # a week worth of seconds
		for cd, path in files:
			if cd < youngest_date:
				os.unlink(path)				

	def resized_files(self):
		"""Returns an array of info about resized image files in the form (creation_date, path), sorted in chronological order by modified date"""
		from django.conf import settings
		from front.templatetags.imagetags import RESIZED_IMAGE_DIR

		resize_image_dir = os.path.join(settings.MEDIA_ROOT, RESIZED_IMAGE_DIR, 'artcam_photo')
		if not os.path.isdir(resize_image_dir):
			print 'No resized image directory'
			return None

		entries = (os.path.join(resize_image_dir, fn) for fn in os.listdir(resize_image_dir))
		entries = ((os.stat(path), path) for path in entries)
		
		# leave only regular files, insert creation date
		return sorted(((stat[ST_MTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE])))

