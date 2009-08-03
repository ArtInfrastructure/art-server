"""A utility wrapper around various BACnet libraries, with a handy mock wrapper for testing"""

class BACnetHandler:
	def __init__(self, timeout=None):
		self.timeout = timeout
		
	def take_reading(self, address, type, instance, property_name, index=None):
		"""Attempts to read a property, returning it as a string or None if it times out or is not readable"""
		pass
	def list_properties(self, address, type, instance):
		"""Attempts to fetch a list of an object's properties"""
		pass

class MockBACnetHandler(BACnetHandler):
	def __init__(self, timeout=None):
		self.__reading_value = 22
		BACnetHandler.__init__(self, timeout)
	def take_reading(self, address, type, instance, property_name, index=None):
		self.__reading_value = self.__reading_value + 2
		return 'Reading %s' % self.__reading_value
		
class BACPipesHandler(BACnetHandler):
	def __init__(self, timeout=None):
		raise Exception # this is not implemented
	
def main():
	
		
if __name__ == "__main__": main()
