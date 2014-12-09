# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userevent',
            name='advisor_approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userevent',
            name='advisor_email',
            field=models.CharField(default='test@example.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userevent',
            name='advisor_name',
            field=models.CharField(blank=True, max_length=100, default='Joe Cool'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userevent',
            name='email_verification_key',
            field=models.CharField(blank=True, max_length=50, default='abcdefg'),
            preserve_default=False,
        ),
    ]
