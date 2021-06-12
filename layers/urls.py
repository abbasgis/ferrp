from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', layer_data_browse, name='layer_browse'),
    url(r'^upload/shp/$', upload_shapefile, name='shp_upload'),
    url(r'^upload/shp/info/$', info_shapefile, name='shp_info'),
    url(r'^download/shp/$', download_layer, name='lyr_download'),
    url(r'^upload/add2existing/shp/$', add2existing_shapefile, name='shp_add2existing'),

    url(r'^upload/raster/$', upload_raster, name='raster_upload'),
    url(r'^upload/process_raster/$', process_raster, name='process_raster'),

    url(r'^check_layer_name/$', check_layer_name, name='check_layer_name'),
    url(r'^layer/createview/$', create_view_vector_layer, name='create_view_layer'),
    url(r'^viewlayer/$', view_layer, name='view_layer'),

    url(r'^layers/delete_layer/$', delete_layer, name='lyr_delete'),
    url(r'^layers/set_layer_icon/$', set_layer_icon, name='set_layer_icon'),
    url(r'^set_layer_permission/$', set_layer_permission, name='set_layer_permission'),
    url(r'^set_layer_category/$', set_layer_category, name='set_layer_category'),
    url(r'^get_layer_permission/$', get_layer_permission, name='get_layer_permission'),
    url(r'^get_layer_extent/$', get_layer_extent, name='get_layer_extent'),

]
