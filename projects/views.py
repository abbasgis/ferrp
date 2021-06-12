import json
import os

from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from ferrp.models import Activity_Log
from ferrp.projects.models import Directory, DirectoryTemplate, Projects, Files
from ferrp.settings import DOCUMENT_PATH, DOCUMENT_URL
from ferrp.utils import Log_Error, Common_Utils

from ferrp.models import Items_Permission
from django.template.defaultfilters import register
from django.conf import settings

from ferrp.documents.models import Doc_Info


@register.filter(name='chk_admin')
def chk_admin(url, admin_name):
    arrURL = url.split('/')
    if arrURL[1] == "admin":
        return True
    else:
        return False


def get_view_project_page(request, template=loader.get_template('view_projects.html')):
    project_id = request.GET.get('project_id')
    data = list(Projects.objects.all().values('project_id', 'project_name'))
    projects_data = json.dumps(data, default=date_handler)
    return HttpResponse(template.render({'project_id': project_id, 'projects': projects_data}, request))


def perform_action_on_file(request):
    file_name = request.GET.get('file_name', '1')
    action = request.GET.get('action', '1')
    file = Files.objects.filter(file_name=file_name).get()
    file_type = file.file_type.model
    url = ''
    if file_type == 'doc_info' and action == 'v' or action == 'e':
        url = reverse("view_document") + "?doc_name=" + file_name
    elif file_type == 'doc_info' and action == 'd':
        url = reverse("download_document") + "?doc_name=" + file_name
    if file_type == 'info' and action == 'v' or action == 'e':
        url = reverse("view_layer") + "?layer_name=" + file_name
    elif file_type == 'info' and action == 'd':
        url = reverse("lyr_download") + "?layer_name=" + file_name
    return HttpResponseRedirect(url)


def get_directories_data(request):
    project_id = request.GET.get('project_id', '1')
    if project_id == '1' or  project_id == 'None':
        d = [] #list(Directory.objects.all().values())
    else:
        d = list(Directory.objects.filter(project_id=project_id).values())
    json_data = json.dumps(d, default=date_handler)
    return HttpResponse(json_data)


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def project_browser(request):
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


def create_directory(directory):
    # destination_directory = '/uploaded/'
    destination_directory = directory
    # SITE_ROOT = os.path.dirname(sys.modules['__main__'].__file__)
    SITE_ROOT = settings.BASE_DIR
    destination_path = SITE_ROOT + destination_directory
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    return destination_directory


def add_project_in_db_from_admin(instance, request):
    user = request.user.id
    max_project_id = Projects.objects.all().aggregate(Max('id'))
    max_project_id = max_project_id['id__max']
    if max_project_id is None:
        max_project_id = 0
    project_id = 'DCH_' + str(max_project_id + 1)
    instance.project_id = project_id
    d = create_directory('/uploaded/' + project_id.lower())
    activity = Directory(project_id=instance.project_id, dir_name=instance.project_name, dir_level=0, dir_path=d,
                         parent_dir_id=None, created_by=user)
    act = activity.save(force_insert=True)
    add_templates_directories(instance.project_id, activity.dir_id, d, user)
    return True


def add_templates_directories(project_id, dir_id, dir_path, user):
    temp = list(DirectoryTemplate.objects.filter(dir_level=0).values())
    for t in temp:
        add_child_directory(t, project_id, dir_id, dir_path, user)


def add_child_directory(t, project_id, dir_id, dir_path, user):
    d_name = t.get('dir_name')
    d_name = d_name.replace(' ', '_')
    d_name = d_name.lower()
    d = create_directory(dir_path + '/' + d_name)
    activity = Directory(project_id=project_id, dir_name=t.get('dir_name'), dir_level=t.get('dir_level') + 1,
                         dir_path=d, parent_dir_id=Directory.objects.filter(dir_id=dir_id).get(), created_by=user)
    activity.save(force_insert=True)
    childs = DirectoryTemplate.objects.filter(parent_dir_id=t.get('dir_id'))
    if childs.count() > 0:
        childs = list(childs.values())
        for c in childs:
            add_child_directory(c, project_id, activity.dir_id, activity.dir_path, user)


def insert_project_info(project_id, dir_id, file_title, file_name, file_path, user, file_info_obj):
    file_size = os.path.getsize(file_path)
    file_type = os.path.splitext(file_path)[1][1:].strip()
    dir_parent = Directory.objects.filter(dir_id=dir_id).get()
    directory = Directory(project_id=project_id, dir_name=file_title, dir_level=dir_parent.dir_level + 1,
                          dir_path=file_path, file_size=file_size, file_type=file_type,
                          file_name=file_name,
                          parent_dir_id=dir_parent, created_by=user.id)
    directory.save(force_insert=True)
    proj_obj = Projects.objects.filter(project_id=project_id).get()
    dir_obj = Directory.objects.filter(dir_id=dir_id).get()
    Files().insert_row(file_info_obj, file_name, proj_obj, dir_obj)
