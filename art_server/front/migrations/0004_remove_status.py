
from south.db import db
from django.db import models
from art_server.front.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'DummyModel'
        db.create_table('front_dummymodel', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=512, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['DummyModel'])
        
        # Deleting model 'statuslistenertest'
        db.delete_table('front_statuslistenertest')
        
        # Deleting model 'statuslistener'
        db.delete_table('front_statuslistener')
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'DummyModel'
        db.delete_table('front_dummymodel')
        
        # Adding model 'statuslistenertest'
        db.create_table('front_statuslistenertest', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=512, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['statuslistenertest'])
        
        # Adding model 'statuslistener'
        db.create_table('front_statuslistener', (
            ('host', models.CharField(max_length=1024, unique=True, null=False, blank=False)),
            ('tests', models.ManyToManyField(orm['front.StatusListenerTest'], null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('front', ['statuslistener'])
        
    
    
    models = {
        'front.statuslistenertest': {
            '_stub': True,
            'id': 'models.AutoField(primary_key=True)'
        },
        'front.dummymodel': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '512', 'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['front']
