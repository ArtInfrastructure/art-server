
from south.db import db
from django.db import models
from art_server.iboot.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'IBootEvent'
        db.create_table('iboot_ibootevent', (
            ('id', orm['iboot.ibootevent:id']),
            ('active', orm['iboot.ibootevent:active']),
            ('days', orm['iboot.ibootevent:days']),
            ('hours', orm['iboot.ibootevent:hours']),
            ('minutes', orm['iboot.ibootevent:minutes']),
            ('last_run', orm['iboot.ibootevent:last_run']),
            ('tries', orm['iboot.ibootevent:tries']),
            ('command', orm['iboot.ibootevent:command']),
            ('device', orm['iboot.ibootevent:device']),
        ))
        db.send_create_signal('iboot', ['IBootEvent'])
        
        # Changing field 'IBootDevice.ip'
        # (to signature: django.db.models.fields.IPAddressField(max_length=15, null=True))
        db.alter_column('iboot_ibootdevice', 'ip', orm['iboot.ibootdevice:ip'])
        
        # Changing field 'IBootDevice.mac_address'
        # (to signature: django.db.models.fields.CharField(max_length=1024))
        db.alter_column('iboot_ibootdevice', 'mac_address', orm['iboot.ibootdevice:mac_address'])
        
        # Changing field 'IBootDevice.name'
        # (to signature: django.db.models.fields.CharField(max_length=1024))
        db.alter_column('iboot_ibootdevice', 'name', orm['iboot.ibootdevice:name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'IBootEvent'
        db.delete_table('iboot_ibootevent')
        
        # Changing field 'IBootDevice.ip'
        # (to signature: models.IPAddressField(null=True, blank=False))
        db.alter_column('iboot_ibootdevice', 'ip', orm['iboot.ibootdevice:ip'])
        
        # Changing field 'IBootDevice.mac_address'
        # (to signature: models.CharField(max_length=1024, null=False, blank=False))
        db.alter_column('iboot_ibootdevice', 'mac_address', orm['iboot.ibootdevice:mac_address'])
        
        # Changing field 'IBootDevice.name'
        # (to signature: models.CharField(max_length=1024, null=False, blank=False))
        db.alter_column('iboot_ibootdevice', 'name', orm['iboot.ibootdevice:name'])
        
    
    
    models = {
        'iboot.ibootdevice': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'iboot.ibootevent': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'command': ('django.db.models.fields.CharField', [], {'default': "'cycle'", 'max_length': '12'}),
            'days': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iboot.IBootDevice']"}),
            'hours': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'minutes': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'tries': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['iboot']
