import json

from django.contrib.gis.geos import Polygon
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ferrp.layers.models import Info
from ferrp.models import Activity_Log
from ferrp.utils import Log_Error


def vieew_layer_3d_map(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "map_3d", "vieew_layer_3d_map", "View Layer on 3d Map",
                                     request.path_info)
    response = HttpResponse()
    try:
        # layer_name = request.GET.get("layer_name")
        layer_name = "gis_ph_ii_road_line_20180519094621853654"
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        extent = layer_info.extent.split(",")
        srid = layer_info.srid
        polygon =  Polygon().from_bbox(extent)
        polygon.srid = srid
        polygon.transform(4326)
        extent = list(polygon.extent)
        # coords = list(polygon.coords)
        # print(coords)
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'map_3d_jqx.html', {"extent":extent})

