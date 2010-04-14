#!/usr/bin/python
"""
A simple task scheduling script which schedules tasks defined in settings.SCHEDULED_TASKS.
Copied wholesale from http://code.activestate.com/recipes/114644/ then tweaked for Django
"""
import os, sys
import time
import threading
import readline
import cmd
import logging
import traceback
import datetime

class Task(threading.Thread):
	def __init__(self, action, loopdelay, initdelay):
		"""The action is a function which will be called in a new thread every loopdelay microseconds, starting after initdelay microseconds"""
		self._action = action
		self._loopdelay = loopdelay
		self._initdelay = initdelay
		self._running = 1
		self.last_alert_datetime = None
		threading.Thread.__init__(self)

	def send_alert(self, subject, message):
		try:
			if self.last_alert_datetime and self.last_alert_datetime > datetime.datetime.now() - datetime.timedelta(minutes=10):
				print 'Not sending an alert because there was one sent in the last 10 minutes: %s' % subject
				return
			from front.management.commands.send_alert import Command as SendAlertCommand
			alert_command = SendAlertCommand()
			alert_command.handle(subject, message)
			self.last_alert_datetime = datetime.datetime.now()
		except:
			traceback.print_exc()
			logging.exception('Could not send an alert')

	def run(self):
		"""There's no need to override this.  Pass your action in as a function to the __init__."""
		if self._initdelay:
			time.sleep(self._initdelay)
		self._runtime = time.time()
		while self._running:
			start = time.time()
			self._action()
			self._runtime += self._loopdelay
			time.sleep(max(0, self._runtime - start))
	
	def stop(self):
		self._running = 0

class TestTask(Task):
	"""An example task"""
	def __init__(self, loopdelay, initdelay, name="TestTask"):
		self.name = name
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		print 'Doing it: %s' % self.name

class Scheduler:
	"""The class which manages starting and stopping of tasks."""
	def __init__(self):
		self._tasks = []
	
	def __repr__(self):
		rep = ''
		for task in self._tasks:
			rep += '%s\n' % `task`
		return rep
	
	def add_task(self, task):
		self._tasks.append(task)
	
	def start_all_tasks(self):
		print 'Starting scheduler'
		for task in self._tasks:
			print 'Starting task', task
			task.start()
		print 'All tasks started'
	
	def stop_all_tasks(self):
		for task in self._tasks:
			print 'Stopping task', task
			task.stop()
			task.join()
			print 'Stopped'

class Console(cmd.Cmd):
	def do_it(self, args):
		print 'doing it'
	def default(self, line):
		print 'line %s' % line

def write_proc(lockfile_path):
	if os.access(lockfile_path, os.F_OK):
		pidfile = open(lockfile_path, "r")
		pidfile.seek(0)
		old_pd = pidfile.readline()
		if os.path.exists("/proc/%s" % old_pd): # this only works on OSes with /proc/ (e.g. linux)
			print "You already have an instance of the program running"
			print "It is running as process %s," % old_pd
			return False
		else:
			os.remove(lockfile_path)

	pidfile = open(lockfile_path, "w")
	pidfile.write("%s" % os.getpid())
	pidfile.close
	return True

if __name__ == '__main__':
	import sys
	from django.core.management import setup_environ
	import settings
	import logging
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='/tmp/scheduler-art-server.txt', filemode = 'w')
	setup_environ(settings)

	write_proc('/tmp/artserver_scheduler.pid')

	s = Scheduler()
	for task in settings.SCHEDULED_TASKS:
		s.add_task(task)
	s.start_all_tasks()
