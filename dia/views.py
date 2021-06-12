from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa

import json
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import datetime
from ferrp.maps.models import Map_Info
# from ferrp.mhvra.db_flood import *
from ferrp.dia.models import *
from ferrp.dia.forms import *
from ferrp.dia.functions import *
from ferrp.models import Activity_Log
from ferrp.utils import date_handler, Log_Error
from django.contrib.auth.models import *


def view_dia_project(request):
    return render(request, 'view_dia_projects.html')
    # return render(request, 'mhvra_dia.html')


# add and view section 1 and 2 forms
def view_dia_add_data(request):
    template_name = 'main_dia_add_data.html'
    long = '73.8896392'
    lat = '32.210412'
    address=get_address(lat,long)
    user = str(request.user)
    project_id = request.GET.get('project_id')
    project_name = get_project_name(project_id)
    climate_class= climate_classification(project_id)
    project_data_one = MhvraSectionOne.objects.filter(project_id=project_id).all()
    project_data_two = mhvra_section_two.objects.filter(project_id=project_id).all()
    if (len(project_data_one) > 0):
        project_data_one = list(MhvraSectionOne.objects.filter(project_id=project_id).all())
        # project_name = project_data_one[0].project_name
        form_one_data = {
            'project_name': project_name,
            'project_type': project_data_one[0].project_type,
            'project_extend': address,
            # 'project_extend': project_data_one[0].project_extend,
            'project_climate_condition': project_data_one[0].project_climate_condition,
            'rainfall_value': project_data_one[0].rainfall_value,
            'return_period': project_data_one[0].return_period,
            'project_location_features': project_data_one[0].project_location_features,
            'public_places_nearby': project_data_one[0].public_places_nearby
        }
    else:
        form_one_data = {
            'project_type': 'extension',
            'project_climate_condition': 'arid_zone',
            'project_location_features': 'flat_land',
            'project_extend': address,
        }
    if (len(project_data_two) > 0):
        project_data_two = list(mhvra_section_two.objects.filter(project_id=project_id).all())
        default_data = {
            'culture_data': project_data_two[0].culture_data,
            'recongized_hazard': project_data_two[0].recongized_hazard,
            'earthquake': project_data_two[0].earthquake,
            'landslide': project_data_two[0].landslide,
            'flood': project_data_two[0].flood,
            'glof': project_data_two[0].glof,
            'slope_failure': project_data_two[0].slope_failure,
            'heavy_rain': project_data_two[0].heavy_rain,
            'other': project_data_two[0].other,
            'landslide_data': project_data_two[0].landslide_data,
            'flood_data': project_data_two[0].flood_data,
            'forest_reserves_data': project_data_two[0].forest_reserves_data,
            'nature_reserves_data': project_data_two[0].nature_reserves_data,
            'riverine_conservation_data': project_data_two[0].riverine_conservation_data,
            'wetlands_data': project_data_two[0].wetlands_data,
            'archeological_data': project_data_two[0].archeological_data
        }

    else:
        default_data = {'culture_data': 't',
                        'recongized_hazard': '',
                        'earthquake': 'low',
                        'landslide': 'low',
                        'flood': 'low',
                        'glof': 'low',
                        'slope_failure': 'low',
                        'heavy_rain': 'low',
                        'other': 'low',
                        'landslide_data': 't',
                        'flood_data': 'yes',
                        'forest_reserves_data': 't',
                        'nature_reserves_data': 'yes',
                        'riverine_conservation_data': 'yes',
                        'wetlands_data': 'yes',
                        'archeological_data': 'yes'
                        }

    if request.method == 'POST':
        form = mhvra_section_one(request.POST)
        form_section_two = Mhvra_section_two(request.POST)

        if form.is_valid():
            # formobj = form.save()
            projectid_sectionOne = MhvraSectionOne.objects.create()
            projectid_sectionOne.project_id = project_id
            # projectid_sectionOne.project_name=form.project_name
            projectid_sectionOne.project_extend = form.project_extend
            projectid_sectionOne.project_type = form.project_type
            projectid_sectionOne.rainfall_value = form.rainfall_value
            projectid_sectionOne.return_period = form.return_period
            projectid_sectionOne.public_places_nearby = form.public_places_nearby
            projectid_sectionOne.project_location_features = form.project_location_features
            projectid_sectionOne.project_climate_condition = form.project_climate_condition
            projectid_sectionOne.save()

            tbl_project_admin = TblprojectMhvra.objects.create()
            tbl_project_admin.project_id = project_id
            tbl_project_admin.created_by = user
            tbl_project_admin.created_at = datetime.datetime.now()
            tbl_project_admin.project_name = str(form.project_name)
            tbl_project_admin.save()
            form.cleaned_data
            messages.success(request, 'Your data has been saved!', extra_tags='')
            return render(request, template_name, {'section': 1, 'form': form, 'project_id': project_id})

        elif form_section_two.is_valid():
            formobj = form_section_two.save()
            projectid_section_two = mhvra_section_two.objects.create()
            projectid_section_two.project_id = project_id
            projectid_section_two.save()
            messages.success(request, 'Your data has been saved!', extra_tags='')
            return render(request, template_name,
                          {'section': 2, 'form_section_two': form_section_two, 'project_id': project_id})

        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        section = request.GET.get('section', 1)
        form = mhvra_section_one(initial=form_one_data)
        form_section_two = Mhvra_section_two(initial=default_data)
        return render(request, 'main_dia_add_data.html',
                      {'form': form, 'form_section_two': form_section_two, 'section': section,
                       'project_id': project_id, 'project_name': project_name})


def view_mhvra_page(request):
    project_id = request.GET.get('project_id')

    return render(request, 'mhvra.html',
                  {"project_id": project_id, 'section': 1})


def get_dia_data(request):
    dia_list_arr = []
    submitted_dia_list = list(TblprojectMhvra.objects.all())
    for d_position, d_item in enumerate(submitted_dia_list):
        if (submitted_dia_list):
            dia_list_obj = {
                'project_id': d_item.project_id,
                'project_name': d_item.project_name,
                'created_by': d_item.created_by,
                'date': d_item.created_at
            }
            dia_list_arr.append(dia_list_obj)
        else:
            dia_list_obj = {
                'project_name': '',
                'created_by': '',
                'date': ''
            }
            dia_list_arr.append(dia_list_obj)
    json_dia_list = json.dumps(dia_list_arr, default=date_handler)
    return HttpResponse(json_dia_list)


def get_hazard_flood_data(request):
    print('in flood data')
    project_id = request.GET.get('project_id')
    # project_id='9356'
    # print(project_id)
    long = '73.45'
    lat = '32.21'
    # long = request.GET.get('long')
    lat = request.GET.get('lat')
    latlong = geom_to_point(project_id)
    arrFinal = []
    # pnt = GEOSGeometry('POINT(' + long + ' ' + lat + ')')
    # pnt.srid = 4326
    # pnt = pnt.transform(3857, True)
    list_hazard_flood_tblnames = [HFlood005, HFlood025, HFlood050, HFlood100, HFlood250]
    list_hazard_earthQuake_tblnames = [HEarthquake0050, HEarthquake0100, HEarthquake0250, HEarthquake0475,
                                       HEarthquake1000]
    flood_years = ['5 years', '25 years', '50 years', '100 years', '250 years']
    earthquake_years = ['50 years', '100 years', '250 years', '475 years', '1000 years']
    list_risk_flood_tblnames = [RFloodRisk005, RFloodRisk025, RFloodRisk050, RFloodRisk100, RFloodRisk250]
    list_risk_earthquake_tblnames = [REarthquakeRisk0050, REarthquakeRisk0100, REarthquakeRisk0250, REarthquakeRisk0475,
                                     REarthquakeRisk1000]
    risk_flood_years = [5, 25, 50, 100, 250]
    risk_earthquake_years = [50, 100, 250, 475, 1000]

    for h_position, h_item in enumerate(list_hazard_flood_tblnames):
        flood_hazard = list(h_item.objects.filter(geom__intersects=latlong))
        earthquake_hazard = list(list_hazard_earthQuake_tblnames[h_position].objects.filter(geom__intersects=latlong))
        flood_risk = list(list_risk_flood_tblnames[h_position].objects.filter(geom__intersects=latlong))
        earthquake_risk = (list_risk_earthquake_tblnames[h_position].objects.filter(geom__intersects=latlong))

        if (len(flood_hazard) > 0):

            h_obj = {
                'category': 'Flood',
                'design_criteria': flood_years[h_position],
                'value_mhvra': flood_hazard[0].depth_m,
                'value_unit': 'meters',
                'risk': flood_risk[0].risk_class,
                'qualitative_measure': flood_risk[0].risk_class,
                'probability': 1 / risk_flood_years[h_position]
            }
            arrFinal.append(h_obj)
        else:
            h_obj = {
                'category': '',
                'design_criteria': '',
                'value_mhvra': '',
                'value_unit': '',
                'risk': '',
                'qualitative_measure': '',
                'probability': ''
            }

        if (len(earthquake_hazard) > 0):
            h_obj = {
                'category': 'Earthquake',
                'design_criteria': earthquake_years[h_position],
                'value_mhvra': earthquake_hazard[0].pga,
                'value_unit': 'pga',
                'risk': earthquake_risk[0].risk_class,
                'qualitative_measure': earthquake_risk[0].risk_class,
                'probability': 1 / risk_earthquake_years[h_position]
            }
            arrFinal.append(h_obj)
        else:
            h_obj = {
                'category': '',
                'design_criteria': '',
                'value_mhvra': '',
                'value_unit': '',
                'risk': '',
                'qualitative_measure': '',
                'probability': ''
            }
            # messages.warning(request, 'Please select another location')
            arrFinal.append(h_obj)
            json_hf05 = json.dumps(arrFinal, default=date_handler)
            return HttpResponse(json_hf05)

    json_hf05 = json.dumps(arrFinal, default=date_handler)
    return HttpResponse(json_hf05)


def view_mitigation_design_plan(request):
    template_name = 'section_four.html'
    user = str(request.user)
    projectId = request.GET.get('project_id')
    project_name = get_project_name(projectId)
    # project_data_one = MhvraSectionOne.objects.filter(project_id=projectId).all()
    # if (len(project_data_one) > 0):
    #     project_data_one = list(MhvraSectionOne.objects.filter(project_id=projectId).all())
    project_name = project_name
    # form_one_data = {
    #     'project_name': project_data_one[0].project_name
    # }
    if request.method == 'POST':
        form_section_four = Dia_section_four(request.POST)
        form_file_field = Section_Four_Files_Field(request.POST, request.FILES)
        files = request.FILES.getlist('filedoc')
        if form_section_four.is_valid() and form_file_field.is_valid():
            form_four_obj = form_section_four.save(commit=False)
            form_four_obj.project_id = projectId
            form_four_obj.save()
            for f in files:
                file_instance = SectionFourFiles(filedoc=f, sfid=form_four_obj)
                file_instance.save()
            messages.success(request, 'Your data has been saved!', extra_tags='')
            return render(request, template_name,
                          {'form_section_four': form_section_four, 'form_file_field': form_file_field,
                           'project_id': projectId,
                           'project_name': project_name})

    else:
        form_section_four = Dia_section_four()
        form_file_field = Section_Four_Files_Field()
    return render(request, template_name,
                  {'form_section_four': form_section_four, 'form_file_field': form_file_field, 'project_id': projectId,
                   'project_name': project_name})


def view_section_five(request):
    template_name = 'section_five.html'
    project_id = request.GET.get('project_id')
    project_name = get_project_name(project_id)
    # project_data_one = MhvraSectionOne.objects.filter(project_id=project_id).all()
    # if (len(project_data_one) > 0):
    project_name = project_name
    #     form_one_data = {
    #         'project_name': project_data_one[0].project_name
    #     }
    if request.method == 'POST':
        form_section_five = Dia_section_five(request.POST)
        if form_section_five.is_valid():
            obj_five = SectionFive.objects.create()
            obj_five.comments = form_section_five.data['editor']
            obj_five.project_id = form_section_five.data['project_id']
            obj_five.save()
            messages.success(request, 'Your data has been saved!', extra_tags='')
            return render(request, template_name, {'form_section_five': form_section_five, 'project_id': project_id,
                                                   'project_name': project_name})
    else:
        form_section_five = Dia_section_five()
        return render(request, template_name, {'form_section_five': form_section_five, 'project_id': project_id,
                                               'project_name': project_name})

    return render(request, template_name, {'project_name': project_name, 'project_id': project_id})


def view_mark_location(request):
    template_name = 'mark_location.html'
    project_id = request.GET.get('project_id')
    project_name = get_project_name(project_id)
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "mhvra", "view_mhvra_page", "View MHVRA Change Page",
                                     request.path_info)
    try:
        map_name = 'map_climate_change_ferrppndsu_20181018162236832819'  # request.GET.get("item_name")
        map_info = Map_Info.objects.filter(name=map_name)
        info = {'extent': None, 'group_layers': []}
        if map_info.count() > 0:
            map_info = list(map_info.values('params'))[0]
            info["extent"] = [float(e) if float(e) else str(e) for e in map_info['params']['extent'].split(",")]
            info["group_layers"] = map_info['params']['group_layers']
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, template_name, {"info": info, "map_name": map_name, 'section': 1, 'project_id': project_id,
                                           'project_nmae': project_name})


def print_dia(request):
    # template_name = 'print_dia.html'
    # project_id = request.GET.get('project_id')
    # project_name = get_project_name(project_id)
    # project_name = project_name
    template = get_template('print_dia.html')
    sourceHtml = request.POST.get('sourceHtml')
    html = template.render({'sourceHtml': sourceHtml}, request)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        response = HttpResponse(response.getvalue(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
    else:
        return HttpResponse("Error Rendering PDF", status=400)
    # return render(request, template_name, {'project_name': project_name, 'project_id': project_id})
