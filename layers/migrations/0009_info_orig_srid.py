# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-05 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0008_info_app_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='orig_srid',
            field=models.IntegerField(null=True),
        ),
    ]
