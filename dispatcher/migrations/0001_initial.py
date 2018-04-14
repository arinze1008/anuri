# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-01 15:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respondent_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='respondent name')),
                ('respondent_phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='respondent phone')),
                ('respondent_location', models.CharField(blank=True, max_length=255, null=True, verbose_name='respondent location')),
                ('ticket_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ticket Id')),
                ('officer_reachout_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('entered_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('note', models.TextField()),
                ('last_note', models.TextField(blank=True, null=True)),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatch_agency', to='userprofile.Agency')),
            ],
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Reason',
            },
        ),
        migrations.CreateModel(
            name='Resolved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Resolution',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.AddField(
            model_name='dispatch',
            name='reason',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reason', to='dispatcher.Reason'),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='resolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resolves', to='dispatcher.Resolved'),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='dispatcher.Status'),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatchuser', to=settings.AUTH_USER_MODEL),
        ),
    ]