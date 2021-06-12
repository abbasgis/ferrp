import json
import os

from django.apps import apps
from django.conf.global_settings import MEDIA_ROOT
from django.db import connections
from django.forms import model_to_dict
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from ferrp.settings import STATIC_URL


def get_model_dict_array(rows):
    data_array = []
    for row in rows:
        row_dict = model_to_dict(row)
        data_array.append(row_dict)
    return data_array

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def getQueryResultAsJson(strQuery, as_string = True):
    connection = connections['pc1_db']
    cursor = connection.cursor()
    cursor.execute(strQuery)
    data = dictfetchall(cursor)
    if as_string == True:
        json_data = json.dumps(data, default=date_handler)
    else:
        json_data = data
    return json_data

def get_query_result_as_array(str_query):
    connection = connections['pc1_db']
    cursor = connection.cursor()
    cursor.execute(str_query)
    data = dictfetchall(cursor)
    return data

def execute_query(str_query):
    connection = connections['pc1_db']
    cursor = connection.cursor()
    try:
        cursor.execute(str_query)
        return True
    except SyntaxError:
        return False

def get_modal_image(request):
    name = request.GET.get('modal')
    new_name = name.replace('_', ' ')
    tbl_help = apps.get_model(app_label='pc1', model_name='TblHelp')
    help_table_obj = tbl_help.objects.filter(info_name=new_name).get()
    image_path = help_table_obj.help_image
    help_image = '<img id="image-gallery-image" class="img-responsive col-md-12" src="' +  STATIC_URL + image_path + '">'
    return help_image

def get_scheme_detail(request):
    gs_no = request.GET.get('scheme')
    if gs_no == None or gs_no == 'null' or gs_no == '':
        return '';
    else:
        adp_schemes = apps.get_model(app_label='pc1', model_name='AdpDraft201718Vw')
        scheme_detail = adp_schemes.objects.filter(gs_no=gs_no).get()
        model_dict = model_to_dict(scheme_detail)
        json_data = json.dumps(model_dict, default=date_handler)
        return json_data

def get_scheme_saved_data(request):
    gs_no = request.GET.get('scheme')
    if gs_no == None or gs_no == 'null' or gs_no == '':
        return ''
    else:
        tbl_schemes_history = apps.get_model(app_label='pc1', model_name='TblSchemesHistory')
        scheme_detail = tbl_schemes_history.objects.filter(gs_no=gs_no).get()
        model_dict = model_to_dict(scheme_detail)
        json_data = json.dumps(model_dict, default=date_handler)
        return json_data

def get_scheme_annexures_data(request):
    gs_no = request.GET.get('scheme')
    if gs_no == None or gs_no == 'null' or gs_no == '':
        return ''
    else:
        try:
            tbl_schemes_annexures = apps.get_model(app_label='pc1', model_name='tblschemesannexure')
            scheme_detail = tbl_schemes_annexures.objects.filter(gs_no=gs_no).get()
            model_dict = model_to_dict(scheme_detail)
            json_data = json.dumps(model_dict, default=date_handler)
            return json_data
        except Exception as e:
            return 'null'

def get_scheme_pc1_detail(request):
    gs_no = request.GET.get('scheme')
    if gs_no == None or gs_no == 'null' or gs_no == '':
        return HttpResponse("");
    else:
        tbl_schemes_history = apps.get_model(app_label='pc1', model_name='TblSchemesHistory')
        scheme_detail = tbl_schemes_history.objects.filter(gs_no=gs_no).get()
        model_dict = model_to_dict(scheme_detail)
        json_data = json.dumps(model_dict, default=date_handler)
        return HttpResponse(json_data)

@csrf_exempt
def insert_basic_info_data_in_db(request):
    basic_data = request.body
    data = json.loads(basic_data)
    try:
        gs_no = data['gs_no']
        tbl_schemes_history = apps.get_model(app_label='pc1', model_name='TblSchemesHistory')
        record = tbl_schemes_history.objects.get(gs_no=gs_no)
        record.authorities_responsible = data['authorities_responsible']
        record.plan_provision = data['plan_provision']
        record.annual_operating_cost = data['annual_operating_cost']
        record.capital_cost_estimates = data['capital_cost_estimates']
        record.physical_plan = data['physical_plan']
        record.financial_plan = data['financial_plan']
        record.financial_plan_text = data['financial_plan_text']
        record.project_objectives = data['project_objectives']
        record.demand_and_supply_analysis = data['demand_and_supply_analysis']
        record.benefits_of_the_projects_analysis = data['benefits_of_the_projects_analysis']
        record.implementation_schedule = data['implementation_schedule']
        record.additional_projects_decisions_required = data['additional_projects_decisions_required']
        record.ms_and_mp = data['ms_and_mp']
        record.certified = data['certified']
        record.save()
        return HttpResponse("{status:'Successful', message:'Data Inserted'}")
    except Exception as e:
        return HttpResponse(e)

@csrf_exempt
def insert_annexure_in_db(request):
    basic_data = request.body
    data = json.loads(basic_data)
    try:
        gs_no = data['gs_no']
        annexure_id = data['annexure_id']
        annexure_data = data['annexure_data']
        annexure_title = data['annexure_title']
        tbl_schemes_annexure = apps.get_model(app_label='pc1', model_name='TblSchemesAnnexure')
        annexure, created = tbl_schemes_annexure.objects.update_or_create(id=annexure_id, gs_no=gs_no, annexure_title=annexure_title, annexure_data=annexure_data)
        if(created == True):
            return HttpResponse("{status:'Successful', message:'Annexure Created'}")
        else:
            return HttpResponse("{status:'Successful', message:'Annexure Updated'}")
    except Exception as e:
        return HttpResponse(e)

def download_sample(request):
    type = request.GET.get('type')
    file_path = 'pc1\\static\\asstes\\doc\\'
    file_name = ''
    if type == 'authorities_responsible':
        file_name = 'Authorities Responsible.docx'
        file_path = file_path + file_name
    if type == 'plan_provision':
        file_path = file_path + 'Plan Provision.docx'
    if type == 'project_objectives':
        file_name = 'ProjectObjective.docx'
        file_path = file_path + file_name
    if type == 'demand_and_supply_analysis':
        file_name = 'demand_and_supply_analysis.docx'
        file_path = file_path + file_name
    if type == 'benefits_of_the_projects_analysis':
        file_name = 'benefits_of_the_projects_analysis.docx'
        file_path = file_path + file_name
    if type == 'financial_plan':
        file_name = 'Financial Plan.docx'
        file_path = file_path + file_name
    if type == 'financial_plan_text':
        file_name = 'financial_plan_text.docx'
        file_path = file_path + file_name
    if type == 'physical_plan':
        file_name = 'Physical Plan.docx'
        file_path = file_path + file_name
    if type == 'implementation_schedule':
        file_name = 'implementation_schedule.docx'
        file_path = file_path + file_name
    if type == 'annual_operating_cost':
        file_name = 'annual_operating_cost.docx'
        file_path = file_path + file_name
    if type == 'ms_and_mp':
        file_name = 'Management Structure & Manpower Requirement.docx'
        file_path = file_path + file_name
    if type == 'additional_projects_decisions_required':
        file_name = 'additional_projects_decisions_required.docx'
        file_path = file_path + file_name
    if type == 'certified':
        file_name = 'certified.docx'
        file_path = file_path + file_name
    complete_file_path = os.path.join(MEDIA_ROOT, file_path)
    if complete_file_path:
        with open(complete_file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename=' + file_name
            return response
    raise Http404

