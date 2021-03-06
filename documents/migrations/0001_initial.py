# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-17 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doc_Info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=500)),
                ('file_extension', models.CharField(default='pdf', max_length=100)),
                ('upload_date', models.DateField()),
                ('upload_time', models.TimeField()),
                ('icon', models.CharField(max_length=500, null=True)),
                ('created_by', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
