from __future__ import unicode_literals

from django.contrib.gis.db import models
from django import forms




class EvCrop(models.Model):
    gid = models.AutoField(primary_key=True)
    crop = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ev_crop'


class EvLandcover(models.Model):
    gid = models.AutoField(primary_key=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    agg_name = models.CharField(max_length=254, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ev_landcover'


class EvPopulationUcPhaseI(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    male_child = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    normalized = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    male_young = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    normaliz_1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    male_old = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    normaliz_2 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    female_chi = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    normaliz_3 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    female_you = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    normaliz_4 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    female_old = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    normaliz_5 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    arithmetic = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    square_root = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    vulnerabil = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ev_population_uc_phase_i'


class EvSocioEconomicUcPhaseIRevised(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    social_vulnerbility = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ev_socio_economic_uc_phase_i_revised'


class EvVulnerabilityUcPhaseI(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    disaster_v = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ev_vulnerability_uc_phase_i'


class GDistrictBoundary(models.Model):
    gid = models.AutoField(primary_key=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    distt_name = models.CharField(max_length=50, blank=True, null=True)
    piupdma_sd = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.CharField(max_length=10, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_district_boundary'


class GDivisionBoundary(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    div_name = models.CharField(max_length=50, blank=True, null=True)
    shape_le_1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_division_boundary'


class GFactory(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    join_count = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    target_fid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name1 = models.CharField(max_length=254, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    first_dist = models.CharField(max_length=100, blank=True, null=True)
    distt_name = models.CharField(max_length=50, blank=True, null=True)
    piupdma_sd = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.CharField(max_length=10, blank=True, null=True)
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_factory'


class GFloodProneEducationFacilities(models.Model):
    gid = models.AutoField(primary_key=True)
    survey_id = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    surveyor_n = models.CharField(max_length=254, blank=True, null=True)
    checked_un = models.CharField(max_length=254, blank=True, null=True)
    latitude = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    longitude = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    district_n = models.CharField(max_length=254, blank=True, null=True)
    tehsil_nam = models.CharField(max_length=254, blank=True, null=True)
    qanungoi_h = models.CharField(max_length=254, blank=True, null=True)
    patwar_cir = models.CharField(max_length=254, blank=True, null=True)
    mauza_name = models.CharField(max_length=254, blank=True, null=True)
    survey_typ = models.CharField(max_length=254, blank=True, null=True)
    respondent = models.CharField(max_length=254, blank=True, null=True)
    responde_1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    respondant = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    name_of_sc = models.CharField(max_length=254, blank=True, null=True)
    office_pho = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    responde_2 = models.CharField(max_length=254, blank=True, null=True)
    ownership = models.CharField(max_length=254, blank=True, null=True)
    level_of_i = models.CharField(max_length=254, blank=True, null=True)
    number_of_field = models.DecimalField(db_column='number_of_', max_digits=1000, decimal_places=1000, blank=True,
                                          null=True)  # Field renamed because it ended with '_'.
    number_of1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    number_o_1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    number_o_2 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    electricit = models.CharField(max_length=254, blank=True, null=True)
    boundry_wa = models.CharField(max_length=254, blank=True, null=True)
    age_of_bui = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    type_of_co = models.CharField(max_length=254, blank=True, null=True)
    plenth_lev = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    security_g = models.CharField(max_length=254, blank=True, null=True)
    emergency_field = models.CharField(db_column='emergency_', max_length=254, blank=True,
                                       null=True)  # Field renamed because it ended with '_'.
    evacuation = models.CharField(max_length=254, blank=True, null=True)
    building_e = models.CharField(max_length=254, blank=True, null=True)
    type_of_de = models.CharField(max_length=254, blank=True, null=True)
    level_of_d = models.CharField(max_length=254, blank=True, null=True)
    level_field = models.CharField(db_column='level_', max_length=100, blank=True,
                                   null=True)  # Field renamed because it ended with '_'.
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_flood_prone_education_facilities'


class GFloodProneHealthFacilities(models.Model):
    gid = models.AutoField(primary_key=True)
    survey_id = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    surveyor_n = models.CharField(max_length=254, blank=True, null=True)
    checked_un = models.CharField(max_length=254, blank=True, null=True)
    latitude = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    longitude = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    district_n = models.CharField(max_length=254, blank=True, null=True)
    tehsil_nam = models.CharField(max_length=254, blank=True, null=True)
    qanungoi_h = models.CharField(max_length=254, blank=True, null=True)
    patwar_cir = models.CharField(max_length=254, blank=True, null=True)
    mauza_name = models.CharField(max_length=254, blank=True, null=True)
    survey_typ = models.CharField(max_length=254, blank=True, null=True)
    respondent = models.CharField(max_length=254, blank=True, null=True)
    responde_1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    respondant = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    name_of_he = models.CharField(max_length=254, blank=True, null=True)
    medical_fa = models.CharField(max_length=254, blank=True, null=True)
    official_p = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    ownership = models.CharField(max_length=254, blank=True, null=True)
    number_of_field = models.DecimalField(db_column='number_of_', max_digits=1000, decimal_places=1000, blank=True,
                                          null=True)  # Field renamed because it ended with '_'.
    number_of1 = models.CharField(max_length=254, blank=True, null=True)
    number_o_1 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    number_o_2 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    number_o_3 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    snake_byte = models.CharField(max_length=254, blank=True, null=True)
    epidemic_d = models.CharField(max_length=254, blank=True, null=True)
    type_of_co = models.CharField(max_length=254, blank=True, null=True)
    number_o_4 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    number_o_5 = models.CharField(max_length=254, blank=True, null=True)
    number_o_6 = models.CharField(max_length=254, blank=True, null=True)
    last_epide = models.CharField(max_length=254, blank=True, null=True)
    health_inf = models.CharField(max_length=254, blank=True, null=True)
    boundry_wa = models.CharField(max_length=254, blank=True, null=True)
    age_of_bui = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    plenth_lev = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    security_g = models.CharField(max_length=254, blank=True, null=True)
    emergency_field = models.CharField(db_column='emergency_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    evacuation = models.CharField(max_length=254, blank=True, null=True)
    building_e = models.CharField(max_length=254, blank=True, null=True)
    type_of_de = models.CharField(max_length=254, blank=True, null=True)
    level_of_d = models.CharField(max_length=254, blank=True, null=True)
    query = models.CharField(max_length=10, blank=True, null=True)
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_flood_prone_health_facilities'


class GHeadwork(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    geom = models.PointField(srid=3857, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_headwork'


class GIndustry(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    join_count = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    target_fid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name1 = models.CharField(max_length=254, blank=True, null=True)
    other_name = models.CharField(max_length=254, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    first_dist = models.CharField(max_length=100, blank=True, null=True)
    distt_name = models.CharField(max_length=50, blank=True, null=True)
    piupdma_sd = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.CharField(max_length=10, blank=True, null=True)
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_industry'


class GPopulationDensity(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    population = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    males_201 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    females_2 = models.DecimalField(db_column='females__2', max_digits=10, decimal_places=0, blank=True,
                                    null=True)  # Field renamed because it contained more than one '_' in a row.
    age_group = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_gorup1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_2 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_3 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_4 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_5 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_6 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_chec = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_7 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_8 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_goru_9 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_gor_10 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_gor_11 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_gor_12 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_gor_13 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    age_gor_14 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_ch_1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    no_of_hous = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_uc_a = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    total_road = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    total_health = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_education = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pop_densty = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_population_density'


class GPunjabDistricts(models.Model):
    gid = models.AutoField(primary_key=True)
    distt_name = models.CharField(max_length=50, blank=True, null=True)
    area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.CharField(max_length=10, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_punjab_districts'


class GRailway(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name1 = models.CharField(max_length=70, blank=True, null=True)
    disp_class = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created_us = models.CharField(max_length=254, blank=True, null=True)
    created_da = models.DateField(blank=True, null=True)
    last_edite = models.CharField(max_length=254, blank=True, null=True)
    last_edi_1 = models.DateField(blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiLineStringField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_railway'


class GRailwayStation(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid_2 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    classifica = models.CharField(max_length=50, blank=True, null=True)
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_railway_station'


class GRivers(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    layer = models.CharField(max_length=17, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_rivers'


class GRoads(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    f_junc = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    t_junc = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    rc = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    rt = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    srt = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    rs = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    structure = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    toll = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    oneway = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vtr_pos = models.CharField(max_length=8, blank=True, null=True)
    vtr_neg = models.CharField(max_length=8, blank=True, null=True)
    spd_pos = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    spd_neg = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    spd_valid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    kph_pos = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    kph_neg = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    kph_valid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    f_level = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    t_level = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    prefix1 = models.CharField(max_length=15, blank=True, null=True)
    stname1 = models.CharField(max_length=70, blank=True, null=True)
    suffix1 = models.CharField(max_length=15, blank=True, null=True)
    alt_prefix = models.CharField(max_length=15, blank=True, null=True)
    alt_stname = models.CharField(max_length=70, blank=True, null=True)
    alt_suffix = models.CharField(max_length=15, blank=True, null=True)
    alt_pref_1 = models.CharField(max_length=15, blank=True, null=True)
    alt_stna_1 = models.CharField(max_length=70, blank=True, null=True)
    alt_suff_1 = models.CharField(max_length=15, blank=True, null=True)
    routenum1 = models.CharField(max_length=30, blank=True, null=True)
    i_routenum = models.CharField(max_length=15, blank=True, null=True)
    l_scheme = models.CharField(max_length=1, blank=True, null=True)
    l_numbers = models.CharField(max_length=150, blank=True, null=True)
    r_scheme = models.CharField(max_length=1, blank=True, null=True)
    r_numbers = models.CharField(max_length=150, blank=True, null=True)
    l_admin8_1 = models.CharField(max_length=70, blank=True, null=True)
    r_admin8_1 = models.CharField(max_length=70, blank=True, null=True)
    l_admin9_1 = models.CharField(max_length=70, blank=True, null=True)
    r_admin9_1 = models.CharField(max_length=70, blank=True, null=True)
    l_adminid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    r_adminid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    l_postcode = models.CharField(max_length=10, blank=True, null=True)
    r_postcode = models.CharField(max_length=10, blank=True, null=True)
    u_turn = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    bua = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    bua_valid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    cj = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    lanes = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name_org = models.CharField(max_length=150, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiLineStringField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_roads'


class GSchools(models.Model):
    gid = models.AutoField(primary_key=True)
    msi = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    sch = models.CharField(max_length=250, blank=True, null=True)
    gnd = models.CharField(max_length=50, blank=True, null=True)
    lvl = models.CharField(max_length=25, blank=True, null=True)
    moza = models.CharField(max_length=250, blank=True, null=True)
    lat = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    lon = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_schools'


class GSettlements(models.Model):
    gid = models.AutoField(primary_key=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_settlements'


class GTehsilBoundary(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    first_dist = models.CharField(max_length=100, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_tehsil_boundary'


class GUcBoundary(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    flooded = models.CharField(max_length=20, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_uc_boundary'


class GUcCentroidCrop(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    flooded = models.CharField(max_length=20, blank=True, null=True)
    orig_fid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    rice = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    sugarcane = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_uc_centroid_crop'


class GWaterChannel(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    layer = models.CharField(max_length=17, blank=True, null=True)
    map_name = models.CharField(max_length=19, blank=True, null=True)
    division = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiLineStringField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_water_channel'


class HDrought(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    id_1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    id_12 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    vci_99 = models.CharField(max_length=254, blank=True, null=True)
    vhi_99 = models.CharField(max_length=254, blank=True, null=True)
    tci_99 = models.CharField(max_length=254, blank=True, null=True)
    fd_99 = models.CharField(max_length=254, blank=True, null=True)
    fd_991 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    max_99 = models.CharField(max_length=254, blank=True, null=True)
    max_991 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    min_99 = models.CharField(max_length=254, blank=True, null=True)
    min_991 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    vci_2000 = models.CharField(max_length=254, blank=True, null=True)
    vhi_2000 = models.CharField(max_length=254, blank=True, null=True)
    tci_2000 = models.CharField(max_length=254, blank=True, null=True)
    fd_2000 = models.CharField(max_length=254, blank=True, null=True)
    fd_20001 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    max_2000 = models.CharField(max_length=254, blank=True, null=True)
    max_20001 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    min_2000 = models.CharField(max_length=254, blank=True, null=True)
    min_20001 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    vci_2001 = models.CharField(max_length=254, blank=True, null=True)
    vhi_2001 = models.CharField(max_length=254, blank=True, null=True)
    tci_2001 = models.CharField(max_length=254, blank=True, null=True)
    fd_2001 = models.CharField(max_length=254, blank=True, null=True)
    fd_20011 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    max_2001 = models.CharField(max_length=254, blank=True, null=True)
    max_20011 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    min_2001 = models.CharField(max_length=254, blank=True, null=True)
    min_20011 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    vci_2002 = models.CharField(max_length=254, blank=True, null=True)
    vhi_2002 = models.CharField(max_length=254, blank=True, null=True)
    tci_2002 = models.CharField(max_length=254, blank=True, null=True)
    fd_2002 = models.CharField(max_length=254, blank=True, null=True)
    fd_20021 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    max_2002 = models.CharField(max_length=254, blank=True, null=True)
    max_20021 = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    severity_d = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    hdcl = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_drought'


class HEarthquake0050(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pga = models.FloatField(blank=True, null=True)
    vs30 = models.FloatField(blank=True, null=True)
    site_response = models.FloatField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_earthquake_0050'


class HEarthquake0100(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pga = models.FloatField(blank=True, null=True)
    vs30 = models.FloatField(blank=True, null=True)
    site_response = models.FloatField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_earthquake_0100'


class HEarthquake0250(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pga = models.FloatField(blank=True, null=True)
    vs30 = models.FloatField(blank=True, null=True)
    site_response = models.FloatField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_earthquake_0250'


class HEarthquake0475(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pga = models.FloatField(blank=True, null=True)
    vs30 = models.FloatField(blank=True, null=True)
    site_response = models.FloatField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_earthquake_0475'


class HEarthquake1000(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pga = models.FloatField(blank=True, null=True)
    vs30 = models.FloatField(blank=True, null=True)
    site_response = models.FloatField(blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_earthquake_1000'


class HFlood005(models.Model):
    gid = models.AutoField(primary_key=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    dist = models.CharField(max_length=35, blank=True, null=True)
    teh = models.CharField(max_length=35, blank=True, null=True)
    uc_name = models.CharField(max_length=35, blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True)
    depth_m = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_flood_005'


class HFlood010(models.Model):
    gid = models.AutoField(primary_key=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    dist = models.CharField(max_length=35, blank=True, null=True)
    teh = models.CharField(max_length=35, blank=True, null=True)
    uc_name = models.CharField(max_length=35, blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True)
    depth_m = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_flood_010'


class HFlood025(models.Model):
    gid = models.AutoField(primary_key=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    dist = models.CharField(max_length=35, blank=True, null=True)
    teh = models.CharField(max_length=35, blank=True, null=True)
    uc_name = models.CharField(max_length=35, blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True)
    depth_m = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_flood_025'


class HFlood050(models.Model):
    gid = models.AutoField(primary_key=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    dist = models.CharField(max_length=35, blank=True, null=True)
    teh = models.CharField(max_length=35, blank=True, null=True)
    uc_name = models.CharField(max_length=35, blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True)
    depth_m = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_flood_050'


class HFlood100(models.Model):
    gid = models.AutoField(primary_key=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    dist = models.CharField(max_length=35, blank=True, null=True)
    teh = models.CharField(max_length=35, blank=True, null=True)
    uc_name = models.CharField(max_length=35, blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True)
    depth_m = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_flood_100'


class HFlood250(models.Model):
    gid = models.AutoField(primary_key=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    dist = models.CharField(max_length=35, blank=True, null=True)
    teh = models.CharField(max_length=35, blank=True, null=True)
    uc_name = models.CharField(max_length=35, blank=True, null=True)
    code = models.CharField(max_length=15, blank=True, null=True)
    depth_m = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_flood_250'


class Layer(models.Model):
    topology = models.ForeignKey('Topology', models.DO_NOTHING, primary_key=True)
    layer_id = models.IntegerField()
    schema_name = models.CharField(max_length=250)
    table_name = models.CharField(max_length=250)
    feature_column = models.CharField(max_length=250)
    feature_type = models.IntegerField()
    level = models.IntegerField()
    child_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layer'
        unique_together = (('topology', 'layer_id'), ('schema_name', 'table_name', 'feature_column'),)


class RCompositeRisk050(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_composite_risk_050'


class RDroughtRiskClasses(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_drought_risk_classes'


class REarthquakeRisk0050(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_earthquake_risk_0050'


class REarthquakeRisk0100(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_earthquake_risk_0100'


class REarthquakeRisk0250(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_earthquake_risk_0250'


class REarthquakeRisk0475(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_earthquake_risk_0475'


class REarthquakeRisk1000(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_length = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_earthquake_risk_1000'


class RFloodRisk005(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_flood_risk_005'


class RFloodRisk025(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_flood_risk_025'


class RFloodRisk050(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_flood_risk_050'


class RFloodRisk100(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_length = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_flood_risk_100'


class RFloodRisk250(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100, blank=True, null=True)
    uc_name = models.CharField(max_length=100, blank=True, null=True)
    uc_no = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    shape_length = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)
    phase = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gis_id = models.CharField(max_length=20, blank=True, null=True)
    uc_id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    risk_class = models.CharField(max_length=254, blank=True, null=True)
    geom = models.MultiPolygonField(srid=3857, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_flood_risk_250'


class Topology(models.Model):
    name = models.CharField(unique=True, max_length=250)
    srid = models.IntegerField()
    precision = models.FloatField()
    hasz = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'topology'

class MhvraSectionOne(models.Model):
    soid = models.AutoField(primary_key=True)
    # project=models.ForeignKey(blank=True)
    project_name = models.CharField(max_length=100, blank=False,unique=True)
    project_type = models.CharField(max_length=100, blank=True, null=True)
    project_extend = models.CharField(max_length=100, blank=True, null=True)
    project_climate_condition = models.CharField(max_length=100, blank=True, null=True)
    rainfall_value = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    return_period = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    project_location_features = models.CharField(max_length=100, blank=False)
    public_places_nearby = models.CharField(max_length=100, blank=False)
    project_id = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        managed = False
        db_table = 'mhvra_section_one'

class mhvra_section_two(models.Model):
    stid = models.AutoField(primary_key=True)
    recongized_hazard = models.CharField(max_length=200, blank=True, null=True)
    earthquake = models.CharField(max_length=200, blank=True, null=True)
    landslide = models.CharField(max_length=200, blank=True, null=True)
    flood = models.CharField(max_length=200, blank=True, null=True)
    glof = models.CharField(max_length=200, blank=True, null=True)
    slope_failure = models.CharField(max_length=200, blank=True, null=True)
    heavy_rain = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    other_name = models.CharField(max_length=200, blank=True, null=True)
    landslide_data= models.NullBooleanField(blank=True, null=True)
    landslide_return_period=models.IntegerField(blank=True, null=True)
    flood_data = models.NullBooleanField(blank=True, null=True)
    flood_return_period = models.IntegerField(blank=True, null=True)
    forest_reserves_data = models.NullBooleanField(blank=True, null=True)
    forest_reserves_return_period = models.IntegerField(blank=True, null=True)
    nature_reserves_data = models.NullBooleanField(blank=True, null=True)
    nature_reserves_return_period = models.IntegerField(blank=True, null=True)
    riverine_conservation_data = models.NullBooleanField(blank=True, null=True)
    riverine_conservation_return_period = models.IntegerField(blank=True, null=True)
    wetlands_data = models.NullBooleanField(blank=True, null=True)
    wetlands_return_period = models.IntegerField(blank=True, null=True)
    # marshy_data = models.BooleanField(blank=True, null=False)
    # marshy_return_period = models.IntegerField(blank=True, null=True)
    archeological_data = models.NullBooleanField(blank=True, null=True)
    archeological_return_period = models.IntegerField(blank=True, null=True)
    culture_data = models.NullBooleanField(blank=True, null=True)
    culture_data_return_period = models.IntegerField(blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    project_id = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'mhvra_section_two'

class SectionFour(models.Model):
    # project_id = models.ForeignKey(MhvraSectionOne)
    # file_name = models.CharField(max_length=255, blank=True)
    # filedoc = models.FileField(upload_to='documents/')
    building_codes = models.CharField(max_length=255, blank=True, null=True)
    building_bye_laws = models.CharField(max_length=255, blank=True, null=True)
    disaster_risk_reduction = models.CharField(max_length=255, blank=True, null=True)
    flood_hazard_guideline = models.CharField(max_length=255, blank=True, null=True)
    environmental_impact_assessment_field = models.CharField(db_column='environmental_impact_assessment ', max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    sf_id = models.AutoField(primary_key=True)
    project_id = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'section_four'



class SectionFourFiles(models.Model):
    filedoc = models.FileField(upload_to='dia/')
    sfid = models.ForeignKey(SectionFour, models.DO_NOTHING, db_column='sfid', blank=True, null=True)
    fid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'section_four_Files'

class SectionFive(models.Model):
    cid = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section_five'

class TblprojectMhvra(models.Model):

    project_id = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    update_at = models.DateTimeField(blank=True, null=True)
    mhvra_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=1000, blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'tblproject_mhvra'


class SectionFive(models.Model):
    cid = models.AutoField(primary_key=True)
    project_id = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section_five'