# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models


#this is used
class AdpDistrict(models.Model):
    name = models.CharField(max_length=5000, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'adp_district'

#this is used
class AdpReport201718(models.Model):
    GS_No = models.CharField(db_column='GS_No', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Name_of_Scheme = models.CharField(db_column='Name_of_Scheme', max_length=500, blank=True, null=True)  # Field name made lowercase.
    District = models.CharField(db_column='District', max_length=500, blank=True, null=True)  # Field name made lowercase.
    Type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Approval_Date = models.CharField(db_column='Approval_Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Total_Cost = models.FloatField(db_column='Total Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid = models.FloatField(db_column='Foreign_Aid', blank=True, null=True)  # Field name made lowercase.
    LocalCapital = models.FloatField(db_column='LocalCapital', blank=True, null=True)  # Field name made lowercase.
    LocalRevenue = models.FloatField(db_column='LocalRevenue', blank=True, null=True)  # Field name made lowercase.
    TotalCapital = models.FloatField(db_column='TotalCapital', blank=True, null=True)  # Field name made lowercase.
    TotalRevenue = models.FloatField(db_column='TotalRevenue', blank=True, null=True)  # Field name made lowercase.
    ForeignCapital = models.FloatField(db_column='ForeignCapital', blank=True, null=True)  # Field name made lowercase.
    ForeignRevenue = models.FloatField(db_column='ForeignRevenue', blank=True, null=True)  # Field name made lowercase.
    Allocation = models.FloatField(db_column='Allocation', blank=True, null=True)  # Field name made lowercase.
    Exp_upto_June = models.FloatField(db_column='Exp_upto_June', blank=True, null=True)  # Field name made lowercase.
    Projection_2017_18 = models.FloatField(db_column='Projection_2017-18', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Projection_2018_19 = models.FloatField(db_column='Projection_2018-19', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Throw_Forward = models.FloatField(db_column='Throw_Forward', blank=True, null=True)  # Field name made lowercase.
    Id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adp_report_201718'

#this is used
class AdpSchemes1018Mpr(models.Model):
    Id = models.AutoField(db_column='id', primary_key=True)
    Scheme_Name = models.CharField(db_column='Scheme Name', max_length=2500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Year = models.TextField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    GS_No = models.IntegerField(db_column='GS No', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    District = models.CharField(db_column='District', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    Sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Main_Sector = models.CharField(db_column='Main Sector', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Approval = models.TextField(db_column='Approval', blank=True, null=True)  # Field name made lowercase.
    Local_Capital = models.DecimalField(db_column='Local Capital', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Local_Revenue = models.DecimalField(db_column='Local Revenue', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Total_Capital = models.DecimalField(db_column='Total Capital', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Total_Revenue = models.DecimalField(db_column='Total Revenue', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid_Capital = models.DecimalField(db_column='Foreign Aid Capital', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid_Revenue = models.DecimalField(db_column='Foreign Aid Revenue', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid_Total = models.DecimalField(db_column='Foreign Aid Total', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Total_Cost = models.DecimalField(db_column='Total Cost', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Allocation = models.DecimalField(db_column='Allocation', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    Release = models.DecimalField(db_column='Release', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    Utilization = models.DecimalField(db_column='Utilization', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    Expense_Upto_June = models.DecimalField(db_column='Expense Upto June', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Projection_One = models.DecimalField(db_column='Projection One', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Projection_Two = models.DecimalField(db_column='Projection Two', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Throw_Forward = models.DecimalField(db_column='Throw Forward', max_digits=250, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'adp_schemes_10_18_mpr'

#this is used
class AdpYearlyFacts1018(models.Model):
    Year = models.TextField(db_column='year_old', blank=True, null=True)  # Field name made lowercase.
    District = models.CharField(db_column='District', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    Sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Main_Sector = models.CharField(db_column='Main Sector', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Approval = models.TextField(db_column='Approval', blank=True, null=True)  # Field name made lowercase.
    Schemes_Count = models.BigIntegerField(db_column='Schemes Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Local_Capital = models.FloatField(db_column='Local Capital', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Local_Revenue = models.FloatField(db_column='Local Revenue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Total_Capital = models.FloatField(db_column='Total Capital', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Total_Revenue = models.FloatField(db_column='Total Revenue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid_Capital = models.FloatField(db_column='Foreign Aid Capital', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid_Revenue = models.FloatField(db_column='Foreign Aid Revenue', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Foreign_Aid_Total = models.FloatField(db_column='Foreign Aid Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Total_Cost = models.FloatField(db_column='Total Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Allocation = models.FloatField(db_column='Allocation', blank=True, null=True)  # Field name made lowercase.
    Expense_Upto_June = models.FloatField(db_column='Expense Upto June', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Projection_One = models.FloatField(db_column='Projection One', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Projection_Two = models.FloatField(db_column='Projection Two', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Throw_Forward = models.FloatField(db_column='Throw Forward', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    Id = models.AutoField(db_column='id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'adp_yearly_facts_1018'
