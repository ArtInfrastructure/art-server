
from south.db import db
from django.db import models
from art_server.artcam.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Artcam'
        db.create_table('artcam_artcam', (
            ('port', models.IntegerField(null=True, blank=True)),
            ('ip', models.IPAddressField(null=True, blank=False)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal('artcam', ['Artcam'])
        
        # Adding model 'ArtcamPhoto'
        db.create_table('artcam_artcamphoto', (
            ('artcam', models.ForeignKey(orm.Artcam, null=False, blank=False)),
            ('image', models.ImageField(blank=False)),
            ('id', models.AutoField(primary_key=True)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('artcam', ['ArtcamPhoto'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Artcam'
        db.delete_table('artcam_artcam')
        
        # Deleting model 'ArtcamPhoto'
        db.delete_table('artcam_artcamphoto')
        
    
    
    models = {
        'artcam.artcam': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', [], {'null': 'True', 'blank': 'False'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'port': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'artcam.artcamphoto': {
            'Meta': {'ordering': "['-created']"},
            'artcam': ('models.ForeignKey', ['Artcam'], {'null': 'False', 'blank': 'False'}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {'blank': 'False'})
        }
    }
    
    complete_apps = ['artcam']
