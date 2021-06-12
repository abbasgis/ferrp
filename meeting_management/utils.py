import base64
import json
import zlib
import urllib.request as urllib2
import httplib2

import oauth2client
import strgen

from django.contrib.sites.models import Site
from django.db import connections
from django.db.models import Q
from django.http import HttpResponseBadRequest
from googleapiclient.discovery import build
from urllib.parse import quote
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from django.apps import apps
from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from oauth2client.client import GoogleCredentials

from ferrp.meeting_management.models import *
from ferrp.settings import SITE_ID
from ferrp.utils import DB_Query, Common_Utils, Log_Error


class GoogleCalendarHandler:
    @classmethod
    def google_calendar_access(cls, user_id):
        try:
            site_info = Site.objects.filter(pk=SITE_ID).first()
            socialapp_info = SocialApp.objects.filter(sites=site_info, provider='google').first()
            socialaccount_info = SocialAccount.objects.filter(user_id=user_id).first()
            if socialaccount_info:
                socialtoken_info = SocialToken.objects.filter(app=socialapp_info, account=socialaccount_info).first()
                if socialaccount_info:
                    access_token = socialtoken_info.token
                    client_id = socialapp_info.client_id
                    client_secret = socialapp_info.secret
                    refresh_token = socialtoken_info.token_secret
                    token_expiry = socialtoken_info.expires_at
                    token_uri = oauth2client.GOOGLE_TOKEN_URI
                    user_agent = 'my-user-agent/1.0'
                    revoke_uri = oauth2client.GOOGLE_REVOKE_URI
                    credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, token_expiry,
                                                    token_uri, user_agent, revoke_uri)
                    http = httplib2.Http()
                    http = credentials.authorize(http)
                    service = build('calendar', 'v3', http=http)
                    return service
                else:
                    return HttpResponseBadRequest()
            else:
                return HttpResponseBadRequest()
        except Exception as e:
            Log_Error.log_error_message(e)

    @classmethod
    def add_events_2_gcalendar(cls, user_id, event_param):
        try:
            service = GoogleCalendarHandler.google_calendar_access(user_id)
            if service:
                calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
                event = service.events().insert(calendarId='primary', body=event_param).execute()
                return event
            else:
                return None
        except Exception as e:
            Log_Error.log_error_message(e)
    @classmethod
    def view_events_from_gcalender(cls, user_id, user_agent):
        service = GoogleCalendarHandler.google_calendar_access(user_id, user_agent)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    @classmethod
    def change_event_2_gcalendar(cls, user_id, event_param):
        service = GoogleCalendarHandler.google_calendar_access(user_id)
        if service:
            event = service.events().get(calendarId='primary', eventId=event_param['id']).execute()
            event = event_param
            updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            return updated_event
        else:
            return None

    @classmethod
    def delete_event_2_gcalendar(cls, user_id, calendar_id):
        service = GoogleCalendarHandler.google_calendar_access(user_id)
        if service:
            event = service.events().delete(calendarId='primary', eventId=calendar_id).execute()
            return event
        else:
            return None


def get_attendees_list(participants):
    attendees_list = []
    for participant in participants:
        attendees = {
            'displayName': participant['name'],
            'email': participant['email_id'],
        }
        attendees_list.append(attendees)
    return attendees_list


def get_initiatives_list(meeting_id):
    initiatives_list = MeetingsInitiatives.objects.filter(meeting_agenda_id=meeting_id).all()
    str_initiatives = ''
    if initiatives_list:
        for initiative in initiatives_list:
            initiative_id = initiative.id
            assignment = initiative.assignment
            initiative_link = '\t<a href="http://pnddch.info/mm/?type=all&id=' + str(
                initiative_id) + '" target="_blank">' + assignment + '</a>\n'
            str_initiatives = str_initiatives + initiative_link
    return str_initiatives


def get_meeting_event_object(obj, participants):
    attendees_list = get_attendees_list(participants)
    initiatives_list = get_initiatives_list(obj.id)
    meeting_date = obj.meeting_date

    meeting_agenda = str(obj.name)
    if meeting_agenda == None:
        meeting_agenda = ""
    decisions = str(obj.decisions)
    if decisions == None:
        decisions = ""
    meeting_start_time = str(obj.meeting_start_time)
    if meeting_start_time == None:
        meeting_start_time = "00:00:00"
    meeting_end_time = str(obj.meeting_end_time)
    if meeting_end_time == None:
        meeting_end_time = "00:00:00"

    meeting_start_date = meeting_date.strftime(
        '%Y-%m-%dT' + meeting_start_time)  # 'dateTime': '2018-12-18T09:00:00-07:00',
    meeting_end_date = meeting_date.strftime(
        '%Y-%m-%dT' + meeting_end_time)  # 'dateTime': '2018-12-18T09:00:00-07:00',
    event_to_sync = {
        'etag': obj.id,
        'summary': str(obj.name),
        'location': 'Lahore Pakistan, 54000',
        'description': '<b>Agenda:</b>' + meeting_agenda + ' \n<b>Venue:</b>' + str(
            obj.venue) + ' \n<b>Decisions:</b>' + decisions
                       + '\n<b>Proceedings:</b>\n' + initiatives_list,
        'start': {
            'dateTime': meeting_start_date,
            'timeZone': 'Asia/Karachi',
        },
        'end': {
            'dateTime': meeting_end_date,
            'timeZone': 'Asia/Karachi',
        },
        'attendees': attendees_list
    }
    return event_to_sync


def add_event_to_users(event):
    sync_users_model = TblUsersToSync.objects.all()
    sync_users_list = list(sync_users_model)
    for user in sync_users_list:
        user_id = user.auth_user_id_id
        meeting_id = event['etag']
        Log_Error.log_error_message(meeting_id)
        synced_user = TblMeetingsUsersEvents.objects.filter(meeting_id=meeting_id, user_id=user_id).all()
        if not synced_user:
            synced_event = sync_event_to_calender(event, user_id)
            if synced_event:
                event_id = synced_event['id']
                meeting_user_event_obj = TblMeetingsUsersEvents.objects.create()
                meeting_user_event_obj.meeting_id = meeting_id
                meeting_user_event_obj.user_id = user_id
                meeting_user_event_obj.calendar_event_id = event_id
                meeting_user_event_obj.save()


def change_event_for_users(event):
    meeting_id = event['etag']
    sync_users_obj = TblMeetingsUsersEvents.objects.filter(meeting_id=meeting_id).all()
    sync_user_list = list(sync_users_obj)
    for user in sync_user_list:
        calendar_id = user.calendar_event_id
        user_id = user.user_id
        event['id'] = calendar_id
        change_event_to_calendar(event, user_id)


def delete_event_for_users(meeting_id):
    sync_users_obj = TblMeetingsUsersEvents.objects.filter(meeting_id=meeting_id).all()
    sync_user_list = list(sync_users_obj)
    for user in sync_user_list:
        calendar_id = user.calendar_event_id
        user_id = user.user_id
        delete_event_to_calendar(calendar_id, user_id)


def change_event_to_calendar(event, user_id):
    try:
        google_event = GoogleCalendarHandler.change_event_2_gcalendar(user_id, event)
        return google_event
    except Exception as e:
        Log_Error.log_error_message(e)


def delete_event_to_calendar(calendar_id, user_id):
    try:
        google_event = GoogleCalendarHandler.delete_event_2_gcalendar(user_id, calendar_id)
        return google_event
    except Exception as e:
        Log_Error.log_error_message(e)



def sync_event_to_calender(event, user_id):
    try:
        google_event = GoogleCalendarHandler.add_events_2_gcalendar(user_id, event)
        return google_event
    except Exception as e:
        Log_Error.log_error_message(e)


def get_event_object(obj, action):
    event_to_sync = None
    if action == 'save':
        meeting_date = obj.meeting_date
        due_date = obj.due_date
        meeting_date = meeting_date.strftime('%Y-%m-%dT%H:%M:%S+05:00')  # 'dateTime': '2018-12-18T09:00:00-07:00',
        due_date = due_date.strftime('%Y-%m-%dT04:00:00Z')
        event_to_sync = {
            'summary': str(obj.meeting_agenda),
            'id': str(obj.calendar_id),
            'location': 'Lahore Pakistan, 54000',
            'description': 'Assignment:' + str(obj.assignment) + ' \nRemarks:' + str(obj.remarks) + ' \nSector:' + str(
                obj.sector) + ' \nDepartment:' + str(obj.department) + ' \nAssigned To:' + str(obj.assigned_to),
            'start': {
                'dateTime': meeting_date,
                'timeZone': 'Asia/Karachi',
            },
            'end': {
                'dateTime': due_date,
                'timeZone': 'Asia/Karachi',
            }
        }
    else:

        event_to_sync = {
            'id': str(obj.calendar_id),
        }
    return event_to_sync


def get_calendar_id():
    calendar_id = strgen.StringGenerator("[a-z0-9]{26}").render()
    # id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))
    # calendar_id = id.replace('w', 'a').replace('x', 'b').replace('y', 'c').replace('z', 'd')
    return calendar_id
    # return 'abcdefghi154567'


def get_meeting_participants_list(participants_list):
    participants = []
    for participant in participants_list:
        user_id = participant.tblusers_id
        user_obj = list(TblUsers.objects.filter(id=user_id).all())
        obj = get_model_dict_array(user_obj)
        if len(obj) > 0:
            participants.append(obj[0])
    return participants


def get_meetings_data():
    meetings_model = apps.get_model(app_label='meeting_management', model_name='MeetingsInitiatives')
    table_rows = list(meetings_model.objects.all().order_by('id'))
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed


def get_meeting_grid_data(request):
    type = request.GET.get('type')
    if type == None:
        type = 'quick'
    title = get_meeting_title(type)
    if type == 'calender':
        # sync_form = SyncForm()
        # data_dict = {'sync_form': sync_form, 'title': title, 'type': type}
        data_dict = {'title': title, 'type': type}
    elif type == 'meeting_initiatives_search':
        meetings_list = get_model_dict_array(TblMeetings.objects.all())
        meeting = request.GET.get('meeting')
        if meeting:
            meeting = meeting
        else:
            meeting = ''
        query = get_meeting_query(type, meeting)
        grid_data = get_jqx_columns_info_with_data(query, 'meeting_management', is_geom_include=False,
                                                   grid_width=2000)
        meetings_json_data = json.dumps(meetings_list, default=date_handler)
        compressed_meetings_data = base64.b64encode(zlib.compress(str.encode(meetings_json_data), 9))
        json_data = json.dumps(grid_data, default=date_handler)
        compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
        data_dict = {'grid_data': compressed, 'title': title, 'type': type, 'meetings_list': compressed_meetings_data,
                     'meeting': meeting}
    else:
        query = get_meeting_query(type)
        grid_data = get_jqx_columns_info_with_data(query, 'meeting_management', is_geom_include=False,
                                                   grid_width=2000)
        json_data = json.dumps(grid_data, default=date_handler)
        compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
        data_dict = {'grid_data': compressed, 'title': title, 'type': type}
    return data_dict


# def get_foreign_briefs_data(request):
#     type = request.GET.get('type')
#     if type == None:
#         type = 'foreign'
#     title = get_briefs_title(type)
#     data = get_dono_agencies_list()
#     data_dict = {'data': data, 'title': title, 'type': type}
#     return data_dict
#
# def get_briefs_title(type):
#     if type == 'foreign':
#         return 'Foreign Briefs'
#     else:
#         return 'Local Briefs'
#
# def get_dono_agencies_list():
#     meetings_model = apps.get_model(app_label='meeting_management', model_name='TblDonorAgencies')
#     table_rows = list(meetings_model.objects.all())
#     data_array = get_model_dict_array(table_rows)
#     json_data = json.dumps(data_array, default=date_handler)
#     compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
#     return compressed

def get_meetings_remarks_history(request):
    record_id = request.GET.get('id')
    meetings_model = apps.get_model(app_label='meeting_management', model_name='MeetingsInitiativesHistroy')
    table_rows = list(meetings_model.objects.filter(~Q(remarks=None), ~Q(remarks=''), id=record_id).distinct('remarks'))
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed


def get_participants_list(request):
    record_id = request.GET.get('id')
    query = 'select * from tbl_meeting_participants_vw where meeting_id = ' + record_id
    data_array = get_query_resultset_asjson(query)
    json_data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed


def get_meeting_initiatives_list(request):
    meeting_id = request.GET.get('meeting_id')
    initiative_instance = MeetingsInitiatives.objects.filter(meeting_agenda=meeting_id).all()
    data_array = get_model_dict_array(initiative_instance)
    json_data = json.dumps(data_array, default=date_handler)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return compressed


def send_sms_email_data(request):
    type = request.GET.get('type')
    id = request.GET.get('id')
    body = request.GET.get('body')
    if type == 'sms':
        html = Common_Utils.send_sms(id, body)
        return html
    if type == 'email':
        html = Common_Utils.send_email(id, 'Message from Chairman P&D', body)
        return html


def send_sms(contact_no, msg_body):
    try:
        qouted_text = quote(msg_body)
        sms_url = 'http://api.bizsms.pk/api-send-branded-sms.aspx?username=pnd@bizsms.pk&pass=p5890hg99&text=' + \
                  qouted_text + '&masking=P&DD-FERRP&destinationnum=' + contact_no + '&language=English'
        response = urllib2.urlopen(sms_url)
        html = response.msg
        return html
    except Exception as e:
        return e


def send_email(email_id, msg_subject, msg_body):
    try:
        msg = EmailMultiAlternatives(msg_subject, msg_body, None, [email_id])
        msg.attach_alternative(msg_body, "text/html")
        msg.send()
        return {"Email sent."}
    except Exception as e:
        return e


def get_meeting_query(type, meeting_id=None):
    if type == 'quick':
        return 'select * from tbl_quick_tasks_vw order by id DESC;'
    if type == 'meetings':
        return 'select * from tbl_meetings_vw;'
    if type == 'important':
        return 'select * from important_meetings_initiatives_vw order by id DESC;'
    if type == 'short':
        return 'select * from short_meetings_initiatives_vw order by id DESC;'
    if type == 'long':
        return 'select * from long_meetings_initiatives_vw order by id DESC;'
    if type == 'all':
        return 'select * from all_meetings_initiatives_vw order by id DESC;'
    if type == 'meeting_initiatives_search':
        return "select * from all_meetings_initiatives_vw WHERE meeting_id = " + meeting_id + " order by id DESC;"
    if type == 'completed':
        return 'select * from completed_meetings_initiatives_vw order by id DESC;'
    if type == 'foreign':
        return 'select * from tbl_foreign_briefs_vw;'
    if type == 'local':
        return 'select * from tbl_local_briefs_vw;'
    if type == 'contacts':
        return 'select * from tbl_users_pnd_vw;'
    if type == 'non_pnd':
        return 'select * from tbl_users_nonpnd_vw;'
    if type == 'foreigners':
        return 'select * from tbl_users_foreigners_vw;'
    else:
        return 'select * from tbl_quick_tasks_vw order by id DESC;'


def get_meeting_title(type):
    if type == 'quick':
        return 'Quick Tasks'
    if type == 'meetings':
        return 'Meetings'
    if type == 'important':
        return 'Important Initiatives'
    if type == 'short':
        return 'Short Term Initiatives'
    if type == 'long':
        return 'Long Term Initiatives'
    if type == 'all':
        return 'All Initiatives'
    if type == 'meeting_initiatives_search':
        return 'Meeting Initiatives Search'
    if type == 'completed':
        return 'Completed Initiatives'
    if type == 'foreign':
        return 'Foreign Briefs'
    if type == 'local':
        return 'Local Briefs'
    if type == 'contacts':
        return 'P&D Contacts List'
    if type == 'non_pnd':
        return 'Other Departments Contacts List'
    if type == 'foreigners':
        return 'Foreigners Contacts List'
    if type == 'calender':
        return 'Sync Google Calendar'
    else:
        return 'Quick Tasks'


def insert_data_2_meeting_participants(meeting_id, participant_id):
    obj_participants = TblMeetingsParticipants.objects.create()
    obj_participants.meeting_id = meeting_id
    obj_participants.user_id = participant_id
    obj_participants.save()


def insert_sync_to_db(request):
    # add_event_to_calender(request)
    initiatives_to_sync = request.GET.get("initiatives_to_sync")
    users_to_monitor = request.GET.get("users_to_monitor")
    user = request.user.id
    obj_social_account = SocialAccount.objects.filter(user_id=user).first()
    obj_tbl_sync = TblCalenderSync()
    obj_tbl_sync.initiative_type = initiatives_to_sync
    obj_tbl_sync.sync_to = users_to_monitor
    obj_tbl_sync.sync_by = obj_social_account
    obj_tbl_sync.syncing = True
    obj_tbl_sync.save()
    return 'synchronization successful'


def get_google_callback(request):
    params = request
    return params


def get_model_dict_array(rows):
    data_array = []
    inner_array = []
    for row in rows:
        row_dict = model_to_dict(row)
        participants = row_dict.get('participants')
        if participants:
            participants = row_dict['participants']
            for participant in participants:
                inner_array_dict = model_to_dict(participant)
                inner_array.append(inner_array_dict)
            row_dict['participants'] = inner_array
        data_array.append(row_dict)
    return data_array



def get_query_resultset_asjson(query, as_string=True):
    connection = connections['db_mm']
    cursor = connection.cursor()
    cursor.execute(query)
    data = dictfetchall(cursor)
    if as_string == True:
        json_data = json.dumps(data, default=date_handler)
    else:
        json_data = data
    return json_data


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_jqx_columns_info_with_data(query, app_label, is_geom_include=True, grid_width=-1):
    # app_label = layer_info.app_label

    connection = connections[DB_Query.get_connection_name(app_label=app_label)]  # connections[SPATIAL_DB]
    result = None
    grid_cols = []
    data_cols = []
    data_fields = []
    numeric_data_type_names = ["5", "701"]  # {"5": "int", "701": "float"}
    date_data_type_names = ['1082', 'date', 'datetime', 'timez']
    row_count = 0
    with connection.cursor() as cursor:
        cursor.execute(query)

        total_width = 0;
        for col in cursor.description:
            if is_geom_include == False and col[1] == 47806:
                continue
            c_width = 200 if col[3] == -1 else col[3]
            if col[0] == 'assignment': c_width = 500
            total_width = total_width + c_width

        for col in cursor.description:
            # if row_count == 20: break;
            if is_geom_include == False and col[0] == "geom":
                continue
            if col[0] in data_cols:
                continue
            if col[0] == "pop":
                continue
            align = "left"
            data_type = "string"
            filter_type = 'checkedlist'  # 'input'
            cellsformat = None
            if str(col[1]) in numeric_data_type_names:
                align = "right"
                data_type = 'number'  # numeric_data_type_names[str(col[1])]
                filter_type = 'number'
                # if re.search("price", col[0], re.IGNORECASE):
                #     cellsformat = 'c2'
                # else:
                cellsformat = 'F2'
            elif str(col[1]) in date_data_type_names:
                data_type = 'date'
                filter_type = 'range'
                cellsformat = 'D'
            col_width = 200 if col[3] == -1 else col[3]
            # col_width = int(col[3])
            if col[0] == 'assignment':
                col_width = 500
            if total_width >= grid_width:
                col_width = grid_width / total_width * col_width;
            if col_width < 100:
                col_width = 100
            # total_width = total_width + col_width
            if data_type == 'date':
                data_field = {
                    "name": col[0],
                    "type": data_type,
                    "format": 'dd.MM.yyyy'
                }
            else:
                data_field = {
                    "name": col[0],
                    "type": data_type,
                    # "values": {"width": col_width, "align": align}
                }

            data_fields.append(data_field)
            if data_type == 'date':
                col_info = {
                    "text": get_column_header_text(col[0]),
                    "datafield": col[0],
                    'datatype': data_type,
                    "cellsalign": align,
                    "align": align,
                    'filtertype': filter_type,
                    "width": col_width,
                    "resizable": True,
                    'cellsformat': 'dd.MM.yyyy'
                }
            else:
                col_info = {
                    "text": get_column_header_text(col[0]),
                    "datafield": col[0],
                    'datatype': data_type,
                    "cellsalign": align,
                    "align": align,
                    'filtertype': filter_type,
                    "width": col_width,
                    "resizable": True,
                    # "draggable":True,
                }
            grid_cols.append(col_info)
            data_cols.append(col[0])
            row_count = row_count + 1
        data = [
            dict(zip(data_cols, row))
            for row in cursor.fetchall()
        ]
        return {"total_width": total_width, "data_fields": data_fields, "columns": grid_cols, "data": data}


def get_column_header_text(column_name):
    if column_name == 'task_name':
        return 'Task'
    elif column_name == 'assigned_to':
        return 'Assigned To'
    elif column_name == 'is_completed':
        return 'Completed'
    elif column_name == 'task_date':
        return 'Task Date'
    elif column_name == 'assignment':
        return 'Assignment'
    elif column_name == 'assignment_date':
        return 'Assignment Date'
    elif column_name == 'due_date':
        return 'Due Date'
    elif column_name == 'sector':
        return 'Sector'
    elif column_name == 'sub_sector':
        return 'Sub Sector'
    elif column_name == 'department':
        return 'Department'
    elif column_name == 'nature':
        return 'Nature'
    elif column_name == 'meeting_agenda':
        return 'Meeting Agenda'
    elif column_name == 'meeting_date':
        return 'Meeting Date'
    elif column_name == 'referred_by':
        return 'Reffered By'
    elif column_name == 'status':
        return 'Status'
    elif column_name == 'priority':
        return 'Priority'
    elif column_name == 'remarks':
        return 'Remarks'
    elif column_name == 'term':
        return 'Term'
    elif column_name == 'assigned_to':
        return 'Assigned To'
    elif column_name == 'is_important':
        return 'Is Important'
    elif column_name == 'attachments':
        return 'Attachments'
    elif column_name == 'pics':
        return 'Pictures'
    elif column_name == 'name':
        return 'Name'
    elif column_name == 'designation':
        return 'Designation'
    elif column_name == 'contact_no':
        return 'Contact No'
    elif column_name == 'pic_path':
        return 'Picture'
    elif column_name == 'donor_agency':
        return 'Donor Agency'
    elif column_name == 'project_name':
        return 'Project Name'
    elif column_name == 'funding_mode':
        return 'Funding Mode'
    elif column_name == 'local_share':
        return 'Local Share'
    elif column_name == 'foreign_share':
        return 'Foreign Share'
    elif column_name == 'total_cost':
        return 'Total Cost'
    elif column_name == 'duration':
        return 'Duration'
    elif column_name == 'loan_effiectiveness_date':
        return 'Loan Effectiveness Date'
    elif column_name == 'loan_closing_date':
        return 'Loan Closing Date'
    elif column_name == 'loan_negotiation_date':
        return 'Loan Negotiation Date'
    elif column_name == 'loan_signing_date':
        return 'Loan Signing Date'
    elif column_name == 'implementing_agency':
        return 'Implementing Agency'
    elif column_name == 'gs_no':
        return 'GS No'
    elif column_name == 'scheme_name':
        return 'Scheme Name'
    elif column_name == 'districts':
        return 'Districts'
    elif column_name == 'tehsils':
        return 'Tehsils'
    elif column_name == 'location':
        return 'Location'
    elif column_name == 'scheme_type':
        return 'Scheme Type'
    elif column_name == 'scheme_sub_type':
        return 'Scheme Sub-type'
    elif column_name == 'major_components':
        return 'Major Components'
    elif column_name == 'total_cost':
        return 'Total Cost'
    elif column_name == 'total_capital':
        return 'Total Capital'
    elif column_name == 'total_revenue':
        return 'Assigned To'
    elif column_name == 'projection_one':
        return 'Projection One'
    elif column_name == 'projection_two':
        return 'Projection Two'
    elif column_name == 'throw_forward':
        return 'Throw Forward'
    elif column_name == 'expense_upto_june':
        return 'Expense Upto June'
    elif column_name == 'currently_assigned_to':
        return 'Currently Assigned To'
    elif column_name == 'approval_revision_date':
        return 'Approval Revision Date'
    elif column_name == 'modified_by':
        return 'Modified By'
    elif column_name == 'modified_date':
        return 'Modified Date'
    elif column_name == 'local_capital_release':
        return 'Local Capital Release'
    elif column_name == 'local_revenue_release':
        return 'Local Capital Release'
    elif column_name == 'last_updated_release':
        return 'Last Updated Release'
    elif column_name == 'priority':
        return 'Priority'
    elif column_name == 'pp_no':
        return 'PP No'
    elif column_name == 'is_in_adp':
        return 'Is In ADP'
    else:
        return column_name

# credentials = {"client_id": "911030215740-4j68uf78ercur0g00pbak3ca3srr41mm.apps.googleusercontent.com",
#                "project_id": "geocoding-154104", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                "token_uri": "https://www.googleapis.com/oauth2/v3/token",
#                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#                "client_secret": "k9N_HcQp0LX55UclJIRM8ER0"
#                }
