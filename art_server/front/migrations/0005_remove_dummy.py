
from south.db import db
from django.db import models
from art_server.front.models import *

class Migration:
    
    def forwards(self, orm):
        
        
        # Deleting model 'DummyModel'
        db.delete_table('front_dummymodel')
        
    
    
    def backwards(self, orm):
        # Adding model 'DummyModel'
        db.create_table('front_dummymodel', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=512, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['DummyModel'])
    
    models = {
    }
    
    complete_apps = ['front']
