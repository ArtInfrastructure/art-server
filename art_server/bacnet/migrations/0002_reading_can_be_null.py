
from south.db import db
from django.db import models
from art_server.bacnet.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'BACnetProperty.last_reading_attempt'
        db.alter_column('bacnet_bacnetproperty', 'last_reading_attempt', models.DateTimeField(null=True, editable=False, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Changing field 'BACnetProperty.last_reading_attempt'
        db.alter_column('bacnet_bacnetproperty', 'last_reading_attempt', models.DateTimeField(null=False, editable=False, blank=True))
        
    
    
    models = {
        'bacnet.bacnetobject': {
            'Meta': {'ordering': "['name']"},
            'address': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'type_name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'})
        },
        'bacnet.bacnetproperty': {
            'Meta': {'ordering': "['name']"},
            'bacnet_object': ('models.ForeignKey', ["orm['bacnet.BACnetObject']"], {'related_name': "'bacnet_properties'", 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_reading_attempt': ('models.DateTimeField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'reading_frequency': ('models.IntegerField', [], {'default': '0', 'null': 'False', 'blank': 'False'}),
            'type_name': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'bacnet.bacnetpropertyreading': {
            'Meta': {'ordering': "['-created']"},
            'bacnet_property': ('models.ForeignKey', ["orm['bacnet.BACnetProperty']"], {'related_name': "'bacnet_property_readings'", 'null': 'False', 'blank': 'False'}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'reading': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['bacnet']
