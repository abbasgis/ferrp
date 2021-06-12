# from django.db import models

# Create your models here.
from django.contrib.gis.db import models


class TblSchools(models.Model):
    oid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(db_column='OBJECTID', blank=True, null=True)  # Field name made lowercase.
    srno_field = models.FloatField(db_column='Srno_', blank=True,
                                   null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    emiscode = models.FloatField(db_column='Emiscode', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    school_nam = models.CharField(db_column='School_Nam', max_length=254, blank=True,
                                  null=True)  # Field name made lowercase.
    district = models.CharField(db_column='DISTRICT', max_length=254, blank=True,
                                null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=254, blank=True, null=True)  # Field name made lowercase.
    level = models.CharField(db_column='Level', max_length=254, blank=True, null=True)  # Field name made lowercase.
    muza = models.CharField(db_column='Muza', max_length=254, blank=True, null=True)  # Field name made lowercase.
    near_fid = models.IntegerField(db_column='NEAR_FID', blank=True, null=True)  # Field name made lowercase.
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_schools_20180305040332823564'
        app_label = 'gis'


class TblHospitals(models.Model):
    oid = models.AutoField(primary_key=True)
    objectid_1 = models.IntegerField(db_column='OBJECTID_1', blank=True, null=True)  # Field name made lowercase.
    fid_punjab = models.IntegerField(db_column='FID_Punjab', blank=True, null=True)  # Field name made lowercase.
    objectid = models.IntegerField(db_column='OBJECTID', blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='PROVINCE', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shape_leng = models.FloatField(db_column='SHAPE_Leng', blank=True, null=True)  # Field name made lowercase.
    fid_pakist = models.IntegerField(db_column='FID_Pakist', blank=True, null=True)  # Field name made lowercase.
    long = models.FloatField(db_column='LONG', blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='LAT', blank=True, null=True)  # Field name made lowercase.
    province_1 = models.CharField(db_column='Province_1', max_length=60, blank=True,
                                  null=True)  # Field name made lowercase.
    hf_name = models.CharField(db_column='HF_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dist_name = models.CharField(db_column='Dist_Name', max_length=25, blank=True,
                                 null=True)  # Field name made lowercase.
    hf_type = models.CharField(db_column='HF_Type', max_length=30, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    near_fid = models.IntegerField(db_column='NEAR_FID', blank=True, null=True)  # Field name made lowercase.
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_hospital_20180222164038855331'
        app_label = 'gis'


class TblPopulation2015(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    envelope = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rst_population_2015_20180605083744316942'
        app_label = 'gis'


class TblGlCF(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.TextField(blank=True, null=True)  # This field type is a guess.
    envelope = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rst_glc0_20180604185708871393'
        app_label = 'gis'


class TblGlcPunjabClasses(models.Model):
    value = models.CharField(db_column='Value', max_length=255, primary_key=True)  # Field name made lowercase.
    count = models.CharField(db_column='Count', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classes = models.CharField(db_column='CLASSES', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'glc_punjab_classes'
        app_label = 'gis'


class TblFlood2010(models.Model):
    oid = models.AutoField(primary_key=True)
    updated = models.DateField(db_column='Updated', blank=True, null=True)  # Field name made lowercase.
    area_name = models.CharField(db_column='Area_name', max_length=254, blank=True,
                                 null=True)  # Field name made lowercase.
    shape_area = models.FloatField(db_column='Shape_Area', blank=True, null=True)  # Field name made lowercase.
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_flood_2010_20180517083901459264'
        app_label = 'gis'


class TblFlood2014(models.Model):
    oid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(db_column='OBJECTID', blank=True, null=True)  # Field name made lowercase.
    shape_area = models.FloatField(db_column='Shape_Area', blank=True, null=True)  # Field name made lowercase.
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gis_flood_2014_20180518041816254847'
        app_label = 'gis'


class TblEpicenter(models.Model):
    oid = models.AutoField(primary_key=True)
    epi_id = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'gis'
        db_table = 'gis_earthquake_epicenter_20180320143042027943'


class TblPGAInfo(models.Model):
    oid = models.AutoField(primary_key=True)
    id = models.IntegerField(db_column='Id', blank=True, null=True)  # Field name made lowercase.
    pga_inter = models.FloatField(blank=True, null=True)
    geom = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        app_label = 'gis'
        managed = False
        db_table = 'gis_pga_20180519054202030361'


class ClimateLocationNoaa(models.Model):
    station_id = models.IntegerField(blank=True, null=True)
    year_m_d = models.IntegerField(blank=True, null=True)
    date_acquired = models.DateField(blank=True, null=True)
    temp_fahrenheit = models.FloatField(blank=True, null=True)
    dew_point_fahrenheit = models.FloatField(blank=True, null=True)
    sea_level_pressure_mb = models.FloatField(blank=True, null=True)
    station_pressure_mb = models.FloatField(blank=True, null=True)
    visibility_miles = models.FloatField(blank=True, null=True)
    wind_speed_knots = models.FloatField(blank=True, null=True)
    maximum_sustained_wind_speed_knots = models.FloatField(blank=True, null=True)
    maximum_wind_gust_knots = models.FloatField(blank=True, null=True)
    maximum_temperature_fahrenheit = models.CharField(max_length=255, blank=True, null=True)
    min_temperature_fahrenheit = models.CharField(max_length=255, blank=True, null=True)
    precipitation_inches = models.FloatField(blank=True, null=True)
    precipitation_description = models.CharField(max_length=255, blank=True, null=True)
    snow_depth_inches = models.FloatField(blank=True, null=True)
    frshtt = models.IntegerField(db_column='FRSHTT', blank=True, null=True)  # Field name made lowercase.
    # code = models.IntegerField(blank=True, null=True)
    stations = models.CharField(max_length=255, blank=True, null=True)
    # country = models.CharField(max_length=255, blank=True, null=True)
    # st_code = models.CharField(max_length=255, blank=True, null=True)
    # latitude = models.FloatField(blank=True, null=True)
    # longitude = models.FloatField(blank=True, null=True)
    # elevation_m = models.FloatField(blank=True, null=True)
    # begin = models.IntegerField(blank=True, null=True)
    # end = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'gis'
        db_table = 'climate_location_noaa'


# Dams and barages db models
class PakDamsAndBarragesGS(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    dam_name = models.CharField(db_column='dam_name', max_length=254, blank=True, null=True)
    river = models.CharField(db_column='river', max_length=254, blank=True, null=True)
    main_basin = models.CharField(db_column='main_basin', max_length=254, blank=True, null=True)
    near_city = models.CharField(db_column='near_city', max_length=254, blank=True, null=True)
    catch_skm = models.DecimalField(db_column='catch_skm', max_digits=65535, decimal_places=65535, blank=True,
                                    null=True)
    main_use = models.CharField(db_column='main_use', max_length=254, blank=True, null=True)
    extent = models.CharField(db_column='extent', max_length=254, blank=True, null=True)
    geojson = models.CharField(db_column='geojson', max_length=254, blank=True, null=True)
    geom = models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'irrigation'
        db_table = 'gis_pakistan_dam_and_barrages'


class DischargeDataGS(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    discharge_date = models.DateField(db_column='discharge_date', max_length=254, blank=True, null=True)
    discharge_time = models.DateTimeField(db_column='discharge_time', max_length=254, blank=True, null=True)
    river = models.CharField(db_column='river', max_length=254, blank=True, null=True)
    head_works = models.CharField(db_column='head_works', max_length=254, blank=True, null=True)
    flow = models.CharField(db_column='flow', max_length=254, blank=True, null=True)
    us = models.FloatField(db_column='us', default=-1)
    ds = models.FloatField(db_column='ds', default=-1)

    class Meta:
        managed = False
        app_label = 'irrigation'
        db_table = 'discharge_data'


class TblWqDetailGS(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    year = models.IntegerField(db_column='year', blank=True, null=True)
    season = models.CharField(db_column='season', max_length=25, blank=True, null=True)
    quality_type = models.CharField(db_column='quality_type', max_length=25, blank=True, null=True)
    water_quality = models.DecimalField(db_column='water_quality', decimal_places=2, max_digits=25, blank=True,
                                        null=True)
    elevation = models.CharField(db_column='elevation', max_length=25, blank=True, null=True)
    ql_id = models.IntegerField(db_column='ql_id', blank=True, null=True)
    geom_text = models.CharField(db_column='geom_xy', max_length=50, blank=True, null=True)
    geom = models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'irrigation'
        db_table = 'gis_water_quality_detail'


class TblWlDetailGS(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    year = models.IntegerField(db_column='year', blank=True, null=True)
    season = models.CharField(db_column='season', max_length=25, blank=True, null=True)
    water_depth = models.DecimalField(db_column='water_depth', decimal_places=2, max_digits=25, blank=True, null=True,
                                      verbose_name='water_table_depth')
    elevation = models.DecimalField(db_column='elevation', decimal_places=2, max_digits=25, blank=True, null=True)
    ql_id = models.IntegerField(db_column='ql_id', blank=True, null=True)
    geom_text = models.CharField(db_column='geom_xy', max_length=50, blank=True, null=True)
    geom = models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'irrigation'
        db_table = 'gis_water_level_detail'
