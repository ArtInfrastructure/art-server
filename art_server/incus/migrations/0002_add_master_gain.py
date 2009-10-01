
from south.db import db
from django.db import models
from art_server.incus.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'ABChannelGroup.master_gain'
        db.add_column('incus_abchannelgroup', 'master_gain', models.FloatField(default=0, null=False))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'ABChannelGroup.master_gain'
        db.delete_column('incus_abchannelgroup', 'master_gain')
        
    
    
    models = {
        'incus.abdevice': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', [], {'null': 'False', 'blank': 'False'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'port': ('models.IntegerField', [], {'default': '55128', 'null': 'False', 'blank': 'False'})
        },
        'incus.abchannelgroup': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'master_gain': ('models.FloatField', [], {'default': '0', 'null': 'False'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'})
        },
        'incus.abchannel': {
            'Meta': {'ordering': "['number']"},
            'audioBoxDevice': ('models.ForeignKey', ["orm['incus.ABDevice']"], {'null': 'False', 'blank': 'False'}),
            'channel_group': ('models.ForeignKey', ["orm['incus.ABChannelGroup']"], {'related_name': '"channels"', 'null': 'True', 'blank': 'True'}),
            'gain': ('models.FloatField', [], {'default': '0', 'null': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'number': ('models.IntegerField', [], {'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['incus']
