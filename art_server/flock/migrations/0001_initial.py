
from south.db import db
from django.db import models
from art_server.flock.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'StatusListenerTest'
        db.create_table('flock_statuslistenertest', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=512, null=False, blank=False)),
        ))
        db.send_create_signal('flock', ['StatusListenerTest'])
        
        # Adding model 'StatusListener'
        db.create_table('flock_statuslistener', (
            ('id', models.AutoField(primary_key=True)),
            ('host', models.CharField(unique=True, max_length=1024, null=False, blank=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('flock', ['StatusListener'])
        
        # Adding ManyToManyField 'StatusListener.tests'
        db.create_table('flock_statuslistener_tests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('statuslistener', models.ForeignKey(orm.StatusListener, null=False)),
            ('statuslistenertest', models.ForeignKey(orm.StatusListenerTest, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'StatusListenerTest'
        db.delete_table('flock_statuslistenertest')
        
        # Deleting model 'StatusListener'
        db.delete_table('flock_statuslistener')
        
        # Dropping ManyToManyField 'StatusListener.tests'
        db.delete_table('flock_statuslistener_tests')
        
    
    
    models = {
        'flock.statuslistenertest': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '512', 'null': 'False', 'blank': 'False'})
        },
        'flock.statuslistener': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'host': ('models.CharField', [], {'unique': 'True', 'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'tests': ('models.ManyToManyField', ["orm['flock.StatusListenerTest']"], {'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['flock']
