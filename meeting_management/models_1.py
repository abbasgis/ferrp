# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AdpSchemes1018(models.Model):
    scheme_name = models.CharField(db_column='Scheme Name', max_length=2500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year = models.TextField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    gs_no = models.IntegerField(db_column='GS No', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    district = models.CharField(db_column='District', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    main_sector = models.CharField(db_column='Main Sector', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    approval = models.TextField(db_column='Approval', blank=True, null=True)  # Field name made lowercase.
    local_capital = models.FloatField(db_column='Local Capital', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    local_revenue = models.FloatField(db_column='Local Revenue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_capital = models.FloatField(db_column='Total Capital', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_revenue = models.FloatField(db_column='Total Revenue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid_capital = models.FloatField(db_column='Foreign Aid Capital', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid_revenue = models.FloatField(db_column='Foreign Aid Revenue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid_total = models.FloatField(db_column='Foreign Aid Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cost = models.FloatField(db_column='Total Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    allocation = models.FloatField(db_column='Allocation', blank=True, null=True)  # Field name made lowercase.
    release = models.FloatField(db_column='Release', blank=True, null=True)  # Field name made lowercase.
    utilization = models.FloatField(db_column='Utilization', blank=True, null=True)  # Field name made lowercase.
    expense_upto_june = models.FloatField(db_column='Expense Upto June', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    projection_one = models.FloatField(db_column='Projection One', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    projection_two = models.FloatField(db_column='Projection Two', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    throw_forward = models.FloatField(db_column='Throw Forward', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id = models.AutoField()

    class Meta:
        managed = False
        db_table = 'adp_schemes_10_18'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class MainSector(models.Model):
    msectid = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    member_name = models.CharField(db_column='Member Name', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grant = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_sector'


class MeetingsInitiatives(models.Model):
    nature = models.ForeignKey('TblTaskNature', models.DO_NOTHING, db_column='nature', blank=True, null=True)
    sector = models.CharField(max_length=-1, blank=True, null=True)
    sub_sector = models.CharField(max_length=-1, blank=True, null=True)
    department = models.CharField(max_length=-1, blank=True, null=True)
    referred_by = models.CharField(max_length=-1, blank=True, null=True)
    assigned_to = models.CharField(max_length=-1, blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    status = models.ForeignKey('TblTaskStatus', models.DO_NOTHING, db_column='status', blank=True, null=True)
    priority = models.ForeignKey('TblTaskPriority', models.DO_NOTHING, db_column='priority', blank=True, null=True)
    remarks = models.CharField(max_length=-1, blank=True, null=True)
    is_important = models.NullBooleanField()
    term = models.CharField(max_length=-1, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    meeting_agenda = models.TextField(blank=True, null=True)
    assignment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meetings_initiatives'


class PointcloudFormats(models.Model):
    pcid = models.IntegerField(primary_key=True)
    srid = models.IntegerField(blank=True, null=True)
    schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pointcloud_formats'


class Sector(models.Model):
    sectorid = models.DecimalField(db_column='SectorID', max_digits=255, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    msecid = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    adj9 = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    adj10 = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    g = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector'

