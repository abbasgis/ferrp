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
            name='AdpDistrict',
            fields=[
                ('name', models.CharField(blank=True, max_length=5000, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'adp_district',
            },
        ),
        migrations.CreateModel(
            name='AdpReport201718',
            fields=[
                ('GS_No', models.CharField(blank=True, db_column='GS_No', max_length=255, null=True)),
                ('Name_of_Scheme', models.CharField(blank=True, db_column='Name_of_Scheme', max_length=500, null=True)),
                ('District', models.CharField(blank=True, db_column='District', max_length=500, null=True)),
                ('Type', models.CharField(blank=True, db_column='Type', max_length=255, null=True)),
                ('Sector', models.CharField(blank=True, db_column='Sector', max_length=255, null=True)),
                ('Approval_Date', models.CharField(blank=True, db_column='Approval_Date', max_length=255, null=True)),
                ('Total_Cost', models.FloatField(blank=True, db_column='Total Cost', null=True)),
                ('Foreign_Aid', models.FloatField(blank=True, db_column='Foreign_Aid', null=True)),
                ('LocalCapital', models.FloatField(blank=True, db_column='LocalCapital', null=True)),
                ('LocalRevenue', models.FloatField(blank=True, db_column='LocalRevenue', null=True)),
                ('TotalCapital', models.FloatField(blank=True, db_column='TotalCapital', null=True)),
                ('TotalRevenue', models.FloatField(blank=True, db_column='TotalRevenue', null=True)),
                ('ForeignCapital', models.FloatField(blank=True, db_column='ForeignCapital', null=True)),
                ('ForeignRevenue', models.FloatField(blank=True, db_column='ForeignRevenue', null=True)),
                ('Allocation', models.FloatField(blank=True, db_column='Allocation', null=True)),
                ('Exp_upto_June', models.FloatField(blank=True, db_column='Exp_upto_June', null=True)),
                ('Projection_2017_18', models.FloatField(blank=True, db_column='Projection_2017-18', null=True)),
                ('Projection_2018_19', models.FloatField(blank=True, db_column='Projection_2018-19', null=True)),
                ('Throw_Forward', models.FloatField(blank=True, db_column='Throw_Forward', null=True)),
                ('Id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'adp_report_201718',
            },
        ),
        migrations.CreateModel(
            name='AdpSchemes1018Mpr',
            fields=[
                ('Id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('Scheme_Name', models.CharField(blank=True, db_column='Scheme Name', max_length=2500, null=True)),
                ('Year', models.TextField(blank=True, db_column='Year', null=True)),
                ('GS_No', models.IntegerField(blank=True, db_column='GS No', null=True)),
                ('District', models.CharField(blank=True, db_column='District', max_length=5000, null=True)),
                ('Sector', models.CharField(blank=True, db_column='Sector', max_length=255, null=True)),
                ('Main_Sector', models.CharField(blank=True, db_column='Main Sector', max_length=255, null=True)),
                ('Type', models.CharField(blank=True, db_column='Type', max_length=255, null=True)),
                ('Approval', models.TextField(blank=True, db_column='Approval', null=True)),
                ('Local_Capital', models.DecimalField(blank=True, db_column='Local Capital', decimal_places=2, max_digits=250, null=True)),
                ('Local_Revenue', models.DecimalField(blank=True, db_column='Local Revenue', decimal_places=2, max_digits=250, null=True)),
                ('Total_Capital', models.DecimalField(blank=True, db_column='Total Capital', decimal_places=2, max_digits=250, null=True)),
                ('Total_Revenue', models.DecimalField(blank=True, db_column='Total Revenue', decimal_places=2, max_digits=250, null=True)),
                ('Foreign_Aid_Capital', models.DecimalField(blank=True, db_column='Foreign Aid Capital', decimal_places=2, max_digits=250, null=True)),
                ('Foreign_Aid_Revenue', models.DecimalField(blank=True, db_column='Foreign Aid Revenue', decimal_places=2, max_digits=250, null=True)),
                ('Foreign_Aid_Total', models.DecimalField(blank=True, db_column='Foreign Aid Total', decimal_places=2, max_digits=250, null=True)),
                ('Total_Cost', models.DecimalField(blank=True, db_column='Total Cost', decimal_places=2, max_digits=250, null=True)),
                ('Allocation', models.DecimalField(blank=True, db_column='Allocation', decimal_places=2, max_digits=250, null=True)),
                ('Release', models.DecimalField(blank=True, db_column='Release', decimal_places=2, max_digits=250, null=True)),
                ('Utilization', models.DecimalField(blank=True, db_column='Utilization', decimal_places=2, max_digits=250, null=True)),
                ('Expense_Upto_June', models.DecimalField(blank=True, db_column='Expense Upto June', decimal_places=2, max_digits=250, null=True)),
                ('Projection_One', models.DecimalField(blank=True, db_column='Projection One', decimal_places=2, max_digits=250, null=True)),
                ('Projection_Two', models.DecimalField(blank=True, db_column='Projection Two', decimal_places=2, max_digits=250, null=True)),
                ('Throw_Forward', models.DecimalField(blank=True, db_column='Throw Forward', decimal_places=2, max_digits=250, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'adp_schemes_10_18_mpr',
            },
        ),
        migrations.CreateModel(
            name='AdpYearlyFacts1018',
            fields=[
                ('Year', models.TextField(blank=True, db_column='Year', null=True)),
                ('District', models.CharField(blank=True, db_column='District', max_length=5000, null=True)),
                ('Sector', models.CharField(blank=True, db_column='Sector', max_length=255, null=True)),
                ('Main_Sector', models.CharField(blank=True, db_column='Main Sector', max_length=255, null=True)),
                ('Type', models.CharField(blank=True, db_column='Type', max_length=255, null=True)),
                ('Approval', models.TextField(blank=True, db_column='Approval', null=True)),
                ('Schemes_Count', models.BigIntegerField(blank=True, db_column='Schemes Count', null=True)),
                ('Local_Capital', models.FloatField(blank=True, db_column='Local Capital', null=True)),
                ('Local_Revenue', models.FloatField(blank=True, db_column='Local Revenue', null=True)),
                ('Total_Capital', models.FloatField(blank=True, db_column='Total Capital', null=True)),
                ('Total_Revenue', models.FloatField(blank=True, db_column='Total Revenue', null=True)),
                ('Foreign_Aid_Capital', models.FloatField(blank=True, db_column='Foreign Aid Capital', null=True)),
                ('Foreign_Aid_Revenue', models.FloatField(blank=True, db_column='Foreign Aid Revenue', null=True)),
                ('Foreign_Aid_Total', models.FloatField(blank=True, db_column='Foreign Aid Total', null=True)),
                ('Total_Cost', models.FloatField(blank=True, db_column='Total Cost', null=True)),
                ('Allocation', models.FloatField(blank=True, db_column='Allocation', null=True)),
                ('Expense_Upto_June', models.FloatField(blank=True, db_column='Expense Upto June', null=True)),
                ('Projection_One', models.FloatField(blank=True, db_column='Projection One', null=True)),
                ('Projection_Two', models.FloatField(blank=True, db_column='Projection Two', null=True)),
                ('Throw_Forward', models.FloatField(blank=True, db_column='Throw Forward', null=True)),
                ('Id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
                'db_table': 'adp_yearly_facts_1018',
            },
        ),
    ]
