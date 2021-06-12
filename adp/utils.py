import json
import base64
import zlib
from django.apps import apps
from django.forms import model_to_dict

def get_adp_yearly_analysis():
    adpanalysis_model_class = apps.get_model(app_label='adp', model_name='AdpSchemes1018Mpr')
    table_rows = list(adpanalysis_model_class.objects.all().order_by('Year'))
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array)
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