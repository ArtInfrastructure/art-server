# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ProxyDestination'
        db.create_table('epoxy_proxydestination', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('epoxy', ['ProxyDestination'])


    def backwards(self, orm):
        
        # Deleting model 'ProxyDestination'
        db.delete_table('epoxy_proxydestination')


    models = {
        'epoxy.proxydestination': {
            'Meta': {'ordering': "['id']", 'object_name': 'ProxyDestination'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['epoxy']
