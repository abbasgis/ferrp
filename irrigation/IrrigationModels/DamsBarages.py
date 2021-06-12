import json
import base64
import zlib

from django.apps import apps

from ferrp.irrigation.IrrigationModels.AppFunctions import getQueryResultAsJson, date_handler, execute_query, \
    get_model_dict_array


def getDamsData():
    strQuery = 'select dam_name, river, main_basin, near_city, catch_skm::DOUBLE PRECISION, main_use, extent, geojson, latest_discharge ' \
               'from gis_pakistan_dam_and_barrages order by dam_name asc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def get_dams_data_from_model():
    dams_model_class = apps.get_model(app_label='irrigation', model_name='PakDamsAndBarrages')
    table_rows = list(dams_model_class.objects.order_by('dam_name'))
    data_array = get_model_dict_array(table_rows)
    return data_array

def getDamsGeoJson():
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(lg.geom, 4)::json As geometry , row_to_json(' \
               '(SELECT l FROM (SELECT dam_name, river, catch_skm::DOUBLE PRECISION, latest_discharge::double precision as discharge) As l )) As properties ' \
               'FROM gis_pakistan_dam_and_barrages As lg order by dam_name asc) As f ) As fc;'
    json_data = getQueryResultAsJson(strQuery)
    return json_data

def getDischargeData(request):
    strHeadWork = request.GET.get('head')
    where_clause = string_to_where_clause(strHeadWork)
    strQuery = 'select * from discharge_data where ' + where_clause + ' and us is not null order by discharge_date asc;'
    json_data = getQueryResultAsJson(strQuery)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed

def to_from_discharge_data(request):
    strHeadWork = request.GET.get('head')
    strFromDate = request.GET.get('from')
    strToDate = request.GET.get('to')
    strQuery = 'select * from discharge_data where head_works = \'' + strHeadWork + '\' and ' \
                'discharge_date > \'' + strFromDate + '\' and discharge_date < \'' + strToDate + '\' ' \
                'and us is not null order by discharge_date, discharge_time asc;'
    json_data = getQueryResultAsJson(strQuery)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed

def getDamsCombinedData():
    damsData = get_dams_data_from_model()
    damsGeoJson = getDamsGeoJson()
    allData = json.dumps({'damsData':damsData, 'damsGeoJson':damsGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(allData), 9))
    return compressed

def updateDischargeValue(request):
    year = request.GET.get('year')
    str_query = 'update gis_pakistan_dam_and_barrages d set latest_discharge = ( ' \
                'select max(us) from discharge_data dd where d.dam_name = dd.head_works and ' \
                'dd.discharge_date > \'' +year+ '-01-01 13:00:00+05\' and dd.discharge_date < \'' +year+ '-12-31 13:00:00+05\');'
    updated = execute_query(str_query)
    data = getDamsCombinedData()
    return data

def string_to_where_clause(str_hd_array):
    hd_array = str_hd_array.split(',')
    where_clause = ''
    if len(hd_array) > 0:
        index = 0
        for hd_name in hd_array:
            if index == 0:
                where_clause = ' head_works = \'' + hd_name + '\''
            else:
                where_clause = where_clause + ' or head_works = \'' + hd_name + '\''
            index += 1
    else:
        where_clause = ' head_works = \'' + hd_array  + '\''
    return where_clause


