import json
from collections import OrderedDict

from allauth.socialaccount.providers.oauth2 import client
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import datetime
from google.auth.transport import requests
from google.oauth2 import id_token

from ferrp.meeting_management.models import *

from ferrp.utils import date_handler


def for_testing(request):
    return HttpResponse('success')


def checkIsEmailRegistered(request):
    email = request.GET.get('email')
    user = User.objects.filter(email=email)
    result = False
    if user.count() > 0:
        result = True
    return HttpResponse(result)


def authenticate_mobile_user(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    user = authenticate(username=email, password=password)
    #   user = authenticate(username='shakir', password='shakir2840')
    if user is not None:
        user_id = user.id
        token = get_token(request)
        data = {'token': token, 'result': 200, 'userid': user_id}
    else:
        data = {'result': 401, 'error': 'invalid_credentials'}

    json_data = json.dumps(data, default=date_handler)
    return HttpResponse(json_data)


def get_user_info(request):
    auth_code = request.POST.get("auth_code")
    # If this request does not have `X-Requested-With` header, this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        return False

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = '/path/to/client_secret.json'

    # Exchange auth code for access token, refresh token, and ID token


@csrf_exempt
def get_assignments_data(request):
    # auth_token = request.POST.get("token")
    # is_valid = checkGoogleToken(request, auth_token)
    # if is_valid:
    #     get_user_info(request)

    meeting_model = AllMeetingsInitiativesVw
    init_type = request.POST.get('init_type')
    if init_type == "quick_tasks":
        data = list(TblQuickTasks.objects.all().values().annotate(
            assignment=F('task_name'), due_date=F('task_date'),
            assig_to=F('assigned_to__name'), assign_date=F('task_date')).order_by('task_date'))
    else:
        if init_type == 'long':
            meeting_model = LongMeetingsInitiativesVw
        if init_type == 'short':
            meeting_model = ShortMeetingsInitiativesVw
        if init_type == 'important':
            meeting_model = ImportantMeetingsInitiativesVw
        data = list(meeting_model.objects.all().values('id', 'assignment', 'due_date').order_by('due_date'))
    json_data = json.dumps(data, default=date_handler)
    return HttpResponse(json_data)


def checkGoogleToken(request, token):
    CLIENT_ID = "60779150521-kuropp0psgvu9b8kv1gus7e32enmhdoo.apps.googleusercontent.com"
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        return idinfo
    except Exception as e:
        print(e)
        # Invalid token
        return False


@csrf_exempt
def get_assignment_detail(request):
    assignment_id = int(request.POST.get('assignment_id', -1))
    r = AllMeetingsInitiativesVw.objects.filter(id=assignment_id).get()
    new_r = OrderedDict()
    new_r['Assignment'] = r.assignment
    new_r['Meeting Agenda'] = r.meeting_agenda
    new_r['Due Date'] = r.due_date
    new_r['Assign To'] = r.assigned_to
    new_r['Assignment Date'] = r.assignment_date
    new_r['Status'] = r.status
    new_r['Sector'] = r.sector
    new_r['Sub Sector'] = r.sub_sector
    new_r['Department'] = r.department
    new_r['Nature'] = r.nature
    new_r['Referred By'] = r.referred_by
    new_r['Priority'] = r.priority
    new_r['Remarks'] = r.remarks
    new_r['Term'] = r.term
    new_r['Important'] = r.is_important
    new_r['Attachments'] = r.attachments
    new_r['Photos'] = r.pics
    json_data = json.dumps(new_r, default=date_handler)
    return HttpResponse(json_data)


@csrf_exempt
def get_remarks_history(request):
    assignment_id = int(request.POST.get('assignment_id', -1))
    remarks = MeetingsInitiativesHistroy.objects.filter(id=assignment_id).exclude(remarks='')
    remarks = list(remarks.values('id', 'remarks', 'remarks_date').order_by("-remarks_date"))
    json_data = json.dumps(remarks, default=date_handler)
    return HttpResponse(json_data)


@csrf_exempt
def get_users_list(request):
    users = list(TblUsers.objects.all().values().order_by('name'))
    json_data = json.dumps(users, default=date_handler)
    return HttpResponse(json_data)


@csrf_exempt
def sync_quick_tasks(request):
    server_current_datetime = get_current_date_time()
    # print("Time: \n" + str(server_current_datetime))
    user_id = request.POST.get("user_id")
    sync_date_tasks = request.POST.get("sync_date_tasks")
    sync_date_users = request.POST.get("sync_date_users")
    client_updates = json.loads(request.POST.get("client_updates"))
    res = sync_client_updates_with_server(client_updates, user_id)
    try:
        if sync_date_tasks:
            sync_date_tasks = convert_date_format(
                sync_date_tasks)  # datetime.datetime.strptime(sync_date_tasks, '%Y-%m-%d %H:%M:%S')
            tasks = TblQuickTasks.objects.filter(updated_at__gte=sync_date_tasks)
        else:
            tasks = TblQuickTasks.objects.all()
        tasks_server = []
        if tasks.count() > 0:
            tasks_server = list(tasks.values().annotate(id_server=F('id'),
                                                        assigned_to=F('assigned_to__id')).order_by('task_date'))
        tasks_server_deleted = []
        if sync_date_users:
            sync_date_users = convert_date_format(
                sync_date_users)  # datetime.datetime.strptime(sync_date_users, '%Y-%m-%d %H:%M:%S')
            users = TblUsers.objects.filter(updated_at__gte=sync_date_users)
        else:
            users = TblUsers.objects.all()
        users_server = []
        if users.count() > 0:
            users_server = list(users.values().order_by('name'))
        result = {'tasks_server': tasks_server, 'users_server': users_server, 'tasks_client': res,
                  'tasks_server_deleted': tasks_server_deleted}
        json_data = json.dumps(result, default=date_handler)
        return HttpResponse(json_data)
    except Exception as e:
        print(e)
        return HttpResponse("404")


def sync_client_updates_with_server(data, user_id):
    res = []
    try:
        for d in data:
            # d['updated_at'] = get_current_date_time()
            is_completed = d['is_completed']
            if is_completed == 'f' or is_completed == 'false' or is_completed == 0 or is_completed == '0':
                is_completed = False
            else:
                is_completed = True
            if d['assigned_to_id_server'] == '0':
                d['assigned_to_id_server'] = 1
            if d['id_server'] == "":
                d['id_server'] = -1
            if d['updated_by'] == 'null':
                d['updated_by'] = None
            if d['created_by'] == 'null':
                d['created_by'] = None
            assigned_to = TblUsers.objects.filter(id=d['assigned_to_id_server']).get()
            task = TblQuickTasks.objects.filter(id=d['id_server'])
            task_date = change_date_format(d['task_date'])
            # datetime.datetime.strptime(d['task_date'], "%Y-%m-%d").date()
            if task.count() == 0:
                id_client = d['id']
                quick_task = TblQuickTasks(task_name=d['task_name'], task_date=task_date, assigned_to=assigned_to,
                                           is_completed=is_completed, is_synced=True, created_by=d['created_by'],
                                           updated_by=d['updated_by'])
                quick_task.save(force_insert=True)
                r = {'id_client': id_client, 'id_server': quick_task.pk}
            else:
                task.update(task_name=d['task_name'], task_date=task_date, assigned_to=assigned_to,
                            is_completed=is_completed, is_synced=True, updated_by=d['updated_by'])
                task = task.get()
                r = {'id_client': d['id'], 'id_server': task.pk}
            res.append(r)
    except Exception as e:
        print(e)
    return res


@csrf_exempt
def save_task(request):
    try:
        id = request.POST.get("id", -1)
        if id == '':
            id = -1
        task_name = request.POST.get("task_name")
        assigned_to_id = request.POST.get("assigned_to")
        # assigned_to_id = assigned_to.split(":")[0]
        assigned_to = TblUsers.objects.filter(id=assigned_to_id).get()
        task_date = change_date_format(request.POST.get("task_date"))
        is_completed = request.POST.get("is_completed")
        if is_completed == 'true':
            is_completed = True
        else:
            is_completed = False
        task = TblQuickTasks.objects.filter(id=id)
        if task.count() > 0:
            task.update(task_name=task_name, task_date=task_date, assigned_to=assigned_to, is_completed=is_completed)
        else:
            task = TblQuickTasks(task_name=task_name, task_date=task_date, assigned_to=assigned_to,
                                 is_completed=is_completed)
            task.save(force_insert=True)
        return HttpResponse("Task Saved Successfully. . .")
    except Exception as e:
        return HttpResponse("404")


@csrf_exempt
def delete_task(request):
    id = request.POST.get("id", -1)
    task = TblQuickTasks.objects.filter(id=id)
    message = "Deleted Failed"
    if task.count() > 0:
        task.delete()
        message = "Deleted Successfully"
    return HttpResponse(message)


def change_date_format(date):
    if date.find('/') > 0:
        d = date.split("/")
        return datetime.date(int(d[2]), int(d[1]), int(d[0]))
    else:
        return date


def delete_property(prop, obj):
    if prop in obj:
        del obj[prop]


def get_current_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def convert_date_format(d):
    d = d.replace('T', ' ')
    d = d.split('.')
    return datetime.datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S')
