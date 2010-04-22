# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import time
import urllib
import datetime
import sys
import tempfile
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
	help = "Deletes and then restores the DB and non-static media from a backup created using the make_backup management command."
	args = "[backup_file_path]"
	requires_model_validation = False

	def call_system(self, command):
		print command
		return os.system(command) == 0

	def handle(self, *labels, **options):
		if settings.DATABASE_ENGINE != 'postgresql_psycopg2': raise CommandError('This command only works with PostgreSQL')
		if not labels or len(labels) != 1: raise CommandError('Enter one argument, the path to the backup tar file.')
		backup_path = os.path.realpath(labels[0])
		if not os.path.exists(backup_path): raise CommandError('The backup file "%s" does not exist.' % backup_path)
		if not os.path.isfile(backup_path): raise CommandError('The specified backup file "%s" is not a file.' % backup_path)
		if not backup_path.endswith('.tar'): raise CommandError('The specified backup file "%s" must be a tar file.' % backup_path)

		print 'Restoring from backup file "%s"' % backup_path

		# create the working directory
		working_dir = tempfile.mkdtemp('backup-temp')

		# untar the backup file, which should result in two files: sql and media
		command = 'cd "%s" && tar -xzf "%s"' % (working_dir, backup_path)
		if not self.call_system(command): raise CommandError('Aborting restoration.')

		# create a sub directory for the media, and untar it
		media_dir = os.path.join(working_dir, 'media')
		os.mkdir(media_dir)
		command = 'cd "%s" && tar -xzf %s/*-media.tgz' % (media_dir, working_dir)
		if not self.call_system(command): raise CommandError('Aborting restoration.')

		# move each media dir from the temp media dir into the project media dir
		for new_media_dir in os.listdir(media_dir):
			target_dir = os.path.join(settings.MEDIA_ROOT, new_media_dir)
			if os.path.exists(target_dir): shutil.rmtree(target_dir)
			shutil.move(os.path.join(media_dir, new_media_dir), target_dir)

		# now delete and recreate the database
		command = 'echo "drop database %s; create database %s; grant all on database %s to %s;" | psql -U %s' % (settings.DATABASE_NAME, settings.DATABASE_NAME, settings.DATABASE_NAME, settings.DATABASE_USER, settings.DATABASE_USER)
		if not self.call_system(command): raise CommandError('Aborting restoration.')

		# now load the SQL into the database
		command = 'gunzip -c %s/*-sql.gz | psql -U %s %s' % (working_dir, settings.DATABASE_USER, settings.DATABASE_NAME)
		if not self.call_system(command): raise CommandError('Aborting restoration.')
