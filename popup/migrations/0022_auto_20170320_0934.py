# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0021_auto_20170320_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentbreak',
            name='time_spent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
