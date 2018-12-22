# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialAuthProvider'
        db.create_table('social_socialauthprovider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='socialauthprovider', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=250)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('social', ['SocialAuthProvider'])

        # Adding unique constraint on 'SocialAuthProvider', fields ['user', 'uuid']
        db.create_unique('social_socialauthprovider', ['user_id', 'uuid'])

        # Adding unique constraint on 'SocialAuthProvider', fields ['name', 'email']
        db.create_unique('social_socialauthprovider', ['name', 'email'])

        # Adding model 'SocialProfileProvider'
        db.create_table('social_socialprofileprovider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='socialprofileprovider', to=orm['auth.User'])),
            ('provider', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=100, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('social', ['SocialProfileProvider'])

        # Adding unique constraint on 'SocialProfileProvider', fields ['user', 'provider']
        db.create_unique('social_socialprofileprovider', ['user_id', 'provider'])

    def backwards(self, orm):
        # Removing unique constraint on 'SocialProfileProvider', fields ['user', 'provider']
        db.delete_unique('social_socialprofileprovider', ['user_id', 'provider'])

        # Removing unique constraint on 'SocialAuthProvider', fields ['name', 'email']
        db.delete_unique('social_socialauthprovider', ['name', 'email'])

        # Removing unique constraint on 'SocialAuthProvider', fields ['user', 'uuid']
        db.delete_unique('social_socialauthprovider', ['user_id', 'uuid'])

        # Deleting model 'SocialAuthProvider'
        db.delete_table('social_socialauthprovider')

        # Deleting model 'SocialProfileProvider'
        db.delete_table('social_socialprofileprovider')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social.socialauthprovider': {
            'Meta': {'ordering': "['user__username', 'uuid']", 'unique_together': "(('user', 'uuid'), ('name', 'email'))", 'object_name': 'SocialAuthProvider'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'socialauthprovider'", 'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'social.socialprofileprovider': {
            'Meta': {'ordering': "['provider']", 'unique_together': "(('user', 'provider'),)", 'object_name': 'SocialProfileProvider'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'socialprofileprovider'", 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['social']