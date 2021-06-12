import json
import os

import shutil
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ferrp.decorators import permission_required
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from ferrp.models import Activity_Log
from ferrp.projects.models import Directory, Files, Projects
from ferrp.projects.views import insert_project_info
from ferrp.settings import DOCUMENT_PATH, DOCUMENT_URL
from ferrp.utils import Log_Error, Common_Utils
from .forms import *
from .models import *


def document_browser(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "Browse maps", "Browse maps",
                                     request.path_info)
    response = HttpResponse()
    try:
        # document_list = []
        # doc_list = list(Info.objects.all().values('name','title','upload_date','icon','created_by'))
        can_upload = request.user.has_perm('ferrp.file_upload')
        entity_list = list(request.user.groups.values_list('name', flat=True))
        entity_list.append(request.user.username)
        entity_list.append('Public')
        doc_name_list = list(
            Items_Permission.objects.filter(entity_name__in=entity_list, permission_type__in=['V', 'P', 'O'])
                .values_list('item_name', flat=True))
        doc_list = list(
            Doc_Info.objects.filter(name__in=doc_name_list).values('name', 'title', 'upload_date', 'icon',
                                                                   'created_by'))
        # can_download = len(list(Permission.objects.filter(entity_name=request.user.username, permission_type='D'))) > 0
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'documents_dataview.html',
                  {'list': doc_list, 'count': len(doc_list), 'can_upload': can_upload})


@permission_required('D', 'doc_name', Common_Utils.get_info_item_content_type('documents', 'doc_info'))
def download_document(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "document", "download_document", "Download document",
                                     request.path_info)
    response = HttpResponse()
    try:
        doc_name = request.GET.get('doc_name')
        doc_info_list = list(Doc_Info.objects.filter(name=doc_name))
        # doc_info = model_to_dict(doc_info_list[0])
        doc_info = doc_info_list[0]
        path = doc_info.path
        # name = doc_info.name
        url = os.path.join(DOCUMENT_URL, doc_info.path, doc_info.name + "." + doc_info.file_extension)

        # file_path_name = os.path.join(doc_info.path, doc_info.name)
        # with open(file_path_name, 'rb') as pdf:
        #     response = HttpResponse(pdf.read())
        #     response['content_type'] = 'application/pdf'
        #     response['Content-Disposition'] = 'attachment;filename=file.pdf'
        #     return response
        return HttpResponseRedirect(url)
    except Exception as e:
        Log_Error.log_error_message(e, act_log)
        Common_Utils.bad_request("Failed to find file")
    act_log.update_complete_status()
    return HttpResponse("")


@permission_required('O', 'doc_name', Common_Utils.get_info_item_content_type('documents', 'doc_info'))
def delete_document(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "document", "delete_document", "Delete document",
                                     request.path_info)
    response = HttpResponse()
    try:
        doc_name = request.GET.get('doc_name')
        doc_info_list = list(Doc_Info.objects.filter(name=doc_name))
        # doc_info = model_to_dict(doc_info_list[0])
        doc_info = doc_info_list[0]
        # path = doc_info.path
        # name = doc_info.name
        # file_path_name = os.path.join(DOCUMENT_PATH, doc_info.path, doc_info.name +"." + doc_info.file_extension )
        file_path_name = os.path.join(DOCUMENT_PATH, doc_info.path)
        if os.path.exists(file_path_name):
            shutil.rmtree(file_path_name)
            # os.remove(file_path_name)
        doc_info.delete()
    except Exception as e:
        Log_Error.log_error_message(e, act_log)
        Common_Utils.bad_request("Failed to delete file")
    act_log.update_complete_status()
    return HttpResponse("202")


@permission_required('V', 'doc_name', Common_Utils.get_info_item_content_type('documents', 'doc_info'))
def view_document(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "document", "view_document", "View document",
                                     request.path_info)
    response = HttpResponse()
    try:
        doc_name = request.GET.get('doc_name')
        fields = Doc_Info._meta.get_fields()
        field_names = []
        remove_field = ['document_id', 'path', 'icon']
        # field_names = [ field.attname  for field in fields]
        for field in fields:
            if field.is_relation == False:
                if field.attname not in remove_field:
                    field_names.append(field.attname)
        # field_names.remove('document_id')
        doc_info_list = list(Doc_Info.objects.filter(name=doc_name).values(*field_names))
        # doc_info = model_to_dict(doc_info_list[0])
        doc_info = doc_info_list[0]
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return render(request, 'document_view.html', {'info': doc_info, 'doc_name': doc_info['name']})


@login_required
def upload_document(request):
    dir_id = request.GET.get('dir_id')
    project_id = request.GET.get('project_id')
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "layers", "Upload Shapefile", "Upload Shapefile",
                                     request.get_full_path())
    response = HttpResponse()
    try:
        if request.method == 'POST':
            user = request.user
            files = request.FILES.getlist('select_document')
            created_at = request.POST.get('created_at')
            dir_id = request.POST.get('dir_id', '-1')
            project_id = request.POST.get('project_id', '-1')
            file = files[0]
            file_name_token = file.name.split('.')
            file_name = file_name_token[0]
            file_Ext = file_name_token[len(file_name_token) - 1]
            file_name_timestamp = Common_Utils.add_timestamp_to_string(file_name)
            file_path = file_name_timestamp
            file_full_path = os.path.join(DOCUMENT_PATH, file_name_timestamp)
            file_title = Common_Utils.convert_file_name_2_title(file_name)

            if not os.path.exists(file_full_path):
                os.makedirs(file_full_path)
            file_path_name = os.path.join(file_full_path, file_name_timestamp + '.' + file_Ext)
            Common_Utils.handle_uploaded_file(file, file_path_name)
            doc_info = Doc_Info()
            doc_info.insert_row(name=file_name_timestamp, title=file_title, path=file_path, created_by=request.user,
                                created_at=created_at, extension=file_Ext)
            if dir_id != '' and dir_id != 'None':
                # dir_parent = Directory.objects.filter(dir_id=dir_id).get()
                # activity = Directory(project_id=project_id, dir_name=file_title, dir_level=dir_parent.dir_level + 1,
                #                      dir_path=dir_parent.dir_path + '/' + file_name_timestamp,
                #                      file_name=file_name_timestamp,
                #                      parent_dir_id=dir_parent, act_addby=user)
                # activity.save(force_insert=True)
                # proj_obj = Projects.objects.filter(project_id=project_id).get()
                # dir_obj = Directory.objects.filter(dir_id=dir_id).get()
                # Files().insert_row(doc_info, file_name_timestamp, proj_obj, dir_obj)
                insert_project_info(project_id, dir_id, file_title, file_name_timestamp, file_path_name, user, doc_info)
            # perms =

            # Permission().insert_row(info=info, document_name=file_name_timestamp, entity_name=request.user,
            #                         entity_type='U', permission_type='D')
            # try:
            #     doc_info.update_icon(file_name_timestamp, file_path_name)
            # except Exception as e:
            #     Log_Error.log_error_message(e)
            # doc_info = Doc_Info.objects.filter(name=file_name_timestamp)[0]
            # return render(request, 'documents_dataview.html',{'info': doc_info, 'doc_name': doc_info['name']})

            return HttpResponseRedirect(reverse('view_document') + "?doc_name=" + doc_info.name)
        else:
            form = Document_Upload_Form()
            return render(request, 'document_upload.html', {'form': form, 'dir_id': dir_id, 'project_id': project_id})
        messages.add_message(request, messages.INFO,
                             'Click on chose file button to select file for uploading...')  # , extra_tags='alert'
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    act_log.update_complete_status()
    return HttpResponseRedirect(reverse('document_browser'))


def add_record_in_files(dir_id, project_id, dir_name, user):
    pass


@login_required
@permission_required('O', 'item_name', Common_Utils.get_info_item_content_type('maps', 'map_info'))
def set_doc_permission(request):
    act_log = Activity_Log()
    act_log.insert_into_activity_log(request, "maps", "create_map", "Create new map",
                                     request.path_info)
    response = HttpResponse()

    doc_name = request.GET.get('item_name')
    try:
        doc_info = Doc_Info.objects.filter(name=doc_name)[0]
        Items_Permission.set_item_permission(doc_info, doc_name, request, d_or_s_permission_type='D')
    except Exception as e:
        return Log_Error.log_view_error_message(request, e, act_log)
    return HttpResponse('{"res_no":200, "res_text": "Permissions are added successfully"}')
