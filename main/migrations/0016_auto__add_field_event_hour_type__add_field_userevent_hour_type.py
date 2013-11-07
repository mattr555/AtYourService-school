# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.hour_type'
        db.add_column('main_event', 'hour_type',
                      self.gf('django.db.models.fields.CharField')(max_length=3, default='SRV'),
                      keep_default=False)

        # Adding field 'UserEvent.hour_type'
        db.add_column('main_userevent', 'hour_type',
                      self.gf('django.db.models.fields.CharField')(max_length=3, default='SRV'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.hour_type'
        db.delete_column('main_event', 'hour_type')

        # Deleting field 'UserEvent.hour_type'
        db.delete_column('main_userevent', 'hour_type')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.event': {
            'Meta': {'object_name': 'Event'},
            'confirmed_participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'confirmed_events'", 'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hour_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['main.Organization']"}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events_organized'", 'to': "orm['auth.User']"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'main.organization': {
            'Meta': {'object_name': 'Organization'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orgs_admin'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'organizations'", 'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'})
        },
        'main.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leadership_hours': ('django.db.models.fields.IntegerField', [], {}),
            'service_hours': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'related_name': "'settings'", 'to': "orm['sites.Site']"})
        },
        'main.userevent': {
            'Meta': {'object_name': 'UserEvent'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hour_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hours_worked': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_events'", 'to': "orm['auth.User']"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_validation_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'grad_class': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'related_name': "'user_profile'", 'to': "orm['auth.User']"})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']