
from django.conf.urls import url, include
from django.contrib import admin

from ferrp.pc1 import views
from ferrp.pc1.utils import *

urlpatterns = [
    url(r'^$', views.index_template, name='pc1'),
    url(r'^modal_image/$', views.modal_image, name='modal_image'),
    url(r'^getSchemeNames/$', views.getSchemeNames, name='getSchemeNames'),
    url(r'^getSchemeDetail/$', views.getSchemeDetail, name='getSchemeDetail'),
    url(r'^view_scheme_plan/$', views.view_scheme_plan, name='view_scheme_plan'),

    url(r'^basic_info/$', views.getBasicInfoView, name='basic_info'),
    url(r'^specific_info/$', views.getSpecificInfoView, name='specific_info'),
    url(r'^location/$', views.getLocationInfoView, name='location_info'),

    url(r'^insert_basic_info_data_in_db', insert_basic_info_data_in_db, name='insert_basic_info'),
    url(r'^insert_annexure_in_db', insert_annexure_in_db, name='insert_annexure_in_db'),
    url(r'^get_scheme_pc1_detail', get_scheme_pc1_detail, name='get_scheme_pc1_detail'),
    url(r'^get_sample_file', download_sample, name='get_sample_file'),

]