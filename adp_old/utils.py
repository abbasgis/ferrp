import json
import base64
import zlib
from django.apps import apps
from django.db import connections
from django.forms import model_to_dict

# Create your models here.
def get_adp_report_data_from_model():
    adpreport_model_class = apps.get_model(app_label='adp', model_name='AdpReport201718')
    table_rows = list(adpreport_model_class.objects.all())
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    return json_data

def get_adp_mpr_data_from_model():
    adpmpr_model_class = apps.get_model(app_label='adp', model_name='AdpSchemes1018Mpr')
    table_rows = list(adpmpr_model_class.objects.all().order_by('GS_No'))
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed
    return json_data

def get_adp_yearly_analysis_data_from_model():
    adpanalysis_model_class = apps.get_model(app_label='adp', model_name='AdpYearlyFacts1018')
    table_rows = list(adpanalysis_model_class.objects.all().order_by('Year'))
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed

def adpDistrictGeoJSON():
    connection = connections['adp']
    cursor = connection.cursor()
    query = "SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, " \
            "array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type , " \
            "ST_AsGeoJSON(st_simplify(lg.geom, 0.0009), 4)::json As geometry , " \
            "row_to_json((SELECT l FROM (SELECT id, name) As l )) As properties " \
            "FROM adp_district As lg where geom is not null) As f ) As fc;"
    cursor.execute(query)
    data = dictfetchall(cursor)
    json_data = json.dumps(data, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed


def get_model_dict_array(rows):
    data_array = []
    for row in rows:
        row_dict = model_to_dict(row)
        data_array.append(row_dict)
    return data_array

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]