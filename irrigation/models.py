# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models

# Commanded area models
class GisIrrigationZone(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=254, blank=True, null=True)
    gca_ma = models.DecimalField(db_column='gca_ma', max_digits=65535, decimal_places=3, blank=True, null=True)
    cca_ma = models.DecimalField(db_column='cca_ma', max_digits=65535, decimal_places=3, blank=True, null=True)
    gca_geom_ma = models.DecimalField(db_column='gca_geom_ma', max_digits=65535, decimal_places=3, blank=True, null=True)
    cca_geom_ma = models.DecimalField(db_column='cca_geom_ma', max_digits=65535, decimal_places=3, blank=True, null=True)
    outlets = models.IntegerField(db_column='outlets', blank=True, null=True)
    canal_length = models.DecimalField(db_column='channels_length_km', max_digits=65535, decimal_places=3, blank=True, null=True)
    shape_length = models.DecimalField(db_column='canals_shape_length', max_digits=65535, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_zone_origs'

class GisIrrigationCircle(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=254, blank=True, null=True)
    zone_name = models.CharField(db_column='zone_name', max_length=254, blank=True, null=True)
    gca_ma = models.DecimalField(db_column='gca_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    cca_ma = models.DecimalField(db_column='cca_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    gca_geom_ma = models.DecimalField(db_column='gca_geom_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    cca_geom_ma = models.DecimalField(db_column='cca_geom_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    outlets = models.DecimalField(db_column='outlets', max_digits=65535, decimal_places=65535, blank=True, null=True)
    length = models.DecimalField(db_column='channels_length_km', max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_length = models.DecimalField(db_column='canals_shape_length', max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_circle_origs'

class GisIrrigationDivision(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=254, blank=True, null=True)
    zone_name = models.CharField(db_column='zone_name', max_length=254, blank=True, null=True)
    gca_ma = models.DecimalField(db_column='gca_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    cca_ma = models.DecimalField(db_column='cca_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    gca_geom_ma = models.DecimalField(db_column='gca_geom_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    cca_geom_ma = models.DecimalField(db_column='cca_geom_ma', max_digits=65535, decimal_places=65535, blank=True, null=True)
    outlets = models.DecimalField(db_column='outlets', max_digits=65535, decimal_places=65535, blank=True, null=True)
    length = models.DecimalField(db_column='channels_length_km', max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_length = models.DecimalField(db_column='canals_shape_length', max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_division_origs'


# Dams and barages db models
class PakDamsAndBarrages(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    dam_name = models.CharField(db_column='dam_name', max_length=254, blank=True, null=True)
    river = models.CharField(db_column='river', max_length=254, blank=True, null=True)
    main_basin = models.CharField(db_column='main_basin', max_length=254, blank=True, null=True)
    near_city = models.CharField(db_column='near_city', max_length=254, blank=True, null=True)
    catch_skm = models.DecimalField(db_column='catch_skm', max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_use = models.CharField(db_column='main_use', max_length=254, blank=True, null=True)
    extent = models.CharField(db_column='extent', max_length=254, blank=True, null=True)
    geojson = models.CharField(db_column='geojson', max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_pakistan_dam_and_barrages'

class DischargeData(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    discharge_date = models.DateField(db_column='discharge_date', max_length=254, blank=True, null=True)
    discharge_time = models.DateTimeField(db_column='discharge_time', max_length=254, blank=True, null=True)
    river = models.CharField(db_column='river', max_length=254, blank=True, null=True)
    head_works = models.CharField(db_column='head_works', max_length=254, blank=True, null=True)
    flow = models.CharField(db_column='flow', max_length=254, blank=True, null=True)
    us = models.DecimalField(db_column='us', max_digits=65535, decimal_places=65535, blank=True, null=True)
    ds = models.DecimalField(db_column='ds', max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharge_data'


#### Ground water models
class TblWqWlCombinedData(models.Model):
    # geom = models.GeometryField(primary_key=True)  # This field type is a guess.
    id = models.IntegerField(db_column='id', primary_key=True)
    sr_no = models.CharField(db_column='sr_no', max_length=254, blank=True, null=True)
    gis_no = models.CharField(db_column='gis_no', max_length=254, blank=True, null=True)
    y_axis = models.DecimalField(db_column='y', decimal_places=2, max_digits=25, blank=True, null=True)
    x_axis = models.DecimalField(db_column='x', decimal_places=2, max_digits=25, blank=True, null=True)
    major_canal = models.CharField(db_column='major_canal', max_length=254, blank=True, null=True)
    disty_minor = models.CharField(db_column='disty_minor', max_length=254, blank=True, null=True)
    circle = models.CharField(db_column='circle', max_length=254, blank=True, null=True)
    division = models.CharField(db_column='division', max_length=254, blank=True, null=True)
    zone = models.CharField(db_column='zone', max_length=254, blank=True, null=True)
    reclamation = models.CharField(db_column='reclamation', max_length=254, blank=True, null=True)
    district = models.CharField(db_column='district', max_length=254, blank=True, null=True)
    tehsil = models.CharField(db_column='tehsil', max_length=254, blank=True, null=True)
    elevation = models.CharField(db_column='elevation', max_length=254, blank=True, null=True)
    type_wl_wq = models.CharField(db_column='type_wl_wq', max_length=254, blank=True, null=True)
    extent = models.CharField(db_column='extent', max_length=254, blank=True, null=True)
    geojson = models.CharField(db_column='geojson', max_length=254, blank=True, null=True)
    district_name = models.CharField(db_column='district_name', max_length=254, blank=True, null=True)
    tehsil_name = models.CharField(db_column='tehsil_name', max_length=254, blank=True, null=True)
    qanongo_halka = models.CharField(db_column='qanongo_halka', max_length=254, blank=True, null=True)
    patwar_circle = models.CharField(db_column='patwar_circle', max_length=254, blank=True, null=True)
    mauza = models.CharField(db_column='mauza', max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_wq_wl'

class TblWlDetail(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    year = models.IntegerField(db_column='year', blank=True, null=True)
    season = models.CharField(db_column='season', max_length=25, blank=True, null=True)
    water_depth = models.DecimalField(db_column='water_depth', decimal_places=2, max_digits=25, blank=True, null=True)
    elevation = models.DecimalField(db_column='elevation', decimal_places=2, max_digits=25, blank=True, null=True)
    ql_id = models.IntegerField(db_column='ql_id', blank=True, null=True)
    geom_text = models.CharField(db_column='geom_xy', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_water_level_detail'

class TblWqDetail(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    year = models.IntegerField(db_column='year', blank=True, null=True)
    season = models.CharField(db_column='season', max_length=25, blank=True, null=True)
    quality_type = models.CharField(db_column='quality_type', max_length=25, blank=True, null=True)
    water_quality = models.DecimalField(db_column='water_quality', decimal_places=2, max_digits=25, blank=True, null=True)
    elevation = models.CharField(db_column='elevation', max_length=25, blank=True, null=True)
    ql_id = models.IntegerField(db_column='ql_id', blank=True, null=True)
    geom_text = models.CharField(db_column='geom_xy', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_water_quality_detail'


