from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# from django.template import loader

from ferrp.meeting_management.utils import get_meetings_data, get_meeting_grid_data, get_meetings_remarks_history, \
    send_sms_email_data, insert_sync_to_db, get_google_callback, get_participants_list, get_initiatives_list, \
    get_meeting_initiatives_list


@login_required
def mm_index(request):
    is_staff = request.user.is_staff
    if is_staff == True:
        template_data = get_meeting_grid_data(request)
        return render(request, 'important_mm.html', context=template_data)
    else:
        return render(request, 'not_authorized.html')


# def foreign_brief_index(request):
#     briefs_data = get_foreign_briefs_data(request)
#     return render(request, 'foreign_briefs.html', context= briefs_data )

def meetings_list(self):
    meetings_data = get_meetings_data()
    return HttpResponse(meetings_data)


def meeting_grid_data(self):
    grid_data = get_meeting_grid_data()
    return HttpResponse(grid_data)


def meeting_remarks_history_data(request):
    history_data = get_meetings_remarks_history(request)
    return HttpResponse(history_data)


def participants_list(request):
    participants = get_participants_list(request)
    return HttpResponse(participants)


def initiatives_list(request):
    participants = get_meeting_initiatives_list(request)
    return HttpResponse(participants)



def sms_email_data(request):
    history_data = send_sms_email_data(request)
    return HttpResponse(history_data)


def sync_to(request):
    resp = insert_sync_to_db(request)
    return HttpResponse(resp)


def google_callback(request):
    google = get_google_callback(request)
    return HttpResponse(google)
