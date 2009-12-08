
from south.db import db
from django.db import models
from art_server.lighting.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Projector'
        db.create_table('lighting_projector', (
            ('id', orm['lighting.Projector:id']),
            ('name', orm['lighting.Projector:name']),
        ))
        db.send_create_signal('lighting', ['Projector'])
        
        # Adding model 'BACNetLight'
        db.create_table('lighting_bacnetlight', (
            ('id', orm['lighting.BACNetLight:id']),
            ('name', orm['lighting.BACNetLight:name']),
        ))
        db.send_create_signal('lighting', ['BACNetLight'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Projector'
        db.delete_table('lighting_projector')
        
        # Deleting model 'BACNetLight'
        db.delete_table('lighting_bacnetlight')
        
    
    
    models = {
        'lighting.bacnetlight': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'lighting.projector': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }
    
    complete_apps = ['lighting']
