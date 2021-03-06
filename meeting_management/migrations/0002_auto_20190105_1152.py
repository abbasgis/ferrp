# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-05 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblMeetingsUsersEvents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('meeting_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('calendar_event_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'tbl_meetings_users_calendarevents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUsersToSync',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calendar_link', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'tbl_users_to_sync_calendar',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='tblcalendersync',
            options={'managed': True},
        ),
    ]
