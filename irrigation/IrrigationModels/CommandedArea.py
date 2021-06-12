import json
import base64
import zlib
from ferrp.irrigation.IrrigationModels.AppFunctions import getQueryResultAsJson, date_handler

def getIrrigationBoundaryGeoJsonQuery(level, value):
    strQuery = ""
    if (level == 'zone_name'):
        strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
                   'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ' + \
                   'ST_AsGeoJSON(st_simplify(lg.geom, 0.005), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT cca_geom_ma::numeric, name) As l )) As properties ' + \
                   'FROM gis_zone_origs As lg where geom is not null) As f ) As fc;'
    elif (level == 'circle_name'):
        strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
                   'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ' + \
                   'ST_AsGeoJSON(st_simplify(lg.geom, 0.005), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT cca_geom_ma::numeric, name) As l )) As properties ' + \
                   'FROM gis_circle_origs As lg where geom is not null and zone_name = \'' + value + '\') As f ) As fc;'
    elif (level == 'division_name'):
        strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
                   'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ' + \
                   'ST_AsGeoJSON(st_simplify(lg.geom, 0.005), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT cca_geom_ma::numeric, name) As l )) As properties ' + \
                   'FROM gis_division_origs As lg where geom is not null and circle_name = \'' + value + '\') As f ) As fc;'
    elif (level == 'cca'):
        strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
                   'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ' + \
                   'ST_AsGeoJSON(st_simplify(lg.geom, 0.005), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT area_ha::numeric as cca_geom_ma, cca_name as name) As l )) As properties ' + \
                   'FROM gis_cca_acz As lg where geom is not null and division_name = \'' + value + '\') As f ) As fc;'
    return strQuery

def getCommandedAreaStatsQuery(levelName, levelValue):
    strQuery = ''
    if (levelName == 'zone_name'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as canal_length, ' \
                   'z.canals_shape_length::double precision as shape_length, z.outlets::integer ' \
                   'FROM gis_zone_origs z  order by z.name;'
    elif (levelName == 'circle_name'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as length, ' \
                   'z.canals_shape_length::double precision as shape_length, z.outlets::double precision  ' \
                   'FROM gis_circle_origs z  where z.zone_name = \'' + levelValue + '\'' + '  order by z.name;'
    elif (levelName == 'division_name'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as length, ' \
                   'z.canals_shape_length::double precision as shape_length, z.outlets::double precision  ' \
                   'FROM gis_division_origs z  where z.circle_name = \'' + levelValue + '\'   order by z.name;'
    elif (levelName == 'cca'):
        strQuery = 'select acz_name, cca_name, doab, basin, area_ha::double precision, cca_dam, zone_name, circle_name, ' \
                   'division_name, area_acre::double precision  from gis_cca_acz where division_name = \'' + levelValue + '\';'
    return strQuery

def get_ca_query_for_filters(levelName, where_clause):
    strQuery = ''
    if (levelName == 'zone_name'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as length, ' \
                   'z.outlets::double precision  ' \
                   'FROM gis_zone_origs z where ' + where_clause.replace('zone_name', 'name') + ' order by z.name;'
    elif (levelName == 'circle_name'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as length, z.outlets::double precision  ' \
                   'FROM gis_circle_origs z  where ' + where_clause + \
                   ' group by z.name, z.cca_ma, z.gca_ma, z.cca_geom_ma, z.gca_geom_ma, z.channels_length_km, z.outlets order by z.name;'
    elif (levelName == 'division_name'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as length, z.outlets::double precision  ' \
                   'FROM gis_division_origs z  where ' + where_clause + \
                   ' group by z.name, z.cca_ma, z.gca_ma, z.cca_geom_ma, z.gca_geom_ma, z.channels_length_km, z.outlets order by z.name;'
    elif (levelName == 'cca'):
        strQuery = 'select acz_name, cca_name, doab, basin, area_ha::double precision, cca_dam, zone_name, circle_name, ' \
                   'division_name, area_acre::double precision  from gis_cca_acz where ' + where_clause + ';'
    return strQuery

def getDistrictQuery(level, value):
    strQuery = ''
    if (level == 'zone_name'):
        strQuery = 'select gid, district_name, name, admin_boundary_area, admin_boundary_part, admin_boundary_percentage, district_area ' \
                   'from gis_districts_zone where name = \'' + value + '\''
    elif (level == 'circle_name'):
        strQuery = 'select gid, district_name, name, admin_boundary_area, admin_boundary_part, admin_boundary_percentage, district_area ' \
                   'from gis_districts_circle where name = \'' + value + '\''
    elif (level == 'division_name'):
        strQuery = 'select gid, district_name, name, admin_boundary_area, admin_boundary_part, admin_boundary_percentage, district_area ' \
                   'from gis_districts_division where name = \'' + value + '\''
    return strQuery

def get_dist_query_for_filters(level, where_clause):
    strQuery = ''
    if (level == 'zone_name'):
        strQuery = 'select gid, district_name, name, admin_boundary_area, admin_boundary_part, admin_boundary_percentage, district_area ' \
                   'from gis_districts_zone where ' + where_clause.replace('zone_name', 'name') + ';'
    elif (level == 'circle_name'):
        strQuery = 'select gid, district_name, name, admin_boundary_area, admin_boundary_part, admin_boundary_percentage, district_area ' \
                   'from gis_districts_circle where ' + where_clause.replace('circle_name', 'name') + ';'
    elif (level == 'division_name'):
        strQuery = 'select gid, district_name, name, admin_boundary_area, admin_boundary_part, admin_boundary_percentage, district_area ' \
                   'from gis_districts_division where ' + where_clause.replace('division_name', 'name') + ';'
    return strQuery

def getCanalsLengthQuery(level, value):
    strQuery = ""
    if (level == 'zone_name'):
        strQuery = 'SELECT channel_type as canal_type, sum(length_ft)/(1000 * 3.33)::double precision as length ' \
                   'from gis_irrigation_network ' + \
                   'group by channel_type order by channel_type;'
    elif (level == 'circle_name'):
        strQuery = 'SELECT channel_type as canal_type, sum(length_ft)/(1000 * 3.33)::double precision as length ' \
                   'from gis_irrigation_network where zone_name = \'' + value + '\' ' + \
                   'group by channel_type order by channel_type;'
    elif (level == 'division_name'):
        strQuery = 'SELECT channel_type as canal_type, sum(length_ft)/(1000 * 3.33)::double precision as length ' \
                   'from gis_irrigation_network where circle_name = \'' + value + '\' ' + \
                   'group by channel_type order by channel_type;'
    elif (level == 'cca'):
        strQuery = 'SELECT channel_type as canal_type, sum(length_ft)/(1000 * 3.33)::double precision as length ' \
                   'from gis_irrigation_network where cca_name = \'' + value + '\' ' + \
                   'group by channel_type order by channel_type;'
    return strQuery

def getIrrigationBoundaryGeoJson(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    strQuery = getIrrigationBoundaryGeoJsonQuery(level, value)
    json_data = getQueryResultAsJson(strQuery)

    return json_data

def getCanalStats(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    strQuery = getCommandedAreaStatsQuery(level, value)
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getCanalsLength(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    strQuery = getCanalsLengthQuery(level, value)
    json_data = getQueryResultAsJson(strQuery)
    return json_data

# districts information
def getDistrictsInformation(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    strQuery = getDistrictQuery(level, value)
    json_data = getQueryResultAsJson(strQuery)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed

def getCombinedData(request):
    canalsLength = getCanalsLength(request)
    canalsStats = getCanalStats(request)
    adminGeoJson = getIrrigationBoundaryGeoJson(request)
    all_data = json.dumps({'canals': canalsLength, 'stats': canalsStats, 'geojson':adminGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(all_data), 9))
    return compressed