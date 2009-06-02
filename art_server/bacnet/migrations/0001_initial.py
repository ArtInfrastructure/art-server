
from south.db import db
from django.db import models
from art_server.bacnet.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'BACnetObject'
        db.create_table('bacnet_bacnetobject', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
            ('address', models.CharField(max_length=1024, null=False, blank=False)),
            ('type_name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('bacnet', ['BACnetObject'])
        
        # Adding model 'BACnetProperty'
        db.create_table('bacnet_bacnetproperty', (
            ('id', models.AutoField(primary_key=True)),
            ('bacnet_object', models.ForeignKey(orm.BACnetObject, related_name='bacnet_properties', null=False, blank=False)),
            ('name', models.CharField(max_length=1024, null=True, blank=True)),
            ('type_name', models.CharField(max_length=1024, null=True, blank=True)),
            ('reading_frequency', models.IntegerField(default=0, null=False, blank=False)),
            ('last_reading_attempt', models.DateTimeField(null=False, editable=False, blank=True)),
        ))
        db.send_create_signal('bacnet', ['BACnetProperty'])
        
        # Adding model 'BACnetPropertyReading'
        db.create_table('bacnet_bacnetpropertyreading', (
            ('id', models.AutoField(primary_key=True)),
            ('bacnet_property', models.ForeignKey(orm.BACnetProperty, related_name='bacnet_property_readings', null=False, blank=False)),
            ('reading', models.CharField(max_length=1024, null=False, blank=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('bacnet', ['BACnetPropertyReading'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'BACnetObject'
        db.delete_table('bacnet_bacnetobject')
        
        # Deleting model 'BACnetProperty'
        db.delete_table('bacnet_bacnetproperty')
        
        # Deleting model 'BACnetPropertyReading'
        db.delete_table('bacnet_bacnetpropertyreading')
        
    
    
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
            'last_reading_attempt': ('models.DateTimeField', [], {'null': 'False', 'editable': 'False', 'blank': 'True'}),
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
