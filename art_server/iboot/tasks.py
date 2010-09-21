from scripts.scheduler import Task
import traceback
import logging
from datetime import datetime, timedelta

import sys, os, time

class IBootEventTask(Task):
	"""The task which runs scheduled events."""
	def __init__(self, loopdelay=60, initdelay=1):
		Task.__init__(self, self.do_it, loopdelay, initdelay)

	def do_it(self):
		from models import IBootEvent
		for event in IBootEvent.objects.all():
			if event.due_for_execution(): event.execute()
