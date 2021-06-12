import base64
import json
from functools import partial
from itertools import chain
from operator import is_not

import zlib
from django.apps import apps
from django.db import connections
from django.db import models
from django.utils.termcolors import background


def get_table_names():
    app_models = apps.all_models['remote_MHVRA']
    models_dict = get_tables_name_rows_count_array(app_models)
    models_json = json.dumps(models_dict, default=date_handler)
    return models_json

def get_server_table_names():
    app_models = apps.all_models['remote_MHVRA']
    models_dict = get_server_tables_name_array(app_models)
    models_json = json.dumps(models_dict, default=date_handler)
    return models_json

def get_table_data(request):
    table_name = request.GET.get('table')
    remote_model = apps.get_model(app_label='remote_MHVRA', model_name=table_name)
    local_model = apps.get_model(app_label='local_MHVRA', model_name=table_name)
    remote_table_rows = None
    if table_name == 'surveyproperty':
        remote_table_rows = list(remote_model.objects.exclude(x=5))
    remote_table_rows = list(remote_model.objects.all())
    inserted = 0
    not_insterted = 0
    for table_row in remote_table_rows:
        record_count = local_model.objects.filter(pk = table_row.pk).count()
        if record_count == 0:
            table_row_dict = model_to_dict(table_row)
            row_to_insert = local_model.objects.create(**table_row_dict);
            row_to_insert.save()
            inserted += 1
        else:
            not_insterted += 1
    return '{inserted:' + str(inserted) + ', not_inserted:' + str(not_insterted) + '}'

def get_tables_name_rows_count_array(app_models):
    models_dict = tables_list_dict(app_models)
    table_name_count = []
    for table in models_dict:
        table_name = table['name']
        remote_count = get_remote_table_records_count(table_name)
        local_count = get_local_table_records_count(table_name)
        record = {'name':table_name, 'remote_count':remote_count, 'local_count':local_count}
        table_name_count.append(record)
    return table_name_count

def get_server_tables_name_array(app_models):
    models_dict = tables_list_dict(app_models)
    table_name_count = []
    for table in models_dict:
        table_name = table['name']
        remote_count = get_remote_table_records_count(table_name)
        record = {'name':table_name, 'remote_count':remote_count}
        table_name_count.append(record)
    return table_name_count

def get_remote_table_records_count(table):
    remote_model = apps.get_model(app_label='remote_MHVRA', model_name=table)
    records_count = remote_model.objects.all().count()
    return records_count

def get_local_table_records_count(table):
    remote_model = apps.get_model(app_label='local_MHVRA', model_name=table)
    records_count = remote_model.objects.all().count()
    return records_count


def get_survey_table_data_bydate(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    remote_model = apps.get_model(app_label='remote_MHVRA', model_name='surveyproperty')
    local_model = apps.get_model(app_label='local_MHVRA', model_name='surveyproperty')
    # remote_table_rows = None
    remote_table_rows = list(remote_model.objects.filter(upload_datetime__gte=from_date, upload_datetime__lt = to_date ))
    inserted = 0
    not_insterted = 0
    for table_row in remote_table_rows:
        record_count = local_model.objects.filter(pk=table_row.pk).count()
        if record_count == 0:
            table_row_dict = model_to_dict(table_row)
            row_to_insert = local_model.objects.create(**table_row_dict)
            row_to_insert.save()
            inserted += 1
        else:
            not_insterted += 1
    return '{inserted:' + str(inserted) + ', not_inserted:' + str(not_insterted) + '}'

def get_survey_data_tofrom_date(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    remote_model = apps.get_model(app_label='remote_MHVRA', model_name='survey')
    remote_table_rows = list(remote_model.objects.filter(upload_datetime__gte=from_date, upload_datetime__lt=to_date).order_by('survey_id'))
    data_array = get_model_dict_array(remote_table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    return json_data

def import_survey_property_date_in_local_db(request):
    survey_id = request.GET.get('survey_id')
    survey_type_id = request.GET.get('survey_type_id')
    remote_model = apps.get_model(app_label='remote_MHVRA', model_name='SurveyProperty')
    remote_table_rows = list(remote_model.objects.filter(survey_id = survey_id).order_by('property_id'))
    if survey_type_id == '1':
        result = insert_residential_survey_data_in_local_db(remote_table_rows, survey_id)
        return result
    if survey_type_id == '5':
        result = insert_commercial_survey_data_in_local_db(remote_table_rows, survey_id)
        return result

###   http://localhost:9898/survey_stats/parse_survey_property?survey_id=263&survey_type_id=1
###   Residential Survey Type Functions start here

residential_attributes_jsonb = ['age_group', 'education_group', 'disability_group', 'living_facilities', 'livestock']
residential_attributes_multi_strings = ['source_of_income', 'govt_compensation', 'relief_from_ngo_ingo', 'transport', 'relief_you_seek',
                                        'last_epidemic_diseases']
residential_attributes_multi_strings_count = ['source_of_income_count', 'govt_compensation_count', 'relief_from_ngo_ingo_count',
                                              'transport_count', 'relief_you_seek_count', 'last_epidemic_diseases_count']
residential_attributes_single_strings = ['respondent_gender', 'family_type', 'respondent_relation', 'religion', 'monthly_income', 'hoh_gender',
                                         'connected_infrastructure', 'rescue', 'disaster_management', 'is_property_restored', 'swimmers',
                                         'medical_accessibility', 'mode_of_information', 'media_awareness_help', 'source_of_water_supply',
                                         'experienced_last_natural_disaster', 'sewerage', 'type_of_crops']

def insert_residential_survey_data_in_local_db_old(remote_table_rows, survey_id):
    residential_model = apps.get_model(app_label='local_MHVRA', model_name='Residential')
    residential_columns_dict = get_residential_record_dict()
    age_group = 0
    education_group = 0
    disability_group = 0
    relief_you_seek = 0
    living_facilities = 0
    last_epidemic_diseases = 0
    type_of_crops = 0
    livestock = 0;
    for table_row in remote_table_rows:
        table_row_dict = model_to_dict(table_row)
        gender = table_row_dict['gender']
        property_id = table_row_dict['property_id']
        string_value = table_row_dict['string_value']
        integer_value = table_row_dict['integer_value']
        column_name = get_residential_column_from_id(str(property_id))
        if column_name:
            residential_columns_dict[column_name] = get_int_string_value(integer_value, string_value)
        print(get_int_string_value(integer_value, string_value))
        if column_name == 'age_group':
            age_group += 1
        elif column_name == 'education_group':
            education_group += 1
        elif column_name == 'disability_group':
            disability_group += 1
        elif column_name == 'relief_you_seek':
            relief_you_seek += 1
        elif column_name == 'living_facilities':
            living_facilities += 1
        elif column_name == 'last_epidemic_diseases':
            last_epidemic_diseases += 1
        elif column_name == 'type_of_crops':
            type_of_crops += 1
        elif column_name == 'livestock':
            livestock += 1
    residential_columns_dict['survey_id'] = str(survey_id)
    residential_columns_dict['age_group'] = str(age_group)
    residential_columns_dict['education_group'] = str(education_group)
    residential_columns_dict['disability_group'] = str(disability_group)
    residential_columns_dict['relief_you_seek'] = str(relief_you_seek)
    residential_columns_dict['living_facilities'] = str(living_facilities)
    residential_columns_dict['last_epidemic_diseases'] = str(last_epidemic_diseases)
    residential_columns_dict['type_of_crops'] = str(type_of_crops)
    residential_columns_dict['livestock'] = str(livestock)
    print(residential_columns_dict)
    try:
        row_to_insert = residential_model.objects.create(**residential_columns_dict)
        row_to_insert.save()
        return 'Row saved.'
    except Exception as e:
        return 'Row not saved: '

def insert_residential_survey_data_in_local_db(remote_table_rows, survey_id):
    residential_model = apps.get_model(app_label='local_MHVRA', model_name='Residential')
    residential_columns_dict = get_residential_record_dict()
    for table_row in remote_table_rows:
        table_row_dict = model_to_dict(table_row)
        property_id = table_row_dict['property_id']
        string_value = table_row_dict['string_value']
        column_name = get_residential_column_from_id(str(property_id))
        if (column_name in residential_attributes_jsonb) or (column_name in residential_attributes_multi_strings) or (column_name in residential_attributes_single_strings):
            print(column_name)
        else:
            residential_columns_dict[column_name] = parse_null_value(string_value)
    residential_columns_jsonb_dict = set_residential_jsonb_attribs(residential_columns_dict, remote_table_rows)
    residential_columns_jsonb_multi_dict = set_residential_multistring_attribs(residential_columns_jsonb_dict, remote_table_rows)
    residential_columns_jsonb_multi_single_dict = set_residential_single_attribs(residential_columns_jsonb_multi_dict, remote_table_rows)
    residential_final_dict = set_residential_attribs_count(residential_columns_jsonb_multi_single_dict, remote_table_rows)
    residential_final_dict['survey_id'] = str(survey_id)
    try:
        del residential_final_dict[None]
    except Exception as e:
        print(e)
    try:
        row_to_insert = residential_model.objects.create(**residential_final_dict)
        row_to_insert.save()
        return 'Row saved.'
    except Exception as e:
        return e

def set_residential_jsonb_attribs(residential_record_dict, survey_data_resultset):
    for item in residential_attributes_jsonb:
        item_jsonb_array = []
        column_name = ''
        for row_data in survey_data_resultset:
            item_jsonb_record = {"Name":'', "Value":0, "Gender":''}
            table_row_dict = model_to_dict(row_data)
            property_id = table_row_dict['property_id']
            column_name = get_residential_column_from_id(str(property_id))
            if column_name == item:
                gender = table_row_dict['gender']
                integer_value = table_row_dict['integer_value']
                string_value = table_row_dict['string_value']
                if integer_value == 0:
                    print(parse_null_value(integer_value))
                else:
                    item_jsonb_record["Name"] = parse_null_value(string_value)
                    item_jsonb_record["Value"] = parse_null_value(integer_value)
                    item_jsonb_record["Gender"] = parse_null_value(gender)
                    item_jsonb_array.append(item_jsonb_record)
        residential_record_dict[item] = item_jsonb_array
    return residential_record_dict

def set_residential_multistring_attribs(residential_record_dict, survey_data_resultset):
    for item in residential_attributes_multi_strings:
        multi_string_item = []
        column_name = ''
        for row_data in survey_data_resultset:
            table_row_dict = model_to_dict(row_data)
            property_id = table_row_dict['property_id']
            column_name = get_residential_column_from_id(str(property_id))
            if column_name == item:
                integer_value = table_row_dict['integer_value']
                string_value = table_row_dict['string_value']
                if integer_value == 0:
                    print(integer_value)
                else:
                    multi_string_item.append(parse_null_value(string_value))
        residential_record_dict[item] = multi_string_item
    return residential_record_dict

def set_residential_single_attribs(residential_record_dict, survey_data_resultset):
    for item in residential_attributes_single_strings:
        single_string_item = ''
        column_name = ''
        for row_data in survey_data_resultset:
            table_row_dict = model_to_dict(row_data)
            property_id = table_row_dict['property_id']
            column_name = get_residential_column_from_id(str(property_id))
            if column_name == item:
                integer_value = table_row_dict['integer_value']
                string_value = table_row_dict['string_value']
                if integer_value == 0:
                    print(integer_value)
                else:
                    single_string_item = (parse_null_value(string_value))
        residential_record_dict[item] = single_string_item
    return residential_record_dict

def set_residential_attribs_count(residential_record_dict, survey_data_resultset):
    for item in residential_attributes_multi_strings:
        items_count = 0
        column_name = ''
        for row_data in survey_data_resultset:
            table_row_dict = model_to_dict(row_data)
            property_id = table_row_dict['property_id']
            column_name = get_residential_column_from_id(str(property_id))
            if column_name == item:
                items_count += 1
        residential_record_dict[(item+'_count')] = items_count
    return residential_record_dict

def get_residential_record_dict():
    residential_columns_dict = {
        'survey_id':'','age_group': '','respondent_name':'','respondent_gender':'','respondant_cnic':'','respondent_cinic_availability_date':'',
        'respondant_contact':'','respondent_education':'','family_type': '','respondent_relation':'','family_cast':'',
        'religion':'','monthly_income':'','bank_account_number':'','source_of_income':'','hoh_name': '',
        'hoh_gender':'','hoh_contact':'','hoh_cnic':'','hoh_cinic_availability_date':'','current_address':'','permanent_address':'',
        'education_group': '','disability_group':'','avg_electricity_bill_rs':'','no_of_stories':'','no_of_pakka_rooms':'',
        'no_of_kacha_rooms':'','plinth_level_ft':'','building_age_yr': '','building_area_marla':'','construction_type':'',
        'govt_compensation':'','relief_from_ngo_ingo':'','living_facilities':'','transport':'',
        'connected_infrastructure': '','livestock':'','damage_in_last_disaster':'','source_of_foreign_remittance':'','first_aid':'',
        'civil_defence':'','rescue':'','disaster_management': '','is_property_restored':'','other_training':'','swimmers':'',
        'relief_you_seek':'','medical_accessibility':'','year_of_disaster':'','mode_of_information': '','last_epidemic_diseases':'',
        'media_awareness_help':'','source_of_water_supply':'','experienced_last_natural_disaster':'','time_to_restore_months':'',
        'drinkable_water_depth_ft':'','drinkable_water_distance_ft': '','sewerage':'','type_of_crops':'','no_of_crops':'',
        'total_gricultural_land':'','agricultural_land_unit':'','owner_total_cultivated_land':'','owner_total_cultivated_land_unit': '',
        'tenant_total_cultivated_land':'','tenant_cultivated_land_unit':'','any_uncultivated_land':'','area_of_uncultivated_land':'',
        'uncultivated_land_unit':'','reason_of_uncultivated_land':'','application_version': '','form_number':'','source_of_income_count':''
        , 'govt_compensation_count': '','relief_from_ngo_ingo_count':'','transport_count':'','relief_you_seek_count':'','last_epidemic_diseases_count':''
    }
    return residential_columns_dict

def get_int_string_value(int_value, str_value):
    integer_value = str(int_value)
    if (int_value == None) and (str_value == None):
        return ''
    elif (int_value == None) and (str_value != None) :
        return str_value
    elif (int_value != None) and (str_value == None):
        return integer_value
    else:
        return integer_value + ',' + str_value

def get_residential_column_from_value(column_name):
    if column_name == 'Age Group':
        return 'age_group'
    elif column_name == 'Respondent Name':
        return 'respondent_name'
    elif column_name == 'Respondent Gender':
        return 'respondent_gender'
    elif column_name == 'Respondent CNIC':
        return 'respondant_cnic'
    elif column_name == 'Respondent CNIC Availability Date':
        return 'respondent_cinic_availability_date'
    elif column_name == 'Respondent Phone no':
        return 'respondant_contact'
    elif column_name == 'Respondent Education':
        return 'respondent_education'
    elif column_name == 'Type of Family':
        return 'family_type'
    elif column_name == 'Respondent Relation':
        return 'respondent_relation'
    elif column_name == 'Family Cast':
        return 'family_cast'
    elif column_name == 'Religion':
        return 'religion'
    elif column_name == 'Monthly Income':
        return 'monthly_income'
    elif column_name == 'Bank Account Number':
        return 'bank_account_number'
    elif column_name == 'Source of Income':
        return 'source_of_income'
    elif column_name == 'HOH Name':
        return 'hoh_name'
    elif column_name == 'HOH Gender':
        return 'hoh_gender'
    elif column_name == 'HOH Phone no':
        return 'hoh_contact'
    elif column_name == 'HOH CNIC':
        return 'hoh_cnic'
    elif column_name == 'HOH CNIC Availability Date':
        return 'hoh_cinic_availability_date'
    elif column_name == 'Current Address':
        return 'current_address'
    elif column_name == 'Permanent Address':
        return 'permanent_address'
    elif column_name == 'Education Group':
        return 'education_group'
    elif column_name == 'Disability Group':
        return 'disability_group'
    elif column_name == 'Average Electricity Bill (Rupees)':
        return 'avg_electricity_bill_rs'
    elif column_name == 'No of Stories':
        return 'no_of_stories'
    elif column_name == 'No of Pakka Rooms':
        return 'no_of_pakka_rooms'
    elif column_name == '':
        return 'no_of_kacha_rooms'
    elif column_name == 'No of Kacha Rooms':
        return 'plinth_level_ft'
    elif column_name == 'Age of Building (Years)':
        return 'building_age_yr'
    elif column_name == 'Area of the Building (Marla)':
        return 'building_area_marla'
    elif column_name == 'Type Of Construction':
        return 'construction_type'
    elif column_name == 'Compensation From Govt':
        return 'govt_compensation'
    elif column_name == 'Relief From NGO/INGO':
        return 'relief_from_ngo_ingo'
    elif column_name == 'Living Facilities':
        return 'living_facilities'
    elif column_name == 'Transport':
        return 'transport'
    elif column_name == 'Connected Infrastructure':
        return 'connected_infrastructure'
    elif column_name == 'Livestock':
        return 'livestock'
    elif column_name == 'Source of Foreign Remittance':
        return 'source_of_foreign_remittance'
    elif column_name == 'First Aid':
        return 'first_aid'
    elif column_name == 'Civil Defence':
        return 'civil_defence'
    elif column_name == 'Rescue':
        return 'rescue'
    elif column_name == 'Disaster Management':
        return 'disaster_management'
    elif column_name == 'Is Property Restored':
        return 'is_property_restored'
    elif column_name == 'Other Training':
        return 'other_training'
    elif column_name == 'Swimmers':
        return 'swimmers'
    elif column_name == 'Relief You Seek':
        return 'relief_you_seek'
    elif column_name == 'Medical Accessibility':
        return 'medical_accessibility'
    elif column_name == 'Year of Disaster':
        return 'year_of_disaster'
    elif column_name == 'Mode of Information':
        return 'mode_of_information'
    elif column_name == 'Last Epidemic Diseases':
        return 'last_epidemic_diseases'
    elif column_name == 'How Much Media Awareness Was Helpfull':
        return 'media_awareness_help'
    elif column_name == 'Source of Water Supply':
        return 'source_of_water_supply'
    elif column_name == 'Experienced Last Natural Disaster':
        return 'experienced_last_natural_disaster'
    elif column_name == 'Time Taken To Restore (Months)':
        return 'time_to_restore_months'
    elif column_name == 'Depth Of Drinkable Water (Feet)':
        return 'drinkable_water_depth_ft'
    elif column_name == 'Distance To Drinkable Water (Meters)':
        return 'drinkable_water_distance_ft'
    elif column_name == 'Sewerage System':
        return 'sewerage'
    elif column_name == 'Type of Crops':
        return 'type_of_crops'
    elif column_name == 'No of Crops':
        return 'no_of_crops'
    elif column_name == 'Total Agricultural Land':
        return 'total_gricultural_land'
    elif column_name == 'Total Agricultural Land Unit':
        return 'agricultural_land_unit'
    elif column_name == 'Total Cultivated Land As Owner':
        return 'owner_total_cultivated_land'
    elif column_name == 'Total Cultivated Land As Owner Unit':
        return 'owner_total_cultivated_land_unit'
    elif column_name == 'Total Cultivated Land As Tenant':
        return 'tenant_total_cultivated_land'
    elif column_name == 'Total Cultivated Land As Tenant Unit':
        return 'tenant_cultivated_land_unit'
    elif column_name == 'Any Uncultivated Land':
        return 'any_uncultivated_land'
    elif column_name == 'Area of Uncultivated Land':
        return 'area_of_uncultivated_land'
    elif column_name == 'Area of Uncultivated Land Unit':
        return 'uncultivated_land_unit'
    elif column_name == 'Reason of Uncultivated Land':
        return 'reason_of_uncultivated_land'
    elif column_name == 'Application Version':
        return 'application_version'
    elif column_name == 'Form Number':
        return 'form_number'

def get_residential_column_from_id(column_name):
    if column_name == '1':
        return 'age_group'
    elif column_name == '581':
        return 'respondent_name'
    elif column_name == '427':
        return 'respondent_gender'
    elif column_name == '582':
        return 'respondant_cnic'
    elif column_name == '583':
        return 'respondent_cinic_availability_date'
    elif column_name == '585':
        return 'respondant_contact'
    elif column_name == '586':
        return 'respondent_education'
    elif column_name == '392':
        return 'family_type'
    elif column_name == '430':
        return 'respondent_relation'
    elif column_name == '454':
        return 'family_cast'
    elif column_name == '532':
        return 'religion'
    elif column_name == '394':
        return 'monthly_income'
    elif column_name == '411':
        return 'bank_account_number'
    elif column_name == '280':
        return 'source_of_income'
    elif column_name == '577':
        return 'hoh_name'
    elif column_name == '713':
        return 'hoh_gender'
    elif column_name == '578':
        return 'hoh_contact'
    elif column_name == '579':
        return 'hoh_cnic'
    elif column_name == '580':
        return 'hoh_cinic_availability_date'
    elif column_name == '587':
        return 'current_address'
    elif column_name == '588':
        return 'permanent_address'
    elif column_name == '9':
        return 'education_group'
    elif column_name == '19':
        return 'disability_group'
    elif column_name == '367':
        return 'avg_electricity_bill_rs'
    elif column_name == '617':
        return 'no_of_stories'
    elif column_name == '739':
        return 'no_of_pakka_rooms'
    elif column_name == '740':
        return 'no_of_kacha_rooms'
    elif column_name == '591':
        return 'plinth_level_ft'
    elif column_name == '592':
        return 'building_age_yr'
    elif column_name == '593':
        return 'building_area_marla'
    elif column_name == '605':
        return 'construction_type'
    elif column_name == '569':
        return 'govt_compensation'
    elif column_name == '576':
        return 'relief_from_ngo_ingo'
    elif column_name == '561':
        return 'living_facilities'
    elif column_name == '554':
        return 'transport'
    elif column_name == '538':
        return 'connected_infrastructure'
    elif column_name == '400':
        return 'livestock'
    elif column_name == '259':
        return 'source_of_foreign_remittance'
    elif column_name == '594':
        return 'first_aid'
    elif column_name == '595':
        return 'civil_defence'
    elif column_name == '709':
        return 'rescue'
    elif column_name == '710':
        return 'disaster_management'
    elif column_name == '712':
        return 'is_property_restored'
    elif column_name == '598':
        return 'other_training'
    elif column_name == '31':
        return 'swimmers'
    elif column_name == '267':
        return 'relief_you_seek'
    elif column_name == '276':
        return 'medical_accessibility'
    elif column_name == '299':
        return 'year_of_disaster'
    elif column_name == '300':
        return 'mode_of_information'
    elif column_name == '317':
        return 'last_epidemic_diseases'
    elif column_name == '318':
        return 'media_awareness_help'
    elif column_name == '320':
        return 'source_of_water_supply'
    elif column_name == '327':
        return 'experienced_last_natural_disaster'
    elif column_name == '366':
        return 'time_to_restore_months'
    elif column_name == '370':
        return 'drinkable_water_depth_ft'
    elif column_name == '371':
        return 'drinkable_water_distance_ft'
    elif column_name == '372':
        return 'sewerage'
    elif column_name == '260':
        return 'type_of_crops'
    elif column_name == '377':
        return 'no_of_crops'
    elif column_name == '378':
        return 'total_gricultural_land'
    elif column_name == '412':
        return 'agricultural_land_unit'
    elif column_name == '425':
        return 'owner_total_cultivated_land'
    elif column_name == '420':
        return 'owner_total_cultivated_land_unit'
    elif column_name == '426':
        return 'tenant_total_cultivated_land'
    elif column_name == '416':
        return 'tenant_cultivated_land_unit'
    elif column_name == '720':
        return 'any_uncultivated_land'
    elif column_name == '721':
        return 'area_of_uncultivated_land'
    elif column_name == '722':
        return 'uncultivated_land_unit'
    elif column_name == '723':
        return 'reason_of_uncultivated_land'
    elif column_name == '714':
        return 'application_version'
    elif column_name == '715':
        return 'form_number'

###   Commercial Survey Type Functions Start Here

def insert_commercial_survey_data_in_local_db(remote_table_rows, survey_id):
    commercial_model = apps.get_model(app_label='local_MHVRA', model_name='Commercial')
    commercial_columns_dict = get_commercial_record_dict()
    for table_row in remote_table_rows:
        table_row_dict = model_to_dict(table_row)
        property_id = table_row_dict['property_id']
        string_value = table_row_dict['string_value']
        column_name = get_commercial_column_from_id(str(property_id))
        commercial_columns_dict[column_name] = parse_null_value(string_value)
        commercial_columns_dict['survey_id'] = str(survey_id)
    try:
        del commercial_columns_dict[None]
    except Exception as e:
        print(e)
    try:
        row_to_insert = commercial_model.objects.create(**commercial_columns_dict)
        row_to_insert.save()
        return 'Row saved.'
    except Exception as e:
        return e

def get_commercial_record_dict():
    commercial_columns_dict = {
        'respondent_name':'','respondant_cnic': '','respondent_phone_no':'','age_of_building':'','plinth_level_of_building':'',
        'security_guard':'','emergency_exit':'','evacuation_plan':'','does_this_building_submerge_during_flood': '',
        'type_of_business':'','name_of_business':'', 'number_of_employees':'','application_version':'','form_number':'','survey_id':''
    }
    return commercial_columns_dict

def get_commercial_column_from_id(column_name):
    if column_name == '581':
        return 'respondent_name'
    elif column_name == '427':
        return 'respondent_gender'
    elif column_name == '582':
        return 'respondant_cnic'
    elif column_name == '583':
        return 'respondent_cinic_availability_date'
    elif column_name == '585':
        return 'respondent_phone_no'
    elif column_name == '586':
        return 'respondent_education'
    elif column_name == '603':
        return 'age_of_building'
    elif column_name == '604':
        return 'plinth_level_of_building'
    elif column_name == '606':
        return 'security_guard'
    elif column_name == '607':
        return 'emergency_exit'
    elif column_name == '608':
        return 'evacuation_plan'
    elif column_name == '609':
        return 'does_this_building_submerge_during_flood'
    elif column_name == '639':
        return 'type_of_business'
    elif column_name == '640':
        return 'name_of_business'
    elif column_name == '641':
        return 'number_of_employees'
    elif column_name == '714':
        return 'application_version'
    elif column_name == '715':
        return 'form_number'

def get_survey_type_location_ids_tofromtime(request):
    type_id = int(request.GET.get('type_id'))
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    remote_model = apps.get_model(app_label='remote_MHVRA', model_name='survey')
    remote_table_rows = list(remote_model.objects.filter(upload_datetime__gt=from_date, upload_datetime__lte=to_date, survey_type_id = type_id).order_by('survey_id'))
    remote_table_rows_dict = get_model_dict_array(remote_table_rows)
    remote_table_json = json.dumps(remote_table_rows_dict, default=date_handler)
    return remote_table_json

def get_table_geojson_query(table_name, properties):
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom, 3857), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
                properties + ') As l )) As properties ' + \
               'FROM ' + table_name + ' As lg) As f ) As fc;'
    return strQuery

def get_table_geojson_query_whereclause(table_name, properties, where_clause):
    strQuery = 'SELECT row_to_json(fc) as geojson FROM ( SELECT \'FeatureCollection\' As type, ' + \
               'array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type , ' + \
               'ST_AsGeoJSON(st_transform(lg.geom, 3857), 4)::json As geometry , row_to_json((SELECT l FROM (SELECT ' + \
                properties + ') As l )) As properties ' + \
               'FROM ' + table_name + ' As lg where ' + where_clause + ' ) As f ) As fc;'
    return strQuery

def get_district_geojson():
    districtGeoJsonQuery = get_table_geojson_query('district', 'district_id, district_name')
    districtGeoJson = getQueryResultAsJson(districtGeoJsonQuery)
    jsonData = json.dumps(districtGeoJson, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(jsonData), 9))
    return compressed

#  Residential Json Data
def get_survey_type_json_data():
    strResQuery = 'select * from residential_survey_property_vw order by upload_datetime;'
    resData = getQueryResultAsJson(strResQuery)
    locationGeoJsonQuery = get_table_geojson_query('survey_location_mv', 'survey_id, survey_type_id, mauza_id')
    locationGeoJson = getQueryResultAsJson(locationGeoJsonQuery)
    jsonData = json.dumps({'resData':resData, 'comData':'', 'pbData':'', 'eduData':'', 'hfData':'', 'rbData':'',
                           'infData':'', 'terData':'', 'mgsData':'', 'grvData':'', 'grvData':'', 'grvData':'',
                           'prkData':'', 'brgData':'', 'indData':'', 'cbData':'', 'djData':'', 'geoJson':locationGeoJson}, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(jsonData), 9))
    return compressed

def parse_null_value(value):
    if value == None:
        return ''
    else:
        return str(value)

def model_to_dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
        # Evaluate ManyToManyField QuerySets to prevent subsequent model
        # alteration of that field from being reflected in the data.
        if isinstance(f, models.ManyToManyField):
            data[f.name] = list(data[f.name])
    return data

def tables_list_dict(tables_dict):
    data = []
    for table in tables_dict:
        name_tuple = {'name':table}
        data.append(name_tuple)
    return data

def get_tables_list():
    strQuery = 'SELECT table_schema,table_name FROM information_schema.tables ' \
               'where table_schema = \'public\' ORDER BY table_schema,table_name;'
    json_data = get_local_query_resultset_asarray(strQuery)
    return json_data

def get_local_query_resultset_asarray(strQuery):
    connection = connections['dmapp_local']
    cursor = connection.cursor()
    cursor.execute(strQuery)
    data = dictfetchall(cursor)
    return data

def get_remote_query_resultset_asarray(strQuery):
    connection = connections['dmapp']
    cursor = connection.cursor()
    cursor.execute(strQuery)
    data = dictfetchall(cursor)
    return data

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
    connection = connections['dmapp_local']
    cursor = connection.cursor()
    cursor.execute(strQuery)
    data = dictfetchall(cursor)
    if as_string == True:
        json_data = json.dumps(data, default=date_handler)
    else:
        json_data = data
    return json_data
