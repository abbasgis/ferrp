from django.db import models

# Create your models here.


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