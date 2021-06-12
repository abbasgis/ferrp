from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class Social_User_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    account_heading = models.CharField(max_length=500)
    email_id = models.CharField(max_length=500)
    phone_no = models.CharField(max_length=500)
    account_type = models.CharField(max_length=500)
    map_url = models.CharField(max_length=500)
    id_from_account = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False


class Rivers(models.Model):
    oid = models.AutoField(primary_key=True)
    river_name = models.CharField(max_length=500)
    geom = models.GeometryField(srid=3857)

    def __str__(self):
        return self.river_name

    class Meta:
        managed = False


class Basin(models.Model):
    oid = models.AutoField(primary_key=True)
    basin_name = models.CharField(max_length=500)
    geom = models.GeometryField(srid=3857)

    class Meta:
        managed = False


class Drainage_Basin(models.Model):
    oid = models.AutoField(primary_key=True)
    drainage_basin_name = models.CharField(max_length=500)
    # river_name = models.CharField(max_length=500)
    river_oid = models.ForeignKey(Rivers, models.DO_NOTHING)
    geom = models.GeometryField(srid=3857)

    class Meta:
        managed = False


class Rivers_Drainage_Basin(models.Model):
    oid = models.AutoField(primary_key=True)
    drainage_basin_name = models.CharField(max_length=500)
    geographic_area = models.FloatField(blank=True, null=True)
    documented_area = models.FloatField(blank=True, null=True)
    river_oid = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=3857)

    class Meta:
        managed = True
