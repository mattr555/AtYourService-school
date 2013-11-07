# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.grad_class'
        db.add_column('main_userprofile', 'grad_class',
                      self.gf('django.db.models.fields.IntegerField')(default=2016),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.grad_class'
        db.delete_column('main_userprofile', 'grad_class')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.event': {
            'Meta': {'object_name': 'Event'},
            'confirmed_participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'confirmed_events'"}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Organization']", 'related_name': "'events'"}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'events_organized'"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'events'"})
        },
        'main.organization': {
            'Meta': {'object_name': 'Organization'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'orgs_admin'"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'organizations'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'})
        },
        'main.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leadership_hours': ('django.db.models.fields.IntegerField', [], {}),
            'service_hours': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'related_name': "'settings'", 'unique': 'True'})
        },
        'main.userevent': {
            'Meta': {'object_name': 'UserEvent'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'hours_worked': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'user_events'"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_validation_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'grad_class': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'timezone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'related_name': "'user_profile'", 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']