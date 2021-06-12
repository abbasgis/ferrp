import base64

import zlib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from ferrp.survey_stats_app.admin_hierarchy_util import get_admin_hierarchy_json
from ferrp.survey_stats_app.survey_utils import get_tehsil_geojson, get_mauza_geojson, \
    get_admin_hierarchy_data, get_admin_geojson, get_mauza_survey_location_data, \
    get_survey_property_data, get_polygon_survey_location_data, get_commercial_facts, \
    get_mauza_survey_type_facts, get_survey_stats, get_survey_combined_level_data_geojson
from ferrp.survey_stats_app.utils import get_table_data, get_table_names, \
    get_survey_type_location_ids_tofromtime, get_server_table_names, import_survey_property_date_in_local_db, \
    get_survey_type_json_data


def insert_or_update_table_data(request):
    data = get_table_data(request)
    return HttpResponse(data)

# def insert_or_update_survey_table_data(request):
#     data = get_survey_table_data_bydate(request)
#     return HttpResponse(data)

def get_tables_list(self):
    data = get_table_names()
    return HttpResponse(data)

def get_server_tables_list(self):
    data = get_server_table_names()
    return HttpResponse(data)

def records_count_view(request, template=loader.get_template('counts.html')):
    return HttpResponse(template.render({}, request))

def records_transfer_view(request, template=loader.get_template('TransferData.html')):
    return HttpResponse(template.render({}, request))

def stats_view(request, template=loader.get_template('stats.html')):
    return HttpResponse(template.render({}, request))

def parse_survey_property_data(request):
    result = import_survey_property_date_in_local_db(request)
    return HttpResponse(result)

def get_survey_type_location_ids_list(request):
    ids_list_json = get_survey_type_location_ids_tofromtime(request)
    return HttpResponse(ids_list_json)

# def district_geojson(self):
#     district_data = get_district_geojson()
#     return HttpResponse(district_data)

def all_survey_data(self):
    all_data = get_survey_type_json_data()
    return HttpResponse(all_data)


def admin_geojson(request):
    admin_data = get_admin_geojson(request)
    return HttpResponse(admin_data)

def level_survey_stats(request):
    stats_data = get_survey_stats(request)
    compressed_json = base64.b64encode(zlib.compress(str.encode(stats_data), 9))
    return HttpResponse(compressed_json)

def tehsil_geojson(request):
    tehsil_data = get_tehsil_geojson(request)
    return HttpResponse(tehsil_data)

def mauza_geojson(request):
    mauza_data = get_mauza_geojson(request)
    return HttpResponse(mauza_data)

def admin_level_json(request):
    admin_json = get_admin_hierarchy_data(request)
    return HttpResponse(admin_json)

# def level_survey_stats(request):
#     stats_json = get_level_survey_stats(request)
#     return HttpResponse(stats_json)

def mauza_survey_location_data(request):
    data = get_mauza_survey_location_data(request)
    return HttpResponse(data)

def polygon_survey_location_data(request):
    data = get_polygon_survey_location_data(request)
    return HttpResponse(data)

def survey_property_data(request):
    json_data = get_survey_property_data(request)
    return HttpResponse(json_data)

#survey type Facts views
def mauza_survey_type_facts(request):
    json_data = get_survey_combined_level_data_geojson(request)
    return HttpResponse(json_data)




# Facts views

@login_required
def facts_view(request, template=loader.get_template('survey_type_facts.html')):
    return HttpResponse(template.render({}, request))

def commercial_facts(request):
    facts_json = get_commercial_facts(request)
    return HttpResponse(facts_json)

def admin_hierarchy_json(self):
    data = get_admin_hierarchy_json()
    return HttpResponse(data)