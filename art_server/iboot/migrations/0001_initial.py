
from south.db import db
from django.db import models
from art_server.iboot.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'IBootDevice'
        db.create_table('iboot_ibootdevice', (
            ('ip', models.IPAddressField(null=True, blank=False)),
            ('mac_address', models.CharField(max_length=1024, null=False, blank=False)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('iboot', ['IBootDevice'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'IBootDevice'
        db.delete_table('iboot_ibootdevice')
        
    
    
    models = {
        'iboot.ibootdevice': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', [], {'null': 'True', 'blank': 'False'}),
            'mac_address': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['iboot']
