##########################################################
# act_log = Activity_Log()
# act_log.insert_into_activity_log(request, "ferrp", "upload sld", "Upload and set sld",
# request.path_info)
# response = HttpResponse()
# try:
#
# except Exception as e:
#     Log_Error.log_view_error_message(response, e, act_log)
#     return response
# act_log.update_complete_status()
# response.write("200")
# return response
##############################################################
import json
import os
import shutil

import datetime

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models import Extent
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from ferrp.decorators import permission_required, is_owner, can_download
from ferrp.layers.forms import ShapeFileFieldForm, LayerViewForm, RasterFieldForm
from ferrp.layers.gis_migration import drop_raster_tables, drop_spatial_table, set_layer_or_table_name, \
    create_raster_table_from_files, save_raster_in_db, create_extent_column_in_raster_table, convert_vector_layer_to_shp
from ferrp.layers.models import Info
from ferrp.layers.utils import read_shapefile, info_layer_context, importShapefile, create_raster_info
from ferrp.local_settings import SPATIAL_EXTENT_3857
from ferrp.models import Activity_Log, Items_Permission
from ferrp.projects.models import Directory, Projects, Files
from ferrp.projects.views import insert_project_info
from ferrp.settings import SHAPEFILE_PATH, RASTER_PATH
from ferrp.utils import Common_Utils, Log_Error, DB_Query, Model_Utils


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def layer_data_browse(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "Browse layers", "Browse vector and raster layers",
                                     request.get_full_path())
    response = HttpResponse()
    try:
        if request.user.is_superuser:
            layer_list = list(Info.objects.all().
                              values('name', 'layer_type', 'layer_name', 'srid', 'upload_at', 'icon', 'created_by',
                                     'created_at'))
        else:
            available = request.user.has_perm('ferrp.file_upload')
            entity_list = list(request.user.groups.values_list('name', flat=True))
            entity_list.append(request.user.username)
            entity_list.append("Public")
            layers_name_list = list(
                Items_Permission.objects.filter(entity_name__in=entity_list,
                                                permission_type__in=['V', 'O']).values_list(
                    'item_name', flat=True))
            layer_list = list(Info.objects.filter(layer_name__in=layers_name_list).
                              values('name', 'layer_type', 'layer_name', 'srid', 'upload_at', 'icon', 'created_by',
                                     'created_at'))
            can_download = len(
                list(Items_Permission.objects.filter(entity_name=request.user.username,
                                                     permission_type__in=['D', 'O']))) > 0
        layer_list = DB_Query.addPermissionType2Items(layer_list, 'layer_name', request.user, "O")
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()

    # layer_list_json = json.dumps(layer_list, default=myconverter)

    return render(request, 'layer_dataview.html', {'layer_list': layer_list, 'layer_count': len(layer_list)})


@login_required(login_url='/account_login/')
def upload_shapefile(request):
    action = request.GET.get('action', 'new')
    dir_id = request.GET.get('dir_id')
    project_id = request.GET.get('project_id')
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "Upload Shapefile", "Upload Shapefile",
                                     request.get_full_path())
    response = HttpResponse()
    try:
        if request.method == 'POST':
            # dir_id = request.POST.get('dir_id', '-1')
            # project_id = request.POST.get('project_id', '-1')
            # form = ShapeFileFieldForm(request.POST, request.FILES)
            # if form.is_valid():
            files = request.FILES.getlist('file_field')
            i = 0
            file_path = SHAPEFILE_PATH
            for f in files:
                # if f.name.endswith('.shp'): filename = f.name
                file_name_token = f.name.split('.')
                file_name = file_name_token[0]
                file_Ext = file_name_token[len(file_name_token) - 1]
                if i == 0:
                    file_name_timestamp = Common_Utils.add_timestamp_to_string(file_name_token[0])
                    file_path = os.path.join(SHAPEFILE_PATH, file_name_timestamp)
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                file_path_name = os.path.join(file_path, file_name_timestamp + '.' + file_Ext)
                Common_Utils.handle_uploaded_file(f, file_path_name)
                i = i + 1
            # res = readShapeFile(filename.replace(" ", "_"))
            return HttpResponse(file_name_timestamp)
        else:
            form = ShapeFileFieldForm()
        messages.add_message(request, messages.INFO,
                             'Click on chose file button to select file for uploading...')  # , extra_tags='alert'
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'shp_upload.html',
                  {'form': form, 'action': action, 'project_id': project_id, 'dir_id': dir_id,
                   'layer_type': 'shapefile'})


@login_required
def add2existing_shapefile(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "add2existing_shapefile", "Add Shapefile to Existing Model",
                                     request.get_full_path())
    response = HttpResponse()
    try:
        if request.method == 'POST':
            mapping = request.POST.get('mapping')
            mapping = json.loads(mapping)
            srid = request.POST.get('srid')
            app_label = request.POST.get('appLabel')
            model_name = request.POST.get('modelName')
            file_name = request.POST.get('fileName')
            file_path = os.path.join(SHAPEFILE_PATH, file_name)
            file_path_name = os.path.join(file_path, file_name + ".shp")
            ds = DataSource(file_path_name)
            model = apps.get_model(app_label, model_name)
            Model_Utils.lyr_2_model(ds[0], model, mapping, src_srid=srid)
            extent = str(Model_Utils.calculate_model_envelop(model))
            extent = extent[1:len(extent) - 1]
            objs = Info.objects.filter(app_label=app_label, lyr_model_name=model_name)
            layer_name = None
            i = 0
            for obj in objs:
                obj.extent = extent
                obj.save()
                if i == 0: layer_name = obj.layer_name
                i = i + 1
            return HttpResponse(json.dumps({"status": 200, "layerName": layer_name}))
        else:
            file_name = request.GET.get('file_name')
            print(file_name)
            shp_params = read_shapefile(file_name)
            app_list = Model_Utils.get_apps_with_model_name()
            # lyr_fields_list = []
            lyr_fields_list = [field['field_name'] for field in shp_params['fields']]
            lyr_fields_list.append(shp_params['geomtype'])
            envelop = [key for key in shp_params['envelop']]
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'layer_add2Existing.html', {'apps': app_list, 'lyrFieldList': json.dumps(lyr_fields_list),
                                                       'srs': shp_params['srs'], 'envelop': envelop,
                                                       'fileName': file_name})

    pass


@login_required
def info_shapefile(request):
    dir_id = request.GET.get('dir_id')
    project_id = request.GET.get('project_id')
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layer", "Shapefile Info", "Shapefile Description", "upload/shp/info/")
    file_name = request.GET.get('file_name')

    shpParam = read_shapefile(file_name);

    messages.add_message(request, messages.INFO,
                         'Confirm shapefile parameters and click on "Add Layer" button...')  # , extra_tags='alert'

    context = info_layer_context(shpParam)
    context['project_id'] = project_id
    context['dir_id'] = dir_id
    act_log.update_complete_status()
    return render(request, 'layer_parameters.html', context)


def create_view_vector_layer(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "create view Shapefile", "Create shapefile and display it",
                                     request.get_full_path())
    response = HttpResponse()
    try:
        user = request.user
        dir_id = request.POST['dir_id']
        project_id = request.POST['project_id']
        form = LayerViewForm(request.POST)  # FileFieldForm(request.POST, request.FILES)
        # if form.is_valid():
        # extent = list(SPATIAL_EXTENT_3857)
        extent = '' + request.POST.get('MinX') + ',' + request.POST.get('MinY') + ',' + request.POST.get(
            'MaxX') + ',' + request.POST.get('MaxY')
        title = request.POST.get('title')

        file_name = request.POST['file_name']
        # name = request.POST['name']
        layer_name = request.POST['layer_name']
        layer_type = request.POST['layer_type']
        # table_name = 'gis_'+layer_name
        orig_srid = int(request.POST['SRID'])
        srs = request.POST['SRS']
        geom_type = request.POST.get('geometry_type')
        created_at = request.POST.get('created_at')
        layer_type_lower = str.lower(layer_type)
        res = None
        if layer_type_lower in ['vector', 'shp', 'shapefile']:
            file_path = os.path.join(SHAPEFILE_PATH, file_name)
            file_path_name = os.path.join(file_path, file_name + ".shp")
            res = importShapefile(file_path_name, layer_name, orig_srid, srs)  # gis_added in table name
        # elif layer_type_lower == 'cad':
        #     file_path_name = os.path.join(CAD_PATH, file_name)
        #     res = import_cad_file(file_path_name, file_name, layer_name, srid, srs, geom_type)

        if type(res['table_name']) is str:
            res['table_name'] = {geom_type: res['table_name']}
        for key in res['table_name']:
            geom_type = key
            layer_name = res['table_name'][key]
            Info.insert_into_layer_info(layer_name, title, layer_name, 'Vector', extent, file_path_name, user,
                                        srid=3857, orig_srid=orig_srid, geom_type=geom_type,
                                        created_at=created_at)

        if dir_id != '' and dir_id != 'None':
            layer_info = Info.objects.filter(layer_name=layer_name).get()
            # layer_info = list(Info.objects.filter(layer_name=layer_name).values().order_by('-id'))[0]
            # Files().insert_row(layer_info, layer_name, proj_obj, dir_obj)
            insert_project_info(project_id, dir_id, title, layer_name, file_path_name, user, layer_info)

        messages.add_message(request, messages.SUCCESS, layer_name + ' layer successfully Uploaded.')
        act_log.update_complete_status()
        return HttpResponseRedirect(reverse('view_layer') + "?layer_name=" + layer_name)


    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)


@permission_required('V', 'layer_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def view_layer(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "Layers", "View Layer", "View Layer", request.get_full_path())
    response = HttpResponse()
    try:
        layer_name = request.GET.get('layer_name')

        info_list = list(Info.objects.filter(layer_name=layer_name))
        if len(info_list) > 0:
            info = info_list[0]
            if info.extent in [None, ""]:
                info.extent = list(SPATIAL_EXTENT_3857)
            else:
                if info.srid != 3857:
                    bbox = Polygon.from_bbox(info.extent.split(","))
                    bbox.srid = info.srid
                    bbox.transform(3857)
                    extent = str(bbox.extent)
                    info.extent = extent[1:len(extent)-1]
                info.extent = list(map(float, info.extent.split(",")))

            owner = True if request.user.is_superuser else is_owner(request.user, layer_name)
            download = True if owner == True else can_download(request.user.username, layer_name)

            context = {'layername': layer_name, 'info': info, "is_owner": owner, "can_download": download}
        else:
            messages.add_message(request, messages.ERROR,
                                 'You are not authorized to view this layer')  # , extra_tags='alert'
            return redirect('/')
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'layer_view_jqx.html', context=context)


# @login_required(login_url='/account_login/')
@permission_required('O', 'layer_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def set_layer_icon(request):
    image = request.POST.get('image')
    img_name = request.POST.get('img_name')
    # icon_request = str(request.body)
    # img_request = json.loads(icon_request)
    # img_name = img_request['img_name']
    icon_url = Common_Utils.save_icon(image=image, img_name=img_name)
    layer_info = Info.objects.filter(layer_name=img_name)
    layer_info.update(icon=icon_url)
    return HttpResponse("200")


# @login_required
@permission_required('D', 'layer_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def download_layer(request, *args, **kw):
    # if kw['redirect_path'] is not None: return redirect(kw['redirect_path'])
    layer_name = request.GET.get('layer_name')  # [4:]
    layer_info = Info.objects.filter(layer_name=layer_name)[0]
    file_path_name = layer_info.file_path
    if file_path_name == None or not os.path.exists(file_path_name):
        file_path_name = convert_vector_layer_to_shp(layer_info)

    file_path, file_name = os.path.split(file_path_name)
    zip_path_name = os.path.join(file_path, layer_name + ".zip")
    zip_file_name = os.path.join(layer_name + ".zip")
    if not os.path.exists(zip_path_name):
        # Files (local path) to put in the .zip
        # shpfile_ext = ['.shp', '.dbf', '.shx']
        file_names = []
        for fn in os.listdir(file_path):
            file_names.append(os.path.join(file_path, fn))
        # zip_files(file_name, filenames)
        # Folder name in ZIP archive which contains the above files
        zip_subdir = layer_name[4:]
        # zip_filename = "%s.zip" % zip_subdir
        # Open StringIO to grab in-memory ZIP contents
        # io.StringIO()
        s = Common_Utils.zip_files(zip_subdir, file_names)

    # Grab ZIP file from in-memory, make response with correct MIME-type
    # resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_file_name

    return resp


@login_required
@permission_required('O', 'layer_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def delete_layer(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "delete_layer", "Delete layer",
                                     request.path_info)
    response = HttpResponse()
    try:
        layer_name = request.GET.get('layer_name')
        layer_type = request.GET.get('layer_type')
        layer_info = Info.objects.filter(layer_name=layer_name).first()
        file_path_name = layer_info.file_path
        table_name = layer_info.table_name
        res = False

        if file_path_name != None and os.path.exists(file_path_name):
            file_path, file_name = os.path.split(layer_info.file_path)
            # file_name = layer_name[4:]
            try:
                shutil.rmtree(file_path)
            except Exception as e:
                print(e)

        if str.lower(layer_type) == 'raster':
            res = drop_raster_tables(layer_info)
            # file_path = os.path.join(RASTER_PATH, file_name)
        elif str.lower(layer_type) == 'vector':
            res = drop_spatial_table(layer_info)
            # file_path = os.path.join(SHAPEFILE_PATH, file_name)


    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return HttpResponse(json.dumps(res))


def get_layer_extent(request):
    try:
        layer_name = request.GET.get("layer_name")
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        arr_extent = layer_info.extent.split(",")
        if len(arr_extent) != 4:
            extent = DB_Query.get_geom_extent_in_3857(layer_info.table_name, layer_info.srid,
                                                      layer_type=layer_info.layer_type)
            arr_extent = extent.split(",")
            if len(arr_extent) != 4:
                arr_extent = SPATIAL_EXTENT_3857
                # arr_extent = extent.split(",")
            layer_info.extent = extent
            layer_info.save()
    except Exception as e:
        arr_extent = SPATIAL_EXTENT_3857
        # arr_extent = extent.split(",")
    res = {"minX": arr_extent[0], "minY": arr_extent[1], "maxX": arr_extent[2], "maxY": arr_extent[3]}
    return HttpResponse(json.dumps(res))


def get_layer_permission(request):
    layer_name = request.GET.get("layer_name")
    user_view_entities = list(
        Items_Permission.objects.filter(item_name=layer_name, entity_type='U', permission_type='V').values_list(
            'entity_name', flat=True))
    dept_view_entities = list(
        Items_Permission.objects.filter(item_name=layer_name, entity_type='D', permission_type='V').values_list(
            'entity_name', flat=True))

    user_download_entities = list(
        Items_Permission.objects.filter(item_name=layer_name, entity_type='U', permission_type='D').values_list(
            'entity_name', flat=True))
    dept_download_entities = list(
        Items_Permission.objects.filter(item_name=layer_name, entity_type='D', permission_type='D').values_list(
            'entity_name', flat=True))
    return HttpResponse(json.dumps({"viewUser": user_view_entities, "downloadUser": user_download_entities,
                                    "viewDept": dept_view_entities, "downloadDept": dept_download_entities}))


@login_required
@permission_required('O', 'item_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def set_layer_permission(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "set_layer_permision", "Set layer permission",
                                     request.path_info)
    response = HttpResponse()
    try:
        layer_name = request.GET.get('item_name')
        # view_users = request.GET.get('view_users')
        # view_depts = request.GET.get('view_depts')
        # download_users = request.GET.get('download_users')
        # download_depts = request.GET.get('download_depts')
        #
        layer_info = Info.objects.filter(layer_name=layer_name)[0]
        Items_Permission.set_item_permission(item_object=layer_info, item_name=layer_name,
                                             request=request, d_or_s_permission_type='D')
        Items_Permission.delete_item_permission(item_object=layer_info, item_name=layer_name,
                                                request=request, d_or_s_permission_type='D')
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
        return HttpResponse('{"res_no":404, "res_text": "Failed to add Permission"}')
    act_log.update_complete_status()
    return HttpResponse('{"res_no":200, "res_text": "Permissions are added successfully"}')


@login_required()
def upload_raster(request):
    act_log = Activity_Log()
    response = HttpResponse()
    action = request.GET.get('action', 'new')
    dir_id = request.GET.get('dir_id')
    project_id = request.GET.get('project_id')
    user = request.user
    # if request.user.has_perm('dhaisl.file_upload'):
    try:
        if request.method == 'POST':
            dir_id = request.POST['dir_id']
            project_id = request.POST['project_id']
            files = request.FILES.getlist('select_raster')
            raster_name = request.POST.get("raster_name")
            raster_type = request.POST.get("raster_type")
            no_of_files = request.POST.get("no_of_files")
            file_index = request.POST.get('file_index')
            raster_name = set_layer_or_table_name(raster_name)
            raster_srid = request.POST.get('raster_srid')
            file_path = os.path.join(RASTER_PATH, raster_name)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            f = files[0]
            file_Ext = os.path.splitext(f.name)[1]
            file_name = set_layer_or_table_name(f.name)
            # file_path_name = os.path.join(file_path, raster_name + file_Ext)
            file_path_name = os.path.join(file_path, file_name)
            Common_Utils.handle_uploaded_file(f, file_path_name)  #
            #         generate_sql_file(file_path_name, raster_name)
            result = {"res": "404"}
            if file_index == no_of_files:
                table_name = create_raster_table_from_files(file_path, raster_name, file_Ext, raster_srid)

                # table_name = set_layer_or_table_name(raster_name, 'raster')
                # file_path_name = os.path.join(file_path, "*." + file_Ext)
                # table_name = save_raster_in_db(file_path_name, table_name)
                # layer_name = create_raster_info(table_name, file_path_name, request.user)
                layer_name = table_name
                # # context = view_layer_context(layer_name)
                result = {"res": "200", "table_name": table_name, "layer_name": layer_name}

            else:
                result = {"res": "400"}
            act_log.update_complete_status()
            return HttpResponse(json.dumps(result))
        else:
            act_log.insert_into_activity_log(request, "layers", "Upload Raster", "Upload Raster", request.path_info)
            form = RasterFieldForm(initial={'raster_type': 'single'})
            messages.add_message(request, messages.INFO,
                                 'Click on chose file button to select file for uploading...')  # , extra_tags='alert'
            return render(request, 'rst_upload.html',
                          {'form': form, 'action': action, 'layer_type': 'raster', 'project_id': project_id,
                           'dir_id': dir_id})
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)


@login_required()
def process_raster(request):
    user = request.user
    act_log = Activity_Log()
    result = {"res": "working.."}
    response = HttpResponse()
    try:
        dir_id = request.POST['dir_id']
        project_id = request.POST['project_id']
        file_name = request.POST.get("file_name")
        file_name = set_layer_or_table_name(file_name)
        table_name = request.POST.get("table_name")
        raster_name = request.POST.get("raster_name")
        raster_type = request.POST.get("raster_type")
        raster_srid = request.POST.get("raster_srid")
        no_of_files = request.POST.get("no_of_files")
        file_index = request.POST.get("file_index")
        print("%s file no %s out %s" % (raster_name, file_index, no_of_files))
        raster_name = set_layer_or_table_name(raster_name)
        file_path = os.path.join(RASTER_PATH, raster_name)
        file_path_name = os.path.join(file_path, file_name)
        save_raster_in_db(file_path_name, table_name, raster_srid)
        result = {"res": "400"}
        if (file_index == no_of_files):
            act_log.insert_into_activity_log(request, "layers", "Process Raster",
                                             "Creating Raster Layer and Table",
                                             request.path_info)
            # create_overview_tables(table_name)
            create_extent_column_in_raster_table(table_name)
            layer_name = create_raster_info(table_name, file_path_name, request.user)

            if dir_id != '' and dir_id != 'None':
                layer_info = Info.objects.filter(layer_name=layer_name).get()
                # Files().insert_row(layer_info, layer_name, proj_obj, dir_obj)
                insert_project_info(project_id, dir_id, raster_name, layer_name, file_path_name, user, layer_info)
            result = {"res": "200", "table_name": table_name, "layer_name": layer_name}
    except MemoryError as m:
        print("Memory Error")
        result = {"res": "Memory Error"}
        return Log_Error.log_view_error_message(request, m, act_log)
    except Exception as e:
        result = {"res": "Generic Error"}
        return Log_Error.log_view_error_message(request, e, act_log)
    response.write(json.dumps(result))
    return response


def check_layer_name(request):
    isfound = False
    layer_name = set_layer_or_table_name(request.GET.get("layer_name"), request.GET.get("layer_type"))
    obj = Info.objects.filter(layer_name=layer_name)
    if obj._fields != None:
        isfound = True
    return HttpResponse(json.dumps(isfound))


@login_required
@permission_required('O', 'item_name', Common_Utils.get_info_item_content_type('layers', 'info'))
def set_layer_category(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "set_layer_permision", "Set layer permission",
                                     request.path_info)
    response = HttpResponse()
    try:

        layer_name = request.GET.get('item_name')
        category = request.GET.get('category', 'Unspecified')
        Info.objects.filter(layer_name=layer_name).update(main_category=category)
    except Exception as e:
        # return Log_Error.log_view_error_message(request, e, act_log)
        messages.add_message(request, messages.ERROR,
                             'Failed to add Category')  # , extra_tags='alert'
        return HttpResponseRedirect(reverse('view_layer') + "?layer_name=" + layer_name)
        # return HttpResponse('{"res_no":404, "res_text": "Failed to add Category"}')
    act_log.update_complete_status()
    messages.add_message(request, messages.SUCCESS,
                         'Category  added successfully')
    return HttpResponseRedirect(reverse('view_layer') + "?layer_name=" + layer_name)
    # return HttpResponse('{"res_no":200, "res_text": "Category  added successfully"}')
