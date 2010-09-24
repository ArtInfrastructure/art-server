# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from scripts.scheduler import Task
import traceback
import logging
from datetime import datetime, timedelta

import sys, os, time

class ProjectorEventTask(Task):
	"""The task which runs scheduled events for the projector."""
	def __init__(self, loopdelay=60, initdelay=1):
		Task.__init__(self, self.do_it, loopdelay, initdelay)

	def do_it(self):
		from models import ProjectorEvent
		for event in ProjectorEvent.objects.all():
			if event.due_for_execution(): event.execute()
