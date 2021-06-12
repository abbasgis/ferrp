import os

from django.contrib.admin import ModelAdmin, TabularInline
from django import forms
from django.shortcuts import redirect
from searchableselect.widgets import SearchableSelect
from simple_history.admin import SimpleHistoryAdmin

from ferrp.meeting_management.models import *
from ferrp.meeting_management.utils import *
from ferrp.settings import PROJECT_ROOT
from ferrp.utils import Common_Utils, Log_Error


class TblMeetingsInitiativesForm(forms.ModelForm):
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'width': 600, 'height': 300}))
    attachments_field = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))
    pic_path_field = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = MeetingsInitiatives
        fields = (
            'meeting_agenda', 'assignment', 'nature', 'sector', 'sub_sector', 'department', 'referred_by',
            'assigned_to',
            'meeting_date', 'due_date', 'status', 'priority', 'term', 'remarks', 'is_important', 'attachments_field',
            'pic_path_field')


class TblMeetingsInitiativesAdmin(SimpleHistoryAdmin):
    list_display = (
        'meeting_agenda', 'assignment', 'nature', 'sector', 'sub_sector', 'department', 'referred_by', 'assigned_to',
        'meeting_date', 'due_date', 'status', 'priority', 'term', 'remarks', 'is_important')
    history_list_display = ['meeting_agenda', 'assignment', 'nature', 'sector', 'sub_sector', 'department',
                            'referred_by', 'assigned_to', 'meeting_date', 'due_date', 'status', 'priority', 'term',
                            'remarks', 'is_important']

    list_display_links = ('assignment',)
    date_hierarchy = 'due_date'
    list_filter = ('nature', 'status')
    search_fields = ('nature', 'priority', 'assignment', 'status', 'meeting_agenda')
    form = TblMeetingsInitiativesForm
    exclude = ['id']

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../'
        return redirect(redirect_url)

    def response_change(self, request, obj):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def response_delete(self, request, obj, post_url_continue=None):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def delete_model(self, request, object):
        try:
            meeting_id = object.meeting_agenda_id
            object.delete()
            meeting_instance = TblMeetingsParticipants.objects.filter(meeting_id=meeting_id)
            participants_array = get_meeting_participants_list(meeting_instance)
            meeting_obj = TblMeetings.objects.filter(id=meeting_id).get()
            event = get_meeting_event_object(meeting_obj, participants_array)
            change_event_for_users(event)
        except Exception as e:
            Log_Error.log_error_message(e)

    def save_model(self, request, obj, form, change):
        pictures = request.FILES.getlist('pic_path_field', None)
        attachments = request.FILES.getlist('attachments_field', None)
        pic_names = ''
        attachments_names = ''

        if len(pictures) > 0:
            for f in pictures:
                if f is not None:
                    file_name_ext = os.path.splitext(f.name)
                    file_name = Common_Utils.add_timestamp_to_string(file_name_ext[0]) + file_name_ext[1]
                    file_path = os.path.join(PROJECT_ROOT, '../uploaded/mm/pics', file_name)
                    # file_path = os.path.join(DOCUMENT_URL, 'mm/pics', file_name)
                    Common_Utils.handle_uploaded_file(f, file_path)
                    pic_names = file_name + ';' + pic_names
            obj.pics = pic_names
        if len(attachments) > 0:
            for f in attachments:
                if f is not None:
                    file_name_ext = os.path.splitext(f.name)
                    file_name = Common_Utils.add_timestamp_to_string(file_name_ext[0]) + file_name_ext[1]
                    file_path = os.path.join(PROJECT_ROOT, '../uploaded/mm/docs', file_name)
                    # file_path = os.path.join(DOCUMENT_URL, 'mm/docs', file_name)
                    Common_Utils.handle_uploaded_file(f, file_path)
                    attachments_names = file_name + ';' + attachments_names
            obj.attachments = attachments_names
        super(TblMeetingsInitiativesAdmin, self).save_model(request, obj, form, change)
        meeting_id = obj.meeting_agenda_id
        meeting_obj = TblMeetings.objects.filter(id=meeting_id).get()
        meeting_instance = TblMeetingsParticipants.objects.filter(meeting_id=meeting_id)
        participants_array = get_meeting_participants_list(meeting_instance)
        event = get_meeting_event_object(meeting_obj, participants_array)
        change_event_for_users(event)


class TblTaskStatusAdmin(ModelAdmin):
    list_display = ['status']
    exclude = ['id']


class TblTaskNatureAdmin(ModelAdmin):
    list_display = ['nature']
    exclude = ['id']


class TblTaskPriorityAdmin(ModelAdmin):
    list_display = ['priority']
    exclude = ['id']


class TblMainSectorAdmin(ModelAdmin):
    list_display = ['name']
    exclude = ['id']


class TblSectorAdmin(ModelAdmin):
    list_display = ['sector']
    exclude = ['id']


class TblTaskTermAdmin(ModelAdmin):
    list_display = ['term']
    exclude = ['id']


class TblDepartmentsAdmin(ModelAdmin):
    list_display = ['name']
    exclude = ['id']


class TblMeetingsAgendaForm(forms.ModelForm):
    # decisions = forms.CharField(max_length= 3000 ,required=False, widget=forms.Textarea(attrs={'width': 600, 'height': 300}))
    # participants = forms.ModelMultipleChoiceField(widget= forms.SelectMultiple(),
    #                                               queryset=TblUsers.objects.all(), required=False)
    # participants = forms.ModelMultipleChoiceField(widget=SearchableSelect(
    #     model='meeting_management.TblUsers', search_field= 'name'  ),
    #     queryset=TblUsers.objects.all(), required=False)
    attachments_field = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))
    pic_path_field = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = TblMeetings
        widgets = {
            'participants': SearchableSelect(model='meeting_management.TblUsers', search_field='name', limit=10)
        }
        # exclude = ()
        fields = (
            'name', 'meeting_date', 'meeting_start_time', 'meeting_end_time', 'venue', 'decisions', 'participants',
            'attachments_field', 'pic_path_field')


def delete_record_and_calendar_event(modeladmin, request, queryset):
    for obj in queryset:
        meeting_id = obj.id
        delete_event_for_users(meeting_id)
        meeting_id = obj.id
        meeting_instance = TblMeetingsParticipants.objects.filter(meeting_id=meeting_id)
        if meeting_instance:
            meeting_instance.delete()
        obj.delete()


def sync_selected_with_calendar(modeladmin, request, queryset):
    for obj in queryset:
        meeting_id = obj.id
        meeting_instance = TblMeetingsParticipants.objects.filter(meeting_id=meeting_id)
        participants_array = get_meeting_participants_list(meeting_instance)
        event = get_meeting_event_object(obj, participants_array)
        add_event_to_users(event)


class AssignmentInline(TabularInline):
    model = MeetingsInitiatives  # .meeting_agenda.through
    fields = ['assignment']


class TblMeetingsAgendaAdmin(ModelAdmin):
    list_display = ['id', 'name', 'meeting_date', 'meeting_start_time', 'meeting_end_time', 'venue', 'decisions']
    list_display_links = ('name',)
    exclude = ['id']
    form = TblMeetingsAgendaForm
    actions = [delete_record_and_calendar_event, sync_selected_with_calendar]
    inlines = [AssignmentInline, ]

    def response_add(self, request, obj, post_url_continue=None):
        meeting_id = obj.id
        meeting_instance = TblMeetingsParticipants.objects.filter(meeting_id=meeting_id)
        participants_array = get_meeting_participants_list(meeting_instance)
        if obj.meeting_date:
            MeetingsInitiatives.objects.filter(meeting_agenda=meeting_id).update(meeting_date=obj.meeting_date)
            event = get_meeting_event_object(obj, participants_array)
            add_event_to_users(event)
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../'
        return redirect(redirect_url)

    def response_change(self, request, obj):
        meeting_id = obj.id
        meeting_instance = TblMeetingsParticipants.objects.filter(meeting_id=meeting_id)
        participants_array = get_meeting_participants_list(meeting_instance)
        if obj.meeting_date:
            MeetingsInitiatives.objects.filter(meeting_agenda=meeting_id).update(meeting_date=obj.meeting_date)
            event = get_meeting_event_object(obj, participants_array)
            change_event_for_users(event)
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def response_delete(self, request, obj_display, obj_id):
        delete_event_for_users(obj_id)
        initiative_instance = MeetingsInitiatives.objects.filter(meeting_agenda=obj_id)
        if initiative_instance:
            initiative_instance.delete()
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def save_model(self, request, obj, form, change):
        pictures = request.FILES.getlist('pic_path_field', None)
        attachments = request.FILES.getlist('attachments_field', None)
        pic_names = ''
        attachments_names = ''

        if len(pictures) > 0:
            for f in pictures:
                if f is not None:
                    file_name_ext = os.path.splitext(f.name)
                    file_name = Common_Utils.add_timestamp_to_string(file_name_ext[0]) + file_name_ext[1]
                    file_path = os.path.join(PROJECT_ROOT, '../uploaded/mm/pics', file_name)
                    Common_Utils.handle_uploaded_file(f, file_path)
                    pic_names = file_name + ';' + pic_names
            obj.pics = pic_names
        if len(attachments) > 0:
            for f in attachments:
                if f is not None:
                    file_name_ext = os.path.splitext(f.name)
                    file_name = Common_Utils.add_timestamp_to_string(file_name_ext[0]) + file_name_ext[1]
                    file_path = os.path.join(PROJECT_ROOT, '../uploaded/mm/docs', file_name)
                    Common_Utils.handle_uploaded_file(f, file_path)
                    attachments_names = file_name + ';' + attachments_names
            obj.attachments = attachments_names
        super(TblMeetingsAgendaAdmin, self).save_model(request, obj, form, change)


class TblUsersForm(forms.ModelForm):
    pic_path_field = forms.FileField(required=False)

    class Meta:
        model = TblUsers
        fields = ('name', 'designation', 'email_id', 'contact_no', 'department', 'country', 'pic_path_field')


class TblUsersAdmin(ModelAdmin):
    list_display = ('name', 'designation', 'email_id', 'contact_no', 'department', 'country')
    fields = ('name', 'designation', 'email_id', 'contact_no', 'department', 'country', 'pic_path_field')

    list_display_links = ('name',)
    list_filter = ('name', 'designation')
    search_fields = ('name', 'designation', 'email_id', 'contact_no')
    form = TblUsersForm
    exclude = ['id']

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = request.GET.get('next')
        if redirect_url:
            return redirect(redirect_url)

    def response_change(self, request, obj):
        redirect_url = request.GET.get('next')
        if redirect_url:
            return redirect(redirect_url)

    def response_delete(self, request, obj_display, obj_id):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('pic_path_field', None)
        f = files[0] if len(files) > 0 else None
        if f is not None:
            file_name_ext = os.path.splitext(f.name)
            file_name = Common_Utils.add_timestamp_to_string(file_name_ext[0]) + file_name_ext[1]
            file_path = os.path.join(PROJECT_ROOT, '../uploaded/mm/user_pictures', file_name)
            # file_path = os.path.join(DOCUMENT_URL, 'mm/users_pictures', file_name)
            Common_Utils.handle_uploaded_file(f, file_path)
            obj.pic_path = file_name
        super(TblUsersAdmin, self).save_model(request, obj, form, change)


class TblCountryAdmin(ModelAdmin):
    list_display = ['name']
    fields = ['name']
    exclude = ['id']


class TblDonorAgenciesAdmin(ModelAdmin):
    list_display = ['name']


class TblQuickTasksAdmin(ModelAdmin):
    list_display = ('task_name', 'assigned_to', 'task_date', 'is_completed')
    exclude = ['id', 'is_synced', 'created_by', 'updated_by', 'updated_at']

    # history_list_display = ['task_name', 'assigned_to', 'task_date', 'is_completed']

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../'
        return redirect(redirect_url)

    def response_change(self, request, obj):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def response_delete(self, request, obj_display, obj_id):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)


class TblForeignBriefsForm(forms.ModelForm):
    scheme_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'width': 600, 'height': 300}))

    class Meta:
        model = TblForeignBriefs
        fields = (
            'donor_agency', 'project_name', 'funding_mode', 'local_share', 'foreign_share', 'total_cost', 'duration',
            'implementing_agency', 'loan_effectiveness_date', 'loan_closing_date', 'loan_negotiation_date',
            'loan_signing_date', 'scheme_description', 'time_lapsed_percent', 'cy_allocation', 'cy_disbursement',
            'cy_utilization',
            'cumulative_allocation', 'cumulative_disbursement', 'cumulative_utilization', 'scope_objectives',
            'components_dli', 'physical_progress',
            'issues_way_forward', 'project_start_date', 'project_end_date')


class TblForeignBriefsAdmin(ModelAdmin):
    list_display = (
        'donor_agency', 'project_name', 'funding_mode', 'local_share', 'foreign_share', 'total_cost', 'duration',
        'implementing_agency', 'loan_effectiveness_date', 'loan_closing_date', 'loan_negotiation_date',
        'loan_signing_date', 'scheme_description', 'time_lapsed_percent', 'cy_allocation', 'cy_disbursement',
        'cy_utilization',
        'cumulative_allocation', 'cumulative_disbursement', 'cumulative_utilization', 'scope_objectives',
        'components_dli', 'physical_progress',
        'issues_way_forward', 'project_start_date', 'project_end_date')
    # form = TblForeignBriefsForm

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../'
        return redirect(redirect_url)

    def response_change(self, request, obj):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def response_delete(self, request, obj_display, obj_id):
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = request.path + '../../'
        return redirect(redirect_url)

    def save_model(self, request, obj, form, change):
        super(TblForeignBriefsAdmin, self).save_model(request, obj, form, change)
        redirect_url = request.GET.get('next')
        if redirect_url:
            redirect(redirect_url)


class TblUsersToSyncAdmin(ModelAdmin):
    list_display = ['id', 'auth_user_id_id', 'calendar_link']
    exclude = ['id']
