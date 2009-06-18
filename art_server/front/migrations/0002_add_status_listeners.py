
from south.db import db
from django.db import models
from art_server.front.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'StatusListener'
        db.create_table('front_statuslistener', (
            ('id', models.AutoField(primary_key=True)),
            ('host', models.CharField(unique=True, max_length=1024, null=False, blank=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('front', ['StatusListener'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'StatusListener'
        db.delete_table('front_statuslistener')
        
    
    
    models = {
        'front.statuslistener': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'host': ('models.CharField', [], {'unique': 'True', 'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['front']
