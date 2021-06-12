from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.template import loader

from ferrp.adp.utils import date_handler
from ferrp.irrigation.IrrigationModels.Canals import getCanalsCombinedData, getLSectionData, getGuagesData, \
    getStructureData, \
    getGatesData, getROWData, getOutletsData, getCrossSectionHeightProfileData, getSelectedCanalsGeoJson, \
    getLSectionCombinedData, getGatesCombinedData, getGaugesCombinedData, getStructureCombinedData, \
    getOutletsCombinedData, canal_detail_data
from ferrp.irrigation.IrrigationModels.CommandedArea import getCombinedData, getDistrictsInformation
from ferrp.irrigation.IrrigationModels.DamsBarages import getDamsCombinedData, getDischargeData, to_from_discharge_data, \
    updateDischargeValue, getDamsGeoJson
from ferrp.irrigation.IrrigationModels.EMailModels import emailDataURL, smsDataURL, get_mail_sms_data
from ferrp.irrigation.IrrigationModels.GroundWater import get_json_geojson_data, get_ground_water_geojson_data, \
    get_water_level_detail, get_water_quality_detail, get_combined_level_quality_detail, get_level_year_type_data


def index(request):
    return HttpResponse("welcome to irrigation home.")

# @login_required(None, 'next', '../../admin/login')
def commanded_area(request, template=loader.get_template('commanded_area.html')):
    return HttpResponse(template.render({}, request))

# @login_required(None, 'next', '../../admin/login')
def canals(request, template=loader.get_template('canals.html')):
    return HttpResponse(template.render({}, request))

# @login_required(None, 'next', '../../admin/login')
def dhb(request, template=loader.get_template('dams.html')):
    return HttpResponse(template.render({}, request))

# @login_required(None, 'next', '../../admin/login')
def ground_water(request, template=loader.get_template('ground_water.html')):
    return HttpResponse(template.render({}, request))

def getAdminGeoJson(request):
    data = getCombinedData(request)
    return HttpResponse(data)

def getCanalsData(self):
    data = getCanalsCombinedData()
    return  HttpResponse(data)

def selectedCanalsGeoJson(request):
    data = getSelectedCanalsGeoJson(request)
    return  HttpResponse(data)

def getDamsData(self):
    data = getDamsCombinedData()
    return  HttpResponse(data)

def getPunjabBarragesData(self):
    data = getDamsCombinedData()
    return  HttpResponse(data)

def getHWDischargeData(request):
    data = getDischargeData(request)
    return  HttpResponse(data)

def get_hw_to_from_discharge_data(request):
    data = to_from_discharge_data(request)
    return  HttpResponse(data)

def update_discharge_in_headworkds(request):
    data = updateDischargeValue(request)
    return HttpResponse(data)

def headworkds_geojson(request):
    data = getDamsGeoJson(request)
    return HttpResponse(data)

def getIrrigationGroundWaterData(self):
    data = get_json_geojson_data()
    return  HttpResponse(data)

def get_water_level_detail_data(request):
    data = get_water_level_detail(request)
    return  HttpResponse(data)

def get_water_quality_detail_data(request):
    data = get_water_quality_detail(request)
    return  HttpResponse(data)

def get_water_level_quality_detail_data(request):
    data = get_combined_level_quality_detail(request)
    return  HttpResponse(data)

def get_gw_levelyeartype_data(request):
    data = get_level_year_type_data(request)
    return HttpResponse(data)

def getIrrigationAdminDistricts(request):
    data = getDistrictsInformation(request)
    return  HttpResponse(data)

def getCanalsLSectionData(request):
    data = getLSectionCombinedData(request)
    return  HttpResponse(data)

def getCanalsGatesData(request):
    data = getGatesCombinedData(request)
    return  HttpResponse(data)

def getCanalsGuagesData(request):
    data = getGaugesCombinedData(request)
    return  HttpResponse(data)

def getCanalsStructureData(request):
    data = getStructureCombinedData(request)
    return  HttpResponse(data)

def getCanalsROWData(request):
    data = getROWData(request)
    return  HttpResponse(data)

def getCanalsOutletsData(request):
    data = getOutletsCombinedData(request)
    return  HttpResponse(data)

def get_canal_detail_data(request):
    data = canal_detail_data(request)
    return HttpResponse(data)

def emailDataService(request):
    emailDataURL(request)
    return HttpResponse("Email sent")
    # try:
    #
    #     return HttpResponse("Email sent")
    # except:
    #     return HttpResponse("Email not sent")

def smsDataService(request):
    resp = smsDataURL(request)
    return HttpResponse(resp)

def getOnlineDataView(request, template=loader.get_template('irrigation_data.html')):
    return HttpResponse(template.render())

def mail_sms_client_data(request):
    resp = get_mail_sms_data(request)
    return HttpResponse(resp)

def getHeightProfileDataFromWKT(request):
    data = getCrossSectionHeightProfileData(request)
    return  HttpResponse(data)

#test function
def getDamsGeoJsonData(self):
    data = getDamsGeoJson()
    return HttpResponse(data)