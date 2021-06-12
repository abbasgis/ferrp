# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-27 18:20
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0002_projection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vector',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Raster_Info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('table_name', models.CharField(max_length=200)),
                ('main_table_name', models.CharField(max_length=200)),
                ('res_x', models.DecimalField(decimal_places=6, default=Decimal('0.0000'), max_digits=20)),
                ('res_y', models.DecimalField(decimal_places=6, default=Decimal('0.0000'), max_digits=20)),
                ('num_bands', models.IntegerField(blank=True, null=True)),
                ('pixel_type', models.CharField(blank=True, max_length=30, null=True)),
                ('Info_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='layers.Info')),
            ],
        ),
    ]
