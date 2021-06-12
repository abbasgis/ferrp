import json
import base64
import zlib
from django.apps import apps
from ferrp.irrigation.IrrigationModels.AppFunctions import getQueryResultAsJson, date_handler, get_model_dict_array

# def getGroundWaterData():
#     strQuery = 'select fid as id, irrigation as zone, canal_circ as circle, canal_divi as division,' \
#                ' major_cana as major_canal, owner__add as address, elevation,  extent, geojson from water_level ' \
#                'order by irrigation, canal_circ, canal_divi, major_cana;'
#     json_data = getQueryResultAsJson(strQuery)
#     return json_data
#
# def getGroundWaterGeoJson():
#     strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
#                'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
#                'ST_AsGeoJSON(lg.geom)::json As geometry , row_to_json(' \
#                '(SELECT l FROM (SELECT major_cana as major_canal, elevation) As l )) As properties ' \
#                'FROM water_level As lg order by major_cana asc) As f ) As fc;'
#     json_data = getQueryResultAsJson(strQuery)
#     return json_data
#
# def getWaterLevelCombinedData():
#     gwData = getGroundWaterData()
#     gwGeoJson = getGroundWaterGeoJson()
#     allData = json.dumps({'wlData':gwData, 'wlGeoJson':gwGeoJson}, default=date_handler)
#     return allData

# water level and quality data functions
# def getWaterLevelQualityDataJson():
#     strQuery = 'select l.id, l.irrigation as zone, l.canal_circ as circle, l.canal_divi as division, l.major_cana as major_canal, ' \
#                'l.owner__add as address, l.tehsil, l.district, ' \
#                'l.dsl as dsl_ft, l.nsl_ft::DOUBLE PRECISION, l.boring_dep::DOUBLE PRECISION , l.discharge from water_level_quality l ' \
#                ' ORDER by l.major_cana desc;'
#     json_data = getQueryResultAsJson(strQuery)
#     return json_data
#
# def getWaterLevelQualityGeojson():
#     strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
#                'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
#                'ST_AsGeoJSON(lg.geom)::json As geometry , row_to_json(' \
#                '(SELECT l FROM (SELECT id, irrigation as zone, canal_circ as circle, ' \
#                'canal_divi as division, major_cana as major_canal) As l )) As properties ' \
#                'FROM water_level_quality As lg order by major_cana asc) As f ) As fc;'
#     json_data = getQueryResultAsJson(strQuery)
#     return json_data
#
# def getWaterLevelQualityCombinedJson():
#     gwData = getWaterLevelQualityDataJson()
#     gwGeoJson = getWaterLevelQualityGeojson()
#     allData = json.dumps({'wlData': gwData, 'wlGeoJson': gwGeoJson}, default=date_handler)
#     return allData
#
# def getIndividualWaterLevelData(request):
#     dataId = request.GET.get('id')
#     strQuery = 'select l.id, l.irrigation as zone, l.canal_circ as circle, l.canal_divi as division, l.major_cana as major_canal, ' \
#                'l.pre_03, l.post_03, l.pre_04, l.post_04, l.pre_05, l.post_05, l.pre_06, l.post_06, l.pre_07, l.post_07, l.pre_08, ' \
#                'l.post_08, l.pre_09, l.post_09, l.pre_10, l.post_10, l.pre_11,' \
#                'l.post_11, l.pre_12, l.post_12, l.pre_13, l.post_13, l.pre_14, l.post_14, l.pre_15 from water_level_quality l where id = ' + dataId + \
#                ' ORDER by irrigation, canal_circ, canal_divi, major_cana;'
#     json_data = getQueryResultAsJson(strQuery)
#     return json_data

def get_ground_water_data_from_model():
    gwater_model_class = apps.get_model(app_label='irrigation', model_name='TblWqWlCombinedData')
    table_rows = list(gwater_model_class.objects.all())
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    return json_data

def get_ground_water_geojson_data():
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(lg.geom)::json As geometry , row_to_json(' \
               '(SELECT l FROM (SELECT id, elevation, type_wl_wq, reclamation, major_canal, disty_minor, circle, division, zone) As l )) As properties ' \
               'FROM gis_wq_wl As lg  order by type_wl_wq asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def get_json_geojson_data():
    jsonData = str(get_ground_water_data_from_model())
    geojsonData = get_ground_water_geojson_data()
    all_data = json.dumps({'json': jsonData, 'geojson': geojsonData}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(all_data), 9))
    return compressed

def get_water_level_detail(request):
    ql_id = request.GET.get('ql_id')
    # wl_detail_model_class = apps.get_model(app_label='irrigation', model_name='TblWlDetail')
    # table_rows = list(wl_detail_model_class.objects.filter(ql_id = ql_id).order_by('year'))
    # data_array = get_model_dict_array(table_rows)
    # json_data = json.dumps(data_array, default=date_handler)
    where_clause = string_to_where_clause(ql_id)
    strQuery = 'select * from gis_water_level_detail where ' + where_clause + '  order by year asc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def get_water_quality_detail(request):
    ql_id = request.GET.get('ql_id')
    # wl_detail_model_class = apps.get_model(app_label='irrigation', model_name='TblWqDetail')
    # table_rows = list(wl_detail_model_class.objects.filter(ql_id = ql_id).order_by('year'))
    # data_array = get_model_dict_array(table_rows)
    # json_data = json.dumps(data_array, default=date_handler)
    where_clause = string_to_where_clause(ql_id)
    strQuery = 'select * from gis_water_quality_detail where ' + where_clause + '  order by year asc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def get_combined_level_quality_detail(request):
    level_data = get_water_level_detail(request)
    quality_data = get_water_quality_detail(request)
    data = json.dumps({'level': str(level_data), 'quality': str(quality_data)}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(data), 9))
    return compressed

def get_level_year_type_data(request):
    year = request.POST.get('year')
    type = request.POST.get('type')
    wl_detail_model_class = apps.get_model(app_label='irrigation', model_name='TblWlDetail')
    table_rows = list(wl_detail_model_class.objects.filter(year=year, season = type).order_by('year'))
    data_array = get_model_dict_array(table_rows)
    data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(data), 9))
    return compressed

def string_to_where_clause(str_id_array):
    id_array = str_id_array.split(',')
    where_clause = ''
    if len(id_array) > 0:
        index = 0
        for id in id_array:
            if index == 0:
                where_clause = ' ql_id = ' + id
            else:
                where_clause = where_clause + ' or ql_id = ' + id
            index += 1
    else:
        where_clause = ' ql_id = ' + str_id_array
    return where_clause

