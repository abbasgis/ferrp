# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-15 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0013_merge_20180815_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='isNetwork',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='info',
            name='app_label',
            field=models.CharField(default='gis', max_length=100, null=True),
        ),
    ]