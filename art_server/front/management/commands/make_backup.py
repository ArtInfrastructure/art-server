# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import time
import urllib
import sys
import datetime

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.conf import settings

class Command(BaseCommand):
	help = "Creates a backup containing an SQL dump and the non-static media files."
	args = ""
	requires_model_validation = False
	option_list = BaseCommand.option_list + (
		make_option('--upload', action='store_true', default=False, help='Upload the file to S3 (default: False)'),
		make_option('--nofiles', action='store_true', default=False, help='Do not include dynamic files (default: False).'),
	)

	def call_system(self, command):
		print command
		return os.system(command) == 0
	
	def handle(self, *labels, **options):
		upload = options['upload']
		nofiles = options['nofiles']
		print upload
		if settings.DATABASE_ENGINE != 'postgresql_psycopg2': raise CommandError('This command only works with PostgreSQL')
		if not hasattr(settings, 'DYNAMIC_MEDIA_DIRS'): raise CommandError('You must define DYNAMIC_MEDIA_DIRS in settings.py')
		for dir_path in settings.DYNAMIC_MEDIA_DIRS:
			if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dir_path)): raise CommandError('Specified dynamic media directory "%s" does not exist.' % dir_path)
			if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, dir_path)): raise CommandError('Specified dynamic media directory "%s" is not a directory.' % dir_path)
		if not hasattr(settings, 'BACKUP_ROOT'): raise CommandError('You must define BACKUP_ROOT in settings.py')
		if not os.path.exists(settings.BACKUP_ROOT): raise CommandError('Backup root "%s" does not exist' % settings.BACKUP_ROOT)
		if not os.path.isdir(settings.BACKUP_ROOT): raise CommandError('Backup root "%s" is not a directory' % settings.BACKUP_ROOT)
		if upload:
			if not hasattr(settings, 'AWS_ACCESS_KEY'): raise CommandError('You must define AWS_ACCESS_KEY in settings.py')
			if not hasattr(settings, 'AWS_SECRET_KEY'): raise CommandError('You must define AWS_SECRET_KEY in settings.py')
			if not hasattr(settings, 'BACKUP_S3_BUCKET'): raise CommandError('You must define BACKUP_S3_BUCKET in settings.py')

		now = datetime.datetime.now()
		if nofiles:
			file_token = '%d-%02d-%02d_%02d-%02d-%02d-nofiles' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
		else:
			file_token = '%d-%02d-%02d_%02d-%02d-%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

		sql_file = '%s-sql.gz' % file_token
		sql_path = '%s%s' % (settings.BACKUP_ROOT, sql_file)
		command = 'pg_dump -U %s %s | gzip > "%s"' % (settings.DATABASE_USER, settings.DATABASE_NAME, sql_path)
		if not self.call_system(command):
			print 'aborting'
			return

		if nofiles == False:
			media_file = '%s-media.tgz' % file_token
			media_path = '%s%s' % (settings.BACKUP_ROOT, media_file)
			command = 'cd "%s" && tar -czf "%s" %s' % (settings.MEDIA_ROOT, media_path, ' '.join(['"%s"' % media_dir for media_dir in settings.DYNAMIC_MEDIA_DIRS]))
			if not self.call_system(command):
				print 'aborting'
				return
	
		backup_file = '%s%s-backup.tar' % (settings.BACKUP_ROOT, file_token)
		if nofiles:
			command = 'cd "%s" && tar -czf "%s" "%s"' % (settings.BACKUP_ROOT, backup_file, sql_file)
		else:
			command = 'cd "%s" && tar -czf "%s" "%s" "%s"' % (settings.BACKUP_ROOT, backup_file, media_file, sql_file)
		if not self.call_system(command):
			print 'aborting'
			return

		if nofiles:
			command = 'rm -f "%s"' % sql_path
		else:
			command = 'rm -f "%s" "%s"' % (media_path, sql_path)
		if not self.call_system(command): print 'Could not erase temp backup files'

		if upload:
			source_path = os.path.join(settings.BACKUP_ROOT, backup_file)
			if not os.path.exists(source_path): raise CommandError('Backup file does not exist: %s' % source_path)
			s3_connection = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
			bucket = s3_connection.lookup(settings.BACKUP_S3_BUCKET)
			if bucket == None:
				bucket = s3_connection.create_bucket(settings.BACKUP_S3_BUCKET)
			k = Key(bucket)
			k.key = os.path.basename(source_path)
			k.set_contents_from_filename(source_path)
