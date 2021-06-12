import os

from django.conf.global_settings import MEDIA_ROOT
from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from ferrp.pc1.utils import *


def index_template(request, template=loader.get_template('index.html')):
    sector_sql = "SELECT DISTINCT sec_name ,sec_id from adp_draft_201718_vw  ORDER BY sec_name;"
    sectors = get_query_result_as_array(sector_sql)
    return HttpResponse(template.render(
        {'sectors': sectors, 'scheme_names': []}, request))

@csrf_exempt
def getBasicInfoView(request, template=loader.get_template('pc1_proforma/basic_info.html')):
    scheme = request.GET.get('scheme')
    scheme_data = get_scheme_saved_data(request)
    scheme_annexures = get_scheme_annexures_data(request)
    if scheme == None or scheme == 'null' or scheme == '':
        return HttpResponse(template.render({'project_id': 'null', 'scheme_data': scheme_data, 'scheme_detail': 'null', 'scheme_annexures':'null'}, request))
    else:
        scheme_detail = get_scheme_detail(request)
        return HttpResponse(template.render({'project_id': scheme, 'scheme_data': scheme_data, 'scheme_detail': scheme_detail, 'scheme_annexures':scheme_annexures}, request))

def getSpecificInfoView(request, template=loader.get_template('pc1_proforma/specific_info.html')):
    scheme = request.GET.get('scheme')
    scheme_data = get_scheme_saved_data(request)
    if scheme == None or scheme == 'null' or scheme == '':
        return HttpResponse(template.render({'project_id': 'null', 'scheme_data': scheme_data, 'scheme_detail': 'null'}, request))
    else:
        scheme_detail = get_scheme_detail(request)
        return HttpResponse(template.render({'project_id': scheme, 'scheme_data': scheme_data, 'scheme_detail': scheme_detail}, request))

def getLocationInfoView(request, template=loader.get_template('pc1_proforma/location.html')):
    scheme = request.GET.get('scheme')
    if scheme == None or scheme == 'null' or scheme == '':
        return HttpResponse(template.render({'project_id': 'null', 'scheme_data': '', 'scheme_detail': 'null'}, request))
    else:
        scheme_detail = get_scheme_detail(request)
        scheme_data = get_scheme_saved_data(request)
        return HttpResponse(template.render({'project_id': scheme, 'scheme_data': scheme_data, 'scheme_detail': scheme_detail}, request))

def getSchemeNames(request):
    sector_id = request.GET.get('sector_id')
    rb_create = request.GET.get('rbc')
    rbc = 'f'
    if rb_create == True:
        rbc = 't'
    sector_id = "'%s'" % sector_id
    query = "SELECT DISTINCT s_name,  gs_no from adp_draft_201718_vw where sec_id = " + sector_id + "  Order BY s_name"
    data = getQueryResultAsJson(query)
    return HttpResponse(data)


def getSchemeDetail(request):
    scheme_id = request.GET.get('scheme_id')
    sql = "select * from adp_draft_201718_vw where gs_no = '" + scheme_id + "'"
    data = getQueryResultAsJson(sql)
    return HttpResponse(data)



def view_scheme_plan(request):
    scheme_id = request.POST.get("scheme_id")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    cost_total = request.POST.get("cost_total")
    adp_schemes = apps.get_model(app_label='pc1', model_name='AdpDraft201718Vw')
    obj = adp_schemes.objects.filter(gs_no=scheme_id)
    if obj.count() > 0:
        obj.update(start_date=start_date, end_date=end_date, cost_total=cost_total)
        data = {'message': 200, 'scheme_id': scheme_id}
        data = json.dumps(data, default=date_handler)
    else:
        data = {'message': 404, 'scheme_id': scheme_id}
        data = json.dumps(data, default=date_handler)
    return HttpResponse(data)


def modal_image(request):
    image = get_modal_image(request)
    return HttpResponse(image)
