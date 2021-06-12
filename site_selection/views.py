import json
import urllib

from datetime import datetime

import requests
import urllib.request as urllib2
from django.db import connection, connections
from django.db.models.expressions import RawSQL, Value, F
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt

from ferrp.maps.models import Map_Info
from ferrp.models import Activity_Log
from ferrp.site_selection.models import *
from ferrp.utils import Log_Error, dictfetchall, date_handler, DB_Query


def view_map_ssa(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "view_map", "View Map",
                                     request.path_info)
    try:
        project_id = request.GET.get("scheme", '-1')
        page = request.GET.get("page", '')
        user_ppms = request.GET.get("u", '')
        # map_name = request.GET.get("item_name")
        map_name_server = 'map_site_selection_ferrppndsu_20181108235210041479'
        map_name = 'map_site_selection_ferrppndsu_20181108164434288554'
        map_name = map_name_server
        map_info = list(Map_Info.objects.filter(name=map_name).values('params'))[0]
        info = {}
        info["extent"] = [float(e) if float(e) else str(e) for e in map_info['params']['extent'].split(",")]
        group_layers = map_info['params']['group_layers']
        info["group_layers"] = json.dumps(group_layers)
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'map_view_full.html',
                  {"info": info, "map_name": map_name, 'project_id': project_id, 'page': page, 'user_ppms': user_ppms})


def get_district_names(request):
    districts = list(
        TblDistrict.objects.all().annotate(label=F('name_admin'), value=F('name_id')).values('label', 'value').order_by(
            'name_admin'))
    districts = json.dumps(districts, default=date_handler)
    return HttpResponse(districts)


def get_tehsil_names(request):
    distt_id = request.GET.get('dist_id', '-1')
    tehsils = list(
        TblTehsil.objects.filter(parent_id=distt_id).annotate(label=F('name_admin'), value=F('name_id')).values('label',
                                                                                                                'value').order_by(
            'name_admin'))
    tehsils_data = json.dumps(tehsils, default=date_handler)
    return HttpResponse(tehsils_data)

    pass


def get_sites_geojson(request):
    project_id = request.POST.get('project_id')
    if project_id == '-1':
        project_id = None
    table_name = 'site_selection_selectedsites'
    query = "Select oid,project_id,site_name,geom from %s where project_id = '%s' " % (table_name, project_id)
    d = DB_Query.execute_query_as_geojson(query, geom_col='geom')
    return HttpResponse(json.dumps(d))


@csrf_exempt
def calculate_site(request):
    params = {"cmb_district": 1, "cmbTehsil-inputEl": 25, "cmbSite-inputEl": "School",
              "rb-rs_hospital_gsd_100": "Far", "rb-rs_schools_gsd_100": "Far", "rb-rs_population_gsd_100": "Max"}
    params = request.POST
    funCondition = '('
    count = 0
    rasters = ''
    mapAlgebraSQL = 'SELECT ST_MapAlgebra(ARRAY['
    mapAlgebraFrom = ''
    str_rb = 'rb-'
    for index, key in enumerate(params):
        value = params[key]
        if key.startswith('rs_') and value != '-1':
            rastNum = count + 1
            tableName = key
            val = 'arrValue[' + str(rastNum) + '][1][1]'
            if value == '0':
                # if (radioButton == 'Outside' or radioButton == 'Min' or radioButton == 'Near'):
                val = '(1-arrValue[' + str(rastNum) + '][1][1])'
            funCondition = funCondition + val + '+'
            raster = 'raster' + str(
                count) + ' as (SELECT ST_resample(ST_Union(rs.rast),raster0.rast) as rast from ' + tableName + ' rs,distGeom,raster0 where st_intersects(extent,distGeom.geom) GROUP BY raster0.rast )'
            if (count == 0):
                raster = 'raster0 as(SELECT ST_Union(rast) as rast from ' + tableName + ' ,distGeom where st_intersects(extent,distGeom.geom))'
            rasters = rasters + ',' + raster
            mapAlgebraSQL = mapAlgebraSQL + 'ROW(raster' + str(count) + '.rast, 1),'
            mapAlgebraFrom = mapAlgebraFrom + 'raster' + str(count) + ','
            count = count + 1
    # mapAlgebraFrom = Substr(mapAlgebraFrom, 0, -1)
    mapAlgebraFrom[:-2] + ''
    # mapAlgebraSQL = Substr(mapAlgebraSQL, 0, -1)
    mapAlgebraSQL[:-2] + ''
    mapAlgebraSQL = mapAlgebraSQL[
                    :-1] + ']::rastbandarg[], \'ssma_mapAlgebra_callbackfunc(double precision[], int[], text[])\'::regprocedure) AS rast FROM ' + mapAlgebraFrom
    # funCondition = Substr(funCondition, 0, -1)
    funCondition[:-3] + ''
    funCondition = funCondition[:-1] + ')/' + str(count) + ';'
    mapAlgebraCallBack = "CREATE OR REPLACE FUNCTION ssma_mapAlgebra_callbackfunc(arrValue double precision[][][], pos integer[][], VARIADIC userargs text[]) RETURNS double precision AS $$ DECLARE returnVal float; BEGIN returnVal :=" + funCondition + " RETURN returnVal; END; $$ LANGUAGE 'plpgsql' IMMUTABLE;"
    updateRecordInDB(mapAlgebraCallBack)
    time_stamp = get_timestamp()
    d = TblTehsil.objects.filter(name_id=params['cmb_tehsil']).get()
    layerName = params['cmb_site'] + '_' + d.name_admin.lower() + '_' + str(time_stamp) + '_ssa_'
    distGeom = "SELECT st_transform(geom,900913) as geom from tbl_tehsil where name_id =" + str(
        params['cmb_tehsil'])
    sqlInsertOrUpdate = 'INSERT into rs_wms_temp (rast,layer_name,dist_id) VALUES ((SELECT finalRaster.rast from finalRaster),\'' + layerName + '\',' + str(
        params['cmb_tehsil']) + ')'
    layer_sql = "select * from rs_wms_temp WHERE layer_name ='" + layerName + "'"
    layer_result = getResultFromDB(layer_sql)
    if len(layer_result) > 0:
        sqlInsertOrUpdate = "update rs_wms_temp set rast =(SELECT finalRaster.rast from finalRaster) ,dist_id=" + \
                            params['cmb_tehsil'] + " where rid =" + layer_result[0].rid

    sql = 'with distGeom as (' + distGeom + ')' + rasters + ',mapAlgebra as(' + mapAlgebraSQL[
                                                                                :-1] + '), finalRaster as(select st_clip(mapAlgebra.rast,distGeom.geom) as rast from mapAlgebra,distGeom),temp_wms as(' + sqlInsertOrUpdate + ') SELECT st_xmin(geom) ||\',\'||st_ymin(geom)||\',\'||st_xmax(geom)||\',\'||st_ymax(geom) as bbox from distGeom'

    res = getResultFromDB(sql)
    sql = "update rs_wms_temp set envelope = st_envelope(rast);"
    updateRecordInDB(sql)
    data = {'layer_name': layerName, 'bbox': res[0]['bbox'], 'tehsil_id': params['cmb_tehsil'],
            'disttric_id': params['cmb_district']}
    data = json.dumps(data, default=date_handler)
    return HttpResponse(data)


from urllib.parse import urlencode, quote_plus


def remove_feature(request):
    # project_id = request.POST.get('project_id')
    oid = request.GET.get('oid')
    obj = SiteSelectionSelectedsites.objects.filter(oid=oid)
    obj.delete()
    response = {'result': 200}
    response = json.dumps(response)
    return HttpResponse(response)


def send_sms(request):
    params = request.POST
    phone_no = params['phone_no']
    message = params['message']
    url = params['url']
    data_url = shorten_url(url)
    message = message + '\n Location: ' + data_url
    message = quote_plus(message)
    #  message = urllib.parse.urlencode(message)
    sms_url = 'http://api.bizsms.pk/api-send-branded-sms.aspx?username=pnd@bizsms.pk&pass=p5890hg99&text=' + message \
              + '&masking=P&DD-FERRP&destinationnum=' + phone_no + '&language=English'
    response = urllib2.urlopen(sms_url)
    msg = response.msg
    data = {'message': ''}
    data = json.dumps(data, default=date_handler)
    return HttpResponse(data)


def shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format('AIzaSyDBKox6Urc8SUwws9mXT9zJFaDbQlN0FL8')
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    url_dict = r.json()
    return url_dict['id']


def getResultFromDB(sql):
    connection = connections['spatialds']
    cursor = connection.cursor()
    cursor.execute(sql)
    data = dictfetchall(cursor)
    return data


def updateRecordInDB(sql):
    connection = connections['spatialds']
    cursor = connection.cursor()
    cursor.execute(sql)
    return True


def get_timestamp(epoch=datetime(1970, 1, 1)):
    dt = datetime.utcnow()
    td = dt - epoch
    # return td.total_seconds()
    return int((td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6)
