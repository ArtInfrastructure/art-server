# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import time
import urllib
import sys
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
	help = "Creates a backup containing an SQL dump and the non-static media files."
	args = ""
	requires_model_validation = False

	def call_system(self, command):
		print command
		return os.system(command) == 0
	
	def handle(self, *labels, **options):
		if settings.DATABASE_ENGINE != 'postgresql_psycopg2': raise CommandError('This command only works with PostgreSQL')
		if not hasattr(settings, 'DYNAMIC_MEDIA_DIRS'): raise CommandError('You must define DYNAMIC_MEDIA_DIRS in settings.py')
		for dir_path in settings.DYNAMIC_MEDIA_DIRS:
			if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dir_path)): raise CommandError('Specified dynamic media directory "%s" does not exist.' % dir_path)
			if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, dir_path)): raise CommandError('Specified dynamic media directory "%s" is not a directory.' % dir_path)
		if not hasattr(settings, 'BACKUP_ROOT'): raise CommandError('You must define BACKUP_ROOT in settings.py')
		if not os.path.exists(settings.BACKUP_ROOT): raise CommandError('Backup root "%s" does not exist' % settings.BACKUP_ROOT)
		if not os.path.isdir(settings.BACKUP_ROOT): raise CommandError('Backup root "%s" is not a directory' % settings.BACKUP_ROOT)

		now = datetime.datetime.now()
		file_token = '%d-%02d-%02d_%02d-%02d-%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

		sql_file = '%s-sql.gz' % file_token
		sql_path = '%s%s' % (settings.BACKUP_ROOT, sql_file)
		command = 'pg_dump -U %s %s | gzip > "%s"' % (settings.DATABASE_USER, settings.DATABASE_NAME, sql_path)
		if not self.call_system(command):
			print 'aborting'
			return

		media_file = '%s-media.tgz' % file_token
		media_path = '%s%s' % (settings.BACKUP_ROOT, media_file)
		command = 'cd "%s" && tar -czf "%s" %s' % (settings.MEDIA_ROOT, media_path, ' '.join(['"%s"' % media_dir for media_dir in settings.DYNAMIC_MEDIA_DIRS]))
		if not self.call_system(command):
			print 'aborting'
			return
	
		backup_file = '%s%s-backup.tar' % (settings.BACKUP_ROOT, file_token)
		command = 'cd "%s" && tar -czf "%s" "%s" "%s"' % (settings.BACKUP_ROOT, backup_file, media_file, sql_file)
		if not self.call_system(command):
			print 'aborting'
			return
	
		command = 'rm -f "%s" "%s"' % (media_path, sql_path)
		if not self.call_system(command): print 'Could not erase temp backup files'
