from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^upload_sld/', upload_sld, name='upload_sld'),

    url(r'^wms/get_map/$', wms_service, name='wms_get_map'),
    url(r'^set_layer_style/$', set_layer_style_view, name='set_layer_style'),
    url(r'^get_layer_style/$', get_layer_style_view, name='get_layer_style'),

    url(r'^wfs/get_layer/data/$', get_attribute_data, name='get_attribute_data'),
    url(r'^wfs/query_layer/get_filter/$', get_query_filter, name='get_query_filter'),
    url(r'^wfs/query_layer/query/$', query_layer, name='query_layer'),
    url(r'^wfs/query_layer/spatial_query/$', spatial_query_layer, name='query_layer'),
    url(r'^wfs/add_feature/$', add_feature, name='add_feature'),
    url(r'^wfs/get_feature/geom/$', get_feature_geometry, name='get_feature_geometry'),
    url(r'^wfs/get_feature/geom/admin_level/$', get_admin_level_geometry, name='get_admin_level_geometry'),
    url(r'^wfs/get_feature/$', get_feature, name='get_feature'),

    url(r'^wps/create_network_topology/$', create_network_topology, name='create_network_topology'),
    url(r'^wps/shortest_path_analysis/$', shortest_path_analysis, name='shortest_path_analysis'),
    url(r'^wps/get_geostatics/$', get_geostatistics, name='get_geostatistics'),
    url(r'^wps/get_project_geo_stats/$', get_project_geo_stats, name='get_project_geo_stats'),
    url(r'^wps/get_stats_detail/$', get_stats_detail, name='get_stats_detail'),

    url(r'^3d/cesium_terrain_provider/$', cesium_terrain_provider, name='cesium_terrain_provider')
]
