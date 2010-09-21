from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from front.models import EventModel, to_array, clean_int_field, previous_element

class EventTest(TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	def test_arrays(self):
		self.assertEqual(None, to_array(None))
		self.assertEqual(None, to_array(''))
		self.assertEqual([1], to_array('1'))
		self.assertEqual([0,3,5], to_array('0,3,5'))
		self.assertEqual(None, clean_int_field(None))
		self.assertEqual('', clean_int_field(''))
		self.assertEqual('1,4,5', clean_int_field('5,1,4'))
		self.assertEqual('1,4,5', clean_int_field('5,1,5,4,4'))
		self.assertEqual(1, previous_element(2, [0, 1, 2, 3]))
		self.assertEqual(3, previous_element(0, [0, 1, 2, 3]))
		self.assertEqual(2, previous_element(3, [0, 1, 2, 3]))
		self.assertEqual(0, previous_element(4, [0]))
		self.assertEqual(0, previous_element(0, [0]))

	def test_timing(self):
		event = EventModel()
		event.active = True
		event.days = '1,3'
		event.hours = '13,20'
		event.minutes = '12'
		
		self.assertEqual(event.last_run, None)
		self.assertFalse(event.due_for_execution(datetime(2010, 9, 21, 14, 0)))
		self.assertTrue(event.due_for_execution(datetime(2010, 9, 21, 13, 13)))
		event.last_run = datetime.now()
		self.assertFalse(event.due_for_execution(datetime(2010, 9, 21, 13, 13)))
		
		self.assertEqual(event.latest_scheduled_time(datetime(2010, 9, 21, 13, 25)), datetime(2010, 9, 21, 13, 12))

		self.assertEqual(event.latest_scheduled_time(datetime(2010, 9, 21, 21, 0)), datetime(2010, 9, 21, 20, 12))

		self.assertEqual(event.latest_scheduled_time(datetime(2010, 9, 21, 12, 19)), datetime(2010, 9, 16, 20, 12))

		self.assertEqual(event.latest_scheduled_time(datetime(2010, 1, 1, 12, 19)), datetime(2009, 12, 31, 20, 12))

		self.assertEqual(event.latest_scheduled_time(datetime(2010, 9, 21, 13, 12)), datetime(2010, 9, 16, 20, 12))

		event.minutes = None
		self.assertEqual(event.latest_scheduled_time(datetime(2010, 9, 21, 12, 19)), datetime(2010, 9, 16, 20, 0))

		event.days = None
		event.hours = None
		event.minutes = None
		self.assertEqual(event.latest_scheduled_time(datetime(2010, 9, 21, 12, 19)), None)

		event.days = None
		event.hours = '13,20'
		event.minutes = '12'
		event.last_run = None
		self.assertTrue(event.due_for_execution(datetime(2010, 9, 21, 13, 13)))

		event.days = None
		event.hours = None
		event.minutes = '12'
		event.last_run = None
		self.assertTrue(event.due_for_execution(datetime(2010, 9, 21, 13, 13)))
		self.assertTrue(event.due_for_execution(datetime(2010, 9, 21, 1, 13)))

