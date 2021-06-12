import json
import base64
import zlib
from ferrp.irrigation.IrrigationModels.AppFunctions import getQueryResultAsJson, date_handler
from ferrp.irrigation.Irrigation_Setting import CANALS_TABLE

def getCanalsGeoJson():
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom_simple, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
               'zone_name, circle_name, division_name, channel_name, channel_type, imis_code, tail_rd::integer,  flowtype_e, ' \
               'head_x::integer, head_y::integer, tail_x::integer, tail_y::integer, ' \
               'gca::double precision, cca::double precision, (length_ft/(3.333*1000))::DOUBLE PRECISION as length_km) As l )) As properties ' + \
               'FROM %s As lg order by channel_name asc) As f ) As fc;' %(CANALS_TABLE)
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getSelectedCanalsGeoJson(request):
    whereClause = request.GET.get('where')
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
       'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
       'ST_AsGeoJSON(st_transform(lg.geom_simple, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
       'zone_name, circle_name, division_name, channel_name, channel_type, imis_code, tail_rd::integer,  flowtype_e, ' \
       'head_x::integer, head_y::integer, tail_x::integer, tail_y::integer, ' \
       'gca::double precision, cca::double precision, (length_ft/(3.333*1000))::DOUBLE PRECISION as length_km) As l )) As properties ' + \
       'FROM %s As lg where ' %(CANALS_TABLE) + whereClause + ' order by channel_name asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed

def getCanalsData():
    strQuery = 'select zone_name, circle_name, division_name, channel_name, channel_type, imis_code, tail_rd::integer,  ' \
           'flowtype_e, head_x::integer, head_y::integer, tail_x::integer, tail_y::integer, gca::double precision, ' \
               'cca::double precision, length_ft::DOUBLE PRECISION as length_km, extent, geojson, ' \
               'is_l_section, is_gate, is_gauge, is_structure, is_row, is_outlet ' \
               'from %s order by zone_name asc, circle_name, division_name, channel_name;' %(CANALS_TABLE)
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getCanalsCombinedData():
    canalsData = getCanalsData()
    canalsGeoJson = getCanalsGeoJson()
    allData = json.dumps({'data':canalsData, 'geojson':canalsGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed

def string_to_where_clause(code):
    imis_code_array = code.split(',')
    where_clause = ''
    if len(imis_code_array) > 0:
        index = 0
        for code in imis_code_array:
            if index == 0:
                where_clause = ' imis_code = \'' + code + '\''
            else:
                where_clause = where_clause + ' or imis_code = \'' + code + '\' '
            index += 1
    else:
        where_clause = ' imis_code = \'' + code + '\''
    return where_clause

# L Section Data
def getLSectionData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'select * from canals_l_section where ' + where_clause + ' order by imis_code asc;'
    json_data = getQueryResultAsJson(strQuery)
    # compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return json_data

# L Section GeoJson Data
def getLSectionGeojsonData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)

    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
       'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
       'ST_AsGeoJSON(st_transform(lg.geom, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
       'name_of_zone, name_of_circle, name_of_division, name_of_canal, from_rd_m, to_rd_m ) As l )) As properties ' + \
       'FROM canals_l_section As lg where ' + where_clause  + ' order by name_of_canal asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    # compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return json_data

def getLSectionCombinedData(request):
    lSectionData = getLSectionData(request)
    lSectionGeoJson = getLSectionGeojsonData(request)
    allData = json.dumps({'data':lSectionData, 'geojson':lSectionGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed

# Gates Data
def getGatesData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'select * from canal_gates where ' + where_clause + ' order by rd_m asc;'
    json_data = getQueryResultAsJson(strQuery)
    # compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return json_data

def getGatesGeoJsonData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
               'name_of_canal, imis_code, rd ) As l )) As properties ' + \
               'FROM canal_gates As lg where ' + where_clause + ' order by rd_m asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    # compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return json_data

def getGatesCombinedData(request):
    gatesData = getGatesData(request)
    gatesGeoJson = getGatesGeoJsonData(request)
    allData = json.dumps({'data': gatesData, 'geojson': gatesGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed

# Guages Data
def getGuagesData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'select * from canal_gauges where ' + where_clause + '  order by rd_m asc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getGaugesGeoJsonData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
               'canal_name, imis_code, rd_m ) As l )) As properties ' + \
               'FROM canal_gauges As lg where ' + where_clause + ' and geom is not null order by rd_m asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getGaugesCombinedData(request):
    gaugesData = getGuagesData(request)
    gaugesGeoJson = getGaugesGeoJsonData(request)
    allData = json.dumps({'data': gaugesData, 'geojson': gaugesGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed

# Structure Data
def getStructureData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'select * from canal_structure where ' + where_clause + ' order by rd_m asc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getStructureGeoJsonData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
               'canal_name, imis_code, rd_m ) As l )) As properties ' + \
               'FROM canal_structure As lg where ' + where_clause + ' and geom is not null order by rd_m asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getStructureCombinedData(request):
    structureData = getStructureData(request)
    structureGeoJson = getStructureGeoJsonData(request)
    allData = json.dumps({'data': structureData, 'geojson': structureGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed

# ROW Data
def getROWData(request):
    imisCode = request.GET.get('code')
    strQuery = 'select name_of_canal, rd_length, l_ft, r_ft, federalgovt, govtofpunjab, irrigation_deptt, others, total, total_l_r_ft, ' \
               'anyotherdeptt, location, zone, circle, divison, sub_divison, section, district, tehsil, police_station, village, action, ' \
               'remarks, imis_code from canal_row where imis_code = \'' + imisCode + '\''
    json_data = getQueryResultAsJson(strQuery)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed

# OutletsData Data
def getOutletsData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'select * from canal_outlets where ' + where_clause + '  order by rd_m asc;'
    json_data = getQueryResultAsJson(strQuery)
    # compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return json_data
def getOutletsGeoJsonData(request):
    imisCode = request.GET.get('code')
    where_clause = string_to_where_clause(imisCode)
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom, 4326), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
               'name_of_canal, imis_code, rd_m ) As l )) As properties ' + \
               'FROM canal_outlets As lg where ' + where_clause + ' order by rd_m asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getOutletsCombinedData(request):
    outletsData = getOutletsData(request)
    outletsGeoJson = getOutletsGeoJsonData(request)
    allData = json.dumps({'data': outletsData, 'geojson': outletsGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed


def canal_detail_data(request):
    type = request.GET.get('type')
    detail_data = None
    if type == 'canal_l_section':
        detail_data = getLSectionCombinedData(request)
    if type == 'canal_gates':
        detail_data = getGatesCombinedData(request)
    if type == 'canal_guages':
        detail_data = getGaugesCombinedData(request)
    if type == 'canal_row':
        detail_data = getROWData(request)
    if type == 'canal_structure':
        detail_data = getStructureCombinedData(request)
    if type == 'outlets':
        detail_data = getOutletsCombinedData(request)
    return detail_data

#Cross section height profile
def getCrossSectionHeightProfileData(request):
    strWKT = request.GET.get('wkt')
    strQuery = 'select * from ferrp_line_heightprofile(\''+strWKT+'\');'
    json_data = getQueryResultAsJson(strQuery)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed
