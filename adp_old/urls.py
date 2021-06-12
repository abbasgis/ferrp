from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin

from ferrp.adp.utils import get_adp_report_data_from_model
from ferrp.adp.views import getADPReport, get_adpreport_model_data, getADPMPR, getADPMPRData, getADPanalysis, \
    getSchemesStats, getDistrictGeoJSON

urlpatterns = [

    url(r'^adpreport/$', getADPReport, name='adpreport'),
    url(r'adpReport/data', get_adpreport_model_data, name='adpReport'),

    url(r'adpmpr/$', getADPMPR, name='adpmpr'),
    url(r'adpMPR/data', getADPMPRData, name='adpmpr_data'),

    url(r'adpanalysis/$', getADPanalysis, name='adp_anaylsis'),
    url(r'^adpanalysis/adpstats', getSchemesStats, name='adp_schemesstats'),
    url(r'adpanalysis/adpmap', getDistrictGeoJSON, name='adp_districtmap'),

]