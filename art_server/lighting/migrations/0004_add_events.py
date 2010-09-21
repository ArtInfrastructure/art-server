
from south.db import db
from django.db import models
from art_server.lighting.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ProjectorEvent'
        db.create_table('lighting_projectorevent', (
            ('id', orm['lighting.projectorevent:id']),
            ('active', orm['lighting.projectorevent:active']),
            ('days', orm['lighting.projectorevent:days']),
            ('hours', orm['lighting.projectorevent:hours']),
            ('minutes', orm['lighting.projectorevent:minutes']),
            ('last_run', orm['lighting.projectorevent:last_run']),
            ('tries', orm['lighting.projectorevent:tries']),
            ('command', orm['lighting.projectorevent:command']),
            ('device', orm['lighting.projectorevent:device']),
        ))
        db.send_create_signal('lighting', ['ProjectorEvent'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ProjectorEvent'
        db.delete_table('lighting_projectorevent')
        
    
    
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
        },
        'lighting.projectorevent': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'command': ('django.db.models.fields.CharField', [], {'default': "'cycle'", 'max_length': '12'}),
            'days': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lighting.Projector']"}),
            'hours': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'minutes': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'tries': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['lighting']
