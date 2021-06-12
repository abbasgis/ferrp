import base64
import json
from django.apps import apps
import zlib
from django.db import connections
from django.db.models import Count, Sum

from ferrp.adp.utils import dictfetchall, get_model_dict_array
from ferrp.survey_stats_app.admin_hierarchy_util import get_admin_hierarchy_json
from ferrp.survey_stats_app.utils import get_table_geojson_query, date_handler, get_table_geojson_query_whereclause


def get_district_geojson():
    dist_geojson_query = get_table_geojson_query('district', 'district_id, district_name, extent')
    district_geojson = getQueryResultAsJson(dist_geojson_query)
    # compressed_geojson = base64.b64encode(zlib.compress(str.encode(district_geojson), 9))
    return district_geojson

def get_tehsil_geojson():
    dist_geojson_query = get_table_geojson_query('tehsil', 'tehsil_id, tehsil_name, extent')
    tehsil_geojson = getQueryResultAsJson(dist_geojson_query)
    # compressed_geojson = base64.b64encode(zlib.compress(str.encode(tehsil_geojson), 9))
    return tehsil_geojson

def get_qanungoi_geojson():
    geojson_query = get_table_geojson_query('qanungoi_halqa', 'qanungoi_halqa_id, qanungoi_halqa_name, extent')
    geojson = getQueryResultAsJson(geojson_query)
    return geojson

def get_patwarcircle_geojson():
    geojson_query = get_table_geojson_query('patwar_circle', 'patwar_circle_id, patwar_circle_name, extent')
    geojson = getQueryResultAsJson(geojson_query)
    return geojson

def get_mauza_geojson():
    geojson_query = get_table_geojson_query('mauza', 'mauza_id, mauza_name, extent')
    geojson = getQueryResultAsJson(geojson_query)
    return geojson

def get_admin_geojson(request):
    survey_stats = get_survey_stats(request)
    # survey_type_locations = get_survey_combined_level_geojson(request)

    district_geojson = get_district_geojson()
    tehsil_geojson = get_tehsil_geojson()
    qanungoi_geojson = get_qanungoi_geojson()
    patwarcircle_geojson = get_patwarcircle_geojson()
    mauza_geojson = get_mauza_geojson()

    district_type_counts = district_surveytype_counts()
    tehsil_type_counts = tehsil_surveytype_counts()
    qanungoi_type_counts = qanungoi_surveytype_counts()
    patwarcircle_type_counts = patwarcircle_surveytype_counts()
    mauza_type_counts = mauza_surveytype_counts()

    admin_geoJson = json.dumps({
        'survey_stats': survey_stats,
        # 'survey_type_locations': survey_type_locations,

        'district':district_geojson,
        'tehsil':tehsil_geojson,
        'qanungoi': qanungoi_geojson,
        'parwar_circle': patwarcircle_geojson,
        'mauza':mauza_geojson,

        'district_type_counts':district_type_counts,
        'tehsil_type_counts': tehsil_type_counts,
        'qanungoi_type_counts': qanungoi_type_counts,
        'patwarcircle_type_counts': patwarcircle_type_counts,
        'mauza_type_counts': mauza_type_counts
    },
    default=date_handler)
    compressed_geojson = base64.b64encode(zlib.compress(str.encode(admin_geoJson), 9))
    return compressed_geojson

def get_admin_hierarchy_data(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    model_data = None
    model_data_rows = None
    if level == 'district_id':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='district')
        model_data_rows = list(model_data.objects.all().order_by('district_name'))
    if level == 'tehsil_id':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='tehsil')
        model_data_rows = list(model_data.objects.filter(district_id = value).order_by('tehsil_name'))
    if level == 'qanungo_halka_id':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='QanungoiHalqa')
        model_data_rows = list(model_data.objects.filter(tehsil_id = value).order_by('qanungoi_halqa_name'))
    if level == 'patwar_circle_id':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='PatwarCircle')
        model_data_rows = list(model_data.objects.filter(qanungoi_halqa_id = value).order_by('patwar_circle_name'))
    if level == 'mauza_id':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='mauza')
        model_data_rows = list(model_data.objects.filter(patwar_circle_id = value).order_by('mauza_name'))
    model_data_rows_dict = get_model_dict_array(model_data_rows)
    model_table_json = json.dumps(model_data_rows_dict, default=date_handler)
    compressed_json = base64.b64encode(zlib.compress(str.encode(model_table_json), 9))
    return model_table_json

def get_survey_stats(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    bridges_model = apps.get_model(app_label='survey_stats_app', model_name='Bridges')
    collaspe_building = apps.get_model(app_label='survey_stats_app', model_name='CollaspeBuilding')
    commercial_model = apps.get_model(app_label='survey_stats_app', model_name='commercial')
    derajaat = apps.get_model(app_label='survey_stats_app', model_name='derajaat')
    educational = apps.get_model(app_label='survey_stats_app', model_name='educational')
    graveyard = apps.get_model(app_label='survey_stats_app', model_name='graveyard')
    health_facility = apps.get_model(app_label='survey_stats_app', model_name='healthfacility')
    industry = apps.get_model(app_label='survey_stats_app', model_name='industry')
    infrastructure = apps.get_model(app_label='survey_stats_app', model_name='Infrastructure')
    mauza_general_survey = apps.get_model(app_label='survey_stats_app', model_name='MauzaGengralSurvey')
    parks = apps.get_model(app_label='survey_stats_app', model_name='parks')
    public_building = apps.get_model(app_label='survey_stats_app', model_name='publicbuilding')
    religious_building = apps.get_model(app_label='survey_stats_app', model_name='religiousbuilding')
    residential = apps.get_model(app_label='survey_stats_app', model_name='residential')
    terminal = apps.get_model(app_label='survey_stats_app', model_name='terminal')
    bridges_count = None
    commercial_count = None
    collaspe_building_count = None
    derajaat_count = None
    educational_count = None
    graveyard_count = None
    health_facility_count = None
    industry_count = None
    infrastructure_count = None
    mauza_general_survey_count = None
    parks_count = None
    public_building_count = None
    religious_building_count = None
    residential_count = None
    terminal_count = None,
    if level == 'punjab':
        bridges_count = bridges_model.objects.count()
        commercial_count = commercial_model.objects.count()
        collaspe_building_count = collaspe_building.objects.count()
        derajaat_count = derajaat.objects.count()
        educational_count = educational.objects.count()
        graveyard_count = graveyard.objects.count()
        health_facility_count = health_facility.objects.count()
        industry_count = industry.objects.count()
        infrastructure_count = infrastructure.objects.count()
        mauza_general_survey_count = mauza_general_survey.objects.count()
        parks_count = parks.objects.count()
        public_building_count = public_building.objects.count()
        religious_building_count = religious_building.objects.count()
        residential_count = residential.objects.count()
        terminal_count = terminal.objects.count()
    elif level == 'district_id':
        bridges_count = bridges_model.objects.filter(district_id = value).count()
        commercial_count = commercial_model.objects.filter(district_id = value).count()
        collaspe_building_count = collaspe_building.objects.filter(district_id = value).count()
        derajaat_count = derajaat.objects.filter(district_id = value).count()
        educational_count = educational.objects.filter(district_id = value).count()
        graveyard_count = graveyard.objects.filter(district_id = value).count()
        health_facility_count = health_facility.objects.filter(district_id = value).count()
        industry_count = industry.objects.filter(district_id = value).count()
        infrastructure_count = infrastructure.objects.filter(district_id = value).count()
        mauza_general_survey_count = mauza_general_survey.objects.filter(district_id = value).count()
        parks_count = parks.objects.filter(district_id = value).count()
        public_building_count = public_building.objects.filter(district_id = value).count()
        religious_building_count = religious_building.objects.filter(district_id = value).count()
        residential_count = residential.objects.filter(district_id = value).count()
        terminal_count = terminal.objects.filter(district_id = value).count()
    elif level == 'tehsil_id':
        bridges_count = bridges_model.objects.filter(tehsil_id = value).count()
        commercial_count = commercial_model.objects.filter(tehsil_id = value).count()
        collaspe_building_count = collaspe_building.objects.filter(tehsil_id = value).count()
        derajaat_count = derajaat.objects.filter(tehsil_id = value).count()
        educational_count = educational.objects.filter(tehsil_id = value).count()
        graveyard_count = graveyard.objects.filter(tehsil_id = value).count()
        health_facility_count = health_facility.objects.filter(tehsil_id = value).count()
        industry_count = industry.objects.filter(tehsil_id = value).count()
        infrastructure_count = infrastructure.objects.filter(tehsil_id = value).count()
        mauza_general_survey_count = mauza_general_survey.objects.filter(tehsil_id = value).count()
        parks_count = parks.objects.filter(tehsil_id = value).count()
        public_building_count = public_building.objects.filter(tehsil_id = value).count()
        religious_building_count = religious_building.objects.filter(tehsil_id = value).count()
        residential_count = residential.objects.filter(tehsil_id = value).count()
        terminal_count = terminal.objects.filter(tehsil_id = value).count()
    elif level == 'qanungoi_halqa_id':
        bridges_count = bridges_model.objects.filter(qanungoi_halqa_id = value).count()
        commercial_count = commercial_model.objects.filter(qanungoi_halqa_id = value).count()
        collaspe_building_count = collaspe_building.objects.filter(qanungoi_halqa_id = value).count()
        derajaat_count = derajaat.objects.filter(qanungoi_halqa_id = value).count()
        educational_count = educational.objects.filter(qanungoi_halqa_id = value).count()
        graveyard_count = graveyard.objects.filter(qanungoi_halqa_id = value).count()
        health_facility_count = health_facility.objects.filter(qanungoi_halqa_id = value).count()
        industry_count = industry.objects.filter(qanungoi_halqa_id = value).count()
        infrastructure_count = infrastructure.objects.filter(qanungoi_halqa_id = value).count()
        mauza_general_survey_count = mauza_general_survey.objects.filter(qanungoi_halqa_id = value).count()
        parks_count = parks.objects.filter(qanungoi_halqa_id = value).count()
        public_building_count = public_building.objects.filter(qanungoi_halqa_id = value).count()
        religious_building_count = religious_building.objects.filter(qanungoi_halqa_id = value).count()
        residential_count = residential.objects.filter(qanungoi_halqa_id = value).count()
        terminal_count = terminal.objects.filter(qanungoi_halqa_id = value).count()
    elif level == 'patwar_circle_id':
        bridges_count = bridges_model.objects.filter(patwar_circle_id = value).count()
        commercial_count = commercial_model.objects.filter(patwar_circle_id = value).count()
        collaspe_building_count = collaspe_building.objects.filter(patwar_circle_id = value).count()
        derajaat_count = derajaat.objects.filter(patwar_circle_id = value).count()
        educational_count = educational.objects.filter(patwar_circle_id = value).count()
        graveyard_count = graveyard.objects.filter(patwar_circle_id = value).count()
        health_facility_count = health_facility.objects.filter(patwar_circle_id = value).count()
        industry_count = industry.objects.filter(patwar_circle_id = value).count()
        infrastructure_count = infrastructure.objects.filter(patwar_circle_id = value).count()
        mauza_general_survey_count = mauza_general_survey.objects.filter(patwar_circle_id = value).count()
        parks_count = parks.objects.filter(patwar_circle_id = value).count()
        public_building_count = public_building.objects.filter(patwar_circle_id = value).count()
        religious_building_count = religious_building.objects.filter(patwar_circle_id = value).count()
        residential_count = residential.objects.filter(patwar_circle_id = value).count()
        terminal_count = terminal.objects.filter(patwar_circle_id = value).count()
    elif level == 'mauza_id':
        bridges_count = bridges_model.objects.filter(mauza_id = value).count()
        commercial_count = commercial_model.objects.filter(mauza_id = value).count()
        collaspe_building_count = collaspe_building.objects.filter(mauza_id = value).count()
        derajaat_count = derajaat.objects.filter(mauza_id = value).count()
        educational_count = educational.objects.filter(mauza_id = value).count()
        graveyard_count = graveyard.objects.filter(mauza_id = value).count()
        health_facility_count = health_facility.objects.filter(mauza_id = value).count()
        industry_count = industry.objects.filter(mauza_id = value).count()
        infrastructure_count = infrastructure.objects.filter(mauza_id = value).count()
        mauza_general_survey_count = mauza_general_survey.objects.filter(mauza_id = value).count()
        parks_count = parks.objects.filter(mauza_id = value).count()
        public_building_count = public_building.objects.filter(mauza_id = value).count()
        religious_building_count = religious_building.objects.filter(mauza_id = value).count()
        residential_count = residential.objects.filter(mauza_id = value).count()
        terminal_count = terminal.objects.filter(mauza_id = value).count()
    counts_array = {'bridges': bridges_count,
                    'collapse_building': collaspe_building_count,
                    'commercial': commercial_count,
                    'dera_jaat': derajaat_count,
                    'education': educational_count,
                    'graveyard': graveyard_count,
                    'health_facility': health_facility_count,
                    'industry': industry_count,
                    'infrastructure': infrastructure_count,
                    'mauza_general_survey': mauza_general_survey_count,
                    'parks': parks_count,
                    'public_building': public_building_count,
                    'religious_building': religious_building_count,
                    'residential': residential_count,
                    'terminal': terminal_count}
    json_data = json.dumps(counts_array, default=date_handler)
    return json_data

def get_mauza_survey_stats(mauza_id):
    bridges_model = apps.get_model(app_label='survey_stats_app', model_name='Bridges')
    collaspe_building = apps.get_model(app_label='survey_stats_app', model_name='CollaspeBuilding')
    commercial_model = apps.get_model(app_label='survey_stats_app', model_name='commercial')
    derajaat = apps.get_model(app_label='survey_stats_app', model_name='derajaat')
    educational = apps.get_model(app_label='survey_stats_app', model_name='educational')
    graveyard = apps.get_model(app_label='survey_stats_app', model_name='graveyard')
    health_facility = apps.get_model(app_label='survey_stats_app', model_name='healthfacility')
    industry = apps.get_model(app_label='survey_stats_app', model_name='industry')
    infrastructure = apps.get_model(app_label='survey_stats_app', model_name='Infrastructure')
    mauza_general_survey = apps.get_model(app_label='survey_stats_app', model_name='MauzaGengralSurvey')
    parks = apps.get_model(app_label='survey_stats_app', model_name='parks')
    public_building = apps.get_model(app_label='survey_stats_app', model_name='publicbuilding')
    religious_building = apps.get_model(app_label='survey_stats_app', model_name='religiousbuilding')
    residential = apps.get_model(app_label='survey_stats_app', model_name='residential')
    terminal = apps.get_model(app_label='survey_stats_app', model_name='terminal')

    bridges_count = bridges_model.objects.filter(mauza_id = mauza_id).count()
    commercial_count = commercial_model.objects.filter(mauza_id = mauza_id).count()
    collaspe_building_count = collaspe_building.objects.filter(mauza_id = mauza_id).count()
    derajaat_count = derajaat.objects.filter(mauza_id = mauza_id).count()
    educational_count = educational.objects.filter(mauza_id = mauza_id).count()
    graveyard_count = graveyard.objects.filter(mauza_id = mauza_id).count()
    health_facility_count = health_facility.objects.filter(mauza_id = mauza_id).count()
    industry_count = industry.objects.filter(mauza_id = mauza_id).count()
    infrastructure_count = infrastructure.objects.filter(mauza_id=mauza_id).count()
    mauza_general_survey_count = mauza_general_survey.objects.filter(mauza_id = mauza_id).count()
    parks_count = parks.objects.filter(mauza_id = mauza_id).count()
    public_building_count = public_building.objects.filter(mauza_id = mauza_id).count()
    religious_building_count = religious_building.objects.filter(mauza_id = mauza_id).count()
    residential_count = residential.objects.filter(mauza_id = mauza_id).count()
    terminal_count = terminal.objects.filter(mauza_id = mauza_id).count()

    counts_array = [{'name': 'bridges', 'value': bridges_count},
                    {'name': 'collapse_building', 'value': collaspe_building_count},
                    {'name': 'commercial', 'value': commercial_count},
                    {'name': 'dera_jaat', 'value': derajaat_count},
                    {'name': 'education', 'value': educational_count},
                    {'name': 'graveyard', 'value': graveyard_count},
                    {'name': 'health_facility', 'value': health_facility_count},
                    {'name': 'industry', 'value': industry_count},
                    {'name': 'infrastructure', 'value': infrastructure_count},
                    {'name': 'mauza_general_survey', 'value': mauza_general_survey_count},
                    {'name': 'parks', 'value': parks_count},
                    {'name': 'public_building', 'value': public_building_count},
                    {'name': 'religious_building', 'value': religious_building_count},
                    {'name': 'residential', 'value': residential_count},
                    {'name': 'terminal', 'value': terminal_count}]
    json_data = json.dumps(counts_array, default=date_handler)
    return json_data

def get_mauza_survey_location_data(request):
    mauza_id = request.GET.get('mauza_id')
    # model_data = apps.get_model(app_label='survey_stats_app', model_name='survey')
    # model_data_rows = list(model_data.objects.filter(mauza_id = mauza_id).order_by('mauza_id'))
    # model_data_rows_dict = get_model_dict_array(model_data_rows)
    mauza_survey_data = get_mauza_survey_stats(mauza_id)
    mauza_survey_location = get_table_geojson_query_whereclause('location', 'location_id, upload_datetime', 'mauza_id = ' + mauza_id)
    location_geojson = getQueryResultAsJson(mauza_survey_location)
    json_data = json.dumps({'survey_data':mauza_survey_data, 'survey_location':location_geojson}, default=date_handler)
    compressed_json = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed_json

def get_polygon_survey_location_data(request):
    wkt = request.GET.get('wkt')
    polygon_survey_query = 'select * from survey_combined where st_contains(st_geomFromText( \''+wkt+'\' ,3857), st_transform(geom,3857));'
    survey_geojson = getQueryResultAsJson(polygon_survey_query)
    json_data = json.dumps({'survey_data':survey_geojson}, default=date_handler)
    compressed_json = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed_json

def get_survey_property_data(request):
    survey_type_id = request.GET.get('survey_type_id')
    survey_id = request.GET.get('survey_id')
    model_data = None
    model_data_rows = None
    if survey_type_id == '1':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='residential')
        model_data_rows = list(model_data.objects.filter(survey_id = survey_id))
    if survey_type_id == '5':
        model_data = apps.get_model(app_label='survey_stats_app', model_name='commercial')
        model_data_rows = list(model_data.objects.filter(survey_id = survey_id))
    model_data_rows_dict = get_model_dict_array(model_data_rows)
    model_table_json = json.dumps(model_data_rows_dict, default=date_handler)
    compressed_json = base64.b64encode(zlib.compress(str.encode(model_table_json), 9))
    return compressed_json

def getQueryResultAsJson(strQuery, as_string = True):
    connection = connections['mhvra_local_db']
    cursor = connection.cursor()
    cursor.execute(strQuery)
    data = dictfetchall(cursor)
    if as_string == True:
        json_data = json.dumps(data, default=date_handler)
    else:
        json_data = data
    return json_data

# commercial facts starts here
def get_commercial_facts(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    commercial_facts = None
    if level == 'all':
        age_of_building_ft = get_table_data('AgeOfBuildingFt', 'age_of_building', 'age_of_building_count')
        building_effected_from_desaster_ft = get_table_data('BuildingEffectedFromDesasterFt', 'building_effected_from_desaster', 'building_effected_from_desaster_count')
        emergency_exit_ft = get_table_data('EmergencyExitFt', 'emergency_exit', 'emergency_exit_count')
        evacuation_plan_ft = get_table_data('EvacuationPlanFt', 'evacuation_plan', 'evacuation_plan_count')
        level_of_demage_ft = get_table_data('LevelOfDemageFt', 'level_of_demage', 'level_of_demage_count')
        plenth_level_of_building_ft = get_table_data('PlenthLevelOfBuildingFt', 'plenth_level_of_building', 'plenth_level_of_building_count')
        security_guard_ft = get_table_data('SecurityGuardFt', 'security_guard', 'security_guard_count')
        type_of_bussiness_ft = get_table_data('TypeOfBussinessFt', 'type_of_bussiness', 'type_of_bussiness_count')
        type_of_desaster_ft = get_table_data('TypeOfDesasterFt', 'type_of_desaster', 'type_of_desaster_count')
        commercial_facts = [{'age_of_building_ft': age_of_building_ft},
                            {'building_effected_from_desaster_ft': building_effected_from_desaster_ft},
                            {'emergency_exit_ft': emergency_exit_ft},
                            {'evacuation_plan_ft': evacuation_plan_ft},
                            {'level_of_demage_ft': level_of_demage_ft},
                            {'plenth_level_of_building_ft': plenth_level_of_building_ft},
                            {'security_guard_ft': security_guard_ft},
                            {'type_of_bussiness_ft': type_of_bussiness_ft},
                            {'type_of_desaster_ft': type_of_desaster_ft}]

    commercial_facts_json = json.dumps(commercial_facts, default=date_handler)
    compressed_json = base64.b64encode(zlib.compress(str.encode(commercial_facts_json), 9))
    return compressed_json

# syrvey type facts functions
def get_mauza_survey_type_facts(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    table_name = request.GET.get('table')
    model_table_json = None
    if table_name == 'BridgesFt':
        str_query = 'select * from agg_bridges_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'CollapseBuildingFt':
        str_query = 'select * from agg_collapse_building_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'CommercialFt':
        str_query = 'select * from agg_commercial_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'DerajaatFt':
        str_query = 'select * from agg_derajaat_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'EducationalFt':
        str_query = 'select * from agg_educational_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'GraveYardFt':
        str_query = 'select * from agg_graveyard_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'HealthFacilityFt':
        str_query = 'select * from agg_health_facility_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'IndustryFt':
        str_query = 'select * from agg_industry_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'InfrastructureFt':
        str_query = 'select * from agg_infrastructure_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'MauzaGengralSurvey':
        str_query = 'select * from mauza_gengral_survey where ' + level + ' = ' + value + ';'
        # model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'ParksFt':
        str_query = 'select * from agg_parks_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'PublicBuildingFt':
        str_query = 'select * from agg_public_building_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'ReligiousBuildingFt':
        str_query = 'select * from agg_religious_building_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    elif table_name == 'TerminalFt':
        str_query = 'select * from agg_terminal_ft(\'' + level + '\', ' + value + ')'
        model_table_json = getQueryResultAsJson(str_query)
    else:
        if level == 'mauza_id':
            model_data = apps.get_model(app_label='survey_stats_app', model_name=table_name)
            model_data_rows = list(model_data.objects.filter(mauza_id=value))
            model_data_rows_dict = get_model_dict_array(model_data_rows)
            model_table_json = json.dumps(model_data_rows_dict, default=date_handler)
        else:
            return None
    return model_table_json

def get_survey_type_name(tableName):
    if tableName == 'BridgesFt':
        return 'Bridges'
    if tableName == 'CollapseBuildingFt':
        return 'COLLAPSE BUILDING'
    if tableName == 'CommercialFt':
        return 'Commercial'
    if tableName == 'DerajaatFt':
        return 'DERA JAAT'
    if tableName == 'EducationalFt':
        return 'Education'
    if tableName == 'GraveYardFt':
        return 'Graveyard'
    if tableName == 'HealthFacilityFt':
        return 'Health Facility'
    if tableName == 'IndustryFt':
        return 'Industry'
    if tableName == 'InfrastructureFt':
        return 'Infrastructure'
    if tableName == 'ParksFt':
        return 'Parks'
    if tableName == 'MauzaGengralSurvey':
        return 'Mauza General Survey'
    if tableName == 'PublicBuildingFt':
        return 'Public Building'
    if tableName == 'ReligiousBuildingFt':
        return 'Religious Building'
    if tableName == 'TerminalFt':
        return 'Terminal'
    else:
        return None


def get_survey_combined_level_data(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    table_name = get_survey_type_name(request.GET.get('table'))
    survey_combined_model = apps.get_model(app_label='survey_stats_app', model_name='SurveyCombined')
    survey_combined_data = None
    if level == 'punjab':
        survey_combined_data = list(survey_combined_model.objects.all())
    elif level == 'district_id':
        survey_combined_data = list(survey_combined_model.objects.filter(district_id = value, survey_type_name = table_name))
    elif level == 'tehsil_id':
        survey_combined_data = list(survey_combined_model.objects.filter(tehsil_id = value, survey_type_name = table_name))
    elif level == 'qanungoi_halqa_id':
        survey_combined_data = list(survey_combined_model.objects.filter(qanungoi_halqa_id = value, survey_type_name = table_name))
    elif level == 'patwar_circle_id':
        survey_combined_data = list(survey_combined_model.objects.filter(patwar_circle_id = value, survey_type_name = table_name))
    elif level == 'mauza_id':
        survey_combined_data = list(survey_combined_model.objects.filter(mauza_id = value, survey_type_name = table_name))
    model_data_rows_dict = get_model_dict_array(survey_combined_data)
    model_table_json = json.dumps(model_data_rows_dict, default=date_handler)
    return model_table_json

def get_survey_combined_level_geojson(request):
    level = request.GET.get('level')
    value = request.GET.get('value')
    where_clause = ''
    survey_location = None
    if level == 'punjab':
        survey_location = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name',
                          ' survey_type_name = \'Bridges\' or survey_type_name = \'COLLAPSE BUILDING\' '
                          ' or survey_type_name = \'DERA JAAT\''
                          ' or survey_type_name = \'Education\' or survey_type_name = \'Graveyard\''                          
                          ' or survey_type_name = \'Health Facility\' or survey_type_name = \'Industry\''
                          ' or survey_type_name = \'Mauza General Survey\' or survey_type_name = \'Parks\''
                          ' or survey_type_name = \'Public Building\' or survey_type_name = \'Religious Building\''                          
                          ' or survey_type_name = \'Terminal\'')
    else:
        where_clause = level + ' = ' + value
        survey_location = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', where_clause)
    survey_geojson = getQueryResultAsJson(survey_location)
    geojson = json.dumps(survey_geojson, default=date_handler)
    return geojson

def get_survey_type_location_data():
    str_query = 'select survey_type_name, coords from survey_combined;'
    query_data = getQueryResultAsJson(str_query)
    return query_data


def get_survey_type_geojson_data():

    bridges = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Bridges'" )
    collapse_building = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'COLLAPSE BUILDING'")
    commercial = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Commercial'")
    dera_jaat = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'DERA JAAT'")
    education = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Education'")
    graveyard = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Graveyard'")
    health_facility = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Health Facility'")
    industry = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Industry'")
    infrastructure = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Infrastructure'")
    mgs = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Mauza General Survey'")
    parks = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Parks'")
    pb = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Public Building'")
    rb = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Religious Building'")
    res = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Residential'")
    ter = get_table_geojson_query_whereclause('survey_combined', 'survey_id, survey_type_name', "survey_type_name = 'Terminal'")

    json_of_geojson = [{'bridges':bridges, 'collapse_building': collapse_building, 'commercial':commercial, 'dera_jaat':dera_jaat,
                        'education':education, 'graveyard':graveyard, 'health_facility':health_facility, 'industry':industry,
                        'infrastructure':infrastructure, 'mauza_general_survey':mgs, 'parks':parks, 'pb':pb, 'rb':rb, 'res':res, 'ter':ter}]
    return json_of_geojson

def district_surveytype_counts():
    surveytype_counts_model = apps.get_model(app_label='survey_stats_app', model_name='DistrictSurveyTypeCount')
    surveytype_counts_data = list(surveytype_counts_model.objects.all().order_by('survey_type_name'))
    surveytype_counts_dict = get_model_dict_array(surveytype_counts_data)
    surveytype_counts_json = json.dumps(surveytype_counts_dict, default=date_handler)
    return surveytype_counts_json

def tehsil_surveytype_counts():
    surveytype_counts_model = apps.get_model(app_label='survey_stats_app', model_name='TehsilSurveyTypeCount')
    surveytype_counts_data = list(surveytype_counts_model.objects.filter(latlon__isnull = False).order_by('survey_type_name'))
    surveytype_counts_dict = get_model_dict_array(surveytype_counts_data)
    surveytype_counts_json = json.dumps(surveytype_counts_dict, default=date_handler)
    return surveytype_counts_json

def qanungoi_surveytype_counts():
    surveytype_counts_model = apps.get_model(app_label='survey_stats_app', model_name='QanungoiSurveyTypeCount')
    surveytype_counts_data = list(surveytype_counts_model.objects.filter(latlon__isnull = False).order_by('survey_type_name'))
    surveytype_counts_dict = get_model_dict_array(surveytype_counts_data)
    surveytype_counts_json = json.dumps(surveytype_counts_dict, default=date_handler)
    return surveytype_counts_json

def patwarcircle_surveytype_counts():
    surveytype_counts_model = apps.get_model(app_label='survey_stats_app', model_name='PatwarCircleSurveyTypeCount')
    surveytype_counts_data = list(surveytype_counts_model.objects.filter(latlon__isnull = False).order_by('survey_type_name'))
    surveytype_counts_dict = get_model_dict_array(surveytype_counts_data)
    surveytype_counts_json = json.dumps(surveytype_counts_dict, default=date_handler)
    return surveytype_counts_json

def mauza_surveytype_counts():
    surveytype_counts_model = apps.get_model(app_label='survey_stats_app', model_name='MauzaSurveyTypeCount')
    surveytype_counts_data = list(surveytype_counts_model.objects.filter(latlon__isnull = False).order_by('survey_type_name'))
    surveytype_counts_dict = get_model_dict_array(surveytype_counts_data)
    surveytype_counts_json = json.dumps(surveytype_counts_dict, default=date_handler)
    return surveytype_counts_json

def get_survey_combined_level_data_geojson(request):
    level = request.GET.get('level')
    survey_type_facts = get_mauza_survey_type_facts(request)
    survey_data = None
    if level == 'mauza_id':
        survey_data = get_survey_combined_level_data(request)
    json_data = json.dumps({'survey_data':survey_data, 'survey_geojson':None, 'survey_facts': survey_type_facts}, default=date_handler)
    compressed_json = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed_json

def get_table_data(table_name, groupby_column, sum_column):
    table_model = apps.get_model(app_label='survey_stats_app', model_name=table_name)
    table_data = table_model.objects.values(groupby_column).annotate(count=Sum(sum_column)).order_by(groupby_column)
    table_data_dict = get_dict_array(table_data)
    json_data = json.dumps(table_data_dict, default=date_handler)
    return json_data

def get_dict_array(rows):
    data_array = []
    for row in rows:
        data_array.append(row)
    return data_array

