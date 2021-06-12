from django.conf.urls import url

from ferrp.survey_stats_app.admin_hierarchy_util import get_admin_hierarchy_json
from ferrp.survey_stats_app.views import records_count_view, \
    get_survey_type_location_ids_list, stats_view, insert_or_update_table_data, get_tables_list, \
    get_server_tables_list, parse_survey_property_data, records_transfer_view, all_survey_data, \
    admin_level_json, admin_geojson, level_survey_stats, mauza_survey_location_data, survey_property_data, \
    polygon_survey_location_data, facts_view, commercial_facts, mauza_survey_type_facts, admin_hierarchy_json

urlpatterns = [

    url(r'^counts_view/$', records_count_view, name='records_count_view'),
    url(r'^transfer_view/$', records_transfer_view, name='transfer_view'),
    url(r'^service', insert_or_update_table_data, name='insert_or_upate_data'),
    url(r'^tables', get_tables_list, name='tables'),
    # url(r'^survey', insert_or_update_survey_table_data, name='survey'),
    url(r'^server_tables', get_server_tables_list, name='server_tables'),
    url(r'^survey_ids_list', get_survey_type_location_ids_list, name='survey_ids_list'),
    url(r'^parse_survey_property', parse_survey_property_data, name='parse_survey_property_data'),
    # url(r'^district_geojson', district_geojson, name='district_geojson'),
    url(r'^all_data', all_survey_data, name='all_data'),


    # stats view urls
    # url(r'^$', stats_view, name='stats_view'),
    url(r'^admin_geojson', admin_geojson, name='admin_geojson'),
    url(r'^level_survey_stats', level_survey_stats, name='level_survey_stats'),
    url(r'^admin_level', admin_level_json, name='admin_level'),
    url(r'^mauza_survey_location_data', mauza_survey_location_data, name='mauza_survey_location_data'),
    url(r'^polygon_survey_location_data', polygon_survey_location_data, name='polygon_survey_location_data'),
    url(r'^survey_property', survey_property_data, name='survey_property'),

    # Facts view urls
    url(r'^$', facts_view, name='socio_economic_home'),
    url(r'^commercial_facts', commercial_facts, name='commercial_facts'),

    # survey types facts data
    url(r'^mauza_survey_type_facts', mauza_survey_type_facts, name='mauza_survey_type_facts'),

    # get admin hierarchy json
    url(r'^admin_hierarchy_json', admin_hierarchy_json, name='admin_hierarchy_json'),

]

