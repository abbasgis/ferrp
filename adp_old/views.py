from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
# Create your views here.
from ferrp.adp.utils import get_adp_report_data_from_model, get_adp_mpr_data_from_model, adpDistrictGeoJSON, \
    get_adp_yearly_analysis_data_from_model

@login_required(None, 'next', '../../admin/login')
def getADPReport(request, template=loader.get_template('adp_report.html')):
    return HttpResponse(template.render({}, request))

def get_adpreport_model_data(self):
    data = get_adp_report_data_from_model()
    return HttpResponse(data)

@login_required(None, 'next', '../../admin/login')
def getADPMPR(request, template=loader.get_template('adp_mpr.html')):
    return HttpResponse(template.render({}, request))

def getADPMPRData(request):
    data = get_adp_mpr_data_from_model()
    return HttpResponse(data)

@login_required(None, 'next', '../../admin/login')
def getADPanalysis(request, template=loader.get_template('adp_analysis.html')):
    return HttpResponse(template.render({}, request))

def getSchemesStats(request):
    data = get_adp_yearly_analysis_data_from_model()
    return HttpResponse(data)

def getDistrictGeoJSON(request):
    data = adpDistrictGeoJSON()
    return HttpResponse(data)