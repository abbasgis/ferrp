import json
import requests
import zlib
import base64

import urllib.request as urllib2
from django.core.mail import send_mail
from ferrp.irrigation.IrrigationModels.AppFunctions import date_handler, getQueryResultAsJson, \
    get_whereclause_from_filters
from ferrp.irrigation.IrrigationModels.CommandedArea import getCommandedAreaStatsQuery, getDistrictQuery, \
    get_ca_query_for_filters, get_dist_query_for_filters
from ferrp.irrigation.Irrigation_Setting import CANALS_TABLE

def shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format('AIzaSyDBKox6Urc8SUwws9mXT9zJFaDbQlN0FL8')
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    url_dict = r.json()
    return url_dict['id']

# def smsDataURL(request):
#     datatype = request.POST.get('data_type')
#     whereClause = request.POST.get('where_clause')
#     contactNo = request.POST.get('contact_no')
#     paramsJson =  '?params=' + json.dumps({'data_type': datatype, 'where_clause': whereClause}, default=date_handler)
#     dataUrl = 'https://pnddch.info/irrigation/onlinedataservice' + paramsJson
#     short_url_dict = shorten_url(dataUrl)
#     data_url = short_url_dict['id']
#     sms_text = 'Irrigation Data:' + data_url
#
#     sms_url = 'http://api.bizsms.pk/api-send-branded-sms.aspx?username=pnd@bizsms.pk&pass=p5890hg99&text='+data_url\
#               +'&masking=P&DD-FERRP&destinationnum='+contactNo+'&language=English'
#     response = urllib2.urlopen(sms_url)
#     html = response.msg
#     return html
#
# def emailDataURLJsonParams(request):
#     datatype = request.POST.get('data_type')
#     whereClause = request.POST.get('where_clause')
#     emailAddress = request.POST.get('emailid')
#     paramsJson =  '?params=' + json.dumps({'data_type': datatype, 'where_clause': whereClause}, default=date_handler)
#     dataUrl = 'http://pnddch.info/irrigation/onlinedataservice' + paramsJson
#     short_url_dict = shorten_url(dataUrl)
#     send_mail('FERRP Irrigation data', short_url_dict['id'], 'ferrp.pnd@gmail.com', [emailAddress], fail_silently=False)

def smsDataURL(request):
    paramsJson = get_url_params(request)
    contactNo = request.POST.get('contact_no')
    dataUrl = 'http://pnddch.info/irrigation/onlinedataservice' + paramsJson
    # dataUrl = 'https://localhost:9898/irrigation/onlinedataservice' + paramsJson
    data_url = shorten_url(dataUrl)
    sms_url = 'http://api.bizsms.pk/api-send-branded-sms.aspx?username=pnd@bizsms.pk&pass=p5890hg99&text='+data_url\
              +'&masking=P&DD-FERRP&destinationnum='+contactNo+'&language=English'
    response = urllib2.urlopen(sms_url)
    html = response.msg
    return html

def emailDataURL(request):
    emailAddress = request.POST.get('emailid')
    paramsJson = get_url_params(request)
    dataUrl = 'http://pnddch.info/irrigation/onlinedataservice' + paramsJson
    # dataUrl = 'http://localhost:9898/irrigation/onlinedataservice' + paramsJson
    short_url = shorten_url(dataUrl)
    send_mail('FERRP Irrigation data', short_url, 'ferrp.pnd@gmail.com', [emailAddress], fail_silently=False)

def get_url_params(request):
    data_type = request.POST.get('data_type')
    whereClause = request.POST.get('where_clause')
    filter_array = request.POST.get('filters')
    paramsJson = '?data_type=' + data_type + '&where_clause=' + whereClause + '&filters=' + filter_array
    return paramsJson

def getQueryFromNullWhereClause(data_type):
    strQuery = ''
    if(data_type == 'commanded_area'):
        strQuery = 'select z.name, z.cca_ma::double precision, z.gca_ma::double precision, z.cca_geom_ma::double precision, ' \
                   'z.gca_geom_ma::double precision, z.channels_length_km::double precision as length, z.outlets::double precision  ' \
                   'FROM gis_zone_origs z ' + \
                   ' group by z.name, z.cca_ma, z.gca_ma, z.cca_geom_ma, z.gca_geom_ma, z.channels_length_km, z.outlets order by z.name;'
    if(data_type == 'canal'):
        strQuery = 'select zone_name, circle_name, division_name, channel_name, channel_type, imis_code, tail_rd::integer, '\
           'flowtype_e, head_x::integer, head_y::integer, tail_x::integer, tail_y::integer, gca::double precision, ' \
           'cca::double precision, (length_ft/(3.333*1000))::DOUBLE PRECISION as length_km, extent, geojson ' \
           'from %s order by zone_name asc, circle_name, division_name, channel_name;' %(CANALS_TABLE)
    if(data_type == 'canal_l_section'):
        strQuery = 'select * from canals_l_section'
    if (data_type == 'canal_gates'):
        strQuery = 'select * from canal_gates'
    if (data_type == 'canal_guages'):
        strQuery = 'select * from canal_gauges'
    if (data_type == 'canal_row'):
        strQuery = 'select * from canal_row'
    if (data_type == 'canal_structure'):
        strQuery = 'select * from canal_structure'
    if (data_type == 'dams'):
        strQuery = 'select dam_name, river, main_basin, near_city, catch_skm::DOUBLE PRECISION, main_use, extent, geojson ' \
               'from gis_pakistan_dam_and_barrages order by dam_name asc;'
    if (data_type == 'discharge'):
        strQuery = 'select * from discharge_data'
    if (data_type == 'ground_water'):
        strQuery = 'select id, zone, circle, division, ' \
               'disty_minor, major_canal, reclamation, type_wl_wq, elevation from gis_wq_wl ' \
               'order by zone, circle, division, major_canal;'
    return strQuery

def getQueryFromWhereClause(data_type, whereClause):
    strQuery = ''
    if(data_type == 'commanded_area'):
        splitWhereClause = whereClause.split('=')
        level = splitWhereClause[0].strip()
        value = splitWhereClause[1].strip().replace('\'', '');
        strQuery = getCommandedAreaStatsQuery(level, value)
    if (data_type == 'district'):
        splitWhereClause = whereClause.split('=')
        level = splitWhereClause[0].strip()
        value = splitWhereClause[1].strip().replace('\'', '');
        strQuery = getDistrictQuery(level, value)
    if (data_type == 'canal'):
        strQuery = 'select zone_name, circle_name, division_name, channel_name, channel_type, imis_code, tail_rd::integer,  ' \
                   'flowtype_e, head_x::integer, head_y::integer, tail_x::integer, tail_y::integer, gca::double precision, ' \
                   'cca::double precision, (length_ft/(3.333*1000))::DOUBLE PRECISION as length_km, extent, geojson ' \
                   'from %s  WHERE ' %(CANALS_TABLE) + whereClause + ' order by zone_name asc, circle_name, division_name, channel_name;'
    if (data_type == 'canal_l_section'):
        strQuery = 'select * from canals_l_section WHERE ' + whereClause
    if (data_type == 'canal_gates'):
        strQuery = 'select * from canal_gates WHERE ' + whereClause
    if (data_type == 'canal_guages'):
        strQuery = 'select * from canal_gauges WHERE ' + whereClause
    if (data_type == 'canal_row'):
        strQuery = 'select * from canal_row WHERE ' + whereClause
    if (data_type == 'canal_structure'):
        strQuery = 'select * from canal_structure WHERE ' + whereClause
    if (data_type == 'dams'):
        strQuery = 'select * from gis_pakistan_dam_and_barrages WHERE ' + whereClause + ' order by dam_name asc;'
    if (data_type == 'discharge'):
        strQuery = 'select * from discharge_data where ' + whereClause + ' and us is not null order by discharge_date asc;'
    if (data_type == 'ground_water'):
        strQuery = 'select * from gis_wq_wl where ' + whereClause + '  order by zone, circle, division, major_canal asc;'
    return strQuery

def get_query_whereclause_filter(data_type, whereClause, filters):
    strQuery = ''
    splitWhereClause = whereClause.split('=')
    level = splitWhereClause[0].strip()
    value = splitWhereClause[1].strip().replace('\'', '');
    complete_where_clause = ''
    if(value == 'null') or (value == 'undefined'):
        complete_where_clause = filters
    else:
        complete_where_clause = whereClause + ' and ' + filters
    if(data_type == 'commanded_area'):
        strQuery = get_ca_query_for_filters(level, complete_where_clause)
    if (data_type == 'district'):
        strQuery = get_dist_query_for_filters(level, complete_where_clause)
    if (data_type == 'canal'):
        strQuery = 'select zone_name, circle_name, division_name, channel_name, channel_type, imis_code, tail_rd::integer,  ' \
                   'flowtype_e, head_x::integer, head_y::integer, tail_x::integer, tail_y::integer, gca::double precision, ' \
                   'cca::double precision, (length_ft/(3.333*1000))::DOUBLE PRECISION as length_km, extent, geojson ' \
                   'from %s  WHERE ' %(CANALS_TABLE) + complete_where_clause + ' order by zone_name asc, circle_name, division_name, channel_name;'
    if (data_type == 'canal_l_section'):
        strQuery = 'select * from canals_l_section WHERE ' + complete_where_clause
    if (data_type == 'canal_gates'):
        strQuery = 'select * from canal_gates WHERE ' + complete_where_clause
    if (data_type == 'canal_guages'):
        strQuery = 'select * from canal_gauges WHERE ' + complete_where_clause
    if (data_type == 'canal_row'):
        strQuery = 'select * from canal_row WHERE ' + complete_where_clause
    if (data_type == 'canal_structure'):
        strQuery = 'select * from canal_structure WHERE ' + complete_where_clause
    if (data_type == 'dams'):
        strQuery = 'select * from gis_pakistan_dam_and_barrages WHERE ' + complete_where_clause + ' order by dam_name asc;'
    if (data_type == 'discharge'):
        strQuery = 'select * from discharge_data where ' + complete_where_clause + ' and us is not null order by discharge_date asc;'
    if (data_type == 'ground_water'):
        strQuery = 'select * from gis_wq_wl where ' + whereClause + '  order by zone, circle, division, major_canal asc;'
    return strQuery

def addEscapeCharacter(str):
    str = str.replace("'", "\\'");
    return str

def get_mail_sms_data(request):
    data_type = request.GET.get('data_type')
    where_clause = request.GET.get('where_clause')
    str_filter = request.GET.get('filters');
    filters_array = json.loads(str_filter)
    str_query = ''
    filter_where_clause = get_whereclause_from_filters(filters_array)

    length = len(filters_array)
    if (length == 0) and (where_clause == 'null'):
        str_query = getQueryFromNullWhereClause(data_type)
    elif (length == 0) and (where_clause != 'null'):
        str_query = getQueryFromWhereClause(data_type, where_clause)
    else:
        if (where_clause == 'null'): # or (where_clause.split('=')[1] == '\'\''):
            str_query = getQueryFromWhereClause(data_type, filter_where_clause)
        else:
            str_query = get_query_whereclause_filter(data_type, where_clause, filter_where_clause)

    json_data = getQueryResultAsJson(str_query)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed


# def getTableData(paramsJson):
#     # paramsJson = json.loads(params)
#     dataType = paramsJson['data_type']
#     whereClause = paramsJson['where_clause']
#     # whereClause = addEscapeCharacter(whereClause)
#     strQuery = ''
#     if(whereClause == 'null'):
#         strQuery = getQueryFromNullWhereClause(dataType)
#     elif(whereClause != 'null'):
#         strQuery = getQueryFromWhereClause(dataType, whereClause)
#     json_data = getQueryResultAsJson(strQuery, as_string=False)
#     return json_data
#
# def getGeoJsonData(paramsJson):
#     dataType = paramsJson['data_type']
#     whereClause = paramsJson['where_clause']
#     whereClause = addEscapeCharacter(whereClause)
#     strQuery = ''
#     if whereClause == 'null':
#         strQuery = getQueryFromNullWhereClause(dataType)
#     elif whereClause != 'null':
#         strQuery = getQueryFromWhereClause(dataType, whereClause)
#     json_data = getQueryResultAsJson(strQuery, as_string=False)
#     return json_data
#
# def getMailData(params):
#     paramsJson = json.loads(params)
#     tableData = getTableData(paramsJson)
#     geoJsonData = getGeoJsonData(paramsJson)
#     allData = json.dumps({'tableData': tableData, 'geoJsonData': geoJsonData, 'params':paramsJson}, default=date_handler)
#     allData = addEscapeCharacter(allData)
#     return allData
