
from scripts.scheduler import Task

class BACnetTask(Task):
	def __init__(self, loopdelay=30, initdelay=30):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		#find all the readings which need to be taken
		# take them
		pass
