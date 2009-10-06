#!/usr/bin/python
"""Creates the HTML documentation for the art-cloud APIs."""
import os
import datetime
import sys

from common_script import *

APP_NAME = 'Art Server'
SETTINGS = 'art_server.settings'

def main():
	command = 'export PYTHONPATH=..; export DJANGO_SETTINGS_MODULE=%s; epydoc --html . -v -o ../docs/ --name "%s API Docs"' % (SETTINGS, APP_NAME)
	if not call_system(command):
		print 'aborting'
		return

if __name__ == '__main__':
	main()