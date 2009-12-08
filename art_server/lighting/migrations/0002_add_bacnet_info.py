
from south.db import db
from django.db import models
from art_server.lighting.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'BACNetLight.property_id'
        db.add_column('lighting_bacnetlight', 'property_id', orm['lighting.bacnetlight:property_id'])
        
        # Adding field 'BACNetLight.device_id'
        db.add_column('lighting_bacnetlight', 'device_id', orm['lighting.bacnetlight:device_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'BACNetLight.property_id'
        db.delete_column('lighting_bacnetlight', 'property_id')
        
        # Deleting field 'BACNetLight.device_id'
        db.delete_column('lighting_bacnetlight', 'device_id')
        
    
    
    models = {
        'lighting.bacnetlight': {
            'device_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'property_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'lighting.projector': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }
    
    complete_apps = ['lighting']
