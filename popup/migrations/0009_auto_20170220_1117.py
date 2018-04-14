# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-20 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0008_account_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='popup.State'),
        ),
    ]
