# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0023_auto_20170320_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLogout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
