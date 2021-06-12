from django.conf.urls import url
from django.views.generic import TemplateView

from ferrp.irrigation.IrrigationModels.Canals import getLSectionCombinedData, canal_detail_data
from ferrp.irrigation.views import getAdminGeoJson, getCanalsData, getDamsData, getPunjabBarragesData, \
    getHWDischargeData, getIrrigationGroundWaterData, getIrrigationAdminDistricts, getCanalsLSectionData, \
    getCanalsGuagesData, getCanalsStructureData, getCanalsGatesData, emailDataService, getOnlineDataView, \
    getCanalsROWData, getHeightProfileDataFromWKT, getCanalsOutletsData, selectedCanalsGeoJson, smsDataService, \
    mail_sms_client_data, get_hw_to_from_discharge_data, update_discharge_in_headworkds, headworkds_geojson, \
    get_water_level_detail_data, get_water_quality_detail_data, get_water_level_quality_detail_data, \
    get_gw_levelyeartype_data, getDamsGeoJson, getDamsGeoJsonData, commanded_area, canals, dhb, ground_water, \
    get_canal_detail_data

urlpatterns = [
    url(r'^$', commanded_area, name='irrigation_home'),
    url(r'canals/$', canals, name='irrigation_canals'),
    url(r'dams/$', dhb, name='irrigation_dams'),
    url(r'groundwater/$', ground_water, name='irrigation_gw'),

    url(r'^irrigationstats', getAdminGeoJson, name='irrigationstats'),
    url(r'^admindistricts', getIrrigationAdminDistricts, name='admindistricts'),

    url(r'^canalsdata', getCanalsData, name='canalsdata'),
    url(r'^selectedcanalsgeojson', selectedCanalsGeoJson, name='selectedcanalsgeojson'),
    url(r'^lsection', getCanalsLSectionData, name='lsection'),
    url(r'^guages', getCanalsGuagesData, name='guages'),
    url(r'^structure', getCanalsStructureData, name='structure'),
    url(r'^gates', getCanalsGatesData, name='gates'),
    url(r'^row', getCanalsROWData, name='row'),
    url(r'^outlets', getCanalsOutletsData, name='row'),
    url(r'^canal_detail_data', get_canal_detail_data, name='canal_detail_data'),
    url(r'^onlineemailservice', emailDataService, name='onlineemailservice'),
    url(r'^linedemprofile', getHeightProfileDataFromWKT, name='linedemprofile'),

    url(r'^damsdata', getDamsData, name='damsdata'),
    url(r'^punjabBarragesdata', getPunjabBarragesData, name='punjabBarragesdata'),
    url(r'^hwdischarge', getHWDischargeData, name='hwdischarge'),
    url(r'^hwtofromdischarge', get_hw_to_from_discharge_data, name='hwtofromdischarge'),
    url(r'^updatedischarge', update_discharge_in_headworkds, name='updatedischarge'),
    url(r'^hwgeojson', headworkds_geojson, name='hwgeojson'),
    #test url
    url(r'^dam_geojson', getDamsGeoJsonData, name='dam_geojson'),

    url(r'^groundwaterdata', getIrrigationGroundWaterData, name='groundwaterdata'),
    url(r'^wl_detail_data', get_water_level_detail_data, name='wl_detail_data'),
    url(r'^wq_detail_data', get_water_quality_detail_data, name='wq_detail_data'),
    url(r'^wl_wq_detail_data', get_water_level_quality_detail_data, name='wl_wq_detail_data'),
    url(r'^level_year_type_data', get_gw_levelyeartype_data, name='level_year_type_data'),

    url(r'^onlinesmsservice', smsDataService, name='onlinesmsservice'),
    url(r'^onlinedataservice', getOnlineDataView, name='onlinedataservice'),
    url(r'^mailsmsdata', mail_sms_client_data, name='mailsmsdata'),

    #onlinedataservice
]