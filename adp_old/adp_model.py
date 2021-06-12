# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Addr(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    fromhn = models.CharField(max_length=12, blank=True, null=True)
    tohn = models.CharField(max_length=12, blank=True, null=True)
    side = models.CharField(max_length=1, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    plus4 = models.CharField(max_length=4, blank=True, null=True)
    fromtyp = models.CharField(max_length=1, blank=True, null=True)
    totyp = models.CharField(max_length=1, blank=True, null=True)
    fromarmid = models.IntegerField(blank=True, null=True)
    toarmid = models.IntegerField(blank=True, null=True)
    arid = models.CharField(max_length=22, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addr'


class Addrfeat(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    statefp = models.CharField(max_length=2)
    aridl = models.CharField(max_length=22, blank=True, null=True)
    aridr = models.CharField(max_length=22, blank=True, null=True)
    linearid = models.CharField(max_length=22, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    lfromhn = models.CharField(max_length=12, blank=True, null=True)
    ltohn = models.CharField(max_length=12, blank=True, null=True)
    rfromhn = models.CharField(max_length=12, blank=True, null=True)
    rtohn = models.CharField(max_length=12, blank=True, null=True)
    zipl = models.CharField(max_length=5, blank=True, null=True)
    zipr = models.CharField(max_length=5, blank=True, null=True)
    edge_mtfcc = models.CharField(max_length=5, blank=True, null=True)
    parityl = models.CharField(max_length=1, blank=True, null=True)
    parityr = models.CharField(max_length=1, blank=True, null=True)
    plus4l = models.CharField(max_length=4, blank=True, null=True)
    plus4r = models.CharField(max_length=4, blank=True, null=True)
    lfromtyp = models.CharField(max_length=1, blank=True, null=True)
    ltotyp = models.CharField(max_length=1, blank=True, null=True)
    rfromtyp = models.CharField(max_length=1, blank=True, null=True)
    rtotyp = models.CharField(max_length=1, blank=True, null=True)
    offsetl = models.CharField(max_length=1, blank=True, null=True)
    offsetr = models.CharField(max_length=1, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'addrfeat'


class AdpDistrict(models.Model):
    name = models.CharField(max_length=5000, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adp_district'


class AdpDraft(models.Model):
    lo_no_cap = models.CharField(db_column='LO_No_CAP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lo_no_rev = models.CharField(db_column='LO_No_REV', max_length=255, blank=True, null=True)  # Field name made lowercase.
    old_gs_no_2014_15 = models.CharField(db_column='Old_GS_No_2014-15', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name_of_scheme = models.CharField(db_column='Name_of_Scheme', max_length=500, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=500, blank=True, null=True)  # Field name made lowercase.
    tehsil = models.CharField(db_column='Tehsil', max_length=500, blank=True, null=True)  # Field name made lowercase.
    pp_no = models.CharField(db_column='PP_No', max_length=500, blank=True, null=True)  # Field name made lowercase.
    approval_revision_date = models.CharField(db_column='Approval _Revision_Date', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid = models.FloatField(db_column='Foreign_aid', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    major_components = models.CharField(db_column='Major_Components', max_length=255, blank=True, null=True)  # Field name made lowercase.
    major_targets = models.CharField(db_column='Major_Targets', max_length=255, blank=True, null=True)  # Field name made lowercase.
    exp_upto_june_2015 = models.FloatField(db_column='Exp_upto_June_2015', blank=True, null=True)  # Field name made lowercase.
    localcapital = models.FloatField(db_column='LocalCapital', blank=True, null=True)  # Field name made lowercase.
    localrevenue = models.FloatField(db_column='LocalRevenue', blank=True, null=True)  # Field name made lowercase.
    foreigncapital = models.FloatField(db_column='ForeignCapital', blank=True, null=True)  # Field name made lowercase.
    foreignrevenue = models.FloatField(db_column='ForeignRevenue', blank=True, null=True)  # Field name made lowercase.
    totalcapital = models.FloatField(db_column='TotalCapital', blank=True, null=True)  # Field name made lowercase.
    totalrevenue = models.FloatField(db_column='TotalRevenue', blank=True, null=True)  # Field name made lowercase.
    grandtotal = models.FloatField(db_column='GrandTotal', blank=True, null=True)  # Field name made lowercase.
    pnd_proposed_allocation = models.FloatField(db_column='PND_Proposed_Allocation', blank=True, null=True)  # Field name made lowercase.
    projectionfor201718 = models.FloatField(db_column='Projectionfor201718', blank=True, null=True)  # Field name made lowercase.
    projectionfor201819 = models.FloatField(db_column='Projectionfor201819', blank=True, null=True)  # Field name made lowercase.
    throwforwardbeyond = models.FloatField(db_column='ThrowForwardBeyond', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subtype = models.CharField(db_column='SubType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subtype1 = models.CharField(max_length=255, blank=True, null=True)
    pref = models.CharField(db_column='Pref', max_length=255, blank=True, null=True)  # Field name made lowercase.
    secid = models.CharField(db_column='SecId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lono = models.CharField(db_column='LONo', max_length=-1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adp_draft'


class AdpSchemes1018(models.Model):
    gs_no = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    scheme_name = models.CharField(max_length=2500, blank=True, null=True)
    district = models.CharField(max_length=2500, blank=True, null=True)
    tehsil = models.CharField(max_length=2500, blank=True, null=True)
    constituency = models.CharField(max_length=5000, blank=True, null=True)
    approval_status = models.CharField(max_length=255, blank=True, null=True)
    est_cost_faid = models.FloatField(blank=True, null=True)
    est_cost_total = models.FloatField(blank=True, null=True)
    exp_upto_june = models.FloatField(blank=True, null=True)
    local_capital = models.FloatField(blank=True, null=True)
    local_revenue = models.FloatField(blank=True, null=True)
    faid_capital = models.FloatField(blank=True, null=True)
    faid_revenue = models.FloatField(blank=True, null=True)
    total_capital = models.FloatField(blank=True, null=True)
    total_revenue = models.FloatField(blank=True, null=True)
    total_capital_revenue = models.FloatField(blank=True, null=True)
    projection_one = models.FloatField(blank=True, null=True)
    projection_two = models.FloatField(blank=True, null=True)
    throw_forward = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    adptype = models.FloatField(blank=True, null=True)
    year_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    sector_id = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    main_sector_id = models.IntegerField(blank=True, null=True)
    allocation = models.FloatField(blank=True, null=True)
    approval = models.TextField(blank=True, null=True)
    release = models.FloatField(blank=True, null=True)
    utilization = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adp_schemes_1018'


class AdpSchemesLast5Yr(models.Model):
    gs_no = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    scheme_name = models.CharField(max_length=5000, blank=True, null=True)
    tehsil = models.CharField(max_length=5000, blank=True, null=True)
    district = models.CharField(max_length=5000, blank=True, null=True)
    approval_status = models.CharField(max_length=255, blank=True, null=True)
    est_cost_faid = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    est_cost_total = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    exp_upto_june = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    local_capital = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    local_revenue = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    faid_capital = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    faid_revenue = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    total_capital = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    total_revenue = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    allocation = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    projection_one = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    projection_two = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    throw_forward = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    constituency = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    year_id = models.IntegerField(blank=True, null=True)
    sector_id = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adp_schemes_last5yr'


class AdpType(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adp_type'


class AdpYear(models.Model):
    id = models.IntegerField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adp_year'


class Bg(models.Model):
    gid = models.AutoField()
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce = models.CharField(max_length=1, blank=True, null=True)
    bg_id = models.CharField(primary_key=True, max_length=12)
    namelsad = models.CharField(max_length=13, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'bg'


class County(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    countyns = models.CharField(max_length=8, blank=True, null=True)
    cntyidfp = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    csafp = models.CharField(max_length=3, blank=True, null=True)
    cbsafp = models.CharField(max_length=5, blank=True, null=True)
    metdivfp = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'county'


class CountyLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'county_lookup'
        unique_together = (('st_code', 'co_code'),)


class CountysubLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField()
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countysub_lookup'
        unique_together = (('st_code', 'co_code', 'cs_code'),)


class Cousub(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    cousubfp = models.CharField(max_length=5, blank=True, null=True)
    cousubns = models.CharField(max_length=8, blank=True, null=True)
    cosbidfp = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    cnectafp = models.CharField(max_length=3, blank=True, null=True)
    nectafp = models.CharField(max_length=5, blank=True, null=True)
    nctadvfp = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
    awater = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cousub'


class DirectionLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    abbrev = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direction_lookup'


class Edges(models.Model):
    gid = models.AutoField(primary_key=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    tfidl = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tfidr = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    smid = models.CharField(max_length=22, blank=True, null=True)
    lfromadd = models.CharField(max_length=12, blank=True, null=True)
    ltoadd = models.CharField(max_length=12, blank=True, null=True)
    rfromadd = models.CharField(max_length=12, blank=True, null=True)
    rtoadd = models.CharField(max_length=12, blank=True, null=True)
    zipl = models.CharField(max_length=5, blank=True, null=True)
    zipr = models.CharField(max_length=5, blank=True, null=True)
    featcat = models.CharField(max_length=1, blank=True, null=True)
    hydroflg = models.CharField(max_length=1, blank=True, null=True)
    railflg = models.CharField(max_length=1, blank=True, null=True)
    roadflg = models.CharField(max_length=1, blank=True, null=True)
    olfflg = models.CharField(max_length=1, blank=True, null=True)
    passflg = models.CharField(max_length=1, blank=True, null=True)
    divroad = models.CharField(max_length=1, blank=True, null=True)
    exttyp = models.CharField(max_length=1, blank=True, null=True)
    ttyp = models.CharField(max_length=1, blank=True, null=True)
    deckedroad = models.CharField(max_length=1, blank=True, null=True)
    artpath = models.CharField(max_length=1, blank=True, null=True)
    persist = models.CharField(max_length=1, blank=True, null=True)
    gcseflg = models.CharField(max_length=1, blank=True, null=True)
    offsetl = models.CharField(max_length=1, blank=True, null=True)
    offsetr = models.CharField(max_length=1, blank=True, null=True)
    tnidf = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tnidt = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'edges'


class Faces(models.Model):
    gid = models.AutoField(primary_key=True)
    tfid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    statefp00 = models.CharField(max_length=2, blank=True, null=True)
    countyfp00 = models.CharField(max_length=3, blank=True, null=True)
    tractce00 = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce00 = models.CharField(max_length=1, blank=True, null=True)
    blockce00 = models.CharField(max_length=4, blank=True, null=True)
    cousubfp00 = models.CharField(max_length=5, blank=True, null=True)
    submcdfp00 = models.CharField(max_length=5, blank=True, null=True)
    conctyfp00 = models.CharField(max_length=5, blank=True, null=True)
    placefp00 = models.CharField(max_length=5, blank=True, null=True)
    aiannhfp00 = models.CharField(max_length=5, blank=True, null=True)
    aiannhce00 = models.CharField(max_length=4, blank=True, null=True)
    comptyp00 = models.CharField(max_length=1, blank=True, null=True)
    trsubfp00 = models.CharField(max_length=5, blank=True, null=True)
    trsubce00 = models.CharField(max_length=3, blank=True, null=True)
    anrcfp00 = models.CharField(max_length=5, blank=True, null=True)
    elsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    scsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    unsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    uace00 = models.CharField(max_length=5, blank=True, null=True)
    cd108fp = models.CharField(max_length=2, blank=True, null=True)
    sldust00 = models.CharField(max_length=3, blank=True, null=True)
    sldlst00 = models.CharField(max_length=3, blank=True, null=True)
    vtdst00 = models.CharField(max_length=6, blank=True, null=True)
    zcta5ce00 = models.CharField(max_length=5, blank=True, null=True)
    tazce00 = models.CharField(max_length=6, blank=True, null=True)
    ugace00 = models.CharField(max_length=5, blank=True, null=True)
    puma5ce00 = models.CharField(max_length=5, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce = models.CharField(max_length=1, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    cousubfp = models.CharField(max_length=5, blank=True, null=True)
    submcdfp = models.CharField(max_length=5, blank=True, null=True)
    conctyfp = models.CharField(max_length=5, blank=True, null=True)
    placefp = models.CharField(max_length=5, blank=True, null=True)
    aiannhfp = models.CharField(max_length=5, blank=True, null=True)
    aiannhce = models.CharField(max_length=4, blank=True, null=True)
    comptyp = models.CharField(max_length=1, blank=True, null=True)
    trsubfp = models.CharField(max_length=5, blank=True, null=True)
    trsubce = models.CharField(max_length=3, blank=True, null=True)
    anrcfp = models.CharField(max_length=5, blank=True, null=True)
    ttractce = models.CharField(max_length=6, blank=True, null=True)
    tblkgpce = models.CharField(max_length=1, blank=True, null=True)
    elsdlea = models.CharField(max_length=5, blank=True, null=True)
    scsdlea = models.CharField(max_length=5, blank=True, null=True)
    unsdlea = models.CharField(max_length=5, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    cd111fp = models.CharField(max_length=2, blank=True, null=True)
    sldust = models.CharField(max_length=3, blank=True, null=True)
    sldlst = models.CharField(max_length=3, blank=True, null=True)
    vtdst = models.CharField(max_length=6, blank=True, null=True)
    zcta5ce = models.CharField(max_length=5, blank=True, null=True)
    tazce = models.CharField(max_length=6, blank=True, null=True)
    ugace = models.CharField(max_length=5, blank=True, null=True)
    puma5ce = models.CharField(max_length=5, blank=True, null=True)
    csafp = models.CharField(max_length=3, blank=True, null=True)
    cbsafp = models.CharField(max_length=5, blank=True, null=True)
    metdivfp = models.CharField(max_length=5, blank=True, null=True)
    cnectafp = models.CharField(max_length=3, blank=True, null=True)
    nectafp = models.CharField(max_length=5, blank=True, null=True)
    nctadvfp = models.CharField(max_length=5, blank=True, null=True)
    lwflag = models.CharField(max_length=1, blank=True, null=True)
    offset = models.CharField(max_length=1, blank=True, null=True)
    atotal = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'faces'


class Featnames(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    predirabrv = models.CharField(max_length=15, blank=True, null=True)
    pretypabrv = models.CharField(max_length=50, blank=True, null=True)
    prequalabr = models.CharField(max_length=15, blank=True, null=True)
    sufdirabrv = models.CharField(max_length=15, blank=True, null=True)
    suftypabrv = models.CharField(max_length=50, blank=True, null=True)
    sufqualabr = models.CharField(max_length=15, blank=True, null=True)
    predir = models.CharField(max_length=2, blank=True, null=True)
    pretyp = models.CharField(max_length=3, blank=True, null=True)
    prequal = models.CharField(max_length=2, blank=True, null=True)
    sufdir = models.CharField(max_length=2, blank=True, null=True)
    suftyp = models.CharField(max_length=3, blank=True, null=True)
    sufqual = models.CharField(max_length=2, blank=True, null=True)
    linearid = models.CharField(max_length=22, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    paflag = models.CharField(max_length=1, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'featnames'


class GeocodeSettings(models.Model):
    name = models.TextField(primary_key=True)
    setting = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geocode_settings'


class GeocodeSettingsDefault(models.Model):
    name = models.TextField(primary_key=True)
    setting = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geocode_settings_default'


class LoaderLookuptables(models.Model):
    process_order = models.IntegerField()
    lookup_name = models.TextField(primary_key=True)
    table_name = models.TextField(blank=True, null=True)
    single_mode = models.BooleanField()
    load = models.BooleanField()
    level_county = models.BooleanField()
    level_state = models.BooleanField()
    level_nation = models.BooleanField()
    post_load_process = models.TextField(blank=True, null=True)
    single_geom_mode = models.NullBooleanField()
    insert_mode = models.CharField(max_length=1)
    pre_load_process = models.TextField(blank=True, null=True)
    columns_exclude = models.TextField(blank=True, null=True)  # This field type is a guess.
    website_root_override = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_lookuptables'


class LoaderPlatform(models.Model):
    os = models.CharField(primary_key=True, max_length=50)
    declare_sect = models.TextField(blank=True, null=True)
    pgbin = models.TextField(blank=True, null=True)
    wget = models.TextField(blank=True, null=True)
    unzip_command = models.TextField(blank=True, null=True)
    psql = models.TextField(blank=True, null=True)
    path_sep = models.TextField(blank=True, null=True)
    loader = models.TextField(blank=True, null=True)
    environ_set_command = models.TextField(blank=True, null=True)
    county_process_command = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_platform'


class LoaderVariables(models.Model):
    tiger_year = models.CharField(primary_key=True, max_length=4)
    website_root = models.TextField(blank=True, null=True)
    staging_fold = models.TextField(blank=True, null=True)
    data_schema = models.TextField(blank=True, null=True)
    staging_schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_variables'


class MainSector(models.Model):
    msectid = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    member_name = models.CharField(db_column='Member Name', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grant = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_sector'


class PagcGaz(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_gaz'


class PagcLex(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_lex'


class PagcRules(models.Model):
    rule = models.TextField(blank=True, null=True)
    is_custom = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_rules'


class Place(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    placefp = models.CharField(max_length=5, blank=True, null=True)
    placens = models.CharField(max_length=8, blank=True, null=True)
    plcidfp = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    cpi = models.CharField(max_length=1, blank=True, null=True)
    pcicbsa = models.CharField(max_length=1, blank=True, null=True)
    pcinecta = models.CharField(max_length=1, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.BigIntegerField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'place'


class PlaceLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    pl_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place_lookup'
        unique_together = (('st_code', 'pl_code'),)


class SecondaryUnitLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    abbrev = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secondary_unit_lookup'


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


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class State(models.Model):
    gid = models.AutoField(unique=True)
    region = models.CharField(max_length=2, blank=True, null=True)
    division = models.CharField(max_length=2, blank=True, null=True)
    statefp = models.CharField(primary_key=True, max_length=2)
    statens = models.CharField(max_length=8, blank=True, null=True)
    stusps = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.BigIntegerField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'state'


class StateLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=40, blank=True, null=True)
    abbrev = models.CharField(unique=True, max_length=3, blank=True, null=True)
    statefp = models.CharField(unique=True, max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'state_lookup'


class StreetTypeLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    abbrev = models.CharField(max_length=50, blank=True, null=True)
    is_hw = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'street_type_lookup'


class Tabblock(models.Model):
    gid = models.AutoField()
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    tabblock_id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=20, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    ur = models.CharField(max_length=1, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tabblock'


class Tract(models.Model):
    gid = models.AutoField()
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    tract_id = models.CharField(primary_key=True, max_length=11)
    name = models.CharField(max_length=7, blank=True, null=True)
    namelsad = models.CharField(max_length=20, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tract'


class UsGaz(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_gaz'


class UsLex(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_lex'


class UsRules(models.Model):
    rule = models.TextField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_rules'


class Zcta5(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2)
    zcta5ce = models.CharField(primary_key=True, max_length=5)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    partflg = models.CharField(max_length=1, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'zcta5'
        unique_together = (('zcta5ce', 'statefp'),)


class ZipLookup(models.Model):
    zip = models.IntegerField(primary_key=True)
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField(blank=True, null=True)
    cousub = models.CharField(max_length=90, blank=True, null=True)
    pl_code = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=90, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup'


class ZipLookupAll(models.Model):
    zip = models.IntegerField(blank=True, null=True)
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField(blank=True, null=True)
    cousub = models.CharField(max_length=90, blank=True, null=True)
    pl_code = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=90, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup_all'


class ZipLookupBase(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    state = models.CharField(max_length=40, blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    city = models.CharField(max_length=90, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup_base'


class ZipState(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    stusps = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_state'
        unique_together = (('zip', 'stusps'),)


class ZipStateLoc(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    stusps = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    place = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'zip_state_loc'
        unique_together = (('zip', 'stusps', 'place'),)
