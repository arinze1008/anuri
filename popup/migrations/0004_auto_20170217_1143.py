# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-17 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0003_auto_20170217_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='street',
            field=models.TextField(blank=True, null=True, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='case',
            name='street_auto',
            field=models.TextField(blank=True, null=True, verbose_name='Street'),
        ),
    ]
