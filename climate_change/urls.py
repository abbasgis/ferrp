from django.conf.urls import url
from django.views.generic import TemplateView

from ferrp.climate_change.views import get_temprature_rcp_data, view_climate_change_page, get_geojson_for_heatmap

urlpatterns = [

    # url(r'^$', TemplateView.as_view(template_name='climate_change.html'), name='cc_main'),
    url(r'^$', view_climate_change_page, name='view_cc_page'),
    url(r'^get_temp_rcp_data/$', get_temprature_rcp_data, name='get_temp_rcp_data'),
    url(r'^get_temperature_geojson/$', get_geojson_for_heatmap, name='get_temperature_geojson'),


]
