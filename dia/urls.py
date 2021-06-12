from django.conf.urls import url

from ferrp.dia.views import *

urlpatterns = [
     url(r'^$', view_dia_project, name='view_dia_project'),
     # Map Page
     url(r'^view_mhvra_page/$', view_mhvra_page, name='view_mhvra_page'),
     # Section Page
     url(r'^view_dia_add_data/$', view_dia_add_data, name='view_dia_add_data'),
     # url(r'^/(?P<stub>[-\w]+)$', view_mhvra_main, name='view_mhvra_main-section-two'),
     url(r'^get_hazard_flood_data/$', get_hazard_flood_data , name='get_hazard_flood_data'),
     # get dia project data from admin ferrp
     url(r'^get_dia_data/$', get_dia_data , name='get_dia_data'),
     # mitigation design and plan
     url(r'^view_mitigation_design_plan/$', view_mitigation_design_plan , name='view_mitigation_design_plan'),
     # conclusion
     url(r'^view_section_five/$', view_section_five , name='view_section_five'),
     # mark location
     url(r'^view_mark_location/$', view_mark_location , name='view_mark_location'),
     # print Dia
     url(r'^print_dia$', print_dia , name='print_dia'),



]
