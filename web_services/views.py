import json

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
# from ferrp.irrigation.models import PakDamsAndBarragesGS, DischargeDataGS, TblWqDetailGS, TblWlDetailGS
from ferrp.layers.models import Info
from ferrp.models import Activity_Log

from ferrp.site_selection.models import SiteSelectionSelectedsites
from ferrp.utils import Log_Error, DB_Query, Common_Utils, date_handler
from ferrp.web_services.layer_styling import Layer_Styling
from ferrp.web_services.models import *
from ferrp.web_services.wms_service import WMS_Service


def wms_service(request):
    act_log = Activity_Log()
    # act_log.insert_into_activity_log(request, "web_services", "WMS Get Map Service ", "WMS Get Map Services",
    #                                  request.path_info)
    response = HttpResponse()
    try:
        request_type = request.GET.get('request') if 'request' in request.GET else request.GET.get('request'.upper())
        format = request.GET.get('format') if 'format' in request.GET else request.GET.get('format'.upper())
        wms = WMS_Service()
        if request_type == 'GetMap' or request_type == 'GetTile':
            content = wms.get_map_service(request)
            if content is None:
                content = wms.create_empty_raster()
            return HttpResponse(content, content_type=format)
    except Exception as e:
        # Log_Error.log_view_error_message(response, e, act_log)
        Log_Error.log_error_message(e, act_log)
        content = wms.create_empty_raster();
        return HttpResponse(content, content_type=format)


def cesium_terrain_provider(request):
    act_log = Activity_Log()
    # act_log.insert_into_activity_log(request, "web_services", "WMS Get Map Service ", "WMS Get Map Services",
    #                                  request.path_info)
    response = HttpResponse()
    try:
        request_type = request.GET.get('request') if 'request' in request.GET else request.GET.get('request'.upper())
        format = request.GET.get('format') if 'format' in request.GET else request.GET.get('format'.upper())
    except Exception as e:
        # Log_Error.log_view_error_message(response, e, act_log)
        Log_Error.log_error_message(e, act_log)
        # content = wms.create_empty_raster();
        return HttpResponse("{}", content_type=format)


def get_layer_style_view(request):
    response = HttpResponse()
    layer_name = request.GET.get("layer_name")
    if layer_name.endswith("_ssa_"):
        style = Layer_Styling.get_functional_layer_style('ssa')
    else:
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        style = layer_info.style
    response.write(json.dumps(style))
    return response


def set_layer_style_view(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "Layer Style", "Layers Style",
                                     request.path_info)
    response = HttpResponse()
    try:
        data = json.loads(request.POST['data'])
        layer_name = request.POST.get("layer_name")
        infoobj = Info.objects.filter(layer_name=layer_name)[0]
        # infoobj.update(style=data['styles'])
        infoobj.style = data
        infoobj.save()
        act_log.update_complete_status()
        return HttpResponse("200")
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)


def upload_sld(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "upload sld", "Upload and set sld",
                                     request.path_info)
    response = HttpResponse()
    try:
        layer_name = request.GET.get('layer_name')
        file = request.FILES.get('file')
        # file_path_name = os.path.join(SHAPEFILE_PATH, layer_name + ".sld")
        # handle_uploaded_file(file, file_path_name)
        layer_styling = Layer_Styling(layer_name)
        layer_styling.process_sld(file)
        style = layer_styling.get_style()
        layer_styling.update_layer_style()
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)

    act_log.update_complete_status()
    response.write("200")
    return response


def add_feature(request):
    wkt = request.POST.get('wkt')
    project_id = request.POST.get('project_id')
    site_name = request.POST.get('site_name')
    geom = GEOSGeometry('SRID=3857;' + wkt)
    # g = ogr.CreateGeometryFromWkt(wkt)
    # g.flattenTo2D()
    # wkt = g.ExportToWkt()
    obj = SiteSelectionSelectedsites(project_id=project_id, site_name=site_name, created_by=request.user.id)
    obj.save(force_insert=True)
    query = "update site_selection_selectedsites set geom =ST_Force_2D(st_geomfromtext('" + wkt + "',3857)) where oid=" + str(
        obj.pk)
    res = DB_Query.execute_dml(query)
    response = {'result': 200}
    response = json.dumps(response)
    return HttpResponse(response)


def spatial_query_layer(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "spatial_query_layer", "Sptial Query on Layers",
                                     request.path_info)
    response = HttpResponse()
    try:
        layer_name1 = request.POST.get("layerName1")
        layer_name2 = request.POST.get("layerName2")
        grid_width = request.POST.get("gridWidth")
        spatial_op = request.POST.get("spatialOp")
        wkt = request.POST.get("wkt")
        layer_info1 = Info.objects.filter(layer_name=layer_name1)[0]
        if wkt == "":
            layer_info2 = Info.objects.filter(layer_name=layer_name2)[0]
            query = 'Select l1.* from "%s" l1,"%s" l2 where %s(l1.geom,l2.geom)' \
                    % (layer_info1.table_name, layer_info2.table_name, spatial_op)
        else:
            geom = GEOSGeometry(wkt)
            geom.srid = 3857
            if layer_info1.srid != 3857:
                geom.transform(layer_info1.srid)
            query = 'Select l1.* from "%s" l1 where %s(l1.geom,\'%s\')' \
                    % (layer_info1.table_name, spatial_op, geom)
        grid_width = int(grid_width) - 50
        # layer_info = Info.objects.filter(layer_name=layer_name)[0]
        query_res = DB_Query.get_jqx_columns_info_with_data(query, layer_info1.app_label, is_geom_include=False,
                                                            grid_width=grid_width)
        res = {"status": "202", "data": query_res}
        # res = {"status": 200}

        response.write(json.dumps(res))
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return response


def query_layer(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "query_layer", "Query Layer",
                                     request.path_info)
    response = HttpResponse()
    try:
        layer_name = request.POST.get("layer_name")
        if "new_layer_name" in request.POST: new_layer_name = request.POST.get("new_layer_name")
        if 'grid_width' in request.POST: grid_width = request.POST.get('grid_width')
        is_create_new_layer = request.POST.get("is_create_new_layer")
        where_clause = request.POST.get("where_clause")
        literals = request.POST.get("literals")
        where_clause_new = ""
        tokens = where_clause.split(" ")
        literals = literals.split(",")
        j = 0
        for i in range(len(tokens)):
            token = tokens[i]
            if token not in ["=", "AND", "OR", "NOT", "?", "(", ")"]:
                token = '"' + token + '"'
            if token == "?":
                token = "'" + literals[j] + "'"
                j = j + 1
            where_clause_new = where_clause_new + token + " "
        where_clause_new = where_clause_new[:len(where_clause_new) - 1]
        layer_info_list = list(Info.objects.filter(layer_name=layer_name))
        if len(layer_info_list) > 0:
            layer_info = layer_info_list[0]
            table_name = layer_info.table_name
            title = new_layer_name  # layer_info.name

            sub_query = 'Select * from "%s" where %s' % (table_name, where_clause_new)

            if Common_Utils.str_2_bool(is_create_new_layer) == True:
                title = Common_Utils.prepare_relation_name_4_db(title)
                view_name = "gis_" + Common_Utils.add_timestamp_to_string(title) + "_vw"
                # view_name = view_name.lower()
                query = 'Create view "%s" as %s' % (view_name, sub_query)
                # Log_Error.log_message(query)
                DB_Query.execute_dml(query)
                extent = Common_Utils.get_geom_extent(view_name)
                Info.insert_into_layer_info(layer_name=view_name, title=title, table_name=view_name,
                                            layer_type='Vector', orig_extent=extent,
                                            file_path_name=None, user=request.user,
                                            srid=layer_info.srid, orig_srid=layer_info.srid,
                                            geom_type=layer_info.geom_type,
                                            created_at=layer_info.created_at)
                # Info.add_layer_style(layer_info.style)
                ls = Layer_Styling(view_name)
                ls.add_layer_style(layer_info.style)

                res = {"status": "202", "new_layer_name": view_name}
            else:
                # sub_query

                grid_width = int(grid_width) - 50
                # layer_info = Info.objects.filter(layer_name=layer_name)[0]
                query_res = DB_Query.get_jqx_columns_info_with_data(sub_query, layer_info.app_label,
                                                                    is_geom_include=False,
                                                                    grid_width=grid_width)
                res = {"status": "202", "data": query_res}

        else:
            Common_Utils.bad_request("layer not found")

        response.write(json.dumps(res))
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return response


def get_query_filter(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "get_query_filter", "Get Filter Information for query",
                                     request.path_info)
    response = HttpResponse()
    try:
        res = {};
        layer_name = request.GET.get("layer_name")
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        cols = DB_Query.get_column_names(layer_info.table_name)
        filters = []
        for col in cols:
            data_type = "string"
            if col['column_name'] != "geom":
                filter = {"id": col['column_name'],
                          "label": col['column_name'],
                          }
                if col["data_type"] in ["integer"]:
                    data_type = "integer"
                else:
                    # query = 'Select distinct("%s") from %s' % (col['column_name'], layer_name)
                    # distinct_values = DB_Query.execute_query_as_list(query)
                    distinct_values = DB_Query.get_column_distinct_value(layer_info.table_name, col['column_name'])
                    filter["values"] = distinct_values
                    filter["input"] = "select"
                filter["type"] = data_type

                filters.append(filter)
        res = {"filters": filters}
        response.write(json.dumps(res))
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)

    act_log.update_complete_status()
    return response


def get_attribute_data(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "get_attribute_data", "Get Attribute Data",
                                     request.path_info)
    response = HttpResponse()
    try:
        layer_name = request.GET.get("layer_name")

        width = request.GET.get('width')
        width = round(float(width)) - 50
        layer_info = Info.objects.filter(layer_name=layer_name).first()
        # if layer_info.app_label == 'remote_app': settings.REMOTE_CONN_NAME = layer_info.remote_conn_name.name
        # if layer_info.layer_type == "Raster":
        #     query = 'SELECT (pvc).* ' \
        #             'FROM (SELECT ST_ValueCount(rast) As pvc ' \
        #             'FROM "%s") As foo ' \
        #             'ORDER BY (pvc).value ' % layer_info.table_name
        # else:
        #     query = 'Select * from "%s"' % layer_info.table_name
        # res = DB_Query.get_jqx_columns_info_with_data(query, layer_info.app_label, is_geom_include=False, grid_width=width)
        res = DB_Query.get_jqx_columns_info_and_data_of_layer(layer_info, is_geom_included=False, grid_width=width)
        # res["data"] = DB_Query.execute_query_as_dict(query,is_geom_include=False);
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)

    act_log.update_complete_status()
    # response.write(json.dumps(res))
    return JsonResponse(res)


def get_feature(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "get_feature_geometry", "Get Feature Geometry",
                                     request.path_info)
    response = HttpResponse()
    try:
        coordinate = request.GET.get('coordinate')

        layer_name = request.GET.get('layer_name')
        map_res = request.GET.get('resolution')
        layer_info = Info.objects.filter(layer_name=layer_name)

        geojson = '{ "type": "Point", "coordinates": [%s]}' % coordinate
        pnt = GEOSGeometry(geojson)
        pnt.srid = 3857
        if layer_info[0].srid != 3857:
            pnt.transform(layer_info[0].srid)
        pnt = pnt.buffer(float(map_res) * 2)
        # wkt = "POINT(%s)" %coordinate.replace(","," ")

        # query = "Select * from %s where st_intersects(geom,st_geomfromtext(%s))" %(layer_name,wkt)

        # result = DB_Query.get_geojson(layer_name, pnt=pnt, layer_type=layer_info.layer_type)
        result = DB_Query.get_geojson(layer_info[0].table_name, geom=pnt, layer_info=layer_info[0])

    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    response.write(json.dumps(result))
    return response


def get_feature_geometry(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "get_feature_geometry", "Get Feature Geometry",
                                     request.path_info)
    response = HttpResponse()
    try:
        res = {}
        layer_name = request.GET.get("layer_name")
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        oid = request.GET.get("oid")
        where_clause = "where oid in (%s)" % oid
        query = "Select st_astext(geom) from %s %s" % (layer_info.table_name, where_clause)
        res = DB_Query.execute_query_as_list(query)
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    response.write(json.dumps(res))
    return response


def get_admin_level_geometry(request):
    response = HttpResponse()
    try:
        res = {}
        level_id = request.GET.get("level_id")
        query = "Select st_astext(ST_SimplifyPreserveTopology(geom,1000)) from tbl_admin_hierarchy where id =" + level_id
        res = DB_Query.execute_query_as_list(query)
    except Exception as e:
        return Log_Error.log_view_error_message(request, e)
    response.write(json.dumps(res))
    return response


def create_network_topology(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "create_network_topology", "Create Network Topology",
                                     request.path_info)
    response = HttpResponse()
    try:
        res = {"status": 200}
        layer_name = request.POST.get("layerName")
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        # try:
        #     source_col_name = 'ferrp_net_source'
        #     target_col_name = "ferrp_net_target"
        #     cost_col_name = 'ferrp_net_cost'
        #     result = Common_Utils.test_column_exist(layer_info.table_name, source_col_name)
        #     if result is None:
        #         dml = 'ALTER TABLE "%s" ADD COLUMN "%s" integer' % (layer_info.table_name, source_col_name)
        #         DB_Query.execute_dml(query=dml)
        #     result = Common_Utils.test_column_exist(layer_info.table_name, target_col_name)
        #     if result is None:
        #         dml = 'ALTER TABLE "%s" ADD COLUMN "%s" integer' % (layer_info.table_name, target_col_name)
        #         DB_Query.execute_dml(query=dml)
        #     result = Common_Utils.test_column_exist(layer_info.table_name, cost_col_name)
        #     if result is None:
        #         dml = 'ALTER TABLE "%s" ADD COLUMN "%s" double precision' % (layer_info.table_name, cost_col_name)
        #         DB_Query.execute_dml(query=dml)
        #         query = 'Update "%s" set "%s"=st_length(geom)' % (layer_info.table_name, cost_col_name)
        #         DB_Query.execute_dml(query)
        # except Exception as e:
        #     Log_Error.log_error_message(e, act_log)

        error_tolerance = 10
        query = 'Create table "%s_LS" as (Select * ,(st_Dump(ST_LineMerge(ST_SnapToGrid(geom,%s)))).geom the_geom from %s)' \
                % (layer_info.table_name, error_tolerance, layer_info.table_name)
        result = DB_Query.execute_dml(query)

        query = "SELECT * FROM pgr_nodeNetwork('%s_LS',%s, 'oid', 'the_geom', 'edge')" % (
            layer_info.table_name, error_tolerance)
        result = DB_Query.execute_query_as_one(query)
        # query = "SELECT pgr_analyzeGraph('%s', %s)" %(layer_info.table_name, error_tolerance)
        # query = "select pgr_createTopology('%s', %s, the_geom:='geom', id:='oid'" \
        #         ", source := '%s', target := '%s')" % (layer_info.table_name, error_tolerance,
        #                                                source_col_name, target_col_name)
        query = "select pgr_createTopology('%s_LS_edge', %s)" % (layer_info.table_name, error_tolerance)
        result = DB_Query.execute_query_as_one(query)

        query = 'Drop table "%s_LS"' % (layer_info.table_name)
        result = DB_Query.execute_dml(query)
        if result == "OK":
            layer_info.isNetwork = True
            layer_info.save()
            res["status"] = "200"
            res["message"] = "Network sucessfully created"
        else:
            res["status"] = "404"
            res["message"] = "Failed to create a network"
            # print(result)
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    response.write(json.dumps(res))
    return response


def shortest_path_analysis(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "web_services", "create_network_topology", "Create Network Topology",
                                     request.path_info)
    response = HttpResponse()
    try:
        res = {"status": 200}
        layer_name = request.POST.get("layerName")
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        sourcePointWKT = request.POST.get("sourcePointWKT")
        destPointWKT = request.POST.get("destinationPointWKT")
        sourcePoint = GEOSGeometry(sourcePointWKT);
        sourcePoint.srid = 3857
        destinationPoint = GEOSGeometry(destPointWKT)
        destinationPoint.srid = 3857

        query = 'Select id, st_distance(the_geom,\'%s\') distance from "%s_LS_edge_vertices_pgr" ' \
                'order by distance limit 1' \
                % (sourcePoint, layer_info.table_name)
        sourcePointId = DB_Query.execute_query_as_one(query)
        query = 'Select id, st_distance(the_geom,\'%s\') distance from "%s_LS_edge_vertices_pgr" ' \
                'order by distance limit 1' \
                % (destinationPoint, layer_info.table_name)
        destinationPointId = DB_Query.execute_query_as_one(query)

        query = "SELECT *,(Select the_geom from \"%s_LS_edge\" ed where ed.id=dij.edge) geom FROM pgr_dijkstra('" \
                "SELECT id, source, target, st_length(the_geom) as cost FROM \"%s_LS_edge\"'," \
                "%s, %s, false) dij" % (layer_info.table_name, layer_info.table_name, sourcePointId, destinationPointId)

        result = DB_Query.execute_query_as_geojson(query=query)
        res["geojson"] = result

    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    response.write(json.dumps(res))
    return response


def convert_to_tree_obj(id, p, v, parent, dataField, data):
    if p == 'ids':
        v = '<button title="' + dataField + '"  value="' + v + '">Detail</button>'
    obj = {}
    obj['s_id'] = id
    obj['dataField'] = dataField
    obj['property'] = p
    obj['value'] = v
    obj['parent'] = parent
    data.append(obj)
    id = id + 1
    return id


def find_key_val_from_array(site_data, required_key):
    for s in site_data:
        if s['dataField'] == required_key:
            return s
    return None


def find_same_datafield_value_from_array(site_data, required_key):
    arr_obj = []
    for s in site_data:
        if s['dataField'] == required_key:
            arr_obj.append(s)
    return arr_obj


def summarize_data(data, site_data, site_id):
    for d in data[0]:
        if d['dataField'] == 'school_count':
            match_obj = find_key_val_from_array(site_data, 'school_count')
            if match_obj['value']:
                d['value'] = d['value'] + match_obj['value']
        if d['dataField'] == 'nearest_school':
            match_obj = find_key_val_from_array(site_data, 'nearest_school')
            if match_obj['value']:
                d['value'] = str(min([d['value'].split()[0], match_obj['value'].split()[0]])) + " " + \
                             match_obj['value'].split()[1]
        if d['dataField'] == 'hospital_count':
            match_obj = find_key_val_from_array(site_data, 'hospital_count')
            if match_obj['value']:
                d['value'] = d['value'] + match_obj['value']
        if d['dataField'] == 'nearest_hospital':
            match_obj = find_key_val_from_array(site_data, 'nearest_hospital')
            if match_obj['value']:
                d['value'] = str(min([d['value'].split()[0], match_obj['value'].split()[0]])) + " " + \
                             match_obj['value'].split()[1]
        if d['dataField'] == 'population_count':
            match_obj = find_key_val_from_array(site_data, 'population_count')
            if match_obj['value']:
                d['value'] = d['value'] + match_obj['value']

        if d['dataField'] == 'land_cover':
            match_obj_classes = find_same_datafield_value_from_array(site_data, 'land_cover_class')
            match_obj_ori = find_key_val_from_array(data[0], 'land_cover_class')
            if match_obj_ori:
                data[0].remove(match_obj_ori)
            new_id = data[0][-1:][0]['s_id'] + 1
            k = {'s_id': new_id, 'property': site_id, 'value': '', 'dataField': '', 'parent': d['s_id']}
            data[0].append(k)
            i = 1
            for c in match_obj_classes:
                c['s_id'] = new_id + i
                c['parent'] = new_id
                c['dataField'] = ''
                data[0].append(c)
                i = i + 1
        if d['dataField'] == 'disaster_info':
            match_obj_classes = find_same_datafield_value_from_array(site_data, 'hazard')
            match_obj_ori = find_key_val_from_array(data[0], 'hazard')
            if match_obj_ori:
                data[0].remove(match_obj_ori)
            new_id = data[0][-1:][0]['s_id'] + 1
            k = {'s_id': new_id, 'property': site_id, 'value': '', 'dataField': '', 'parent': d['s_id']}
            data[0].append(k)
            i = 1
            for c in match_obj_classes:
                c['s_id'] = new_id + i
                c['parent'] = new_id
                c['dataField'] = ''
                data[0].append(c)
                i = i + 1
    return data


def get_project_geo_stats(request):
    project_id = request.POST.get("project_id")
    buffer_dis = int(request.POST.get("buffer", 0))
    sites = SiteSelectionSelectedsites.objects.filter(project_id=project_id)
    data = []
    if sites.count() > 0:
        sites = list(sites.values())
        for site in sites:
            geom = site['geom']
            site_id = site['oid']
            site_data = get_geo_stats(request, geom, buffer_dis)
            if not data and len(site_data) > 0:
                data.append(site_data)
            else:
                data = summarize_data(data, site_data, site_id)
    data = {'data': data[0], 'buffer': buffer_dis}
    response = HttpResponse()
    response.write(json.dumps(data))
    return response


def get_geostatistics(request):
    wkt = request.POST.get("WKT")
    srid = 3857  # request.POST.get("srid")
    buffer_dis = int(request.POST.get("buffer", 0))
    geom = GEOSGeometry(wkt)
    geom.srid = srid
    data = get_geo_stats(request, geom, buffer_dis)
    data = {'data': data, 'buffer': buffer_dis}
    response = HttpResponse()
    response.write(json.dumps(data))
    return response


def get_geo_stats(request, geom, buffer_dis):
    act_log = Activity_Log()
    data = []
    id = 0
    parent_parent = None
    parent = 0
    res = {"msg": "Statistics with in 5 km distance"}
    try:
        # wkt = request.POST.get("WKT")
        # srid = 3857  # request.POST.get("srid")
        # buffer_dis = 5000
        # geom = GEOSGeometry(wkt)
        # geom.srid = srid
        pnt = geom
        buffer_geom = pnt.buffer(buffer_dis)
        # id = convert_to_tree_obj(id, 'Stats', 'Statistics with in 5 km distance', 0, data)
        ######################## School Stats
        school_objs = TblSchools.objects.filter(geom__distance_lte=(pnt, D(m=buffer_dis))).annotate(
            distance=Distance('geom', pnt)).order_by('distance')
        id = convert_to_tree_obj(id, 'School', '', parent_parent, 'school', data)
        parent = id - 1
        count = school_objs.count()
        distance = school_objs[0].distance.m if count > 0 else TblSchools.objects.all().annotate(
            distance=Distance('geom', pnt)).order_by('distance')[:1][0].distance.m
        id = convert_to_tree_obj(id, 'School Count', count, parent, 'school_count', data)

        id = convert_to_tree_obj(id, 'Nearest School Distance', str(round(distance, 2)) + " Meter", parent,
                                 'nearest_school', data)
        spk = []
        for obj in school_objs:
            spk.append(obj.pk)
        # res["schools"]["ids"] = spk
        id = convert_to_tree_obj(id, 'ids', str(spk), parent, 'school_ids', data)

        ############## Hospital Stats
        hospital_objs = TblHospitals.objects.filter(geom__distance_lte=(pnt, D(m=buffer_dis))).annotate(
            distance=Distance('geom', pnt)).order_by('distance')

        id = convert_to_tree_obj(id, 'Hospital', '', parent_parent, 'hospital', data)
        parent = id - 1
        count = hospital_objs.count()
        distance = hospital_objs[0].distance.m if count > 0 else TblHospitals.objects.all().annotate(
            distance=Distance('geom', pnt)).order_by('distance')[:1][0].distance.m
        id = convert_to_tree_obj(id, 'Hospital Count', count, parent, 'hospital_count', data)
        id = convert_to_tree_obj(id, 'Near Hospital Distance', str(round(distance, 2)) + " Meter", parent,
                                 'nearest_hospital', data)
        hpk = []
        for obj in hospital_objs:
            hpk.append(obj.pk)
        # res["hospitals"]["ids"] = hpk
        id = convert_to_tree_obj(id, 'ids', str(hpk), parent, 'hospital_ids', data)

        ############# Population
        id = convert_to_tree_obj(id, 'Population', '', parent_parent, 'population', data)
        query = 'Select ST_Union(rast) rast from "%s" where st_intersects(envelope,\'%s\')' % (
            TblPopulation2015._meta.db_table, buffer_geom)
        union_ras = DB_Query.execute_query_as_one(query)

        parent = id - 1
        if union_ras is not None:
            query = "Select ST_Clip('%s','%s') rast" % (union_ras, buffer_geom)
            clip_rast = DB_Query.execute_query_as_one(query)
            query = "SELECT (stats).sum totalPop FROM (SELECT ST_SummaryStatsAgg('%s', 1, TRUE, 1) AS stats) bar" % (
                clip_rast)
            summary_stats = int(DB_Query.execute_query_as_one(query))
        else:
            summary_stats = None
        id = convert_to_tree_obj(id, 'Total', summary_stats, parent, 'population_count', data)

        ################## Land Cover
        id = convert_to_tree_obj(id, 'Land Cover', '', parent_parent, 'land_cover', data)
        parent = id - 1
        query = 'Select ST_Union(rast) rast from "%s" where st_intersects(st_setsrid(envelope,3857),\'%s\')' % (
            TblGlCF._meta.db_table, buffer_geom)
        union_ras = DB_Query.execute_query_as_one(query)

        if union_ras is not None:
            query = "Select ST_Clip('%s','%s') rast" % (union_ras, buffer_geom)
            clip_rast = DB_Query.execute_query_as_one(query)

            query = "SELECT (pvc).* FROM (SELECT ST_ValueCount('%s') pvc ) As foo ORDER BY (pvc).value" % (clip_rast)
            count_val = DB_Query.execute_query_as_dict(query)
            res["Land Cover"] = {}

            for obj in count_val:
                class_name = TblGlcPunjabClasses.objects.values('classes')[int(obj["value"])]
                area_in_m = (int(obj["count"]) * 100 * 100) / (1000 * 1000)
                res["Land Cover"][class_name['classes']] = area_in_m
                id = convert_to_tree_obj(id, class_name['classes'], str(area_in_m) + " %", parent,
                                         'land_cover_class', data)
        else:
            parent = id - 1
            id = convert_to_tree_obj(id, 'Not_Found', None, parent, 'lc_not_found', data)

            #######Disaster Info
        id = convert_to_tree_obj(id, 'Disaster Info', '', parent_parent, 'disaster_info', data)
        parent = id - 1
        count = TblFlood2010.objects.filter(geom__intersects=pnt).count()
        flooded = "Yes" if count > 0 else "No"
        id = convert_to_tree_obj(id, 'Flood 2010', flooded, parent, 'hazard', data)

        count = TblFlood2014.objects.filter(geom__intersects=pnt).count()
        flooded = "Yes" if count > 0 else "No"
        id = convert_to_tree_obj(id, 'Flood 2014', flooded, parent, 'hazard', data)

        distance = TblEpicenter.objects.all().annotate(distance=Distance('geom', pnt)).order_by('distance')[:1][
            0].distance.m
        id = convert_to_tree_obj(id, 'Epic Center Distance', round(distance, 2), parent, 'hazard', data)
        obj = TblPGAInfo.objects.all().annotate(distance=Distance('geom', pnt)).order_by('distance')[:1]
        pga_val = obj[0].pga_inter if obj.count() > 0 else None
        id = convert_to_tree_obj(id, 'PGA Value', pga_val, parent, 'hazard', data)
        ####### Climate Info
        id = convert_to_tree_obj(id, 'Climate Info', '', parent_parent, 'climate_info', data)
        parent = id - 1
        climateLocationNoaa = ClimateLocationNoaa.objects.all().annotate(distance=Distance('geom', pnt)).distinct(
            'distance').order_by(
            'distance')[:3]
        for i in range(0, 3):
            distance = climateLocationNoaa[i].distance.m
            station_id = str(climateLocationNoaa[i].station_id)
            btn_distance = '<button title="climate"   value="' + station_id + '">' + str(
                round(distance, 2)) + '</button>'
            id = convert_to_tree_obj(id, 'Station ID:' + station_id, btn_distance, parent, 'climate', data)
        ####### Hydro Info
        id = convert_to_tree_obj(id, 'Hydro Info', '', parent_parent, 'hydro_info', data)
        parent = id - 1
        headwork = PakDamsAndBarragesGS.objects.all().annotate(distance=Distance('geom', pnt)).order_by('distance')[:1][
            0]
        distance = headwork.distance.m
        btn_detail = '<button title="headwork_detail"   value="' + headwork.dam_name + '">' + str(
            round(distance, 2)) + ' meters</button>'
        id = convert_to_tree_obj(id, 'Nearest Headwork:' + headwork.dam_name, btn_detail, parent, 'hydro_info', data)
        water_quality = TblWqDetailGS.objects.all().annotate(distance=Distance('geom', pnt)).order_by('distance')[:1][0]
        distance = water_quality.distance.m
        btn_detail = '<button title="water_quality"   value="' + str(water_quality.ql_id) + '">' + str(
            round(distance, 2)) + ' meters</button>'
        id = convert_to_tree_obj(id, 'Water Quality Nearest Piezometer:', btn_detail, parent, 'water_quality', data)
        water_level = TblWlDetailGS.objects.all().annotate(distance=Distance('geom', pnt)).order_by('distance')[:1][0]
        distance = water_level.distance.m
        btn_detail = '<button title="water_level"   value="' + str(water_level.ql_id) + '">' + str(
            round(distance, 2)) + ' meters</button>'
        id = convert_to_tree_obj(id, 'Water Level Nearest Piezometer:', btn_detail, parent, 'water_level', data)
    except Exception as e:
        return []
        # return Log_Error.log_view_error_message(request, e, act_log)
    # act_log.update_complete_status()
    # response.write(json.dumps(data))
    return data


def get_stats_detail(request):
    info_required = request.POST.get('infoRequired')
    ids = request.POST.get('ids')
    data = []
    if info_required == 'climate':
        data = list(ClimateLocationNoaa.objects.filter(station_id=ids).defer('geom').values())
    if info_required == 'school_ids':
        ids = json.loads(ids)
        data = list(TblSchools.objects.filter(oid__in=ids).values())
    if info_required == 'water_quality':
        ids = json.loads(ids)
        data = list(TblWqDetailGS.objects.filter(ql_id=ids).values())
    if info_required == 'water_level':
        ids = json.loads(ids)
        data = list(TblWlDetailGS.objects.filter(ql_id=ids).values())
    if info_required == 'headwork_detail':
        data = list(
            (DischargeDataGS.objects.filter(head_works=ids)).annotate(upstream=Coalesce('us', Value(-1)),downstream=Coalesce('ds', Value(-1))).values('head_works',
                                                                                                           'discharge_date',
                                                                                                           'discharge_time',
                                                                                                           'river',
                                                                                                           'downstream', 'upstream'))
    data = json.dumps(data, default=date_handler)
    return HttpResponse(data)
