from __future__ import unicode_literals

# from django.db import models
from django.contrib.gis.db import models

class Administrativecontacts(models.Model):
    name = models.CharField(db_column='Name', max_length=250, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=250, blank=True, null=True)  # Field name made lowercase.
    contact = models.IntegerField(db_column='Contact', blank=True, null=True)  # Field name made lowercase.
    tehsilid = models.CharField(db_column='TehsilID', max_length=250, blank=True, null=True)  # Field name made lowercase.
    districtid = models.CharField(db_column='DistrictID', max_length=250, blank=True, null=True)  # Field name made lowercase.
    divisionid = models.CharField(db_column='DivisionID', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AdministrativeContacts'


class FloodfightingEquipment(models.Model):
    district = models.CharField(db_column='District', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ambulances = models.BigIntegerField(db_column='Ambulances', blank=True, null=True)  # Field name made lowercase.
    boats = models.BigIntegerField(db_column='Boats', blank=True, null=True)  # Field name made lowercase.
    cars = models.BigIntegerField(db_column='Cars', blank=True, null=True)  # Field name made lowercase.
    dewateringsets = models.BigIntegerField(db_column='DeWateringSets', blank=True, null=True)  # Field name made lowercase.
    lifejackets = models.BigIntegerField(db_column='LifeJackets', blank=True, null=True)  # Field name made lowercase.
    minitrucks = models.BigIntegerField(db_column='MiniTrucks', blank=True, null=True)  # Field name made lowercase.
    pickups = models.BigIntegerField(db_column='Pickups', blank=True, null=True)  # Field name made lowercase.
    tractors = models.BigIntegerField(db_column='Tractors', blank=True, null=True)  # Field name made lowercase.
    watertanks = models.BigIntegerField(db_column='WaterTanks', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FloodFighting_Equipment'


class FloodFightingplan(models.Model):
    equipment_name = models.CharField(db_column='Equipment_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    count = models.BigIntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    operational = models.BigIntegerField(db_column='Operational', blank=True, null=True)  # Field name made lowercase.
    non_operational = models.BigIntegerField(db_column='Non_Operational', blank=True, null=True)  # Field name made lowercase.
    id = models.BigIntegerField(primary_key=True)
    district_name = models.CharField(db_column='District_Name', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Flood_FightingPlan'


class Guage(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    guage_location = models.TextField(db_column='Guage_Location', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    guage_axis = models.TextField(db_column='Guage_Axis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    average_height = models.IntegerField(db_column='Average_Height', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Guage'


class GuageData(models.Model):
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    guage_height_upstream = models.FloatField(db_column='Guage_Height_UpStream', blank=True, null=True)  # Field name made lowercase.
    guage_height_downstream = models.FloatField(db_column='Guage_Height_DownStream', blank=True, null=True)  # Field name made lowercase.
    discharge_upstream = models.FloatField(db_column='Discharge_UpStream', blank=True, null=True)  # Field name made lowercase.
    discharge_downstream = models.FloatField(db_column='Discharge_DownStream', blank=True, null=True)  # Field name made lowercase.
    sr_no = models.IntegerField(db_column='Sr_No', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Guage_Data'


class MessageData(models.Model):
    mid = models.AutoField(db_column='Mid', primary_key=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=250)  # Field name made lowercase.
    messages = models.CharField(db_column='Messages', max_length=1000)  # Field name made lowercase.
    contact_number = models.CharField(db_column='Contact_Number', max_length=15)  # Field name made lowercase.
    ref_id = models.BigIntegerField(db_column='Ref_Id', blank=True, null=True)  # Field name made lowercase.
    date_time = models.TextField(db_column='Date_Time')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Message_Data'


class SchoolsOfPunjab(models.Model):
    gid = models.BigAutoField(primary_key=True)
    emiscode = models.IntegerField(blank=True, null=True)
    school_name = models.CharField(max_length=254, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    lavel = models.CharField(max_length=254, blank=True, null=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    muza = models.CharField(max_length=254, blank=True, null=True)
    uc_name = models.CharField(max_length=254, blank=True, null=True)
    uc = models.ForeignKey('Uc', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Schools of Punjab'


class Districts(models.Model):
    gid = models.AutoField(primary_key=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    area_km2 = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    pro = models.ForeignKey('Province', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'districts'


class Divisions(models.Model):
    gid = models.AutoField(primary_key=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    area_km2 = models.IntegerField(blank=True, null=True)
    divsion = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'divisions'


class FloodExtent2010(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    water_clas = models.SmallIntegerField(blank=True, null=True)
    sensor_id = models.IntegerField(blank=True, null=True)
    sensor_dat = models.DateField(blank=True, null=True)
    confidence = models.SmallIntegerField(blank=True, null=True)
    field_vali = models.SmallIntegerField(blank=True, null=True)
    area_m2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    area_ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'flood_extent2010'


class Healthfacility(models.Model):
    gid = models.AutoField(primary_key=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    hf_type = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'healthfacility'


class Indus(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    descriptio = models.CharField(max_length=80, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'indus'


class Indus10Km(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=18, blank=True, null=True)
    category = models.CharField(max_length=24, blank=True, null=True)
    buff_dist = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'indus_10km'


class LingusticDischarges(models.Model):
    id = models.IntegerField(primary_key=True)
    reach = models.CharField(max_length=250, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    lingustic_value = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lingustic_Discharges'


class PointcloudFormats(models.Model):
    pcid = models.IntegerField(primary_key=True)
    srid = models.IntegerField(blank=True, null=True)
    schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pointcloud_formats'


class Province(models.Model):
    gid = models.AutoField(primary_key=True)
    ogr_fid = models.FloatField(blank=True, null=True)
    province = models.CharField(max_length=90, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'province'


class Reliefcamps(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    tehsil = models.CharField(max_length=254, blank=True, null=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    province = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reliefcamps'


class Roads(models.Model):
    gid = models.AutoField(primary_key=True)
    length = models.FloatField(blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'roads'


class Settlements(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    id_1 = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=30, blank=True, null=True)
    tehsil = models.CharField(max_length=50, blank=True, null=True)
    uc = models.CharField(max_length=50, blank=True, null=True)
    district_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'settlements'


class Settlementsinfo(models.Model):
    villagename = models.CharField(db_column='villageName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unioncouncil = models.CharField(db_column='unionCouncil', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tehsil = models.CharField(max_length=255, blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    noofdisabledperson = models.BigIntegerField(db_column='noofDisabledPerson', blank=True, null=True)  # Field name made lowercase.
    no_of_household = models.BigIntegerField(db_column='no of Household', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    noofelders = models.BigIntegerField(db_column='noofElders', blank=True, null=True)  # Field name made lowercase.
    noofgodown = models.BigIntegerField(db_column='noofGodown', blank=True, null=True)  # Field name made lowercase.
    croparea = models.BigIntegerField(db_column='cropArea', blank=True, null=True)  # Field name made lowercase.
    typeofcrop = models.CharField(db_column='typeofCrop', max_length=255, blank=True, null=True)  # Field name made lowercase.
    noofschools = models.BigIntegerField(db_column='noofSchools', blank=True, null=True)  # Field name made lowercase.
    statusofschoolinfrastructure = models.CharField(db_column='statusofSchoolInfrastructure', max_length=255, blank=True, null=True)  # Field name made lowercase.
    noofschoolgoigchildren = models.BigIntegerField(db_column='noofSchoolgoigChildren', blank=True, null=True)  # Field name made lowercase.
    noofteachers = models.BigIntegerField(db_column='noofTeachers', blank=True, null=True)  # Field name made lowercase.
    noofhouses = models.BigIntegerField(db_column='noofHouses', blank=True, null=True)  # Field name made lowercase.
    noofkutchahouses = models.BigIntegerField(db_column='noofKutchaHouses', blank=True, null=True)  # Field name made lowercase.
    typeofenterprises = models.CharField(db_column='typeofEnterprises', max_length=255, blank=True, null=True)  # Field name made lowercase.
    governmentfacilities = models.CharField(db_column='governmentFacilities', max_length=255, blank=True, null=True)  # Field name made lowercase.
    presenceofcheckpost = models.CharField(max_length=255, blank=True, null=True)
    contactimammasjid = models.CharField(db_column='contactImammasjid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nameimammasjid = models.CharField(db_column='NameImamMasjid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contactschoolteacher = models.CharField(db_column='contactschoolTeacher', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nameofteacher = models.CharField(db_column='NameOfTeacher', max_length=255, blank=True, null=True)  # Field name made lowercase.
    noofhealthfacilities = models.BigIntegerField(db_column='noofHealthfacilities', blank=True, null=True)  # Field name made lowercase.
    availabilityofhealthfacility = models.CharField(db_column='availabilityofHealthfacility', max_length=255, blank=True, null=True)  # Field name made lowercase.
    statusofhealthfacility = models.CharField(db_column='statusofHealthfacility', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estimatemedication = models.CharField(db_column='estimateMedication', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contactdoctors = models.CharField(db_column='contactDoctors', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nameofdoctor = models.CharField(db_column='NameofDoctor', max_length=255, blank=True, null=True)  # Field name made lowercase.
    availabilityofoil = models.CharField(db_column='availabilityofOil', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hightransmissionlines = models.CharField(db_column='highTransmissionlines', max_length=255, blank=True, null=True)  # Field name made lowercase.
    majorcanalswater = models.CharField(db_column='majorCanalswater', max_length=255, blank=True, null=True)  # Field name made lowercase.
    marginalbund = models.CharField(db_column='marginalBund', max_length=255, blank=True, null=True)  # Field name made lowercase.
    streetsdrains = models.CharField(db_column='streetsDrains', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pipedsewarage = models.CharField(db_column='pipedSewarage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    wastewater = models.CharField(db_column='wasteWater', max_length=255, blank=True, null=True)  # Field name made lowercase.
    statusofroad = models.CharField(db_column='statusofRoad', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gid = models.BigAutoField(primary_key=True)
    livestock = models.BigIntegerField(blank=True, null=True)
    focalperson = models.BigIntegerField(blank=True, null=True)
    contactcommunity = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settlementsInfo'


# class SpatialRefSys(models.Model):
#     srid = models.IntegerField(primary_key=True)
#     auth_name = models.CharField(max_length=256, blank=True, null=True)
#     auth_srid = models.IntegerField(blank=True, null=True)
#     srtext = models.CharField(max_length=2048, blank=True, null=True)
#     proj4text = models.CharField(max_length=2048, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'spatial_ref_sys'


class Tehsil(models.Model):
    gid = models.AutoField(primary_key=True)
    perimeter = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    area_km2 = models.FloatField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    tehsil = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    district_fk = models.ForeignKey(Districts, models.DO_NOTHING, db_column='district_FK', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tehsil'


class Uc(models.Model):
    gid = models.AutoField(primary_key=True)
    province = models.CharField(max_length=254, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    tehsil = models.CharField(max_length=30, blank=True, null=True)
    uc_name = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    tehsil_fk = models.ForeignKey(Tehsil, models.DO_NOTHING, db_column='tehsil_FK', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'uc'