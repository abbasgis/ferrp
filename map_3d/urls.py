from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='map_3d_jqx.html'), name='map_3d'),
    url(r'^view_layer_3d/$', vieew_layer_3d_map, name='view_layer_3d_map'),
]
