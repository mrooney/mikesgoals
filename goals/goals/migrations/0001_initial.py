# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Goal'
        db.create_table('goals_goal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('frequency', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('goals', ['Goal'])


    def backwards(self, orm):
        # Deleting model 'Goal'
        db.delete_table('goals_goal')


    models = {
        'goals.goal': {
            'Meta': {'object_name': 'Goal'},
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['goals']