import base64
import json
from sys import getsizeof

import zlib
import datetime
from django.core.serializers import serialize
from django.db.models import Max, F, Min
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ferrp.climate_change.forms import HeatMapInputsForm
from ferrp.climate_change.models import *
from ferrp.maps.models import Map_Info
from ferrp.models import Activity_Log
from ferrp.utils import date_handler, Log_Error, getJSONFromDB, DB_Query


def view_climate_change_page(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "climate_change", "view_cc_page", "View Climate Change Page",
                                     request.path_info)
    form = HeatMapInputsForm(request.POST)
    try:
        map_name = 'map_climate_change_ferrppndsu_20181018162236832819'  # request.GET.get("item_name")
        map_info = Map_Info.objects.filter(name=map_name)
        info = {'extent': None, 'group_layers': []}
        if map_info.count() > 0:
            map_info = list(map_info.values('params'))[0]
            info["extent"] = [float(e) if float(e) else str(e) for e in map_info['params']['extent'].split(",")]
            info["group_layers"] = map_info['params']['group_layers']
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'climate_change.html', {'form': form, "info": info, "map_name": map_name})


def get_temprature_rcp_data(request):
    data = list(TemperatureRcp4525KmPunjab.objects.all().values())
    data = json.dumps(data, default=date_handler)
    print(getsizeof(data))
    compressed = base64.b64encode(zlib.compress(str.encode(data), 9))
    print(getsizeof(compressed))
    response = {'result': compressed}
    # response = json.dumps(response, default=date_handler)
    return HttpResponse(compressed)


def get_geojson_for_heatmap(request):
    month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    month_val = request.GET.get('month', month_list[month - 1])
    year_val = request.GET.get('year', year)
    layer = request.GET.get('layer', 'temperature')
    table_name = 'view_temperature_rcp45_25km_punjab'
    model = TemperatureRcp4525KmPunjab
    if layer != 'temperature':
        table_name = 'view_precipitation_rcp4525_20102099_punjab'
        model = view_precipitation_rcp4525_20102099
    tempr_data = model.objects.filter(year=year_val)
    obj_min = tempr_data.aggregate(Min('jan'), Min('feb'), Min('mar'), Min('apr'), Min('may'), Min('jun'), Min('jul'),
                                   Min('aug'), Min('sep'), Min('oct'), Min('nov'), Min('dec'), Max('jan'), Max('feb'),
                                   Max('mar'), Max('apr'), Max('may'), Max('jun'), Max('jul'),
                                   Max('aug'), Max('sep'), Max('oct'), Max('nov'), Max('dec'))
    temp_list = sorted([float(obj_min[d]) for d in obj_min])
    dem = temp_list[len(temp_list) - 1] - temp_list[0]
    query = 'Select ("%s"-%s)/%s as weight, geom from %s where year = %s order by weight' % (
        month_val, temp_list[0], dem, table_name, year_val)
    d = DB_Query.execute_query_as_geojson(query, geom_col='geom')
    return HttpResponse(json.dumps(d))
