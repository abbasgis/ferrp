# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-10 18:47
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basin',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('basin_name', models.CharField(max_length=500)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Drainage_Basin',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('drainage_basin_name', models.CharField(max_length=500)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rivers',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('river_name', models.CharField(max_length=500)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Social_User_Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
                ('account_heading', models.CharField(max_length=500)),
                ('email_id', models.CharField(max_length=500)),
                ('phone_no', models.CharField(max_length=500)),
                ('account_type', models.CharField(max_length=500)),
                ('map_url', models.CharField(max_length=500)),
                ('id_from_account', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rivers_Drainage_Basin',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('drainage_basin_name', models.CharField(max_length=500)),
                ('geographic_area', models.FloatField(blank=True, null=True)),
                ('documented_area', models.FloatField(blank=True, null=True)),
                ('river_oid', models.IntegerField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
