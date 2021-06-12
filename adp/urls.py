from django.conf.urls import url

from ferrp.adp.views import *

urlpatterns = [

    url(r'^$', adp_analysis_index, name='adp_anaylsis'),
    url(r'^adp_schemes', adp_yearly_analysis, name='adp_schemes'),

]