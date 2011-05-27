# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ProxyDestination.ips'
        db.add_column('epoxy_proxydestination', 'ips', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ProxyDestination.ips'
        db.delete_column('epoxy_proxydestination', 'ips')


    models = {
        'epoxy.proxydestination': {
            'Meta': {'ordering': "['id']", 'object_name': 'ProxyDestination'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ips': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['epoxy']
