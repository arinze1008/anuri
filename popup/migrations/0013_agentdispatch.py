# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-21 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0012_auto_20170221_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentDispatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('incidence', models.CharField(blank=True, max_length=255, null=True, verbose_name='incidence')),
                ('respondent', models.CharField(blank=True, max_length=255, null=True, verbose_name='respondent')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='location')),
                ('community', models.CharField(blank=True, max_length=255, null=True, verbose_name='community')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='status')),
                ('dispatch_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('entered_out', models.DateTimeField(auto_now_add=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('condition', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
            ],
        ),
    ]
