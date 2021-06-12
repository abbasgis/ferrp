import base64
import json

import zlib
from sys import getsizeof

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ferrp.decorators import permission_required
from ferrp.maps.spatial_operations import Spatial_Operations
from ferrp.models import Items_Permission
from ferrp.layers.models import Info
from ferrp.local_settings import SPATIAL_EXTENT_3857
from ferrp.utils import Log_Error, DB_Query, getJSONFromDB
from ferrp.views import date_handler
from .models import *

from ferrp.models import Activity_Log


def map_browser(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "map_browser", "Browse map",
                                     request.path_info)
    response = HttpResponse()
    try:
        can_create_new_map = True  # request.user.has_perm('ferrp.file_upload')
        entity_list = list(request.user.groups.values_list('name', flat=True))
        entity_list.append(request.user.username)
        entity_list.append("Public")
        if request.user.is_superuser:
            map_list = list(
                Map_Info.objects.all().values('name', 'title', 'created_by', 'created_at', 'permissions', 'icon'))
        else:
            item_type = Common_Utils.get_info_item_content_type('maps', 'map_info')
            map_name_list = list(
                Items_Permission.objects.filter(entity_name__in=entity_list, permission_type__in=['V', 'O'],
                                                item_type=item_type)
                    .values_list('item_name', flat=True))  #
            map_list = list(
                Map_Info.objects.filter(name__in=map_name_list).values('name', 'title', 'created_by', 'created_at',
                                                                       'icon'))
        map_list = DB_Query.addPermissionType2Items(map_list, 'name', request.user, "O")
        # can_download = len(list(Permission.objects.filter(entity_name=request.user.username, permission_type='D'))) > 0
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'maps_dataview.html',
                  {'list': map_list, 'count': len(map_list), 'can_upload': can_create_new_map})


@login_required(login_url='/account_login/')
@permission_required('S', 'item_name', Common_Utils.get_info_item_content_type('maps', 'map_info'))
def save_map(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "save_map", "Save map ino",
                                     request.path_info)
    response = HttpResponse()
    try:
        map_title = request.POST.get("map_title")
        # map_title = 'map_' + map_title
        map_name = request.GET.get("item_name")
        if map_name == None or map_name == '':
            map_name = map_title.lower().replace(' ','_')
            # map_title = map_title.lower()
            # map_title = map_title.replace(' ', '_')
            # map_title = map_title + '_' + request.user.username
            map_name = Common_Utils.add_timestamp_to_string(map_title)
        image = request.POST.get('image')
        params_dict = {}
        params_dict['group_layers'] = json.loads(request.POST.get('group_layers'))
        params_dict['extent'] = request.POST.get('extent')

        # params_dict = json.loads(params)
        # si = Map_Info()
        # si.insert_row(map_title, map_name, params_dict, request.user)
        si = Map_Info.insert_or_update(map_title, map_name, params_dict, request.user)

        # Items_Permission().insert_row(si,map_name,request.user,'U','V')
        # Items_Permission().insert_row(si, map_name, request.user, 'U', 'S')
        if image is not None:
            icon_url = Common_Utils.save_icon(image=image, img_name=map_name)
            si.update_icon(icon_url)
        # response.write("200")
        res = {"status":200, "mapName": map_name}
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    return JsonResponse(res)


@login_required
@permission_required('O', 'item_name', Common_Utils.get_info_item_content_type('maps', 'map_info'))
def set_map_permission(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "create_map", "Create new map",
                                     request.path_info)
    response = HttpResponse()

    map_name = request.GET.get('item_name')
    try:
        map_info = Map_Info.objects.filter(name=map_name)[0]
        Items_Permission.set_item_permission(map_info, map_name, request, d_or_s_permission_type='S')
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    return HttpResponse('{"res_no":200, "res_text": "Permissions are added successfully"}')


@login_required(login_url='/account_login/')
def create_map(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "create_map", "Create new map",
                                     request.path_info)
    response = HttpResponse()
    try:
        http_referer = request.META.get('HTTP_REFERER', '')
        info = {}
        info["extent"] = list(SPATIAL_EXTENT_3857)
        info["group_layers"] = []
        return render(request, 'map_view.html', {"info": info, "map_name": ""})
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)


@permission_required('V', 'item_name', Common_Utils.get_info_item_content_type('maps', 'map_info'))
def view_map(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "view_map", "View Map",
                                     request.path_info)
    try:
        map_name = request.GET.get("item_name")
        map_info = list(Map_Info.objects.filter(name=map_name).values('params'))[0]
        info = {}
        info["extent"] = [float(e) if float(e) else str(e) for e in map_info['params']['extent'].split(",")]
        info["group_layers"] = map_info['params']['group_layers']
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'map_view.html', {"info": info, "map_name": map_name})


def add_layer_data_Jqx(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "add_layer_data_jqx", "Add layer data to Map",
                                     request.path_info)
    sel_type = request.GET.get("layer_type")
    root_node = []
    try:
        if sel_type == "dch":
            layer_categories = list(Info.objects.order_by('main_category').values_list('main_category').distinct())
            for cat in layer_categories:
                cat_node = {"label": cat[0], "value": "-1", "expanded": True, "items": [], "icon": ""}
                layer_Info = Info.objects.filter(main_category=cat[0]).order_by('name')
                for info in layer_Info:
                    layer_node = {"label": info.name, "value": info.layer_name, "icon": ""}
                    cat_node["items"].append(layer_node)
                root_node.append(cat_node)

        else:
            base_layers = ['Bing-Hybrid', 'Bing-Road', 'Bing-Aerial', 'OSM']
            for base_layer in base_layers:
                layer_node = {"icon": "", "label": base_layer, "value": base_layer}
                root_node.append(layer_node)
    except Exception as e:
        error_message = Log_Error.log_error_message(e, act_log)
    return HttpResponse(json.dumps(root_node))


def add_layer_data_JqxTreeGrid(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "add_layer_data_jqx", "Add layer data to Map",
                                     request.path_info)
    sel_type = request.GET.get("layer_type")
    root_node = []
    try:
        if sel_type == "dch":
            layer_categories = list(
                Info.objects.order_by('main_category').values_list('main_category', 'id').distinct())
            for cat in layer_categories:
                cat_node = {'id': cat[0], 'parentid': None, "label": cat[0], "value": "-1"}
                root_node.append(cat_node)
                layer_Info = Info.objects.filter(main_category=cat[0]).order_by('name')
                for info in layer_Info:
                    layer_node = {'id': info.name, 'parentid': cat[0], "label": info.name, "value": info.layer_name}
                    root_node.append(layer_node)

        else:
            base_layers = ['Bing-Hybrid', 'Bing-Road', 'Bing-Aerial', 'OSM']
            for base_layer in base_layers:
                layer_node = {'id': base_layer, 'parentid': None, "label": base_layer, "value": base_layer}
                root_node.append(layer_node)
    except Exception as e:
        error_message = Log_Error.log_error_message(e, act_log)
    return HttpResponse(json.dumps(root_node))


def add_layer_data_Ext(request):
    # var data = {
    #     expanded: true, children: [
    #         {text: 'detention', leaf: true},
    #         {text: 'homework', expanded: true, children: [
    #             {text: 'book report', leaf: true},
    #             {text: 'algebra', leaf: true}
    #         ]},
    #         {text: 'buy lottery tickets', leaf: true}
    #     ]
    # }
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "add_layer_data_Ext", "Add layer data to map",
                                     request.path_info)
    sel_type = request.GET.get("type")
    root_node = {"expanded": True, "children": []}
    try:
        if sel_type == "dch":
            layer_categories = list(Info.objects.order_by().values_list('main_category').distinct())
            for cat in layer_categories:
                cat_node = {"text": cat[0], "expanded": True, "children": []}
                layer_Info = Info.objects.filter(main_category=cat[0])
                for info in layer_Info:
                    layer_node = {"text": info.layer_name, "leaf": True}
                    cat_node["children"].append(layer_node)
                root_node["children"].append(cat_node)
        else:
            base_layers = ['Bing-Hybrid', 'Bing-Road', 'Bing-Aerial', 'OSM']
            for base_layer in base_layers:
                layer_node = {"text": base_layer, "leaf": True}
                root_node["children"].append(layer_node)
    except Exception as e:
        error_message = Log_Error.log_error_message(e, act_log)
    return HttpResponse(json.dumps(root_node))


@login_required
@permission_required('O', 'item_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def delete_map(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "map", "delete_map", "Delete Map",
                                     request.path_info)
    response = HttpResponse()
    try:
        map_name = request.GET.get('item_name')
        map_info = Map_Info.objects.filter(name=map_name)
        for info in map_info:
            info.delete()
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return HttpResponseRedirect(reverse('map_browser'))


#####################################3 spatial operations view ##############################33
# parameters wkt
def profile_extractor(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "map", "profile_extractor", "Extract earth terrain profile",
                                     request.path_info)
    try:
        # print("test")
        wkt = request.POST.get('wkt')
        surface_profile = Spatial_Operations().get_surface_profile(wkt, 3857)
        # print(wkt)
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return HttpResponse(json.dumps(surface_profile))


def get_admin_tree_json(request):
    code = request.GET.get('code')
    list_admin_name = ()
    if code == "irb":
        list_admin_name = ('province', 'irrigation_zone', 'irrigation_circle', 'irrigation_division')
    elif code == "bor":
        list_admin_name = ('province', 'division', 'district', 'tehsil', 'quanghoi', 'patwar_circle', 'mauza')
    elif code == "adb":
        list_admin_name = ('province', 'division', 'district', 'tehsil', 'union_council')
    elif code == "lg":
        list_admin_name = ('province', 'division', 'district', 'district_council', 'municipal_council')
    elif code == 'basin':
        list_admin_name = ('basin', 'drainage_basin', 'rivers_drainage_basin')
    sql = "select id, parent_id as parentid,admin_name as text  " \
          " ,admin_level_name from tbl_admin_hierarchy where admin_level_name in" + str(
        list_admin_name) + " ORDER BY admin_level_name,admin_name"

    json = getJSONFromDB(sql, 'spatialds')
    getsizeof(json)
    compressed = base64.b64encode(zlib.compress(str.encode(json), 9))
    getsizeof(json)
    response = {'result': compressed}
    # response = json.dump(response)
    return HttpResponse(compressed)
