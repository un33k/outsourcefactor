# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.subscriptions'
        db.add_column('profiles_userprofile', 'subscriptions',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'UserProfile.subscriptions'
        db.delete_column('profiles_userprofile', 'subscriptions')

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
        'profiles.jobpost': {
            'Meta': {'ordering': "['title']", 'unique_together': "(('user', 'title'),)", 'object_name': 'JobPost'},
            'bookmarked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'employment_option': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '56', 'blank': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 8, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobpost'", 'to': "orm['auth.User']"}),
            'viewed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wage_salary': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'profiles.skill': {
            'Meta': {'ordering': "['category__name', 'name']", 'object_name': 'Skill'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Skill']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.skillset': {
            'Meta': {'ordering': "['skill__category__name', 'skill__name']", 'unique_together': "(('user', 'skill'),)", 'object_name': 'SkillSet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Skill']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skillset'", 'to': "orm['auth.User']"})
        },
        'profiles.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'availability_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 8, 0, 0)'}),
            'bookmarked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'business': ('django.db.models.fields.CharField', [], {'max_length': '58'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'desired_salary': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'employment_option': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'employment_type': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'filled_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hours_per_week': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'is_freelance': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'posted_jobs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'posted_skills': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'subscriptions': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'tier': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '68'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'viewed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '50', 'blank': 'True'}),
            'work_arrangements': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['profiles']