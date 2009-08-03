
from south.db import db
from django.db import models
from art_server.airport.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AirportSnapshot'
        db.create_table('airport_airportsnapshot', (
            ('id', models.AutoField(primary_key=True)),
            ('xml_data', models.TextField(null=False, blank=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('airport', ['AirportSnapshot'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AirportSnapshot'
        db.delete_table('airport_airportsnapshot')
        
    
    
    models = {
        'airport.airportsnapshot': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'xml_data': ('models.TextField', [], {'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['airport']
