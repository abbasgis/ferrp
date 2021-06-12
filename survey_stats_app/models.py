# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AdminLevels(models.Model):
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_levels'


class AgeOfBuildingFt(models.Model):
    age_of_building_count = models.BigIntegerField(blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mz_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_age_of_building_ft'


class Bridges(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.IntegerField(blank=True, null=True)
    longitude = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    year_of_disaster = models.CharField(max_length=500, blank=True, null=True)
    name_of_bridge = models.CharField(max_length=500, blank=True, null=True)
    type_of_bridge = models.CharField(max_length=500, blank=True, null=True)
    operational = models.CharField(max_length=500, blank=True, null=True)
    width_of_bridge = models.IntegerField(blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    ever_effected_by_disaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_disaster = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bridges'


class BuildingEffectedFromDesasterFt(models.Model):
    building_effected_from_desaster_count = models.BigIntegerField(blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_building_effected_from_desaster_ft'


class CollaspeBuilding(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    type_of_building = models.CharField(max_length=500, blank=True, null=True)
    situated_in = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collaspe_building'


class Commercial(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    respondent_father_name = models.CharField(max_length=500, blank=True, null=True)
    type_of_bussiness = models.CharField(max_length=500, blank=True, null=True)
    name_of_bussiness = models.CharField(max_length=500, blank=True, null=True)
    number_of_employee = models.IntegerField(blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    mz_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commercial'


class Derajaat(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    owner_name = models.CharField(max_length=500, blank=True, null=True)
    owner_father_name = models.CharField(max_length=500, blank=True, null=True)
    owner_gender = models.CharField(max_length=500, blank=True, null=True)
    owner_cnic = models.CharField(max_length=500, blank=True, null=True)
    cnic_expected_date = models.CharField(max_length=500, blank=True, null=True)
    contact_no = models.CharField(max_length=500, blank=True, null=True)
    family_cast = models.CharField(max_length=500, blank=True, null=True)
    relogion = models.CharField(max_length=500, blank=True, null=True)
    current_address = models.CharField(max_length=500, blank=True, null=True)
    permannent_addres = models.CharField(max_length=500, blank=True, null=True)
    respondent_relation = models.CharField(max_length=500, blank=True, null=True)
    number_of_stories = models.IntegerField(blank=True, null=True)
    number_of_pakka_rooms = models.IntegerField(blank=True, null=True)
    number_of_kacha_rooms = models.IntegerField(blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    plenth_level = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField( blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'derajaat'


class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    estimated_population = models.IntegerField(blank=True, null=True)
    estimated_surveys = models.IntegerField(blank=True, null=True)
    surveyors = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    # geom = models.GeometryField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    extent = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district'


class Educational(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    name_of_school = models.CharField(max_length=500, blank=True, null=True)
    office_phone_number = models.CharField(max_length=500, blank=True, null=True)
    respondent_designation = models.CharField(max_length=500, blank=True, null=True)
    ownership = models.CharField(max_length=500, blank=True, null=True)
    level_of_institute = models.CharField(max_length=500, blank=True, null=True)
    number_of_teachers = models.IntegerField(blank=True, null=True)
    number_of_students = models.IntegerField(blank=True, null=True)
    number_of_class_rooms = models.IntegerField(blank=True, null=True)
    number_of_washrooms = models.IntegerField(blank=True, null=True)
    watersupply = models.CharField(max_length=500, blank=True, null=True)
    electricity = models.CharField(max_length=500, blank=True, null=True)
    boundry_wall = models.CharField(max_length=500, blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    type_of_construction_of_building = models.CharField(max_length=500, blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'educational'


class EmergencyExitFt(models.Model):
    emergency_exit_count = models.BigIntegerField(blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField( blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_emergency_exit_ft'


class EvacuationPlanFt(models.Model):
    evacuation_plan_count = models.BigIntegerField(blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_evacuation_plan_ft'


class LevelOfDemageFt(models.Model):
    level_of_demage_count = models.BigIntegerField(blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField( blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mz_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_level_of_demage_ft'


class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    location_datetime = models.DateTimeField(blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)
    # geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class Mauza(models.Model):
    mauza_id = models.IntegerField(primary_key=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    hadbast_no = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_id = models.TextField(blank=True, null=True)
    mauza_status = models.NullBooleanField()
    union_council_id = models.TextField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    # geom = models.GeometryField(blank=True, null=True)
    # geom1 = models.GeometryField(blank=True, null=True)
    extent = models.TextField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza'


class PatwarCircle(models.Model):
    patwar_circle_id = models.IntegerField(primary_key=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    surveyed = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'patwar_circle'


class PlenthLevelOfBuildingFt(models.Model):
    plenth_level_of_building_count = models.BigIntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_plenth_level_of_building_ft'


class PointcloudFormats(models.Model):
    pcid = models.IntegerField(primary_key=True)
    srid = models.IntegerField(blank=True, null=True)
    schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pointcloud_formats'


class PublicBuilding(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_father_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    year_of_desester = models.IntegerField(blank=True, null=True)
    department_name = models.CharField(max_length=500, blank=True, null=True)
    official_phone_number = models.CharField(max_length=500, blank=True, null=True)
    respondent_designation = models.CharField(max_length=500, blank=True, null=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    number_of_storries = models.IntegerField(blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'public_building'


class QanungoiHalqa(models.Model):
    qanungoi_halqa_id = models.IntegerField(primary_key=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    surveyed = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'qanungoi_halqa'


class ReligiousBuilding(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    respondent_father_name = models.CharField(max_length=500, blank=True, null=True)
    name_of_religious_building = models.CharField(max_length=500, blank=True, null=True)
    name_of_head_of_religious_building = models.CharField(max_length=500, blank=True, null=True)
    contact_number = models.CharField(max_length=500, blank=True, null=True)
    type_of_religious_building = models.CharField(max_length=500, blank=True, null=True)
    water_supply = models.CharField(max_length=500, blank=True, null=True)
    number_of_washrooms = models.IntegerField(blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'religious_building'


class Residential(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    survey_date = models.DateField(blank=True, null=True)
    survey_time = models.TextField(blank=True, null=True)
    imei_no = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    respondent_father_name = models.CharField(max_length=500, blank=True, null=True)
    religion = models.CharField(max_length=500, blank=True, null=True)
    family_cast = models.CharField(max_length=500, blank=True, null=True)
    current_address = models.CharField(max_length=500, blank=True, null=True)
    permanent_address = models.CharField(max_length=500, blank=True, null=True)
    upload_date = models.DateField(blank=True, null=True)
    upload_time = models.TextField(blank=True, null=True)
    hoh_cnic = models.CharField(max_length=500, blank=True, null=True)
    hoh_name = models.CharField(max_length=500, blank=True, null=True)
    hoh_gender = models.CharField(max_length=500, blank=True, null=True)
    hoh_address = models.CharField(max_length=500, blank=True, null=True)
    hoh_father_name = models.CharField(max_length=500, blank=True, null=True)
    hoh_cnic_avaliablity_date = models.CharField(max_length=500, blank=True, null=True)
    hoh_phone_no = models.CharField(max_length=500, blank=True, null=True)
    respondent_relation = models.CharField(max_length=500, blank=True, null=True)
    respondent_education = models.CharField(max_length=500, blank=True, null=True)
    respondent_cnic_avaliablity_data = models.CharField(max_length=500, blank=True, null=True)
    respondent_gender = models.CharField(max_length=500, blank=True, null=True)
    type_of_family = models.CharField(max_length=500, blank=True, null=True)
    type_of_construction = models.CharField(max_length=500, blank=True, null=True)
    no_of_paka_rooms = models.IntegerField(blank=True, null=True)
    no_of_kacha_rooms = models.IntegerField(blank=True, null=True)
    area_of_facility_building_marla = models.IntegerField(blank=True, null=True)
    number_of_stories = models.IntegerField(blank=True, null=True)
    age_of_building_years = models.IntegerField(blank=True, null=True)
    plenth_level_feet = models.IntegerField(blank=True, null=True)
    media_awarness_helpful = models.CharField(max_length=500, blank=True, null=True)
    is_property_restored = models.CharField(max_length=500, blank=True, null=True)
    time_taken_to_restore_months = models.IntegerField(blank=True, null=True)
    monthly_income = models.CharField(max_length=500, blank=True, null=True)
    depth_of_water_feet = models.IntegerField(blank=True, null=True)
    average_electricity_bill = models.IntegerField(blank=True, null=True)
    year_of_last_disaster = models.IntegerField(blank=True, null=True)
    total_agricultural_land = models.IntegerField(blank=True, null=True)
    total_agricultural_land_unit = models.CharField(max_length=500, blank=True, null=True)
    total_cultivated_agricultural_land_as_owner = models.IntegerField(blank=True, null=True)
    total_cultivated_agricultural_land_as_owner_unit = models.CharField(max_length=500, blank=True, null=True)
    total_cultivated_agricultural_land_as_tenant = models.IntegerField(blank=True, null=True)
    total_cultivated_agricultural_land_as_tenant_unit = models.CharField(max_length=500, blank=True, null=True)
    uncultivated_agriculture_land = models.IntegerField(blank=True, null=True)
    uncultivated_agriculture_land_unit = models.CharField(max_length=500, blank=True, null=True)
    reason_of_uncultivated_land = models.CharField(max_length=500, blank=True, null=True)
    spsid = models.IntegerField(blank=True, null=True)
    dname = models.CharField(max_length=500, blank=True, null=True)
    ssid = models.IntegerField(blank=True, null=True)
    facility_name = models.TextField(blank=True, null=True)
    source_of_water_supply = models.TextField(blank=True, null=True)
    last_epidemic_diseases = models.TextField(blank=True, null=True)
    source_of_income = models.TextField(blank=True, null=True)
    experienced_last_natural_disaster = models.TextField(blank=True, null=True)
    relief_you_seek = models.TextField(blank=True, null=True)
    livestock = models.TextField(blank=True, null=True)
    livestock_count = models.TextField(blank=True, null=True)
    survey_id_a = models.IntegerField(blank=True, null=True)
    age_group_female_14_to_18_years = models.IntegerField(db_column='age group female 14+ to 18 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_14_to_18_years = models.IntegerField(db_column='age group male 14+ to 18 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_14_to_18_years = models.IntegerField(db_column='age group transgender 14+ to 18 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_18_to_30_years = models.IntegerField(db_column='age group female 18+ to 30 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_18_to_30_years = models.IntegerField(db_column='age group male 18+ to 30 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_18_to_30_years = models.IntegerField(db_column='age group transgender 18+ to 30 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_3_to_5_years = models.IntegerField(db_column='age group female 3+ to 5 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_3_to_5_years = models.IntegerField(db_column='age group male 3+ to 5 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_3_to_5_years = models.IntegerField(db_column='age group transgender 3+ to 5 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_30_to_45_years = models.IntegerField(db_column='age group female 30+ to 45 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_30_to_45_years = models.IntegerField(db_column='age group male 30+ to 45 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_30_to_45_years = models.IntegerField(db_column='age group transgender 30+ to 45 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_45_to_60_years = models.IntegerField(db_column='age group female 45+ to 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_45_to_60_years = models.IntegerField(db_column='age group male 45+ to 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_45_to_60_years = models.IntegerField(db_column='age group transgender 45+ to 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_5_to_14_years = models.IntegerField(db_column='age group female 5+ to 14 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_5_to_14_years = models.IntegerField(db_column='age group male 5+ to 14 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_5_to_14_years = models.IntegerField(db_column='age group transgender 5+ to 14 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_above_60_years = models.IntegerField(db_column='age group female Above 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_above_60_years = models.IntegerField(db_column='age group male Above 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_above_60_years = models.IntegerField(db_column='age group transgender Above 60 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_female_up_to_3_years = models.IntegerField(db_column='age group female Up to 3 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_male_up_to_3_years = models.IntegerField(db_column='age group male Up to 3 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    age_group_transgender_up_to_3_years = models.IntegerField(db_column='age group transgender Up to 3 Years', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    survey_id_e = models.IntegerField(blank=True, null=True)
    female_doctor_engineer = models.IntegerField(db_column='female Doctor/Engineer', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_doctor_engineer = models.IntegerField(db_column='male Doctor/Engineer', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_doctor_engineer = models.IntegerField(db_column='transgender Doctor/Engineer', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_graduation = models.IntegerField(db_column='female Graduation', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_graduation = models.IntegerField(db_column='male Graduation', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_graduation = models.IntegerField(db_column='transgender Graduation', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_illiterate = models.IntegerField(db_column='female Illiterate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_illiterate = models.IntegerField(db_column='male Illiterate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_illiterate = models.IntegerField(db_column='transgender Illiterate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_intermediate = models.IntegerField(db_column='female Intermediate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_intermediate = models.IntegerField(db_column='male Intermediate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_intermediate = models.IntegerField(db_column='transgender Intermediate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_literate = models.IntegerField(db_column='female Literate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_literate = models.IntegerField(db_column='male Literate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_literate = models.IntegerField(db_column='transgender Literate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_masters = models.IntegerField(db_column='female Masters', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_masters = models.IntegerField(db_column='male Masters', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_masters = models.IntegerField(db_column='transgender Masters', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_matric = models.IntegerField(db_column='female Matric', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_matric = models.IntegerField(db_column='male Matric', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_matric = models.IntegerField(db_column='transgender Matric', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_middle = models.IntegerField(db_column='female Middle', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_middle = models.IntegerField(db_column='male Middle', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_middle = models.IntegerField(db_column='transgender Middle', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_primary = models.IntegerField(db_column='female Primary', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_primary = models.IntegerField(db_column='male Primary', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_primary = models.IntegerField(db_column='transgender Primary', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    survey_id_d = models.IntegerField(blank=True, null=True)
    female_deaf_and_dumb = models.IntegerField(db_column='female Deaf and Dumb', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_deaf_and_dumb = models.IntegerField(db_column='male Deaf and Dumb', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_deaf_and_dumb = models.IntegerField(db_column='transgender Deaf and Dumb', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_mentally_disable = models.IntegerField(db_column='female Mentally Disable', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_mentally_disable = models.IntegerField(db_column='male Mentally Disable', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_mentally_disable = models.IntegerField(db_column='transgender Mentally Disable', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_physically_disable = models.IntegerField(db_column='female Physically Disable', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_physically_disable = models.IntegerField(db_column='male Physically Disable', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_physically_disable = models.IntegerField(db_column='transgender Physically Disable', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    female_visually_impaired = models.IntegerField(db_column='female Visually Impaired', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    male_visually_impaired = models.IntegerField(db_column='male Visually Impaired', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transgender_visually_impaired = models.IntegerField(db_column='transgender Visually Impaired', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'residential'


class SecurityGuardFt(models.Model):
    security_guard_count = models.BigIntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_security_guard_ft'


class Survey(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    survey_type_id = models.IntegerField(blank=True, null=True)
    surveyor_id = models.IntegerField(blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)
    survey_datetime = models.DateTimeField(blank=True, null=True)
    imei_no = models.CharField(max_length=500, blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)
    verified = models.NullBooleanField()
    mauza_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey'


class Tehsil(models.Model):
    tehsil_id = models.IntegerField(primary_key=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    # geom = models.GeometryField(blank=True, null=True)
    surveyed = models.NullBooleanField()
    extent = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tehsil'


class Terminal(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    bus_relway_station_name = models.CharField(max_length=500, blank=True, null=True)
    ownership = models.CharField(max_length=500, blank=True, null=True)
    terminal_building = models.CharField(max_length=500, blank=True, null=True)
    waiting_area = models.CharField(max_length=500, blank=True, null=True)
    prayer_area = models.CharField(max_length=500, blank=True, null=True)
    parking_area = models.CharField(max_length=500, blank=True, null=True)
    washrooms = models.CharField(max_length=500, blank=True, null=True)
    boundry_wall = models.CharField(max_length=500, blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    year_of_desester = models.IntegerField(blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terminal'


class TypeOfBussinessFt(models.Model):
    type_of_bussiness_count = models.BigIntegerField(blank=True, null=True)
    type_of_bussiness = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_type_of_bussiness_ft'


class TypeOfDesasterFt(models.Model):
    type_of_desaster_count = models.BigIntegerField(blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comm_type_of_desaster_ft'


class GraveYard(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    boundry_wall = models.CharField(max_length=500, blank=True, null=True)
    graveyard_name = models.CharField(max_length=500, blank=True, null=True)
    type_of_graveyard = models.CharField(max_length=500, blank=True, null=True)
    janazagah = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grave_yard'



class HealthFacility(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    name_of_health_facility = models.CharField(max_length=500, blank=True, null=True)
    medical_facility_type = models.CharField(max_length=500, blank=True, null=True)
    official_phone_number = models.CharField(max_length=500, blank=True, null=True)
    ownership = models.CharField(max_length=500, blank=True, null=True)
    number_of_beds = models.IntegerField(blank=True, null=True)
    number_of_nurses = models.IntegerField(blank=True, null=True)
    number_of_dispensers = models.IntegerField(blank=True, null=True)
    number_of_leady_health_visitors = models.IntegerField(blank=True, null=True)
    number_of_medical_technicians = models.IntegerField(blank=True, null=True)
    snake_byte_kit = models.IntegerField(blank=True, null=True)
    epidemic_disease_medicine_available = models.CharField(max_length=500, blank=True, null=True)
    type_of_constructions_of_building = models.CharField(max_length=500, blank=True, null=True)
    number_of_doctors = models.IntegerField(blank=True, null=True)
    number_of_veteran_doctor = models.IntegerField(blank=True, null=True)
    number_of_techinicians_veteran = models.IntegerField(blank=True, null=True)
    last_epidemic_diseases_livestock = models.CharField(max_length=500, blank=True, null=True)
    health_information = models.CharField(max_length=500, blank=True, null=True)
    boundry_wall = models.CharField(max_length=500, blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'health_facility'


class Industry(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_designation = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondent_father_name = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    industry_name = models.CharField(max_length=500, blank=True, null=True)
    type_of_industry = models.CharField(max_length=500, blank=True, null=True)
    owner_name = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=500, blank=True, null=True)
    owner_father_name = models.CharField(max_length=500, blank=True, null=True)
    number_of_employee = models.IntegerField(blank=True, null=True)
    chemical_used = models.CharField(max_length=500, blank=True, null=True)
    industrial_waste_treatment_plant = models.CharField(max_length=500, blank=True, null=True)
    first_aid_facility = models.CharField(max_length=500, blank=True, null=True)
    fire_extinguisher = models.CharField(max_length=500, blank=True, null=True)
    age_of_building = models.IntegerField(blank=True, null=True)
    toxic_chemicals = models.CharField(max_length=500, blank=True, null=True)
    any_fire_incident_happen = models.CharField(max_length=500, blank=True, null=True)
    cost_of_damage = models.IntegerField(blank=True, null=True)
    plenth_level_of_building = models.IntegerField(blank=True, null=True)
    security_guard = models.CharField(max_length=500, blank=True, null=True)
    emergency_exit = models.CharField(max_length=500, blank=True, null=True)
    evacuation_plan = models.CharField(max_length=500, blank=True, null=True)
    building_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'industry'

class Infrastructure(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    road_width = models.IntegerField(blank=True, null=True)
    road_category = models.CharField(max_length=500, blank=True, null=True)
    road_type = models.CharField(max_length=500, blank=True, null=True)
    maintained_by = models.CharField(max_length=500, blank=True, null=True)
    name_number = models.CharField(max_length=500, blank=True, null=True)
    road_effected_from_desaster = models.CharField(max_length=500, blank=True, null=True)
    type_of_desaster = models.CharField(max_length=500, blank=True, null=True)
    year_of_desester = models.IntegerField(blank=True, null=True)
    level_of_demage = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tehsil_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infrastructure'

class MauzaGengralSurvey(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    year_of_disaster = models.CharField(max_length=500, blank=True, null=True)
    name_of_surveying_settlement = models.CharField(max_length=500, blank=True, null=True)
    respondent_personality = models.CharField(max_length=500, blank=True, null=True)
    uc_name = models.CharField(max_length=500, blank=True, null=True)
    uc_no = models.CharField(max_length=500, blank=True, null=True)
    village_population = models.IntegerField(blank=True, null=True)
    no_of_houses_in_village = models.IntegerField(blank=True, null=True)
    mouza_name_chak_no = models.CharField(max_length=500, blank=True, null=True)
    respondent_so_do_wo = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza_gengral_survey'


class Parks(models.Model):
    survey_id = models.IntegerField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    name_of_park = models.CharField(max_length=500, blank=True, null=True)
    boundry_wall = models.CharField(max_length=500, blank=True, null=True)
    securty_guard = models.CharField(max_length=500, blank=True, null=True)
    type_of_building = models.CharField(max_length=500, blank=True, null=True)
    swing_facility = models.CharField(max_length=500, blank=True, null=True)
    tracks = models.CharField(max_length=500, blank=True, null=True)
    refreshment_available = models.CharField(max_length=500, blank=True, null=True)
    toilets = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parks'

class BridgesFt(models.Model):
    type_of_bridge = models.TextField(blank=True, null=True)  # This field type is a guess.
    operational = models.TextField(blank=True, null=True)  # This field type is a guess.
    width_of_bridge = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_damage = models.TextField(blank=True, null=True)  # This field type is a guess.
    ever_effected_by_disaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_disaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'bridges_ft'

class CollapseBuildingFt(models.Model):
    type_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    situated_in = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'collapse_building_ft'

class CommercialFt(models.Model):
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_disaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_damage = models.TextField(blank=True, null=True)  # This field type is a guess.
    plinth_level_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_business = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_disaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'commercial_ft'

class DerajaatFt(models.Model):
    number_of_stories = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_pakka_rooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_kacha_rooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    plinth_level = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'derajaat_ft'

class EducationalFt(models.Model):
    ownership = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_institute = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_teachers = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_students = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_class_rooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_washrooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    watersupply = models.TextField(blank=True, null=True)  # This field type is a guess.
    electricity = models.TextField(blank=True, null=True)  # This field type is a guess.
    boundry_wall = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_construction_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    plenth_level_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_demage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'educational_ft'

class GraveYardFt(models.Model):
    type_of_graveyard = models.TextField(blank=True, null=True)  # This field type is a guess.
    janazagah = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'grave_yard_ft'

class HealthFacilityFt(models.Model):
    name_of_health_facility = models.TextField(blank=True, null=True)  # This field type is a guess.
    medical_facility_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    ownership = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_beds = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_nurses = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_dispensers = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_leady_health_visitors = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_medical_technicians = models.TextField(blank=True, null=True)  # This field type is a guess.
    snake_byte_kit = models.TextField(blank=True, null=True)  # This field type is a guess.
    epidemic_disease_medicine_available = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_construction = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_doctors = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_veteran_doctor = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_veteran_techinicians = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_epidemic_diseases_livestock = models.TextField(blank=True, null=True)  # This field type is a guess.
    health_information = models.TextField(blank=True, null=True)  # This field type is a guess.
    boundry_wall = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    plinth_level = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_disaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_disaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_damage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'health_facility_ft'

class IndustryFt(models.Model):
    type_of_industry = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_employee = models.TextField(blank=True, null=True)  # This field type is a guess.
    chemical_used = models.TextField(blank=True, null=True)  # This field type is a guess.
    industrial_waste_treatment_plant = models.TextField(blank=True, null=True)  # This field type is a guess.
    first_aid_facility = models.TextField(blank=True, null=True)  # This field type is a guess.
    fire_extinguisher = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    toxic_chemicals = models.TextField(blank=True, null=True)  # This field type is a guess.
    any_fire_incident_happen = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_of_damage = models.TextField(blank=True, null=True)  # This field type is a guess.
    plenth_level_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_demage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'industry_ft'

class InfrastructureFt(models.Model):
    road_width = models.TextField(blank=True, null=True)  # This field type is a guess.
    road_category = models.TextField(blank=True, null=True)  # This field type is a guess.
    road_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    maintained_by = models.TextField(blank=True, null=True)  # This field type is a guess.
    road_effected_from_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_demage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'infrastructure_ft'

class ParksFt(models.Model):
    boundry_wall = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    swing_facility = models.TextField(blank=True, null=True)  # This field type is a guess.
    tracks = models.TextField(blank=True, null=True)  # This field type is a guess.
    refreshment_available = models.TextField(blank=True, null=True)  # This field type is a guess.
    toilets = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'parks_ft'

class PublicBuildingFt(models.Model):
    number_of_rooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_stories = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    plenth_level_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_demage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'public_building_ft'

class ReligiousBuildingFt(models.Model):
    type_of_religious_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_supply = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_of_washrooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    plenth_level_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_demage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'religious_building_ft'

class TerminalFt(models.Model):
    ownership = models.TextField(blank=True, null=True)  # This field type is a guess.
    terminal_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    waiting_area = models.TextField(blank=True, null=True)  # This field type is a guess.
    prayer_area = models.TextField(blank=True, null=True)  # This field type is a guess.
    parking_area = models.TextField(blank=True, null=True)  # This field type is a guess.
    washrooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    boundry_wall = models.TextField(blank=True, null=True)  # This field type is a guess.
    age_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    plenth_level_of_building = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_guard = models.TextField(blank=True, null=True)  # This field type is a guess.
    emergency_exit = models.TextField(blank=True, null=True)  # This field type is a guess.
    evacuation_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    building_effected_from_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_of_desaster = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_of_demage = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'terminal_ft'

class SurveyCombined(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    respondent_name = models.CharField(max_length=500, blank=True, null=True)
    respondent_cell_no = models.CharField(max_length=500, blank=True, null=True)
    respondant_cnic = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    surveyor_name = models.CharField(max_length=500, blank=True, null=True)
    checked_unchecked = models.NullBooleanField()
    district_name = models.CharField(max_length=500, blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    uc_name = models.CharField(max_length=500, blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    uc_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_combined'

class DistrictSurveyTypeCount(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    latlon = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_surveytype_count'

class TehsilSurveyTypeCount(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    tehsil_id = models.IntegerField(blank=True, null=True)
    tehsil_name = models.CharField(max_length=500, blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    latlon = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tehsil_surveytype_count'


class QanungoiSurveyTypeCount(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    qanungoi_halqa_id = models.IntegerField(blank=True, null=True)
    qanungoi_halqa_name = models.CharField(max_length=500, blank=True, null=True)
    latlon = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qanungoi_surveytype_count'

class PatwarCircleSurveyTypeCount(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    patwar_circle_id = models.IntegerField(blank=True, null=True)
    patwar_circle_name = models.CharField(max_length=500, blank=True, null=True)
    latlon = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patwar_circle_surveytype_count'

class MauzaSurveyTypeCount(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    survey_type_name = models.CharField(max_length=500, blank=True, null=True)
    mauza_id = models.IntegerField(blank=True, null=True)
    mauza_name = models.CharField(max_length=500, blank=True, null=True)
    latlon = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mauza_surveytype_count'
