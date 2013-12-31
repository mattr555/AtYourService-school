# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Demerit'
        db.create_table('main_demerit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='demerits')),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('main', ['Demerit'])

        # Deleting field 'UserProfile.demerits'
        db.delete_column('main_userprofile', 'demerits')


    def backwards(self, orm):
        # Deleting model 'Demerit'
        db.delete_table('main_demerit')

        # Adding field 'UserProfile.demerits'
        db.add_column('main_userprofile', 'demerits',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.demerit': {
            'Meta': {'object_name': 'Demerit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'demerits'"})
        },
        'main.event': {
            'Meta': {'object_name': 'Event'},
            'confirmed_participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'related_name': "'confirmed_events'", 'symmetrical': 'False'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hour_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'}),
            'nhs_approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Organization']", 'related_name': "'events'"}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'events_organized'"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'related_name': "'events'", 'symmetrical': 'False'})
        },
        'main.organization': {
            'Meta': {'object_name': 'Organization'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'orgs_admin'"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'related_name': "'organizations'", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'})
        },
        'main.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'candidate_leadership_hours': ('django.db.models.fields.IntegerField', [], {}),
            'candidate_service_hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_service_hours': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'related_name': "'settings'", 'unique': 'True'})
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
            'nhs_approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'user_events'"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_validation_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'grad_class': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'membership_status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'timezone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'related_name': "'user_profile'", 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'ordering': "('domain',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']