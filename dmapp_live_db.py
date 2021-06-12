# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ActivityMap(models.Model):
    activity_map_id = models.AutoField(primary_key=True)
    survey_type = models.ForeignKey('SurveyType', models.DO_NOTHING, blank=True, null=True)
    property = models.ForeignKey('Property', models.DO_NOTHING, blank=True, null=True)
    property_type = models.ForeignKey('PropertyType', models.DO_NOTHING, blank=True, null=True)
    show = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    group_number = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_map'


class AgeGroup(models.Model):
    age_group_id = models.AutoField(primary_key=True)
    age_group_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'age_group'


class AppUser(models.Model):
    app_user_id = models.AutoField()
    role_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=12, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    is_locked = models.IntegerField(blank=True, null=True)
    is_expired = models.IntegerField(blank=True, null=True)
    password_expiry_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_user'


class BoundaryWall(models.Model):
    boundary_wall_id = models.AutoField(primary_key=True)
    boundary_wall_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boundary_wall'


class BridgeType(models.Model):
    bridge_type_id = models.AutoField(primary_key=True)
    bridge_type_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bridge_type'


class BuildingInformation(models.Model):
    building_information_id = models.AutoField(primary_key=True)
    building_information_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_information'


class BuildingOwnership(models.Model):
    building_ownership_id = models.AutoField(primary_key=True)
    building_ownership_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_ownership'


class BuildingSituated(models.Model):
    building_situated_id = models.IntegerField(primary_key=True)
    building_situated_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_situated'


class BuildingType(models.Model):
    building_type_id = models.IntegerField(primary_key=True)
    building_type_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_type'


class ConnectedInfrastructure(models.Model):
    connected_infrastructure_id = models.AutoField(primary_key=True)
    connected_infrastructure_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'connected_infrastructure'


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country'


class DamageLevel(models.Model):
    damage_level_id = models.IntegerField(primary_key=True)
    damage_level_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'damage_level'


class DisasterDamage(models.Model):
    disaster_damage_id = models.AutoField(primary_key=True)
    disaster_damage_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disaster_damage'


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    estimated_population = models.IntegerField(blank=True, null=True)
    estimated_surveys = models.IntegerField(blank=True, null=True)
    surveyors = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    phase = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district'


class DistrictGroupsPercentageTab(models.Model):
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    property_type_id = models.IntegerField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True)
    group_option = models.TextField(blank=True, null=True)
    male = models.BigIntegerField(blank=True, null=True)
    male_pecentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    female = models.BigIntegerField(blank=True, null=True)
    female_pecentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transgender = models.BigIntegerField(blank=True, null=True)
    trans_pecentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_groups_percentage_tab'


class DistrictHierarchy(models.Model):
    mauza_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    tehsil_name = models.CharField(max_length=-1, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=-1, blank=True, null=True)
    mauza_name = models.CharField(max_length=-1, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_hierarchy'


class DistrictStatsTab(models.Model):
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    mauzas = models.BigIntegerField(blank=True, null=True)
    patwar_circles = models.BigIntegerField(blank=True, null=True)
    qanungoi_halqas = models.BigIntegerField(blank=True, null=True)
    tehsils = models.BigIntegerField(blank=True, null=True)
    educational_institutes = models.BigIntegerField(blank=True, null=True)
    health_facilities = models.BigIntegerField(blank=True, null=True)
    total_surveys = models.BigIntegerField(blank=True, null=True)
    male = models.BigIntegerField(blank=True, null=True)
    female = models.BigIntegerField(blank=True, null=True)
    transgender = models.BigIntegerField(blank=True, null=True)
    estimated_population = models.IntegerField(blank=True, null=True)
    estimated_surveys = models.IntegerField(blank=True, null=True)
    surveyors = models.IntegerField(blank=True, null=True)
    checked_surveys = models.BigIntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    psds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_stats_tab'


class DistrictStatsView(models.Model):
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    mauzas = models.BigIntegerField(blank=True, null=True)
    patwar_circles = models.BigIntegerField(blank=True, null=True)
    qanungoi_halqas = models.BigIntegerField(blank=True, null=True)
    tehsils = models.BigIntegerField(blank=True, null=True)
    educational_institutes = models.BigIntegerField(blank=True, null=True)
    health_facilities = models.BigIntegerField(blank=True, null=True)
    total_surveys = models.BigIntegerField(blank=True, null=True)
    male = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    female = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    transgender = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    estimated_population = models.IntegerField(blank=True, null=True)
    estimated_surveys = models.IntegerField(blank=True, null=True)
    surveyors = models.IntegerField(blank=True, null=True)
    checked_surveys = models.BigIntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    psds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_stats_view'


class DistrictTemp(models.Model):
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    estimated_population = models.IntegerField(blank=True, null=True)
    estimated_surveys = models.IntegerField(blank=True, null=True)
    surveyors = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_temp'


class Districtall(models.Model):
    mauza_id = models.AutoField()
    mauza_name = models.CharField(max_length=-1)
    hadbast_no = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle_id = models.AutoField()
    patwar_circle_name = models.CharField(max_length=-1)
    qanungoi_halqa_id = models.AutoField()
    qanungoi_halqa_name = models.CharField(max_length=-1)
    tehsil_id = models.AutoField()
    tehsil_name = models.CharField(max_length=-1)
    district_id = models.AutoField()
    district_name = models.CharField(max_length=-1)
    phase = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'districtall'


class EduBuildingStatsTab(models.Model):
    edu_building_stats_tab_id = models.AutoField(primary_key=True)
    survey_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    type_of_construction = models.CharField(max_length=-1, blank=True, null=True)
    institute_level = models.CharField(max_length=-1, blank=True, null=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    survey_type_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edu_building_stats_tab'


class EducationLevel(models.Model):
    education_level_id = models.AutoField(primary_key=True)
    education_level_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education_level'


class EmergencyTrainingDepartment(models.Model):
    emergency_training_department_id = models.AutoField(primary_key=True)
    emergency_training_department_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emergency_training_department'


class EmergencyTrainingType(models.Model):
    emergency_training_type_id = models.AutoField(primary_key=True)
    emergency_training_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emergency_training_type'


class EpidemicDisease(models.Model):
    epidemic_disease_id = models.AutoField(primary_key=True)
    epidemic_disease_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epidemic_disease'


class FamilyCast(models.Model):
    family_cast_id = models.AutoField(primary_key=True)
    family_cast_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'family_cast'


class FinancialCalcDetail(models.Model):
    financial_calc_detail_id = models.AutoField(primary_key=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    financial_calc_parameter_id = models.IntegerField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financial_calc_detail'


class FinancialCalcParameter(models.Model):
    financial_calc_parameter_id = models.IntegerField(primary_key=True)
    parameter_type = models.CharField(max_length=-1, blank=True, null=True)
    survey_type = models.ForeignKey('SurveyType', models.DO_NOTHING, blank=True, null=True)
    parameter_name = models.CharField(max_length=-1, blank=True, null=True)
    param_property_id = models.IntegerField(blank=True, null=True)
    sub_parameter_name = models.CharField(max_length=-1, blank=True, null=True)
    sub_param_property_id = models.IntegerField(blank=True, null=True)
    base_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aggregation = models.CharField(max_length=-1, blank=True, null=True)
    value_field = models.CharField(max_length=-1, blank=True, null=True)
    condition_type = models.IntegerField(blank=True, null=True)
    parameter_heading_id = models.IntegerField(blank=True, null=True)
    parameter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financial_calc_parameter'


class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'


class GovtCompensation(models.Model):
    govt_compensation_id = models.AutoField(primary_key=True)
    govt_compensation_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'govt_compensation'


class HealthFacilityType(models.Model):
    health_facility_type_id = models.AutoField(primary_key=True)
    health_facility_type_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'health_facility_type'


class HealthInformation(models.Model):
    health_information_id = models.IntegerField(primary_key=True)
    health_information_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'health_information'


class HohLandAquired(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    agricultural_land = models.IntegerField(blank=True, null=True)
    agricultural_land_unit = models.CharField(max_length=-1, blank=True, null=True)
    agricultural_land_acre = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cultivated_land_owner = models.IntegerField(blank=True, null=True)
    cultivated_land_owner_unit = models.CharField(max_length=-1, blank=True, null=True)
    cultivated_land_owner_acre = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cultivated_land_tenant = models.IntegerField(blank=True, null=True)
    cultivated_land_tenant_unit = models.CharField(max_length=-1, blank=True, null=True)
    cultivated_land_tenant_acre = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hoh_land_aquired'


class LandOwnership(models.Model):
    land_ownership_id = models.AutoField(primary_key=True)
    land_ownership_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'land_ownership'


class LandUnit(models.Model):
    land_unit_id = models.AutoField(primary_key=True)
    land_unit_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'land_unit'


class LayyahFloodData1(models.Model):
    survey_id = models.IntegerField(unique=True, blank=True, null=True)
    survey_type_id = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    survey_datetime = models.DateTimeField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=-1, blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    tehsil_name = models.CharField(max_length=-1, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=-1, blank=True, null=True)
    mauza_name = models.CharField(max_length=-1, blank=True, null=True)
    mobile_no = models.CharField(max_length=-1, blank=True, null=True)
    family_cast = models.CharField(max_length=-1, blank=True, null=True)
    address = models.CharField(max_length=-1, blank=True, null=True)
    hoh_name = models.CharField(max_length=-1, blank=True, null=True)
    cnic = models.CharField(max_length=-1, blank=True, null=True)
    kacha_rooms = models.IntegerField(blank=True, null=True)
    pakka_rooms = models.IntegerField(blank=True, null=True)
    last_disaster_year = models.IntegerField(blank=True, null=True)
    was_house_damaged = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layyah_flood_data_1'


class LayyahFloodData2(models.Model):
    survey_id = models.IntegerField(unique=True, blank=True, null=True)
    age_group_male_30_to_45_years = models.BigIntegerField(db_column='age_group_male_30+ to 45 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_5_to_14_years = models.BigIntegerField(db_column='age_group_male_5+ to 14 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_up_to_3_years = models.BigIntegerField(db_column='age_group_male_Up to 3 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_45_to_60_years = models.BigIntegerField(db_column='age_group_male_45+ to 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_above_60_years = models.BigIntegerField(db_column='age_group_male_Above 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_18_to_30_years = models.BigIntegerField(db_column='age_group_male_18+ to 30 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_14_to_18_years = models.BigIntegerField(db_column='age_group_male_14+ to 18 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_3_to_5_years = models.BigIntegerField(db_column='age_group_male_3+ to 5 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_up_to_3_years = models.BigIntegerField(db_column='age_group_female_Up to 3 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_45_to_60_years = models.BigIntegerField(db_column='age_group_female_45+ to 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_3_to_5_years = models.BigIntegerField(db_column='age_group_female_3+ to 5 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_14_to_18_years = models.BigIntegerField(db_column='age_group_female_14+ to 18 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_5_to_14_years = models.BigIntegerField(db_column='age_group_female_5+ to 14 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_18_to_30_years = models.BigIntegerField(db_column='age_group_female_18+ to 30 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_30_to_45_years = models.BigIntegerField(db_column='age_group_female_30+ to 45 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_above_60_years = models.BigIntegerField(db_column='age_group_female_Above 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_diable = models.BigIntegerField(blank=True, null=True)
    female_disable = models.BigIntegerField(blank=True, null=True)
    sheep = models.BigIntegerField(db_column='Sheep', blank=True, null=True)  # Field name made lowercase.
    goat = models.BigIntegerField(db_column='Goat', blank=True, null=True)  # Field name made lowercase.
    buffalo = models.BigIntegerField(db_column='Buffalo', blank=True, null=True)  # Field name made lowercase.
    cow = models.BigIntegerField(db_column='Cow', blank=True, null=True)  # Field name made lowercase.
    donkeys = models.BigIntegerField(db_column='Donkeys', blank=True, null=True)  # Field name made lowercase.
    horses = models.BigIntegerField(db_column='Horses', blank=True, null=True)  # Field name made lowercase.
    camels = models.BigIntegerField(db_column='Camels', blank=True, null=True)  # Field name made lowercase.
    hens = models.BigIntegerField(db_column='Hens', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'layyah_flood_data_2'


class LevelOfHelpfulness(models.Model):
    level_of_helpfulness_id = models.AutoField(primary_key=True)
    level_of_helpfulness_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'level_of_helpfulness'


class Livestock(models.Model):
    livestock_id = models.AutoField(primary_key=True)
    livestock_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livestock'


class LivingFacility(models.Model):
    living_facility_id = models.AutoField(primary_key=True)
    living_facility_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'living_facility'


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    mauza = models.ForeignKey('Mauza', models.DO_NOTHING, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    location_datetime = models.DateTimeField(blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class LocationCopy(models.Model):
    location_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    location_datetime = models.DateTimeField(blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_copy'


class LocationDel(models.Model):
    location_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_del'


class MagnitudeOfLoss(models.Model):
    magnitude_of_loss_id = models.AutoField(primary_key=True)
    mangnitude_of_loss_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magnitude_of_loss'


class Mauza(models.Model):
    mauza_id = models.AutoField(primary_key=True)
    mauza_name = models.CharField(max_length=-1, blank=True, null=True)
    hadbast_no = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle = models.ForeignKey('PatwarCircle', models.DO_NOTHING, blank=True, null=True)
    mauza_status = models.NullBooleanField()
    union_council_id = models.IntegerField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    geom = models.GeometryField(blank=True, null=True)
    geom1 = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza'


class Mauza100118(models.Model):
    mauza_id = models.IntegerField(blank=True, null=True)
    mauza_name = models.CharField(max_length=-1, blank=True, null=True)
    hadbast_no = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_status = models.NullBooleanField()
    union_council_id = models.IntegerField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    geom = models.GeometryField(blank=True, null=True)
    geom1 = models.GeometryField(blank=True, null=True)
    survey_geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza_10_01_18'


class MauzaDemographyStats(models.Model):
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=-1, blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    mauza_name = models.CharField(max_length=-1, blank=True, null=True)
    educational_institutes = models.BigIntegerField(blank=True, null=True)
    health_facilities = models.BigIntegerField(blank=True, null=True)
    male_population = models.BigIntegerField(blank=True, null=True)
    female_population = models.BigIntegerField(blank=True, null=True)
    transgender_population = models.BigIntegerField(blank=True, null=True)
    male_disable = models.BigIntegerField(blank=True, null=True)
    female_disable = models.BigIntegerField(blank=True, null=True)
    transgender_disable = models.BigIntegerField(blank=True, null=True)
    no_of_teachers = models.BigIntegerField(blank=True, null=True)
    no_of_kacha_houses = models.BigIntegerField(blank=True, null=True)
    no_of_pakka_houses = models.BigIntegerField(blank=True, null=True)
    no_of_mix_houses = models.BigIntegerField(blank=True, null=True)
    type_of_crops = models.TextField(blank=True, null=True)
    cultivated_area_acre = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tehsil_name = models.CharField(max_length=-1, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza_demography_stats'


class MauzaFim(models.Model):
    mauza_id = models.IntegerField(blank=True, null=True)
    mauza_name = models.CharField(max_length=-1, blank=True, null=True)
    hadbast_no = models.CharField(max_length=-1, blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_status = models.NullBooleanField()
    union_council_id = models.IntegerField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    geom = models.GeometryField(blank=True, null=True)
    geom1 = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza_fim'


class MauzaLandAquired(models.Model):
    mauza_id = models.IntegerField(primary_key=True)
    mauza_agricultural_land_acre = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mauza_cultivated_land_owner_acre = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mauza_cultivated_land_tenant_acre = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza_land_aquired'


class MedicalFacility(models.Model):
    medical_facility_id = models.AutoField(primary_key=True)
    medical_facility_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medical_facility'


class ModeOfInformation(models.Model):
    mode_of_information_id = models.AutoField(primary_key=True)
    mode_of_information_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mode_of_information'


class MonthlyIncome(models.Model):
    monthly_income_id = models.AutoField(primary_key=True)
    monthly_income_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monthly_income'


class MouzaPhase1(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    hb_no = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    drought = models.CharField(max_length=10, blank=True, null=True)
    f_district = models.CharField(max_length=254, blank=True, null=True)
    f_tehsil = models.CharField(max_length=254, blank=True, null=True)
    qh = models.CharField(max_length=254, blank=True, null=True)
    f_pc = models.CharField(max_length=254, blank=True, null=True)
    mouza_name = models.CharField(max_length=254, blank=True, null=True)
    total_popl = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    flood_zone = models.IntegerField(blank=True, null=True)
    f_drought = models.CharField(max_length=254, blank=True, null=True)
    created_us = models.CharField(max_length=254, blank=True, null=True)
    created_da = models.DateField(blank=True, null=True)
    last_edite = models.CharField(max_length=254, blank=True, null=True)
    last_edi_1 = models.DateField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_len = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mouza_phase1'


class NaturalDisaster(models.Model):
    natural_disaster_id = models.AutoField(primary_key=True)
    natural_disaster_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'natural_disaster'


class NgoTypeOfWork(models.Model):
    ngo_type_of_work_id = models.AutoField(primary_key=True)
    ngo_type_of_work_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ngo_type_of_work'


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    option_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'option'


class Parameter(models.Model):
    parameter_id = models.BigIntegerField(blank=True, null=True)
    parameter_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parameter'


class ParameterHeading(models.Model):
    parameter_heading_id = models.BigIntegerField(blank=True, null=True)
    parameter_heading_name = models.CharField(max_length=-1, blank=True, null=True)
    unit = models.CharField(max_length=-1, blank=True, null=True)
    image_path = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parameter_heading'


class ParameterTemp(models.Model):
    parameter_id = models.BigIntegerField(blank=True, null=True)
    parameter_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parameter_temp'


class PatwarCircle(models.Model):
    patwar_circle_id = models.AutoField(primary_key=True)
    patwar_circle_name = models.CharField(max_length=-1, blank=True, null=True)
    qanungoi_halqa = models.ForeignKey('QanungoiHalqa', models.DO_NOTHING, blank=True, null=True)
    surveyed = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'patwar_circle'


class Personality(models.Model):
    personality_id = models.AutoField(primary_key=True)
    personality_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personality'


class PhaseWise(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    estimated_surveys = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phase_wise'


class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    property_name = models.CharField(max_length=-1, blank=True, null=True)
    property_type = models.ForeignKey('PropertyType', models.DO_NOTHING, blank=True, null=True)
    value_lower_limit = models.CharField(max_length=-1, blank=True, null=True)
    value_upper_limit = models.CharField(max_length=-1, blank=True, null=True)
    property_value_type = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property'


class PropertyType(models.Model):
    property_type_id = models.AutoField(primary_key=True)
    property_type_name = models.CharField(max_length=-1, blank=True, null=True)
    ui = models.CharField(max_length=-1, blank=True, null=True)
    genders = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_type'


class PropertyValuesDetailTab(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    property_name = models.CharField(max_length=-1, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    tid = models.BigAutoField()

    class Meta:
        managed = False
        db_table = 'property_values_detail_tab'


class QanungoiHalqa(models.Model):
    qanungoi_halqa_id = models.AutoField(primary_key=True)
    qanungoi_halqa_name = models.CharField(max_length=-1, blank=True, null=True)
    tehsil = models.ForeignKey('Tehsil', models.DO_NOTHING, blank=True, null=True)
    surveyed = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'qanungoi_halqa'


class Religion(models.Model):
    religion_id = models.AutoField(primary_key=True)
    religion_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'religion'


class ResidenceInformation(models.Model):
    residence_information_id = models.IntegerField(primary_key=True)
    residence_information_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'residence_information'


class RespondentRelation(models.Model):
    respondent_relation_id = models.AutoField(primary_key=True)
    respondent_relation_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'respondent_relation'


class River10KmBuffer(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    layer = models.CharField(max_length=17, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    buff_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    orig_fid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'river_10km_buffer'


class River5KmProjected(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    layer = models.CharField(max_length=17, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    buff_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    orig_fid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'river_5km_projected'


class RiversProjected(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid_1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    layer = models.CharField(max_length=17, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    created_us = models.CharField(max_length=254, blank=True, null=True)
    created_da = models.DateField(blank=True, null=True)
    last_edite = models.CharField(max_length=254, blank=True, null=True)
    last_edi_1 = models.DateField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_len = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rivers_projected'


class RoadCategory(models.Model):
    road_category_id = models.CharField(max_length=255, blank=True, null=True)
    road_category_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road_category'


class RoadMaintenanceAuthority(models.Model):
    road_maintenance_authority_id = models.AutoField(primary_key=True)
    road_maintenance_authority = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road_maintenance_authority'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class RolePermission(models.Model):
    role_permission_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)
    user_permission = models.ForeignKey('UserPermission', models.DO_NOTHING, blank=True, null=True)
    update_permission = models.IntegerField(blank=True, null=True)
    create_permission = models.IntegerField(blank=True, null=True)
    delete_permission = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_permission'


class SewerageSystem(models.Model):
    sewerage_system_id = models.AutoField(primary_key=True)
    sewerage_system_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sewerage_system'


class SourceOfIncome(models.Model):
    source_of_income_id = models.AutoField(primary_key=True)
    source_of_income_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_of_income'


class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_type = models.ForeignKey('SurveyType', models.DO_NOTHING, blank=True, null=True)
    surveyor = models.ForeignKey('Surveyor', models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    survey_datetime = models.DateTimeField(blank=True, null=True)
    imei_no = models.CharField(max_length=-1, blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)
    verified = models.NullBooleanField()
    district_id = models.IntegerField(blank=True, null=True)
    surveyor_id_new = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey'


class SurveyD08(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_type_id = models.IntegerField(blank=True, null=True)
    surveyor_id = models.IntegerField(blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)
    survey_datetime = models.DateTimeField(blank=True, null=True)
    imei_no = models.CharField(max_length=-1, blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)
    verified = models.NullBooleanField()
    district_id = models.IntegerField(blank=True, null=True)
    surveyor_id_new = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_D08'


class SurveyCrosstabDataTab(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    hoh_name = models.CharField(db_column='HOH Name', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_gender = models.CharField(db_column='HOH Gender', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_cnic = models.CharField(db_column='HOH CNIC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_cnic_availabilty_date = models.DateField(db_column='HOH CNIC Availabilty Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_phone_no = models.CharField(db_column='HOH Phone no', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    family_cast = models.CharField(db_column='Family Cast', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    religion = models.CharField(db_column='Religion', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    current_address = models.CharField(db_column='Current Address', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    permanent_address = models.CharField(db_column='Permanent Address', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_relation = models.CharField(db_column='Respondent Relation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_education = models.CharField(db_column='Respondent Education', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_name = models.CharField(db_column='Respondent Name', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_gender = models.CharField(db_column='Respondent Gender', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_cnic = models.CharField(db_column='Respondent CNIC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_cnic_availability_date = models.DateField(db_column='Respondent CNIC Availability Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_phone_no = models.CharField(db_column='Respondent Phone no', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_family = models.CharField(db_column='Type of Family', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_the_building_marla_field = models.IntegerField(db_column='Area of the Building (Marla)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    no_of_stories = models.IntegerField(db_column='No of Stories', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_construction = models.CharField(db_column='Type Of Construction', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_pakka_rooms = models.IntegerField(db_column='No of Pakka Rooms', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_kacha_rooms = models.IntegerField(db_column='No of Kacha Rooms', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_of_building_years_field = models.IntegerField(db_column='Age of Building (Years)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    plinth_level_feet_field = models.IntegerField(db_column='Plinth Level (Feet)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    living_facilities_electricity = models.CharField(db_column='Living Facilities ELECTRICITY', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_sui_gas = models.CharField(db_column='Living Facilities SUI GAS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_gas_cylinder = models.CharField(db_column='Living Facilities GAS CYLINDER', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_wood = models.CharField(db_column='Living Facilities WOOD', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_bio_gas = models.CharField(db_column='Living Facilities BIO GAS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depth_of_drinkable_water_feet_field = models.IntegerField(db_column='Depth Of Drinkable Water (Feet)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    source_of_water_supply_hand_pump = models.CharField(db_column='Source of Water Supply HAND PUMP', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_water_supply_motor = models.CharField(db_column='Source of Water Supply MOTOR', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_water_supply_tma_supply = models.CharField(db_column='Source of Water Supply TMA SUPPLY', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_water_supply_pond = models.CharField(db_column='Source of Water Supply Pond', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    distance_to_drinkable_water_meters_field = models.IntegerField(db_column='Distance To Drinkable Water (Meters)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    sewerage_system_non_covered = models.CharField(db_column='Sewerage System Non-Covered', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sewerage_system_covered = models.CharField(db_column='Sewerage System Covered', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sewerage_system_none = models.CharField(db_column='Sewerage System None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_up_to_3_years = models.CharField(db_column='Age Group Male Up to 3 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_up_to_3_years = models.CharField(db_column='Age Group Female Up to 3 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_up_to_3_years = models.CharField(db_column='Age Group Transgender Up to 3 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_3_to_5_years = models.CharField(db_column='Age Group Male 3+ to 5 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_3_to_5_years = models.CharField(db_column='Age Group Female 3+ to 5 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_3_to_5_years = models.CharField(db_column='Age Group Transgender 3+ to 5 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_5_to_14_years = models.CharField(db_column='Age Group Male 5+ to 14 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_5_to_14_years = models.CharField(db_column='Age Group Female 5+ to 14 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_5_to_14_years = models.CharField(db_column='Age Group Transgender 5+ to 14 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_14_to_18_years = models.CharField(db_column='Age Group Male 14+ to 18 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_14_to_18_years = models.CharField(db_column='Age Group Female 14+ to 18 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_14_to_18_years = models.CharField(db_column='Age Group Transgender 14+ to 18 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_18_to_30_years = models.CharField(db_column='Age Group Male 18+ to 30 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_18_to_30_years = models.CharField(db_column='Age Group Female 18+ to 30 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_18_to_30_years = models.CharField(db_column='Age Group Transgender 18+ to 30 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_30_to_45_years = models.CharField(db_column='Age Group Male 30+ to 45 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_30_to_45_years = models.CharField(db_column='Age Group Female 30+ to 45 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_30_to_45_years = models.CharField(db_column='Age Group Transgender 30+ to 45 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_45_to_60_years = models.CharField(db_column='Age Group Male 45+ to 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_45_to_60_years = models.CharField(db_column='Age Group Female 45+ to 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_45_to_60_years = models.CharField(db_column='Age Group Transgender 45+ to 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_above_60_years = models.CharField(db_column='Age Group Male Above 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_above_60_years = models.CharField(db_column='Age Group Female Above 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_above_60_years = models.CharField(db_column='Age Group Transgender Above 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_illiterate = models.CharField(db_column='Eduction Group Male Illiterate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_illiterate = models.CharField(db_column='Eduction Group Female Illiterate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_illiterate = models.CharField(db_column='Eduction Group Transgender Illiterate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_literate = models.CharField(db_column='Eduction Group Male Literate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_literate = models.CharField(db_column='Eduction Group Female Literate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_literate = models.CharField(db_column='Eduction Group Transgender Literate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_primary = models.CharField(db_column='Eduction Group Male Primary', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_primary = models.CharField(db_column='Eduction Group Female Primary', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_primary = models.CharField(db_column='Eduction Group Transgender Primary', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_middle = models.CharField(db_column='Eduction Group Male Middle', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_middle = models.CharField(db_column='Eduction Group Female Middle', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_middle = models.CharField(db_column='Eduction Group Transgender Middle', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_matric = models.CharField(db_column='Eduction Group Male Matric', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_matric = models.CharField(db_column='Eduction Group Female Matric', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_matric = models.CharField(db_column='Eduction Group Transgender Matric', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_intermediate = models.CharField(db_column='Eduction Group Male Intermediate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_intermediate = models.CharField(db_column='Eduction Group Female Intermediate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_intermediate = models.CharField(db_column='Eduction Group Transgender Intermediate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_graduation = models.CharField(db_column='Eduction Group Male Graduation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_graduation = models.CharField(db_column='Eduction Group Female Graduation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_graduation = models.CharField(db_column='Eduction Group Transgender Graduation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_masters = models.CharField(db_column='Eduction Group Male Masters', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_masters = models.CharField(db_column='Eduction Group Female Masters', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_masters = models.CharField(db_column='Eduction Group Transgender Masters', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_doctor_engineer = models.CharField(db_column='Eduction Group Male Doctor/Engineer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_doctor_engineer = models.CharField(db_column='Eduction Group Female Doctor/Engineer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_doctor_engineer = models.CharField(db_column='Eduction Group Transgender Doctor/Engineer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_mentally_disable = models.CharField(db_column='Disability Group Male Mentally Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_mentally_disable = models.CharField(db_column='Disability Group Female Mentally Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_mentally_disable = models.CharField(db_column='Disability Group Transgender Mentally Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_physically_disable = models.CharField(db_column='Disability Group Male Physically Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_physically_disable = models.CharField(db_column='Disability Group Female Physically Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_physically_disable = models.CharField(db_column='Disability Group Transgender Physically Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_visually_impaired = models.CharField(db_column='Disability Group Male Visually Impaired', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_visually_impaired = models.CharField(db_column='Disability Group Female Visually Impaired', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_visually_impaired = models.CharField(db_column='Disability Group Transgender Visually Impaired', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_deaf_and_dumb = models.CharField(db_column='Disability Group Male Deaf and Dumb', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_deaf_and_dumb = models.CharField(db_column='Disability Group Female Deaf and Dumb', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_deaf_and_dumb = models.CharField(db_column='Disability Group Transgender Deaf and Dumb', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_swimmers = models.IntegerField(db_column='Male Swimmers', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_swimmers = models.IntegerField(db_column='Female Swimmers', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_swimmers = models.IntegerField(db_column='Transgender Swimmers', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_pdma = models.CharField(db_column='Civil Defence Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_pdma = models.CharField(db_column='Civil Defence Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_pdma = models.CharField(db_column='Civil Defence Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_civil_defence = models.CharField(db_column='Civil Defence Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_civil_defence = models.CharField(db_column='Civil Defence Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_civil_defence = models.CharField(db_column='Civil Defence Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_1122 = models.CharField(db_column='Civil Defence Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_1122 = models.CharField(db_column='Civil Defence Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_1122 = models.CharField(db_column='Civil Defence Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_qatar_charity = models.CharField(db_column='Civil Defence Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_qatar_charity = models.CharField(db_column='Civil Defence Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_qatar_charity = models.CharField(db_column='Civil Defence Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_islamic_relief = models.CharField(db_column='Civil Defence Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_islamic_relief = models.CharField(db_column='Civil Defence Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_islamic_relief = models.CharField(db_column='Civil Defence Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_pdma = models.CharField(db_column='First Aid Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_pdma = models.CharField(db_column='First Aid Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_pdma = models.CharField(db_column='First Aid Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_civil_defence = models.CharField(db_column='First Aid Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_civil_defence = models.CharField(db_column='First Aid Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_civil_defence = models.CharField(db_column='First Aid Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_1122 = models.CharField(db_column='First Aid Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_1122 = models.CharField(db_column='First Aid Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_1122 = models.CharField(db_column='First Aid Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_qatar_charity = models.CharField(db_column='First Aid Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_qatar_charity = models.CharField(db_column='First Aid Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_qatar_charity = models.CharField(db_column='First Aid Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_islamic_relief = models.CharField(db_column='First Aid Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_islamic_relief = models.CharField(db_column='First Aid Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_islamic_relief = models.CharField(db_column='First Aid Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_pdma = models.CharField(db_column='Rescue Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_pdma = models.CharField(db_column='Rescue Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_pdma = models.CharField(db_column='Rescue Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_civil_defence = models.CharField(db_column='Rescue Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_civil_defence = models.CharField(db_column='Rescue Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_civil_defence = models.CharField(db_column='Rescue Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_1122 = models.CharField(db_column='Rescue Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_1122 = models.CharField(db_column='Rescue Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_1122 = models.CharField(db_column='Rescue Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_qatar_charity = models.CharField(db_column='Rescue Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_qatar_charity = models.CharField(db_column='Rescue Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_qatar_charity = models.CharField(db_column='Rescue Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_islamic_relief = models.CharField(db_column='Rescue Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_islamic_relief = models.CharField(db_column='Rescue Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_islamic_relief = models.CharField(db_column='Rescue Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_pdma = models.CharField(db_column='Disaster Management Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_pdma = models.CharField(db_column='Disaster Management Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_pdma = models.CharField(db_column='Disaster Management Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_civil_defence = models.CharField(db_column='Disaster Management Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_civil_defence = models.CharField(db_column='Disaster Management Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_civil_defence = models.CharField(db_column='Disaster Management Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_1122 = models.CharField(db_column='Disaster Management Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_1122 = models.CharField(db_column='Disaster Management Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_1122 = models.CharField(db_column='Disaster Management Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_qatar_charity = models.CharField(db_column='Disaster Management Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_qatar_charity = models.CharField(db_column='Disaster Management Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_qatar_charity = models.CharField(db_column='Disaster Management Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_islamic_relief = models.CharField(db_column='Disaster Management Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_islamic_relief = models.CharField(db_column='Disaster Management Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_islamic_relief = models.CharField(db_column='Disaster Management Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_pdma = models.CharField(db_column='Other Training Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_pdma = models.CharField(db_column='Other Training Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_pdma = models.CharField(db_column='Other Training Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_civil_defence = models.CharField(db_column='Other Training Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_civil_defence = models.CharField(db_column='Other Training Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_civil_defence = models.CharField(db_column='Other Training Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_1122 = models.CharField(db_column='Other Training Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_1122 = models.CharField(db_column='Other Training Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_1122 = models.CharField(db_column='Other Training Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_qatar_charity = models.CharField(db_column='Other Training Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_qatar_charity = models.CharField(db_column='Other Training Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_qatar_charity = models.CharField(db_column='Other Training Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_islamic_relief = models.CharField(db_column='Other Training Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_islamic_relief = models.CharField(db_column='Other Training Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_islamic_relief = models.CharField(db_column='Other Training Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_mbbs = models.CharField(db_column='Medical Accessibility MBBS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_hakeem = models.CharField(db_column='Medical Accessibility HAKEEM', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_compounder_dispenser = models.CharField(db_column='Medical Accessibility COMPOUNDER / DISPENSER', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_homeo = models.CharField(db_column='Medical Accessibility HOMEO', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    average_electricity_bill_rupees_field = models.IntegerField(db_column='Average Electricity Bill (Rupees)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    connected_infrastructure_solling = models.CharField(db_column='Connected Infrastructure SOLLING', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    connected_infrastructure_kacha_rasta = models.CharField(db_column='Connected Infrastructure KACHA RASTA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    connected_infrastructure_pcc = models.CharField(db_column='Connected Infrastructure PCC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    connected_infrastructure_mettaled = models.CharField(db_column='Connected Infrastructure METTALED', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_tractor_trolly = models.CharField(db_column='Transport TRACTOR / TROLLY', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_m_cycle = models.CharField(db_column='Transport M_CYCLE', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_car_jeep = models.CharField(db_column='Transport CAR / JEEP', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_bicycle = models.CharField(db_column='Transport BICYCLE', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_cart = models.CharField(db_column='Transport CART', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_boat = models.CharField(db_column='Transport BOAT', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_none = models.CharField(db_column='Transport None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    monthly_income = models.CharField(db_column='Monthly Income', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_agriculture_farming = models.CharField(db_column='Source of Income Agriculture Farming', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_private_job = models.CharField(db_column='Source of Income Private job', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_govt_job = models.CharField(db_column='Source of Income Govt Job', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_business = models.CharField(db_column='Source of Income Business', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_labour = models.CharField(db_column='Source of Income Labour', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_shopkeeper = models.CharField(db_column='Source of Income Shopkeeper', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_fish_farming = models.CharField(db_column='Source of Income Fish Farming', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_livestock = models.CharField(db_column='Source of Income Livestock', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_poultry_farming = models.CharField(db_column='Source of Income Poultry Farming', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_pension = models.CharField(db_column='Source of Income Pension', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_brick_kiln = models.CharField(db_column='Source of Income Brick Kiln', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_landlord = models.CharField(db_column='Source of Income Landlord', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_cold_storage = models.CharField(db_column='Source of Income Cold Storage', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_tenant = models.CharField(db_column='Source of Income Tenant', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_local_remittance = models.CharField(db_column='Source of Income Local Remittance', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_foreign_remittance = models.CharField(db_column='Source of Foreign Remittance', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bank_account_number = models.CharField(db_column='Bank Account Number', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_agricultural_land_unit = models.CharField(db_column='Total Agricultural Land Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_agricultural_land = models.IntegerField(db_column='Total Agricultural Land', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_owner = models.IntegerField(db_column='Total Cultivated Land As Owner', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_owner_unit = models.CharField(db_column='Total Cultivated Land As Owner Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_tenant = models.IntegerField(db_column='Total Cultivated Land As Tenant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_tenant_unit = models.CharField(db_column='Total Cultivated Land As Tenant Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    any_uncultivated_land = models.CharField(db_column='Any Uncultivated Land', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_uncultivated_land = models.IntegerField(db_column='Area of Uncultivated Land', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_uncultivated_land_unit = models.CharField(db_column='Area of Uncultivated Land Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reason_of_uncultivated_land = models.CharField(db_column='Reason of Uncultivated Land', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_crops = models.IntegerField(db_column='No of Crops', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_wheat = models.CharField(db_column='Type of Crops Wheat', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_cotton = models.CharField(db_column='Type of Crops Cotton', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_orchards = models.CharField(db_column='Type of Crops Orchards', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_rice = models.CharField(db_column='Type of Crops Rice', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_sugarcane = models.CharField(db_column='Type of Crops Sugarcane', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_vegetable = models.CharField(db_column='Type of Crops Vegetable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_pulses = models.CharField(db_column='Type of Crops Pulses', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_sheep = models.CharField(db_column='Livestock Sheep', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_goat = models.CharField(db_column='Livestock Goat', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_buffalo = models.CharField(db_column='Livestock Buffalo', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_cow = models.CharField(db_column='Livestock Cow', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_donkeys = models.CharField(db_column='Livestock Donkeys', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_horses = models.CharField(db_column='Livestock Horses', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_camels = models.CharField(db_column='Livestock Camels', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_hens = models.CharField(db_column='Livestock Hens', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_food = models.CharField(db_column='Relief You Seek Food', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_clothes = models.CharField(db_column='Relief You Seek Clothes', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_blankets = models.CharField(db_column='Relief You Seek Blankets', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_shelter = models.CharField(db_column='Relief You Seek Shelter', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_drinking_water = models.CharField(db_column='Relief You Seek Drinking Water', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_medicine = models.CharField(db_column='Relief You Seek Medicine', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_rescue = models.CharField(db_column='Relief You Seek Rescue', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_cash = models.CharField(db_column='Relief You Seek Cash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_tax_releif = models.CharField(db_column='Relief You Seek Tax Releif', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_tent = models.CharField(db_column='Relief You Seek Tent', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_seed_fertilizer = models.CharField(db_column='Relief You Seek Seed Fertilizer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_wash = models.CharField(db_column='Relief You Seek Wash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_none = models.CharField(db_column='Relief You Seek None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_flood = models.CharField(db_column='Experienced Last Natural Disaster Flood', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_drought = models.CharField(db_column='Experienced Last Natural Disaster Drought', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_earthquake = models.CharField(db_column='Experienced Last Natural Disaster Earthquake', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_cyclone = models.CharField(db_column='Experienced Last Natural Disaster Cyclone', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_avalanches = models.CharField(db_column='Experienced Last Natural Disaster Avalanches', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_hurricane = models.CharField(db_column='Experienced Last Natural Disaster Hurricane', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_pest_attacks = models.CharField(db_column='Experienced Last Natural Disaster Pest Attacks', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_erosion = models.CharField(db_column='Experienced Last Natural Disaster Erosion', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_tornado_twister = models.CharField(db_column='Experienced Last Natural Disaster Tornado/Twister', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_none = models.CharField(db_column='Experienced Last Natural Disaster None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year_of_disaster = models.CharField(db_column='Year of Disaster', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_house_building = models.CharField(db_column='Damage In Last Disaster House Building', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_livestock = models.CharField(db_column='Damage In Last Disaster Livestock', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_crop = models.CharField(db_column='Damage In Last Disaster Crop', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_human_life = models.CharField(db_column='Damage In Last Disaster Human Life', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_television = models.CharField(db_column='Mode of Information Television', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_radio = models.CharField(db_column='Mode of Information Radio', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_announcement = models.CharField(db_column='Mode of Information Announcement', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_sms = models.CharField(db_column='Mode of Information SMS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_local_newspaper = models.CharField(db_column='Mode of Information Local Newspaper', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_phone = models.CharField(db_column='Mode of Information Phone', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    how_much_media_awareness_was_helpfull = models.CharField(db_column='How Much Media Awareness Was Helpfull', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    is_property_restored = models.CharField(db_column='Is Property Restored', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    time_taken_to_restore_months_field = models.IntegerField(db_column='Time Taken To Restore (Months)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    last_epidemic_diseases_malaria = models.CharField(db_column='Last Epidemic Diseases Malaria', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_cholera = models.CharField(db_column='Last Epidemic Diseases Cholera', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_smallpox = models.CharField(db_column='Last Epidemic Diseases Smallpox', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_typhoid = models.CharField(db_column='Last Epidemic Diseases Typhoid', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_yellow_fever = models.CharField(db_column='Last Epidemic Diseases Yellow Fever', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_dengue = models.CharField(db_column='Last Epidemic Diseases Dengue', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_scabies = models.CharField(db_column='Last Epidemic Diseases Scabies', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_gastro = models.CharField(db_column='Last Epidemic Diseases Gastro', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_diarrhea = models.CharField(db_column='Last Epidemic Diseases Diarrhea', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_khidmat_card = models.CharField(db_column='Compensation From Govt Khidmat Card', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_bisp = models.CharField(db_column='Compensation From Govt BISP', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_kisan_package = models.CharField(db_column='Compensation From Govt Kisan Package', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_watan_card = models.CharField(db_column='Compensation From Govt Watan Card', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_tax_abyana = models.CharField(db_column='Compensation From Govt Tax/ Abyana', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_karc = models.CharField(db_column='Compensation From Govt KARC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_none = models.CharField(db_column='Compensation From Govt None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_food = models.CharField(db_column='Relief From NGO/INGO Food', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_clothes = models.CharField(db_column='Relief From NGO/INGO Clothes', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_blankets = models.CharField(db_column='Relief From NGO/INGO Blankets', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_shelter = models.CharField(db_column='Relief From NGO/INGO Shelter', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_drinking_water = models.CharField(db_column='Relief From NGO/INGO Drinking Water', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_medicine = models.CharField(db_column='Relief From NGO/INGO Medicine', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_rescue = models.CharField(db_column='Relief From NGO/INGO Rescue', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_cash = models.CharField(db_column='Relief From NGO/INGO Cash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_tax_releif = models.CharField(db_column='Relief From NGO/INGO Tax Releif', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_tent = models.CharField(db_column='Relief From NGO/INGO Tent', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_seed_fertilizer = models.CharField(db_column='Relief From NGO/INGO Seed Fertilizer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_wash = models.CharField(db_column='Relief From NGO/INGO Wash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_none = models.CharField(db_column='Relief From NGO/INGO None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'survey_crosstab_data_tab'


class SurveyCrosstabDataTab1(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    hoh_name = models.CharField(db_column='HOH Name', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_gender = models.CharField(db_column='HOH Gender', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_cnic = models.CharField(db_column='HOH CNIC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_cnic_availabilty_date = models.DateField(db_column='HOH CNIC Availabilty Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hoh_phone_no = models.CharField(db_column='HOH Phone no', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    family_cast = models.CharField(db_column='Family Cast', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    religion = models.CharField(db_column='Religion', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    current_address = models.CharField(db_column='Current Address', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    permanent_address = models.CharField(db_column='Permanent Address', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_relation = models.CharField(db_column='Respondent Relation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_education = models.CharField(db_column='Respondent Education', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_name = models.CharField(db_column='Respondent Name', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_gender = models.CharField(db_column='Respondent Gender', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_cnic = models.CharField(db_column='Respondent CNIC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_cnic_availability_date = models.DateField(db_column='Respondent CNIC Availability Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    respondent_phone_no = models.CharField(db_column='Respondent Phone no', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_family = models.CharField(db_column='Type of Family', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_the_building_marla_field = models.IntegerField(db_column='Area of the Building (Marla)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    no_of_stories = models.IntegerField(db_column='No of Stories', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_construction = models.CharField(db_column='Type Of Construction', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_pakka_rooms = models.IntegerField(db_column='No of Pakka Rooms', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_kacha_rooms = models.IntegerField(db_column='No of Kacha Rooms', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_of_building_years_field = models.IntegerField(db_column='Age of Building (Years)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    plinth_level_feet_field = models.IntegerField(db_column='Plinth Level (Feet)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    living_facilities_electricity = models.CharField(db_column='Living Facilities ELECTRICITY', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_sui_gas = models.CharField(db_column='Living Facilities SUI GAS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_gas_cylinder = models.CharField(db_column='Living Facilities GAS CYLINDER', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_wood = models.CharField(db_column='Living Facilities WOOD', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    living_facilities_bio_gas = models.CharField(db_column='Living Facilities BIO GAS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depth_of_drinkable_water_feet_field = models.IntegerField(db_column='Depth Of Drinkable Water (Feet)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    source_of_water_supply_hand_pump = models.CharField(db_column='Source of Water Supply HAND PUMP', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_water_supply_motor = models.CharField(db_column='Source of Water Supply MOTOR', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_water_supply_tma_supply = models.CharField(db_column='Source of Water Supply TMA SUPPLY', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_water_supply_pond = models.CharField(db_column='Source of Water Supply Pond', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    distance_to_drinkable_water_meters_field = models.IntegerField(db_column='Distance To Drinkable Water (Meters)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    sewerage_system_non_covered = models.CharField(db_column='Sewerage System Non-Covered', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sewerage_system_covered = models.CharField(db_column='Sewerage System Covered', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sewerage_system_none = models.CharField(db_column='Sewerage System None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_up_to_3_years = models.CharField(db_column='Age Group Male Up to 3 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_up_to_3_years = models.CharField(db_column='Age Group Female Up to 3 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_up_to_3_years = models.CharField(db_column='Age Group Transgender Up to 3 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_3_to_5_years = models.CharField(db_column='Age Group Male 3+ to 5 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_3_to_5_years = models.CharField(db_column='Age Group Female 3+ to 5 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_3_to_5_years = models.CharField(db_column='Age Group Transgender 3+ to 5 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_5_to_14_years = models.CharField(db_column='Age Group Male 5+ to 14 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_5_to_14_years = models.CharField(db_column='Age Group Female 5+ to 14 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_5_to_14_years = models.CharField(db_column='Age Group Transgender 5+ to 14 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_14_to_18_years = models.CharField(db_column='Age Group Male 14+ to 18 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_14_to_18_years = models.CharField(db_column='Age Group Female 14+ to 18 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_14_to_18_years = models.CharField(db_column='Age Group Transgender 14+ to 18 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_18_to_30_years = models.CharField(db_column='Age Group Male 18+ to 30 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_18_to_30_years = models.CharField(db_column='Age Group Female 18+ to 30 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_18_to_30_years = models.CharField(db_column='Age Group Transgender 18+ to 30 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_30_to_45_years = models.CharField(db_column='Age Group Male 30+ to 45 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_30_to_45_years = models.CharField(db_column='Age Group Female 30+ to 45 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_30_to_45_years = models.CharField(db_column='Age Group Transgender 30+ to 45 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_45_to_60_years = models.CharField(db_column='Age Group Male 45+ to 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_45_to_60_years = models.CharField(db_column='Age Group Female 45+ to 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_45_to_60_years = models.CharField(db_column='Age Group Transgender 45+ to 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_above_60_years = models.CharField(db_column='Age Group Male Above 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_above_60_years = models.CharField(db_column='Age Group Female Above 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_above_60_years = models.CharField(db_column='Age Group Transgender Above 60 Years', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_illiterate = models.CharField(db_column='Eduction Group Male Illiterate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_illiterate = models.CharField(db_column='Eduction Group Female Illiterate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_illiterate = models.CharField(db_column='Eduction Group Transgender Illiterate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_literate = models.CharField(db_column='Eduction Group Male Literate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_literate = models.CharField(db_column='Eduction Group Female Literate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_literate = models.CharField(db_column='Eduction Group Transgender Literate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_primary = models.CharField(db_column='Eduction Group Male Primary', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_primary = models.CharField(db_column='Eduction Group Female Primary', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_primary = models.CharField(db_column='Eduction Group Transgender Primary', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_middle = models.CharField(db_column='Eduction Group Male Middle', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_middle = models.CharField(db_column='Eduction Group Female Middle', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_middle = models.CharField(db_column='Eduction Group Transgender Middle', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_matric = models.CharField(db_column='Eduction Group Male Matric', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_matric = models.CharField(db_column='Eduction Group Female Matric', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_matric = models.CharField(db_column='Eduction Group Transgender Matric', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_intermediate = models.CharField(db_column='Eduction Group Male Intermediate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_intermediate = models.CharField(db_column='Eduction Group Female Intermediate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_intermediate = models.CharField(db_column='Eduction Group Transgender Intermediate', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_graduation = models.CharField(db_column='Eduction Group Male Graduation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_graduation = models.CharField(db_column='Eduction Group Female Graduation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_graduation = models.CharField(db_column='Eduction Group Transgender Graduation', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_masters = models.CharField(db_column='Eduction Group Male Masters', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_masters = models.CharField(db_column='Eduction Group Female Masters', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_masters = models.CharField(db_column='Eduction Group Transgender Masters', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_male_doctor_engineer = models.CharField(db_column='Eduction Group Male Doctor/Engineer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_female_doctor_engineer = models.CharField(db_column='Eduction Group Female Doctor/Engineer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    eduction_group_transgender_doctor_engineer = models.CharField(db_column='Eduction Group Transgender Doctor/Engineer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_mentally_disable = models.CharField(db_column='Disability Group Male Mentally Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_mentally_disable = models.CharField(db_column='Disability Group Female Mentally Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_mentally_disable = models.CharField(db_column='Disability Group Transgender Mentally Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_physically_disable = models.CharField(db_column='Disability Group Male Physically Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_physically_disable = models.CharField(db_column='Disability Group Female Physically Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_physically_disable = models.CharField(db_column='Disability Group Transgender Physically Disable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_visually_impaired = models.CharField(db_column='Disability Group Male Visually Impaired', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_visually_impaired = models.CharField(db_column='Disability Group Female Visually Impaired', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_visually_impaired = models.CharField(db_column='Disability Group Transgender Visually Impaired', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_male_deaf_and_dumb = models.CharField(db_column='Disability Group Male Deaf and Dumb', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_female_deaf_and_dumb = models.CharField(db_column='Disability Group Female Deaf and Dumb', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disability_group_transgender_deaf_and_dumb = models.CharField(db_column='Disability Group Transgender Deaf and Dumb', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_swimmers = models.IntegerField(db_column='Male Swimmers', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_swimmers = models.IntegerField(db_column='Female Swimmers', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_swimmers = models.IntegerField(db_column='Transgender Swimmers', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_pdma = models.CharField(db_column='Civil Defence Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_pdma = models.CharField(db_column='Civil Defence Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_pdma = models.CharField(db_column='Civil Defence Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_civil_defence = models.CharField(db_column='Civil Defence Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_civil_defence = models.CharField(db_column='Civil Defence Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_civil_defence = models.CharField(db_column='Civil Defence Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_1122 = models.CharField(db_column='Civil Defence Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_1122 = models.CharField(db_column='Civil Defence Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_1122 = models.CharField(db_column='Civil Defence Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_qatar_charity = models.CharField(db_column='Civil Defence Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_qatar_charity = models.CharField(db_column='Civil Defence Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_qatar_charity = models.CharField(db_column='Civil Defence Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_male_islamic_relief = models.CharField(db_column='Civil Defence Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_female_islamic_relief = models.CharField(db_column='Civil Defence Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    civil_defence_transgender_islamic_relief = models.CharField(db_column='Civil Defence Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_pdma = models.CharField(db_column='First Aid Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_pdma = models.CharField(db_column='First Aid Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_pdma = models.CharField(db_column='First Aid Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_civil_defence = models.CharField(db_column='First Aid Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_civil_defence = models.CharField(db_column='First Aid Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_civil_defence = models.CharField(db_column='First Aid Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_1122 = models.CharField(db_column='First Aid Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_1122 = models.CharField(db_column='First Aid Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_1122 = models.CharField(db_column='First Aid Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_qatar_charity = models.CharField(db_column='First Aid Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_qatar_charity = models.CharField(db_column='First Aid Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_qatar_charity = models.CharField(db_column='First Aid Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_male_islamic_relief = models.CharField(db_column='First Aid Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_female_islamic_relief = models.CharField(db_column='First Aid Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_aid_transgender_islamic_relief = models.CharField(db_column='First Aid Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_pdma = models.CharField(db_column='Rescue Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_pdma = models.CharField(db_column='Rescue Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_pdma = models.CharField(db_column='Rescue Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_civil_defence = models.CharField(db_column='Rescue Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_civil_defence = models.CharField(db_column='Rescue Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_civil_defence = models.CharField(db_column='Rescue Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_1122 = models.CharField(db_column='Rescue Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_1122 = models.CharField(db_column='Rescue Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_1122 = models.CharField(db_column='Rescue Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_qatar_charity = models.CharField(db_column='Rescue Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_qatar_charity = models.CharField(db_column='Rescue Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_qatar_charity = models.CharField(db_column='Rescue Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_male_islamic_relief = models.CharField(db_column='Rescue Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_female_islamic_relief = models.CharField(db_column='Rescue Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rescue_transgender_islamic_relief = models.CharField(db_column='Rescue Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_pdma = models.CharField(db_column='Disaster Management Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_pdma = models.CharField(db_column='Disaster Management Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_pdma = models.CharField(db_column='Disaster Management Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_civil_defence = models.CharField(db_column='Disaster Management Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_civil_defence = models.CharField(db_column='Disaster Management Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_civil_defence = models.CharField(db_column='Disaster Management Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_1122 = models.CharField(db_column='Disaster Management Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_1122 = models.CharField(db_column='Disaster Management Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_1122 = models.CharField(db_column='Disaster Management Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_qatar_charity = models.CharField(db_column='Disaster Management Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_qatar_charity = models.CharField(db_column='Disaster Management Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_qatar_charity = models.CharField(db_column='Disaster Management Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_male_islamic_relief = models.CharField(db_column='Disaster Management Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_female_islamic_relief = models.CharField(db_column='Disaster Management Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disaster_management_transgender_islamic_relief = models.CharField(db_column='Disaster Management Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_pdma = models.CharField(db_column='Other Training Male PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_pdma = models.CharField(db_column='Other Training Female PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_pdma = models.CharField(db_column='Other Training Transgender PDMA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_civil_defence = models.CharField(db_column='Other Training Male Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_civil_defence = models.CharField(db_column='Other Training Female Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_civil_defence = models.CharField(db_column='Other Training Transgender Civil Defence', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_1122 = models.CharField(db_column='Other Training Male 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_1122 = models.CharField(db_column='Other Training Female 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_1122 = models.CharField(db_column='Other Training Transgender 1122', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_qatar_charity = models.CharField(db_column='Other Training Male Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_qatar_charity = models.CharField(db_column='Other Training Female Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_qatar_charity = models.CharField(db_column='Other Training Transgender Qatar Charity', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_male_islamic_relief = models.CharField(db_column='Other Training Male Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_female_islamic_relief = models.CharField(db_column='Other Training Female Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    other_training_transgender_islamic_relief = models.CharField(db_column='Other Training Transgender Islamic Relief', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_mbbs = models.CharField(db_column='Medical Accessibility MBBS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_hakeem = models.CharField(db_column='Medical Accessibility HAKEEM', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_compounder_dispenser = models.CharField(db_column='Medical Accessibility COMPOUNDER / DISPENSER', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    medical_accessibility_homeo = models.CharField(db_column='Medical Accessibility HOMEO', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    average_electricity_bill_rupees_field = models.IntegerField(db_column='Average Electricity Bill (Rupees)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    connected_infrastructure_solling = models.CharField(db_column='Connected Infrastructure SOLLING', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    connected_infrastructure_kacha_rasta = models.CharField(db_column='Connected Infrastructure KACHA RASTA', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    connected_infrastructure_pcc = models.CharField(db_column='Connected Infrastructure PCC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    connected_infrastructure_mettaled = models.CharField(db_column='Connected Infrastructure METTALED', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_tractor_trolly = models.CharField(db_column='Transport TRACTOR / TROLLY', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_m_cycle = models.CharField(db_column='Transport M_CYCLE', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_car_jeep = models.CharField(db_column='Transport CAR / JEEP', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_bicycle = models.CharField(db_column='Transport BICYCLE', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_cart = models.CharField(db_column='Transport CART', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_boat = models.CharField(db_column='Transport BOAT', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transport_none = models.CharField(db_column='Transport None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    monthly_income = models.CharField(db_column='Monthly Income', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_agriculture_farming = models.CharField(db_column='Source of Income Agriculture Farming', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_private_job = models.CharField(db_column='Source of Income Private job', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_govt_job = models.CharField(db_column='Source of Income Govt Job', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_business = models.CharField(db_column='Source of Income Business', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_labour = models.CharField(db_column='Source of Income Labour', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_shopkeeper = models.CharField(db_column='Source of Income Shopkeeper', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_fish_farming = models.CharField(db_column='Source of Income Fish Farming', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_livestock = models.CharField(db_column='Source of Income Livestock', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_poultry_farming = models.CharField(db_column='Source of Income Poultry Farming', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_pension = models.CharField(db_column='Source of Income Pension', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_brick_kiln = models.CharField(db_column='Source of Income Brick Kiln', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_landlord = models.CharField(db_column='Source of Income Landlord', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_cold_storage = models.CharField(db_column='Source of Income Cold Storage', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_tenant = models.CharField(db_column='Source of Income Tenant', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_income_local_remittance = models.CharField(db_column='Source of Income Local Remittance', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_of_foreign_remittance = models.CharField(db_column='Source of Foreign Remittance', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bank_account_number = models.CharField(db_column='Bank Account Number', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_agricultural_land_unit = models.CharField(db_column='Total Agricultural Land Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_agricultural_land = models.IntegerField(db_column='Total Agricultural Land', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_owner = models.IntegerField(db_column='Total Cultivated Land As Owner', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_owner_unit = models.CharField(db_column='Total Cultivated Land As Owner Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_tenant = models.IntegerField(db_column='Total Cultivated Land As Tenant', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cultivated_land_as_tenant_unit = models.CharField(db_column='Total Cultivated Land As Tenant Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    any_uncultivated_land = models.CharField(db_column='Any Uncultivated Land', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_uncultivated_land = models.IntegerField(db_column='Area of Uncultivated Land', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_uncultivated_land_unit = models.CharField(db_column='Area of Uncultivated Land Unit', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reason_of_uncultivated_land = models.CharField(db_column='Reason of Uncultivated Land', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_crops = models.IntegerField(db_column='No of Crops', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_wheat = models.CharField(db_column='Type of Crops Wheat', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_cotton = models.CharField(db_column='Type of Crops Cotton', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_orchards = models.CharField(db_column='Type of Crops Orchards', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_rice = models.CharField(db_column='Type of Crops Rice', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_sugarcane = models.CharField(db_column='Type of Crops Sugarcane', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_vegetable = models.CharField(db_column='Type of Crops Vegetable', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type_of_crops_pulses = models.CharField(db_column='Type of Crops Pulses', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_sheep = models.CharField(db_column='Livestock Sheep', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_goat = models.CharField(db_column='Livestock Goat', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_buffalo = models.CharField(db_column='Livestock Buffalo', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_cow = models.CharField(db_column='Livestock Cow', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_donkeys = models.CharField(db_column='Livestock Donkeys', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_horses = models.CharField(db_column='Livestock Horses', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_camels = models.CharField(db_column='Livestock Camels', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    livestock_hens = models.CharField(db_column='Livestock Hens', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_food = models.CharField(db_column='Relief You Seek Food', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_clothes = models.CharField(db_column='Relief You Seek Clothes', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_blankets = models.CharField(db_column='Relief You Seek Blankets', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_shelter = models.CharField(db_column='Relief You Seek Shelter', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_drinking_water = models.CharField(db_column='Relief You Seek Drinking Water', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_medicine = models.CharField(db_column='Relief You Seek Medicine', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_rescue = models.CharField(db_column='Relief You Seek Rescue', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_cash = models.CharField(db_column='Relief You Seek Cash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_tax_releif = models.CharField(db_column='Relief You Seek Tax Releif', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_tent = models.CharField(db_column='Relief You Seek Tent', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_seed_fertilizer = models.CharField(db_column='Relief You Seek Seed Fertilizer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_wash = models.CharField(db_column='Relief You Seek Wash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_you_seek_none = models.CharField(db_column='Relief You Seek None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_flood = models.CharField(db_column='Experienced Last Natural Disaster Flood', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_drought = models.CharField(db_column='Experienced Last Natural Disaster Drought', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_earthquake = models.CharField(db_column='Experienced Last Natural Disaster Earthquake', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_cyclone = models.CharField(db_column='Experienced Last Natural Disaster Cyclone', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_avalanches = models.CharField(db_column='Experienced Last Natural Disaster Avalanches', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_hurricane = models.CharField(db_column='Experienced Last Natural Disaster Hurricane', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_pest_attacks = models.CharField(db_column='Experienced Last Natural Disaster Pest Attacks', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_erosion = models.CharField(db_column='Experienced Last Natural Disaster Erosion', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_tornado_twister = models.CharField(db_column='Experienced Last Natural Disaster Tornado/Twister', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    experienced_last_natural_disaster_none = models.CharField(db_column='Experienced Last Natural Disaster None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year_of_disaster = models.CharField(db_column='Year of Disaster', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_house_building = models.CharField(db_column='Damage In Last Disaster House Building', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_livestock = models.CharField(db_column='Damage In Last Disaster Livestock', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_crop = models.CharField(db_column='Damage In Last Disaster Crop', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    damage_in_last_disaster_human_life = models.CharField(db_column='Damage In Last Disaster Human Life', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_television = models.CharField(db_column='Mode of Information Television', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_radio = models.CharField(db_column='Mode of Information Radio', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_announcement = models.CharField(db_column='Mode of Information Announcement', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_sms = models.CharField(db_column='Mode of Information SMS', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_local_newspaper = models.CharField(db_column='Mode of Information Local Newspaper', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_of_information_phone = models.CharField(db_column='Mode of Information Phone', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    how_much_media_awareness_was_helpfull = models.CharField(db_column='How Much Media Awareness Was Helpfull', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    is_property_restored = models.CharField(db_column='Is Property Restored', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    time_taken_to_restore_months_field = models.IntegerField(db_column='Time Taken To Restore (Months)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    last_epidemic_diseases_malaria = models.CharField(db_column='Last Epidemic Diseases Malaria', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_cholera = models.CharField(db_column='Last Epidemic Diseases Cholera', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_smallpox = models.CharField(db_column='Last Epidemic Diseases Smallpox', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_typhoid = models.CharField(db_column='Last Epidemic Diseases Typhoid', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_yellow_fever = models.CharField(db_column='Last Epidemic Diseases Yellow Fever', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_dengue = models.CharField(db_column='Last Epidemic Diseases Dengue', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_scabies = models.CharField(db_column='Last Epidemic Diseases Scabies', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_gastro = models.CharField(db_column='Last Epidemic Diseases Gastro', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_epidemic_diseases_diarrhea = models.CharField(db_column='Last Epidemic Diseases Diarrhea', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_khidmat_card = models.CharField(db_column='Compensation From Govt Khidmat Card', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_bisp = models.CharField(db_column='Compensation From Govt BISP', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_kisan_package = models.CharField(db_column='Compensation From Govt Kisan Package', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_watan_card = models.CharField(db_column='Compensation From Govt Watan Card', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_tax_abyana = models.CharField(db_column='Compensation From Govt Tax/ Abyana', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_karc = models.CharField(db_column='Compensation From Govt KARC', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compensation_from_govt_none = models.CharField(db_column='Compensation From Govt None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_food = models.CharField(db_column='Relief From NGO/INGO Food', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_clothes = models.CharField(db_column='Relief From NGO/INGO Clothes', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_blankets = models.CharField(db_column='Relief From NGO/INGO Blankets', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_shelter = models.CharField(db_column='Relief From NGO/INGO Shelter', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_drinking_water = models.CharField(db_column='Relief From NGO/INGO Drinking Water', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_medicine = models.CharField(db_column='Relief From NGO/INGO Medicine', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_rescue = models.CharField(db_column='Relief From NGO/INGO Rescue', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_cash = models.CharField(db_column='Relief From NGO/INGO Cash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_tax_releif = models.CharField(db_column='Relief From NGO/INGO Tax Releif', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_tent = models.CharField(db_column='Relief From NGO/INGO Tent', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_seed_fertilizer = models.CharField(db_column='Relief From NGO/INGO Seed Fertilizer', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_wash = models.CharField(db_column='Relief From NGO/INGO Wash', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relief_from_ngo_ingo_none = models.CharField(db_column='Relief From NGO/INGO None', max_length=-1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'survey_crosstab_data_tab1'
# Unable to inspect table 'survey_del_log'
# The error was: permission denied for relation survey_del_log

# Unable to inspect table 'survey_picture'
# The error was: permission denied for relation survey_picture



class SurveyProperty(models.Model):
    survey_property_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, models.DO_NOTHING, blank=True, null=True)
    gender = models.CharField(max_length=-1, blank=True, null=True)
    integer_value = models.IntegerField(blank=True, null=True)
    property = models.ForeignKey(Property, models.DO_NOTHING, blank=True, null=True)
    string_value = models.CharField(max_length=-1, blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_property'


class SurveyPropertyD08(models.Model):
    survey_property_id = models.IntegerField(blank=True, null=True)
    survey_id = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=-1, blank=True, null=True)
    integer_value = models.IntegerField(blank=True, null=True)
    property_id = models.IntegerField(blank=True, null=True)
    string_value = models.CharField(max_length=-1, blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_property_D08'


class SurveyPropertyDataTab(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    survey_type_id = models.IntegerField(blank=True, null=True)
    property_type_id = models.IntegerField(blank=True, null=True)
    property_id = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    counter = models.IntegerField(blank=True, null=True)
    property_value_name = models.TextField(blank=True, null=True)
    property_option = models.TextField(blank=True, null=True)
    property_name = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    tid = models.BigAutoField()

    class Meta:
        managed = False
        db_table = 'survey_property_data_tab'


class SurveyPropertyDetailTab(models.Model):
    survey_type_id = models.IntegerField(blank=True, null=True)
    property_type_id = models.IntegerField(blank=True, null=True)
    property_id = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    counter = models.IntegerField(primary_key=True)
    property_value_name = models.TextField(blank=True, null=True)
    property_option = models.TextField(blank=True, null=True)
    property_name = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    tid = models.BigAutoField()

    class Meta:
        managed = False
        db_table = 'survey_property_detail_tab'


class SurveyReport(models.Model):
    district_name = models.CharField(max_length=-1, blank=True, null=True)
    surveyor_name = models.CharField(max_length=-1, blank=True, null=True)
    no_days_infield = models.IntegerField(blank=True, null=True)
    residential = models.IntegerField(blank=True, null=True)
    public_building = models.IntegerField(db_column='Public Building', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    education = models.IntegerField(blank=True, null=True)
    health_facility = models.IntegerField(db_column='Health Facility', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    commercial = models.IntegerField(blank=True, null=True)
    religious_building = models.IntegerField(db_column='Religious Building', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    infrastructure = models.IntegerField(blank=True, null=True)
    terminal = models.IntegerField(blank=True, null=True)
    mauza_general_survey = models.IntegerField(db_column='Mauza General Survey', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    graveyard = models.IntegerField(blank=True, null=True)
    parks = models.IntegerField(blank=True, null=True)
    bridges = models.IntegerField(blank=True, null=True)
    industry = models.IntegerField(blank=True, null=True)
    dera_jaat = models.IntegerField(blank=True, null=True)
    collapse_building = models.IntegerField(blank=True, null=True)
    total_surveys = models.IntegerField(blank=True, null=True)
    daily_avg = models.IntegerField(blank=True, null=True)
    last_day_surveys = models.IntegerField(blank=True, null=True)
    last_day = models.DateField(blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    surveyor_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_report'


class SurveyType(models.Model):
    survey_type_id = models.AutoField(primary_key=True)
    survey_type_name = models.CharField(max_length=-1, blank=True, null=True)
    survey_table_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_type'
# Unable to inspect table 'surveyor'
# The error was: permission denied for relation surveyor



class Tehsil(models.Model):
    tehsil_id = models.AutoField(primary_key=True)
    tehsil_name = models.CharField(max_length=-1, blank=True, null=True)
    district = models.ForeignKey(District, models.DO_NOTHING, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    surveyed = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'tehsil'


class TotalAgriculturalLandUnit(models.Model):
    total_agricultural_land_unit_id = models.AutoField(primary_key=True)
    total_agricultural_land_unit_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'total_agricultural_land_unit'


class Transport(models.Model):
    transport_id = models.AutoField(primary_key=True)
    transport_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport'


class TypeOfBusiness(models.Model):
    type_of_business_id = models.AutoField(primary_key=True)
    type_of_business_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_business'


class TypeOfChemical(models.Model):
    type_of_chemical_id = models.AutoField(primary_key=True)
    type_of_chemical_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_chemical'


class TypeOfConstruction(models.Model):
    type_of_construction_id = models.AutoField(primary_key=True)
    type_of_construction_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_construction'


class TypeOfCrop(models.Model):
    type_of_crop_id = models.AutoField(primary_key=True)
    type_of_crop_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_crop'


class TypeOfDisability(models.Model):
    type_of_disability_id = models.AutoField(primary_key=True)
    type_of_disability_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_disability'


class TypeOfFamily(models.Model):
    type_of_family_id = models.AutoField(primary_key=True)
    type_of_family_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_family'


class TypeOfGraveyard(models.Model):
    type_of_graveyard_id = models.AutoField(primary_key=True)
    type_of_graveyard_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_graveyard'


class TypeOfIndustry(models.Model):
    type_of_industry_id = models.AutoField(primary_key=True)
    type_of_industry_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_industry'


class TypeOfInstitute(models.Model):
    type_of_institute_id = models.AutoField(primary_key=True)
    type_of_institute_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_institute'


class TypeOfPark(models.Model):
    type_of_park_id = models.AutoField(primary_key=True)
    type_of_park_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_park'


class TypeOfRelief(models.Model):
    type_of_relief_id = models.AutoField(primary_key=True)
    type_of_relief_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_relief'


class TypeOfReligiousBuilding(models.Model):
    type_of_religious_building_id = models.AutoField(primary_key=True)
    type_of_religious_building_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_religious_building'


class UcPhase1(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    phase = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_phase1'


class UnionCouncil(models.Model):
    union_council_id = models.AutoField(primary_key=True)
    union_council_name = models.CharField(max_length=-1, blank=True, null=True)
    union_council_no = models.CharField(max_length=-1, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'union_council'


class UserPermission(models.Model):
    user_permission_id = models.AutoField(primary_key=True)
    user_permission_name = models.CharField(max_length=50, blank=True, null=True)
    target_page_url = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_permission'


class WaterSupply(models.Model):
    water_supply_id = models.AutoField(primary_key=True)
    water_supply_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'water_supply'


class XPatwarCircle111(models.Model):
    patwar_circle_id = models.IntegerField()
    patwar_circle_name = models.CharField(max_length=-1, blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    matched = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'x_patwar_circle_111'
