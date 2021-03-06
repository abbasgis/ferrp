# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-02 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblWlDetail',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, db_column='year', null=True)),
                ('season', models.CharField(blank=True, db_column='season', max_length=25, null=True)),
                ('water_depth', models.CharField(blank=True, db_column='water_depth', max_length=25, null=True)),
                ('elevation', models.CharField(blank=True, db_column='elevation', max_length=25, null=True)),
                ('ql_id', models.IntegerField(blank=True, db_column='ql_id', null=True)),
                ('geom_text', models.CharField(blank=True, db_column='geom_xy', max_length=50, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'gis_water_level_detail',
            },
        ),
        migrations.CreateModel(
            name='TblWqDetail',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, db_column='year', null=True)),
                ('season', models.CharField(blank=True, db_column='season', max_length=25, null=True)),
                ('quality_type', models.CharField(blank=True, db_column='quality_type', max_length=25, null=True)),
                ('water_quality', models.CharField(blank=True, db_column='water_quality', max_length=25, null=True)),
                ('elevation', models.CharField(blank=True, db_column='elevation', max_length=25, null=True)),
                ('ql_id', models.IntegerField(blank=True, db_column='ql_id', null=True)),
                ('geom_text', models.CharField(blank=True, db_column='geom_xy', max_length=50, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'gis_water_quality_detail',
            },
        ),
        migrations.CreateModel(
            name='TblWqWlCombinedData',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('sr_no', models.CharField(blank=True, db_column='sr_no', max_length=254, null=True)),
                ('gis_no', models.CharField(blank=True, db_column='gis_no', max_length=254, null=True)),
                ('y_axis', models.DecimalField(blank=True, db_column='y', decimal_places=2, max_digits=25, null=True)),
                ('x_axis', models.DecimalField(blank=True, db_column='x', decimal_places=2, max_digits=25, null=True)),
                ('major_canal', models.CharField(blank=True, db_column='major_canal', max_length=254, null=True)),
                ('disty_minor', models.CharField(blank=True, db_column='disty_minor', max_length=254, null=True)),
                ('circle', models.CharField(blank=True, db_column='circle', max_length=254, null=True)),
                ('division', models.CharField(blank=True, db_column='division', max_length=254, null=True)),
                ('zone', models.CharField(blank=True, db_column='zone', max_length=254, null=True)),
                ('reclamation', models.CharField(blank=True, db_column='reclamation', max_length=254, null=True)),
                ('district', models.CharField(blank=True, db_column='district', max_length=254, null=True)),
                ('tehsil', models.CharField(blank=True, db_column='tehsil', max_length=254, null=True)),
                ('elevation', models.CharField(blank=True, db_column='elevation', max_length=254, null=True)),
                ('type_wl_wq', models.CharField(blank=True, db_column='type_wl_wq', max_length=254, null=True)),
                ('extent', models.CharField(blank=True, db_column='extent', max_length=254, null=True)),
                ('geojson', models.CharField(blank=True, db_column='geojson', max_length=254, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'gis_wq_wl',
            },
        ),
    ]
