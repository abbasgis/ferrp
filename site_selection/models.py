from django.contrib.gis.db import models


# Create your models here.

class RsFlood10Gsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_flood_10_gsd_100'


class RsFlood14Gsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_flood_14_gsd_100'


class RsFuelsGsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_fuels_gsd_100'


class RsGlcfGsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_glcf_gsd_100'


class RsHospitalGsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_hospital_gsd_100'


class RsPopulationGsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_population_gsd_100'


class RsSchoolsGsd100(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    extent = models.GeometryField(srid=900913, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_schools_gsd_100'


class TblDistrict(models.Model):
    objectid = models.IntegerField(blank=True, null=True)
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    name_id = models.SmallIntegerField(primary_key=True)
    parent_id = models.SmallIntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_district'


class TblTehsil(models.Model):
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    name_id = models.SmallIntegerField(primary_key=True)
    division_id = models.SmallIntegerField(blank=True, null=True)
    parent_id = models.SmallIntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_tehsil'


class SiteSelectionSelectedsites(models.Model):
    oid = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=256, blank=True, null=True)
    project_id = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_selection_selectedsites'
