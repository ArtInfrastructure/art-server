# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ABDevice.ip'
        db.alter_column('incus_abdevice', 'ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15))

        # Changing field 'ABDevice.port'
        db.alter_column('incus_abdevice', 'port', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ABDevice.name'
        db.alter_column('incus_abdevice', 'name', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Changing field 'ABChannelGroup.name'
        db.alter_column('incus_abchannelgroup', 'name', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Changing field 'ABChannelGroup.master_gain'
        db.alter_column('incus_abchannelgroup', 'master_gain', self.gf('django.db.models.fields.FloatField')())

        # Adding field 'ABChannel.channel_type'
        db.add_column('incus_abchannel', 'channel_type', self.gf('django.db.models.fields.CharField')(default='o', max_length=1), keep_default=False)

        # Changing field 'ABChannel.channel_group'
        db.alter_column('incus_abchannel', 'channel_group_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['incus.ABChannelGroup']))

        # Changing field 'ABChannel.audioBoxDevice'
        db.alter_column('incus_abchannel', 'audioBoxDevice_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incus.ABDevice']))

        # Changing field 'ABChannel.gain'
        db.alter_column('incus_abchannel', 'gain', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'ABChannel.number'
        db.alter_column('incus_abchannel', 'number', self.gf('django.db.models.fields.IntegerField')())


    def backwards(self, orm):
        
        # Changing field 'ABDevice.ip'
        db.alter_column('incus_abdevice', 'ip', self.gf('models.IPAddressField')(null=False))

        # Changing field 'ABDevice.port'
        db.alter_column('incus_abdevice', 'port', self.gf('models.IntegerField')(null=False))

        # Changing field 'ABDevice.name'
        db.alter_column('incus_abdevice', 'name', self.gf('models.CharField')(max_length=1024, null=False))

        # Changing field 'ABChannelGroup.name'
        db.alter_column('incus_abchannelgroup', 'name', self.gf('models.CharField')(max_length=1024, null=False))

        # Changing field 'ABChannelGroup.master_gain'
        db.alter_column('incus_abchannelgroup', 'master_gain', self.gf('models.FloatField')(null=False))

        # Deleting field 'ABChannel.channel_type'
        db.delete_column('incus_abchannel', 'channel_type')

        # Changing field 'ABChannel.channel_group'
        db.alter_column('incus_abchannel', 'channel_group_id', self.gf('models.ForeignKey')(orm['incus.ABChannelGroup'], null=True))

        # Changing field 'ABChannel.audioBoxDevice'
        db.alter_column('incus_abchannel', 'audioBoxDevice_id', self.gf('models.ForeignKey')(orm['incus.ABDevice'], null=False))

        # Changing field 'ABChannel.gain'
        db.alter_column('incus_abchannel', 'gain', self.gf('models.FloatField')(null=False))

        # Changing field 'ABChannel.number'
        db.alter_column('incus_abchannel', 'number', self.gf('models.IntegerField')(null=False))


    models = {
        'incus.abchannel': {
            'Meta': {'ordering': "['number']", 'object_name': 'ABChannel'},
            'audioBoxDevice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['incus.ABDevice']"}),
            'channel_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'channels'", 'null': 'True', 'to': "orm['incus.ABChannelGroup']"}),
            'channel_type': ('django.db.models.fields.CharField', [], {'default': "'o'", 'max_length': '1'}),
            'gain': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'incus.abchannelgroup': {
            'Meta': {'object_name': 'ABChannelGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master_gain': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'incus.abdevice': {
            'Meta': {'object_name': 'ABDevice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '55128'})
        }
    }

    complete_apps = ['incus']
