# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-22 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseEngines',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'database_engines',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TablesList',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('table_name', models.TextField(blank=True, null=True)),
                ('is_spatial', models.NullBooleanField()),
            ],
            options={
                'db_table': 'tables_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ConnectionsList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('connection_name', models.TextField(blank=True, null=True, unique=True)),
                ('database_host', models.TextField(blank=True, null=True)),
                ('database_name', models.TextField(blank=True, null=True)),
                ('database_user', models.TextField(blank=True, null=True)),
                ('database_password', models.TextField(blank=True, null=True)),
                ('database_port', models.TextField(blank=True, null=True)),
                ('engine_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'connections_list',
                'managed': True,
            },
        ),
    ]
