from django.conf.urls import url
from django.views.generic import TemplateView

from ferrp.climate_change.views import get_temprature_rcp_data, view_climate_change_page, get_geojson_for_heatmap
from ferrp.site_selection.views import *

urlpatterns = [

    url(r'^$', view_map_ssa, name='view_ssa_page'),

    url(r'^get_district_names', get_district_names, name='get_district_names'),
    url(r'^get_tehsil_names', get_tehsil_names, name='get_tehsil_names'),
    url(r'^get_sites_geojson', get_sites_geojson, name='get_sites_geojson'),
    url(r'^ssa_search_site', calculate_site, name='ssa_search_site'),
    url(r'^ssa_send_sms', send_sms, name='ssa_send_sms'),
    url(r'^remove_feature', remove_feature, name='remove_feature'),

    # url(r'^get_temp_rcp_data/$', get_temprature_rcp_data, name='get_temp_rcp_data'),

]
