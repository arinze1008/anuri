# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-23 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0016_auto_20170223_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentdispatch',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='community2', to='popup.Community'),
        ),
    ]
