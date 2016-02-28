# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Profile.contact'
        db.delete_column(u'hello_profile', 'contact')

        # Adding field 'Profile.email'
        db.add_column(u'hello_profile', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='email@mail.com', max_length=75),
                      keep_default=False)

        # Adding field 'Profile.skype'
        db.add_column(u'hello_profile', 'skype',
                      self.gf('django.db.models.fields.CharField')(default='skype_id', max_length=30),
                      keep_default=False)

        # Adding field 'Profile.jabber'
        db.add_column(u'hello_profile', 'jabber',
                      self.gf('django.db.models.fields.EmailField')(default='jabber@jabber.com', max_length=75),
                      keep_default=False)

        # Adding field 'Profile.other_contacts'
        db.add_column(u'hello_profile', 'other_contacts',
                      self.gf('django.db.models.fields.TextField')(default='Other contacts here'),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Profile.contact'
        db.add_column(u'hello_profile', 'contact',
                      self.gf('django.db.models.fields.EmailField')(default='contact', max_length=75),
                      keep_default=False)

        # Deleting field 'Profile.email'
        db.delete_column(u'hello_profile', 'email')

        # Deleting field 'Profile.skype'
        db.delete_column(u'hello_profile', 'skype')

        # Deleting field 'Profile.jabber'
        db.delete_column(u'hello_profile', 'jabber')

        # Deleting field 'Profile.other_contacts'
        db.delete_column(u'hello_profile', 'other_contacts')


    models = {
        u'hello.dbaction': {
            'Meta': {'object_name': 'DBAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'hello.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'hello.request': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Request'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']