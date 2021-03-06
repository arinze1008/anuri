# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-27 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0017_auto_20170223_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone Number')),
            ],
            options={
                'verbose_name_plural': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='LocationContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com', to='popup.Community')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='popup.Contact')),
            ],
        ),
        migrations.RemoveField(
            model_name='respondent',
            name='emergency',
        ),
        migrations.AlterField(
            model_name='case',
            name='emergencies',
            field=models.ManyToManyField(to='userprofile.Emergency'),
        ),
        migrations.AlterField(
            model_name='case',
            name='respondent',
            field=smart_selects.db_fields.ChainedManyToManyField(blank=True, chained_field='emergencies', chained_model_field='emergency', to='userprofile.Respondent'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='emergencies',
            field=models.ManyToManyField(to='userprofile.Emergency'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='respondent',
            field=smart_selects.db_fields.ChainedManyToManyField(blank=True, chained_field='emergencies', chained_model_field='emergency', to='userprofile.Respondent'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state', to='popup.State'),
        ),
        migrations.DeleteModel(
            name='Emergency',
        ),
        migrations.DeleteModel(
            name='Respondent',
        ),
    ]
