import json


from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connections
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ferrp import settings
from ferrp.decorators import permission_required
from ferrp.integration.forms import ConnectionParamsForm, Table_List_Form
from ferrp.integration.models import *
from ferrp.integration.utils import *
from ferrp.layers.models import Info
from ferrp.models import Activity_Log
from ferrp.utils import Log_Error, DB_Query, date_handler


def app_integration(request):
    url = "#"
    app_name = request.GET.get("app")
    if app_name == "road_score":
        url = "http://45.79.6.169:88/ferrp/rsma/"
    elif app_name == "flood_analysis":
        url = "http://digitalarz.info/PDMAWeb/"
    elif app_name == "site_selection":
        url = "http://45.79.6.169:88/ferrp/ssma/"
    context = {"app_url": url}
    return render(request, "app_view.html", context=context)


def datamarts_browser(request):
    datamarts = list(DatabaseConnections.objects.all().values('title', 'name', 'created_by', 'created_at'))
    context = {"datamarts": datamarts}
    return render(request, "datamarts_browser.html", context=context)


@login_required
def conn_params_view(request):
    form = ConnectionParamsForm()
    context = {"form": form}
    return render(request, "conn_params.html", context=context)


@login_required
def add_or_get_connection_details(request):
    act_log = Activity_Log()
    # act_log.insert_into_activity_log(request, "integration", "add_onnection", "Add Connection",request.path_info)
    response = HttpResponse()
    try:
        connection = None
        info = None
        integrated_tables = []
        conn_name = request.GET.get("conn_name") if "conn_name" in request.GET.keys() else None
        if conn_name is None:
            form = ConnectionParamsForm(request.POST)
            res = "404"
            if form.is_valid():
                data = form.data
                info = Integration_Utils.form_data_2_database_connections(data)
                conn_name = info["name"]
                if not conn_name in settings.DATABASES.keys():
                    settings.DATABASES[conn_name] = info["conn_string"]

        else:
            obj = DatabaseConnections.objects.filter(name=conn_name).get()
            integrated_data = obj.integrated_data if obj.integrated_data is not None else {}

            for key in integrated_data:
                if "error" not in integrated_data[key].keys():
                    integrated_tables.append((key))
            if not conn_name in settings.DATABASES.keys():
                settings.DATABASES[conn_name] = obj.con_string
        connection = connections[conn_name]
        tables = connection.introspection.table_names()
        table_list_form = Table_List_Form(tables, conn_name, integrated_table_list=integrated_tables)
        if info:
            DatabaseConnections().insert_row(info["name"], info["title"], info["conn_string"], request.user)
        res = "200"
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log, redirect_path=reverse("conn_params"))
    act_log.update_complete_status()
    return render(request, 'tables_list.html', context={'form': table_list_form})


def test_connection(request):
    act_log = Activity_Log()
    # act_log.insert_into_activity_log(request, "integration", "test_onnection", "Test Connection",
    #                                  request.path_info)
    response = HttpResponse()
    try:
        form = ConnectionParamsForm(request.POST)
        res = "404"
        if form.is_valid():
            data = form.data
            info = Integration_Utils.form_data_2_database_connections(data)
            settings.DATABASES[info["name"]] = info["conn_string"]
            connection = connections[info["name"]]
            tables = connection.introspection.table_names()
            res = "200"
    except Exception as e:
        error_message = Log_Error.log_error_message(e)
        return HttpResponse("404")
    # act_log.update_complete_status()
    return HttpResponse(res)


@login_required
@permission_required('O', 'ds_name', Common_Utils.get_info_item_content_type('intgration', 'databaseconnections'))
def view_datasets(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "integration", "view_datasets", "View Datasets",
                                     request.path_info)
    response = HttpResponse()
    try:
        ds_name = request.GET.get("ds_name")
        db_objs = DatabaseConnections.objects.filter(name=ds_name)
        db_obj = db_objs[0] if db_objs.count() > 0 else None
        info_list = db_obj.integrated_data

    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'integrated_tables.html', context={'info_list': info_list, "ds_name": ds_name})


@login_required
@permission_required('O', 'Connection_Name',
                     Common_Utils.get_info_item_content_type('intgration', 'databaseconnections'))
def add_tables(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "integration", "test_onnection", "Test Connection",
                                     request.path_info)
    response = HttpResponse()
    res = {}
    try:
        db_obj = None
        conn_name = request.POST.get("Connection_Name")
        table_list = request.POST.get("table_list") if "table_list" in request.POST.keys() else None
        table_list = table_list.split(",")
        db_objs = DatabaseConnections.objects.filter(name=conn_name)
        db_obj = db_objs[0] if db_objs.count() > 0 else None
        settings.REMOTE_CONN_NAME = db_obj.name
        if not db_obj.name in settings.DATABASES.keys():
            settings.DATABASES[db_obj.name] = db_obj.con_string
        res = db_obj.integrated_data if db_obj.integrated_data is not None else {}

        app_label = 'remote_app'
        for table_name in table_list:
            try:
                spatial_key_column = DB_Query.get_spatial_and_key_column(app_label, table_name)
                if spatial_key_column["id"] is None:
                    res[table_name] = {"error": "Primary key doesn't exist"}
                elif "geom_field" in spatial_key_column.keys():

                    layer_name = Info.convert_spatial_table_into_layer_info(app_label, table_name, request.user,
                                                                            db_obj.title,
                                                                            spatial_key_column=spatial_key_column, )
                    res[table_name] = {"layer_name": layer_name} if layer_name is not None else {
                        "error": "Layer data doesn't exist"}
                else:
                    res[table_name] = {"table_name": table_name}
            except Exception as e1:
                Log_Error.log_error_message(e1)
                res[table_name] = {"error": str(e1)}
        db_obj.update_integrated_data(res)
    except Exception as e:
        if db_obj is not None:
            redirect_path = reverse("add_conn") + "?conn_name=" + db_obj.name
        else:
            redirect_path = reverse("conn_params")
        return Log_Error.log_view_error_message(request, e, act_log, redirect_path=redirect_path)
    act_log.update_complete_status()
    return render(request, 'integrated_tables.html', context={'info_list': res, "ds_name": conn_name})


@login_required
@permission_required('O', 'ds_name', Common_Utils.get_info_item_content_type('intgration', 'databaseconnections'))
def delete_table(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "integration", "test_onnection", "Test Connection",
                                     request.path_info)
    # response = HttpResponse()
    res = {}
    try:
        conn_name = request.GET.get("ds_name")
        key = request.GET.get("key")
        inner_key = request.GET.get("inner_key")
        obj = DatabaseConnections.objects.filter(name=conn_name).first()
        integrated_data = obj.integrated_data
        if inner_key == "layer_name":
            layer_name = integrated_data[key][inner_key]
            layer_info = Info.objects.filter(layer_name=layer_name).first()
            if layer_info is not None: layer_info.delete()
        if key in integrated_data:
            integrated_data.pop(key)
        obj.integrated_data = integrated_data
        obj.save()

    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return JsonResponse({"msg": "Data is succesfully deleted..."})


@login_required
def view_aspatial_table(request):
    table_name = request.GET.get("table_name")
    conn_name = request.GET.get("conn_name")
    db_obj = DatabaseConnections.objects.filter(name=conn_name).first()
    settings.REMOTE_CONN_NAME = db_obj.name
    if not db_obj.name in settings.DATABASES.keys():
        settings.DATABASES[db_obj.name] = db_obj.con_string
    query = 'Select * from "%s"' %table_name
    res = DB_Query.get_jqx_columns_info_with_data(query,'remote_app', False, 25000)
    return render(request,"common/table_viewer.html", context={"data":json.dumps(res, cls=DjangoJSONEncoder)})
    # return JsonResponse(res)
