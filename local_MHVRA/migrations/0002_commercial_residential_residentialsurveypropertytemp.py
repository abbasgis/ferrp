# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-18 19:05
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('local_MHVRA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commercial',
            fields=[
                ('survey_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('respondent_name', models.CharField(blank=True, max_length=500, null=True)),
                ('respondent_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('respondant_cnic', models.CharField(blank=True, max_length=500, null=True)),
                ('respondent_phone_no', models.CharField(blank=True, max_length=500, null=True)),
                ('age_of_building', models.CharField(blank=True, max_length=500, null=True)),
                ('plinth_level_of_building', models.CharField(blank=True, max_length=500, null=True)),
                ('security_guard', models.CharField(blank=True, max_length=500, null=True)),
                ('emergency_exit', models.CharField(blank=True, max_length=500, null=True)),
                ('evacuation_plan', models.CharField(blank=True, max_length=500, null=True)),
                ('does_this_building_submerge_during_flood', models.CharField(blank=True, max_length=500, null=True)),
                ('type_of_business', models.CharField(blank=True, max_length=500, null=True)),
                ('name_of_business', models.CharField(blank=True, max_length=500, null=True)),
                ('number_of_employees', models.CharField(blank=True, max_length=500, null=True)),
                ('application_version', models.CharField(blank=True, max_length=500, null=True)),
                ('form_number', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'commercial',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Residential',
            fields=[
                ('survey_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('respondent_name', models.CharField(blank=True, max_length=255, null=True)),
                ('respondent_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('respondant_cnic', models.CharField(blank=True, max_length=32, null=True)),
                ('respondent_cinic_availability_date', models.CharField(blank=True, max_length=255, null=True)),
                ('respondant_contact', models.CharField(blank=True, max_length=32, null=True)),
                ('respondent_education', models.CharField(blank=True, max_length=255, null=True)),
                ('family_type', models.CharField(blank=True, max_length=255, null=True)),
                ('respondent_relation', models.CharField(blank=True, max_length=255, null=True)),
                ('family_cast', models.CharField(blank=True, max_length=255, null=True)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('monthly_income', models.CharField(blank=True, max_length=32, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=32, null=True)),
                ('hoh_name', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_contact', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_cnic', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_cinic_availability_date', models.CharField(blank=True, max_length=255, null=True)),
                ('current_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('avg_electricity_bill_rs', models.CharField(blank=True, max_length=32, null=True)),
                ('no_of_stories', models.CharField(blank=True, max_length=32, null=True)),
                ('no_of_pakka_rooms', models.CharField(blank=True, max_length=32, null=True)),
                ('no_of_kacha_rooms', models.CharField(blank=True, max_length=32, null=True)),
                ('plinth_level_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('building_age_yr', models.CharField(blank=True, max_length=32, null=True)),
                ('building_area_marla', models.CharField(blank=True, max_length=32, null=True)),
                ('construction_type', models.CharField(blank=True, max_length=255, null=True)),
                ('connected_infrastructure', models.CharField(blank=True, max_length=255, null=True)),
                ('damage_in_last_disaster', models.CharField(blank=True, max_length=255, null=True)),
                ('source_of_foreign_remittance', models.CharField(blank=True, max_length=255, null=True)),
                ('first_aid', models.CharField(blank=True, max_length=255, null=True)),
                ('civil_defence', models.CharField(blank=True, max_length=255, null=True)),
                ('rescue', models.CharField(blank=True, max_length=255, null=True)),
                ('disaster_management', models.CharField(blank=True, max_length=255, null=True)),
                ('is_property_restored', models.CharField(blank=True, max_length=255, null=True)),
                ('other_training', models.CharField(blank=True, max_length=255, null=True)),
                ('swimmers', models.CharField(blank=True, max_length=255, null=True)),
                ('medical_accessibility', models.CharField(blank=True, max_length=255, null=True)),
                ('year_of_disaster', models.CharField(blank=True, max_length=255, null=True)),
                ('mode_of_information', models.CharField(blank=True, max_length=255, null=True)),
                ('media_awareness_help', models.CharField(blank=True, max_length=255, null=True)),
                ('source_of_water_supply', models.CharField(blank=True, max_length=255, null=True)),
                ('experienced_last_natural_disaster', models.CharField(blank=True, max_length=255, null=True)),
                ('time_to_restore_months', models.CharField(blank=True, max_length=32, null=True)),
                ('drinkable_water_depth_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('drinkable_water_distance_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('sewerage', models.CharField(blank=True, max_length=255, null=True)),
                ('type_of_crops', models.CharField(blank=True, max_length=255, null=True)),
                ('no_of_crops', models.CharField(blank=True, max_length=32, null=True)),
                ('total_gricultural_land', models.CharField(blank=True, max_length=32, null=True)),
                ('agricultural_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('owner_total_cultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('owner_total_cultivated_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('tenant_total_cultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('tenant_cultivated_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('any_uncultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('area_of_uncultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('uncultivated_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('reason_of_uncultivated_land', models.CharField(blank=True, max_length=255, null=True)),
                ('application_version', models.CharField(blank=True, max_length=255, null=True)),
                ('form_number', models.CharField(blank=True, max_length=255, null=True)),
                ('male', models.CharField(blank=True, max_length=32, null=True)),
                ('female', models.CharField(blank=True, max_length=32, null=True)),
                ('total_persons', models.CharField(blank=True, max_length=32, null=True)),
                ('source_of_income', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000, null=True), size=25)),
                ('govt_compensation', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000, null=True), size=25)),
                ('relief_from_ngo_ingo', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000, null=True), size=25)),
                ('relief_you_seek', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000, null=True), size=25)),
                ('transport', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000, null=True), size=25)),
                ('last_epidemic_diseases', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000, null=True), size=25)),
                ('age_group', django.contrib.postgres.fields.jsonb.JSONField()),
                ('education_group', django.contrib.postgres.fields.jsonb.JSONField()),
                ('disability_group', django.contrib.postgres.fields.jsonb.JSONField()),
                ('living_facilities', django.contrib.postgres.fields.jsonb.JSONField()),
                ('livestock', django.contrib.postgres.fields.jsonb.JSONField()),
                ('source_of_income_count', models.IntegerField(blank=True, null=True)),
                ('govt_compensation_count', models.IntegerField(blank=True, null=True)),
                ('relief_from_ngo_ingo_count', models.IntegerField(blank=True, null=True)),
                ('transport_count', models.IntegerField(blank=True, null=True)),
                ('relief_you_seek_count', models.IntegerField(blank=True, null=True)),
                ('last_epidemic_diseases_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'residential',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResidentialSurveyPropertyTemp',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('respondent_name', models.CharField(blank=True, max_length=255, null=True)),
                ('respondent_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('respondant_cnic', models.CharField(blank=True, max_length=32, null=True)),
                ('respondent_cinic_availability_date', models.CharField(blank=True, max_length=255, null=True)),
                ('respondant_contact', models.CharField(blank=True, max_length=32, null=True)),
                ('respondent_education', models.CharField(blank=True, max_length=255, null=True)),
                ('family_type', models.CharField(blank=True, max_length=255, null=True)),
                ('respondent_relation', models.CharField(blank=True, max_length=255, null=True)),
                ('family_cast', models.CharField(blank=True, max_length=255, null=True)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('monthly_income', models.CharField(blank=True, max_length=32, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=32, null=True)),
                ('hoh_name', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_contact', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_cnic', models.CharField(blank=True, max_length=255, null=True)),
                ('hoh_cinic_availability_date', models.CharField(blank=True, max_length=255, null=True)),
                ('current_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('avg_electricity_bill_rs', models.CharField(blank=True, max_length=32, null=True)),
                ('no_of_stories', models.CharField(blank=True, max_length=32, null=True)),
                ('no_of_pakka_rooms', models.CharField(blank=True, max_length=32, null=True)),
                ('no_of_kacha_rooms', models.CharField(blank=True, max_length=32, null=True)),
                ('plinth_level_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('building_age_yr', models.CharField(blank=True, max_length=32, null=True)),
                ('building_area_marla', models.CharField(blank=True, max_length=32, null=True)),
                ('construction_type', models.CharField(blank=True, max_length=255, null=True)),
                ('connected_infrastructure', models.CharField(blank=True, max_length=255, null=True)),
                ('damage_in_last_disaster', models.CharField(blank=True, max_length=255, null=True)),
                ('source_of_foreign_remittance', models.CharField(blank=True, max_length=255, null=True)),
                ('first_aid', models.CharField(blank=True, max_length=255, null=True)),
                ('civil_defence', models.CharField(blank=True, max_length=255, null=True)),
                ('rescue', models.CharField(blank=True, max_length=255, null=True)),
                ('disaster_management', models.CharField(blank=True, max_length=255, null=True)),
                ('is_property_restored', models.CharField(blank=True, max_length=255, null=True)),
                ('other_training', models.CharField(blank=True, max_length=255, null=True)),
                ('swimmers', models.CharField(blank=True, max_length=255, null=True)),
                ('medical_accessibility', models.CharField(blank=True, max_length=255, null=True)),
                ('year_of_disaster', models.CharField(blank=True, max_length=255, null=True)),
                ('mode_of_information', models.CharField(blank=True, max_length=255, null=True)),
                ('media_awareness_help', models.CharField(blank=True, max_length=255, null=True)),
                ('source_of_water_supply', models.CharField(blank=True, max_length=255, null=True)),
                ('experienced_last_natural_disaster', models.CharField(blank=True, max_length=255, null=True)),
                ('time_to_restore_months', models.CharField(blank=True, max_length=32, null=True)),
                ('drinkable_water_depth_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('drinkable_water_distance_ft', models.CharField(blank=True, max_length=32, null=True)),
                ('sewerage', models.CharField(blank=True, max_length=255, null=True)),
                ('type_of_crops', models.CharField(blank=True, max_length=255, null=True)),
                ('no_of_crops', models.CharField(blank=True, max_length=32, null=True)),
                ('total_gricultural_land', models.CharField(blank=True, max_length=32, null=True)),
                ('agricultural_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('owner_total_cultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('owner_total_cultivated_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('tenant_total_cultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('tenant_cultivated_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('any_uncultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('area_of_uncultivated_land', models.CharField(blank=True, max_length=32, null=True)),
                ('uncultivated_land_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('reason_of_uncultivated_land', models.CharField(blank=True, max_length=255, null=True)),
                ('application_version', models.CharField(blank=True, max_length=255, null=True)),
                ('form_number', models.CharField(blank=True, max_length=255, null=True)),
                ('male', models.CharField(blank=True, max_length=32, null=True)),
                ('female', models.CharField(blank=True, max_length=32, null=True)),
                ('total_persons', models.CharField(blank=True, max_length=32, null=True)),
                ('survey_id', models.TextField(blank=True, null=True)),
                ('age_group', models.TextField(blank=True, null=True)),
                ('education_group', models.TextField(blank=True, null=True)),
                ('disability_group', models.TextField(blank=True, null=True)),
                ('living_facilities', models.TextField(blank=True, null=True)),
                ('livestock', models.TextField(blank=True, null=True)),
                ('source_of_income_count', models.IntegerField(blank=True, null=True)),
                ('govt_compensation_count', models.IntegerField(blank=True, null=True)),
                ('relief_from_ngo_ingo_count', models.IntegerField(blank=True, null=True)),
                ('transport_count', models.IntegerField(blank=True, null=True)),
                ('relief_you_seek_count', models.IntegerField(blank=True, null=True)),
                ('last_epidemic_diseases_count', models.IntegerField(blank=True, null=True)),
                ('govt_compensation', models.TextField(blank=True, null=True)),
                ('relief_from_ngo_ingo', models.TextField(blank=True, null=True)),
                ('relief_you_seek', models.TextField(blank=True, null=True)),
                ('last_epidemic_diseases', models.TextField(blank=True, null=True)),
                ('transport', models.TextField(blank=True, null=True)),
                ('source_of_income', models.TextField(blank=True, null=True)),
                ('upload_datetime', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('mauza_id', models.IntegerField(blank=True, null=True)),
                ('mauza_name', models.CharField(blank=True, max_length=500, null=True)),
                ('patwar_circle_name', models.CharField(blank=True, max_length=500, null=True)),
                ('qanungoi_halqa_name', models.CharField(blank=True, max_length=500, null=True)),
                ('tehsil_name', models.CharField(blank=True, max_length=500, null=True)),
                ('district_name', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'residential_survey_property_temp',
                'managed': False,
            },
        ),
    ]