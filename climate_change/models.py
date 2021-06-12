# from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class ClimateLocation(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'climate_location'


class TemperatureRcp4525Km(models.Model):
    id = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    year = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    # latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    # longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    feb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    apr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    may = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jun = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jul = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    aug = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sep = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    oct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nov = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dec = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    tehsil = models.CharField(max_length=255, blank=True, null=True)

    # geom = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'temperature_rcp45_25km'


class TemperatureRcp4525KmPunjab(models.Model):
    id = models.AutoField(primary_key=True)
    # objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    year = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    # latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    # longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    feb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    apr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    may = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jun = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jul = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    aug = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sep = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    oct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nov = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dec = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    tehsil = models.CharField(max_length=255, blank=True, null=True)

    # geom = models.GeometryField(srid=0, blank=True, null=True)
    # @property
    # def weight(self):
    #     return self

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'view_temperature_rcp45_25km_punjab'


class view_precipitation_rcp4525_20102099(models.Model):
    id = models.AutoField(primary_key=True)
    # objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    year = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    # latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    # longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    feb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    apr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    may = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jun = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jul = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    aug = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sep = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    oct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nov = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dec = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    tehsil = models.CharField(max_length=255, blank=True, null=True)

    # geom = models.GeometryField(srid=0, blank=True, null=True)
    # @property
    # def weight(self):
    #     return self

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'precipitation_rcp4525_20102099'
