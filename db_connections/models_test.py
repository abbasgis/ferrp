# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ConnectionsList(models.Model):
    id = models.AutoField()
    connection_name = models.TextField(blank=True, null=True)
    database_host = models.TextField(blank=True, null=True)
    database_name = models.TextField(blank=True, null=True)
    database_user = models.TextField(blank=True, null=True)
    database_password = models.TextField(blank=True, null=True)
    database_port = models.TextField(blank=True, null=True)
    engine_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'connections_list'


class DatabaseEngines(models.Model):
    id = models.AutoField()
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'database_engines'


class PointcloudFormats(models.Model):
    pcid = models.IntegerField(primary_key=True)
    srid = models.IntegerField(blank=True, null=True)
    schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pointcloud_formats'


class TablesList(models.Model):
    id = models.AutoField()
    table_name = models.TextField(blank=True, null=True)
    is_spatial = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'tables_list'
