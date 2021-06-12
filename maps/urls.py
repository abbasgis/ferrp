from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from ferrp.maps.views import *

urlpatterns = [
    url(r'^$', map_browser, name='map_browser'),
    url(r'^view_map/$', view_map, name='view_map'),
    url(r'^create_map/$', create_map, name='create_map'),
    url(r'^save_map/$', save_map, name='save_map'),
    url(r'^delete_map/$', delete_map, name='delete_map'),
    url(r'^set_map_permission/$', set_map_permission, name='set_map_permission'),

    url(r'^add_layer_data/$', add_layer_data_JqxTreeGrid, name='add_layer_data'),

    # spatial functionalities
    url(r'^profile_extractor/$', profile_extractor, name='profile_extractor'),
    url(r'^get_admin_tree/$', get_admin_tree_json, name='get_admin_tree')

    # url(r'^$', TemplateView.as_view(template_name='index_ferrp.html'), name='home'),
]
