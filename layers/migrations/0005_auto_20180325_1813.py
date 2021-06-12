# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-25 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0004_info_main_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='permission_type',
            field=models.CharField(choices=[('V', 'View'), ('D', 'Download'), ('S', 'Save')], max_length=25),
        ),
    ]
