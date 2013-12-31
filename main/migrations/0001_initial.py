# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('main_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orgs_admin', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('geo_lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('main', ['Organization'])

        # Adding M2M table for field members on 'Organization'
        m2m_table_name = db.shorten_name('main_organization_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organization', models.ForeignKey(orm['main.organization'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organization_id', 'user_id'])

        # Adding model 'Event'
        db.create_table('main_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events_organized', to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['main.Organization'])),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('geo_lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hour_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('nhs_approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('main', ['Event'])

        # Adding M2M table for field participants on 'Event'
        m2m_table_name = db.shorten_name('main_event_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['main.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding M2M table for field confirmed_participants on 'Event'
        m2m_table_name = db.shorten_name('main_event_confirmed_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['main.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding model 'UserEvent'
        db.create_table('main_userevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_events', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('geo_lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hours_worked', self.gf('django.db.models.fields.FloatField')()),
            ('hour_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('nhs_approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('main', ['UserEvent'])

        # Adding model 'UserProfile'
        db.create_table('main_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_profile', unique=True, to=orm['auth.User'])),
            ('geo_lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geo_lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('timezone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('email_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_validation_key', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('grad_class', self.gf('django.db.models.fields.IntegerField')()),
            ('membership_status', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('main', ['UserProfile'])

        # Adding model 'SiteSettings'
        db.create_table('main_sitesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(related_name='settings', unique=True, to=orm['sites.Site'])),
            ('candidate_service_hours', self.gf('django.db.models.fields.IntegerField')()),
            ('candidate_leadership_hours', self.gf('django.db.models.fields.IntegerField')()),
            ('member_service_hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['SiteSettings'])

        # Adding model 'Demerit'
        db.create_table('main_demerit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='demerits', to=orm['auth.User'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('main', ['Demerit'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table('main_organization')

        # Removing M2M table for field members on 'Organization'
        db.delete_table(db.shorten_name('main_organization_members'))

        # Deleting model 'Event'
        db.delete_table('main_event')

        # Removing M2M table for field participants on 'Event'
        db.delete_table(db.shorten_name('main_event_participants'))

        # Removing M2M table for field confirmed_participants on 'Event'
        db.delete_table(db.shorten_name('main_event_confirmed_participants'))

        # Deleting model 'UserEvent'
        db.delete_table('main_userevent')

        # Deleting model 'UserProfile'
        db.delete_table('main_userprofile')

        # Deleting model 'SiteSettings'
        db.delete_table('main_sitesettings')

        # Deleting model 'Demerit'
        db.delete_table('main_demerit')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.demerit': {
            'Meta': {'object_name': 'Demerit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'demerits'", 'to': "orm['auth.User']"})
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
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'}),
            'nhs_approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'})
        },
        'main.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'candidate_leadership_hours': ('django.db.models.fields.IntegerField', [], {}),
            'candidate_service_hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_service_hours': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': "orm['sites.Site']"})
        },
        'main.userevent': {
            'Meta': {'object_name': 'UserEvent'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_events'", 'to': "orm['auth.User']"})
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']