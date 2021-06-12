# # This is an auto-generated Django model module.
# # You'll have  do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from __future__ import unicode_literals
#
# from django.db import models
from django.contrib.gis.db import models

# class BoundariesHierarchy(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     admin_name = models.CharField(max_length=64, blank=True, null=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#     admin_level = models.IntegerField(blank=True, null=True)
#     admin_level_name = models.CharField(max_length=-1, blank=True, null=True)
#     code_from_table = models.CharField(max_length=-1, blank=True, null=True)
#     name_from_table = models.CharField(max_length=-1, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#     extent = models.GeometryField(blank=True, null=True)
#     level_complete_code = models.CharField(max_length=-1, blank=True, null=True)
#     extent_boundary = models.CharField(max_length=-1, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'boundaries_hierarchy'
#
#
# class TblDc(models.Model):
#     gid = models.AutoField(primary_key=True)
#     name_admin = models.CharField(max_length=27, blank=True, null=True)
#     name_id = models.IntegerField(blank=True, null=True)
#     parent_id = models.SmallIntegerField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_dc'
#
#
# class TblDistrict(models.Model):
#     objectid = models.IntegerField(blank=True, null=True)
#     name_admin = models.CharField(max_length=50, blank=True, null=True)
#     name_id = models.SmallIntegerField(blank=True, null=True)
#     parent_id = models.SmallIntegerField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_district'
#
#
# class TblDivision(models.Model):
#     name_admin = models.CharField(max_length=50, blank=True, null=True)
#     name_id = models.SmallIntegerField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_division'
#
#
# class TblHierarchy(models.Model):
#     id = models.AutoField(primary_key=True)
#     admin_name = models.CharField(max_length=64, blank=True, null=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#     admin_level = models.IntegerField(blank=True, null=True)
#     admin_level_name = models.CharField(max_length=-1, blank=True, null=True)
#     code_from_table = models.CharField(max_length=-1, blank=True, null=True)
#     name_from_table = models.CharField(max_length=-1, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#     extent = models.GeometryField(blank=True, null=True)
#     level_complete_code = models.CharField(max_length=-1, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_hierarchy'
#
#
# class TblIrrigationCircle(models.Model):
#     name_admin = models.CharField(max_length=254, blank=True, null=True)
#     name_id = models.CharField(max_length=254, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#     parent_id = models.BigIntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_irrigation_circle'
#
#
# class TblIrrigationDivision(models.Model):
#     zone_id = models.CharField(max_length=254, blank=True, null=True)
#     parent_id = models.CharField(max_length=254, blank=True, null=True)
#     name_id = models.IntegerField(blank=True, null=True)
#     name_admin = models.CharField(max_length=25, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_irrigation_division'
#
#
# class TblMauza(models.Model):
#     gid = models.AutoField(primary_key=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#     name_id = models.IntegerField(blank=True, null=True)
#     name_admin = models.CharField(max_length=50, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_mauza'
#
#
# class TblMc(models.Model):
#     name_id = models.AutoField()
#     oid_field = models.IntegerField(db_column='oid_', blank=True, null=True)  # Field renamed because it ended with '_'.
#     name_admin = models.CharField(max_length=254, blank=True, null=True)
#     folderpath = models.CharField(max_length=254, blank=True, null=True)
#     dc1 = models.CharField(max_length=50, blank=True, null=True)
#     distt_name = models.CharField(max_length=50, blank=True, null=True)
#     parent_id = models.SmallIntegerField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_mc'
#
#
# class TblPatwarCircle(models.Model):
#     gid = models.AutoField()
#     parent_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
#     name_id = models.IntegerField(blank=True, null=True)
#     name_admin = models.CharField(max_length=50, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_patwar_circle'
#
#
# class TblProvince(models.Model):
#     name_admin = models.CharField(max_length=30, blank=True, null=True)
#     name_id = models.FloatField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_province'
#
#
# class TblQuanghoi(models.Model):
#     gid = models.AutoField()
#     name_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#     admin_name = models.CharField(max_length=50, blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_quanghoi'
#
#
# class TblTehsil(models.Model):
#     name_admin = models.CharField(max_length=50, blank=True, null=True)
#     name_id = models.SmallIntegerField(blank=True, null=True)
#     division_id = models.SmallIntegerField(blank=True, null=True)
#     parent_id = models.SmallIntegerField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_tehsil'
#
#
# class TblUc(models.Model):
#     name_id = models.AutoField()
#     objectid = models.IntegerField(blank=True, null=True)
#     uc_no = models.CharField(max_length=10, blank=True, null=True)
#     name_admin = models.CharField(max_length=50, blank=True, null=True)
#     tehsil = models.CharField(max_length=50, blank=True, null=True)
#     teh_name = models.CharField(max_length=50, blank=True, null=True)
#     parent_id = models.SmallIntegerField(blank=True, null=True)
#     geom = models.GeometryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_uc'
#
#
# class TehsilJson(models.Model):
#     row_to_json = models.TextField(blank=True, null=True)  # This field type is a guess.
#
#     class Meta:
#         managed = False
#         db_table = 'tehsil_json'
from django.contrib.postgres.fields import JSONField
from django.db.models import Max

from ferrp.layers.models import Info
from ferrp.local_settings import BOUNDARIES_TYPE


class BoundariesInfo(models.Model):
    id = models.AutoField(primary_key=True)
    # type_name = models.CharField(max_length=200)
    bound_name = models.CharField(max_length=200, verbose_name="Boundary Name")
    table_name = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name="Table Name",limit_choices_to={'main_category':'Boundaries'})
    bound_code = models.CharField(max_length=5, choices=BOUNDARIES_TYPE, verbose_name="Boundary Code")
    bound_level = models.SmallIntegerField(null=True, blank=True, verbose_name="Boundary Level")
    parent_bound = models.ForeignKey("self", verbose_name="Parent Boundaries", blank=True, null=True)


    def __str__(self):
        return self.bound_name

    # def __getattr__(self, name):
    #     if (name=='table_name'):
    #         return Info.objects.filter(main_category='Boundaries')
    #     elif (name == 'bound_level'):
    #         return self.get_boundaries_level()
    #     else:
    #         return super(BoundariesInfo, self).__getattr__(name)

    def get_boundaries_level(self):
        # objs = BoundariesInfo.objects.filter(bound_code=self.bound_code).aggregate(Max('bound_level'))
        # bound_level = objs[0] + 1 if len(objs) > 0 else 1
        bound_level = self.parent_bound.bound_level + 1 if self.parent_bound else 0
        return bound_level


# class TblAdminHierarchy(models.Model):
#     admin_name = models.CharField(max_length=64, blank=True, null=True)
#     parent_id = models.IntegerField(blank=True, null=True)
#     admin_level = models.IntegerField(blank=True, null=True)
#     admin_level_name = models.CharField(max_length=-1, blank=True, null=True)
#     code_from_table = models.CharField(max_length=-1, blank=True, null=True)
#     name_from_table = models.CharField(max_length=-1, blank=True, null=True)
#     geom = models.GeometryField(srid=3857, blank=True, null=True)
#     extent = models.GeometryField(srid=3857, blank=True, null=True)
#     level_complete_code = models.CharField(max_length=-1, blank=True, null=True)
#     extent_boundary = models.CharField(max_length=-1, blank=True, null=True)
#     id = models.BigAutoField(primary_key=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_admin_hierarchy'


class TblProvince(models.Model):
    name_admin = models.CharField(max_length=30, blank=True, null=True)
    name_id = models.IntegerField(primary_key=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_province'


class TblDivision(models.Model):
    # id = models.AutoField(primary_key=True)
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    name_id = models.SmallIntegerField(primary_key=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)
    parent = models.ForeignKey(TblProvince)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_division'


class TblDistrict(models.Model):
    # objectid = models.IntegerField(blank=True, null=True)
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    name_id = models.SmallIntegerField(primary_key=True)
    parent = models.ForeignKey(TblDivision)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_district'


class TblTehsil(models.Model):
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    name_id = models.SmallIntegerField(primary_key=True)
    division_id = models.SmallIntegerField(TblDivision)
    parent = models.ForeignKey(TblDistrict)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_tehsil'


class TblUc(models.Model):
    name_id = models.AutoField(primary_key=True)
    # objectid = models.IntegerField(blank=True, null=True)
    uc_no = models.CharField(max_length=10, blank=True, null=True)
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    tehsil = models.CharField(max_length=50, blank=True, null=True)
    # teh_name = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey(TblTehsil)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_uc'


class TblQuanghoi(models.Model):
    gid = models.AutoField(primary_key=True)
    name_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    parent = models.ForeignKey(TblTehsil, blank=True, null=True)
    admin_name = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_quanghoi'


class TblPatwarCircle(models.Model):
    gid = models.AutoField(primary_key=True)
    parent = models.ForeignKey(TblQuanghoi)
    name_id = models.IntegerField(blank=True, null=True)
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_patwar_circle'


class TblMauza(models.Model):
    gid = models.AutoField(primary_key=True)
    parent = models.ForeignKey(TblPatwarCircle)
    name_id = models.IntegerField(blank=True, null=True)
    name_admin = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_mauza'


class TblDistrictCouncil(models.Model):
    gid = models.AutoField(primary_key=True)
    name_admin = models.CharField(max_length=27, blank=True, null=True)
    name_id = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey(TblDistrict)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_district_council'


class TblMunicipalCouncil(models.Model):
    name_id = models.AutoField(primary_key=True)
    oid_field = models.IntegerField(db_column='oid_', blank=True, null=True)  # Field renamed because it ended with '_'.
    name_admin = models.CharField(max_length=254, blank=True, null=True)
    folderpath = models.CharField(max_length=254, blank=True, null=True)
    dc1 = models.CharField(max_length=50, blank=True, null=True)
    distt_name = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey(TblDistrict)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'tbl_municipal_council'

class IndusBasinBasin(models.Model):
    oid = models.AutoField(primary_key=True)
    basin_name = models.CharField(max_length=500)
    geom = models.GeometryField(srid=3857)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'indus_basin_basin'

class IndusBasinRivers(models.Model):
    oid = models.AutoField(primary_key=True)
    river_name = models.CharField(max_length=500)
    geom = models.GeometryField(srid=3857)

    class Meta:
        app_label='gis'
        managed = False
        db_table = 'indus_basin_rivers'

class IndusBasinDrainageBasin(models.Model):
    oid = models.AutoField(primary_key=True)
    drainage_basin_name = models.CharField(max_length=500)
    geom = models.GeometryField(srid=3857)
    river_oid = models.ForeignKey(IndusBasinRivers, models.DO_NOTHING)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'indus_basin_drainage_basin'

class IndusBasinRiversDrainageBasin(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    parent= models.ForeignKey(IndusBasinRivers, models.DO_NOTHING)
    geom = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'indus_basin_rivers_drainage_basin'
