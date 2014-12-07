# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Demerit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('reason', models.CharField(max_length=1000)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='demerits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=300)),
                ('description', models.TextField()),
                ('date_start', models.DateTimeField(db_index=True)),
                ('date_end', models.DateTimeField(db_index=True)),
                ('location', models.CharField(max_length=100)),
                ('geo_lat', models.FloatField(blank=True, null=True)),
                ('geo_lon', models.FloatField(blank=True, null=True)),
                ('hour_type', models.CharField(choices=[('SRV', 'Service'), ('LED', 'Leadership')], max_length=3)),
                ('nhs_approved', models.BooleanField(default=True)),
                ('confirmed_participants', models.ManyToManyField(related_name='confirmed_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=300)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('geo_lat', models.FloatField(blank=True, null=True)),
                ('geo_lon', models.FloatField(blank=True, null=True)),
                ('admin', models.ForeignKey(related_name='orgs_admin', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('candidate_service_hours', models.IntegerField()),
                ('candidate_leadership_hours', models.IntegerField()),
                ('member_service_hours', models.IntegerField()),
                ('site', models.OneToOneField(to='sites.Site', related_name='settings')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('organization', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField(db_index=True, blank=True, null=True)),
                ('location', models.CharField(max_length=100)),
                ('geo_lat', models.FloatField(blank=True, null=True)),
                ('geo_lon', models.FloatField(blank=True, null=True)),
                ('hours_worked', models.FloatField(verbose_name='hours worked')),
                ('hour_type', models.CharField(choices=[('SRV', 'Service'), ('LED', 'Leadership')], max_length=3)),
                ('nhs_approved', models.BooleanField(default=True)),
                ('user', models.ForeignKey(related_name='user_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('geo_lat', models.FloatField(blank=True, null=True)),
                ('geo_lon', models.FloatField(blank=True, null=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('timezone', models.CharField(max_length=100, blank=True)),
                ('email_valid', models.BooleanField(default=False)),
                ('email_validation_key', models.CharField(max_length=50, blank=True)),
                ('grad_class', models.IntegerField()),
                ('membership_status', models.CharField(choices=[('CAN', 'Candidate'), ('MEM', 'Member')], max_length=3)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(related_name='events', to='main.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(related_name='events_organized', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
