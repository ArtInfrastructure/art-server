
from south.db import db
from django.db import models
from art_server.lighting.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Projector.pjlink_password'
        db.add_column('lighting_projector', 'pjlink_password', orm['lighting.projector:pjlink_password'])
        
        # Adding field 'Projector.pjlink_port'
        db.add_column('lighting_projector', 'pjlink_port', orm['lighting.projector:pjlink_port'])
        
        # Adding field 'Projector.pjlink_host'
        db.add_column('lighting_projector', 'pjlink_host', orm['lighting.projector:pjlink_host'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Projector.pjlink_password'
        db.delete_column('lighting_projector', 'pjlink_password')
        
        # Deleting field 'Projector.pjlink_port'
        db.delete_column('lighting_projector', 'pjlink_port')
        
        # Deleting field 'Projector.pjlink_host'
        db.delete_column('lighting_projector', 'pjlink_host')
        
    
    
    models = {
        'lighting.bacnetlight': {
            'device_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'property_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'lighting.projector': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'pjlink_host': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'pjlink_password': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'pjlink_port': ('django.db.models.fields.IntegerField', [], {'default': '4352'})
        }
    }
    
    complete_apps = ['lighting']
