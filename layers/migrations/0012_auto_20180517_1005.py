# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-17 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0011_auto_20180426_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='icon',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
