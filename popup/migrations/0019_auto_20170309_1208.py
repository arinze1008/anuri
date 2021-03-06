# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0018_auto_20170227_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caller', models.CharField(blank=True, default='', max_length=100)),
                ('called', models.CharField(blank=True, default='', max_length=100)),
                ('state', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='complaint',
            name='respondent',
            field=smart_selects.db_fields.ChainedManyToManyField(chained_field='emergencies', chained_model_field='emergency', to='userprofile.Respondent'),
        ),
    ]
