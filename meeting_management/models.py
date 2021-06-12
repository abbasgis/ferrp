# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords
from tinymce.models import HTMLField

server_current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class AdpSchemes1018(models.Model):
    id = models.AutoField(primary_key=True)
    scheme_name = models.CharField(db_column='Scheme Name', max_length=2500, blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year = models.TextField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    gs_no = models.IntegerField(db_column='GS No', blank=True,
                                null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    district = models.CharField(db_column='District', max_length=5000, blank=True,
                                null=True)  # Field name made lowercase.
    sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)  # Field name made lowercase.
    main_sector = models.CharField(db_column='Main Sector', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    approval = models.TextField(db_column='Approval', blank=True, null=True)  # Field name made lowercase.
    local_capital = models.FloatField(db_column='Local Capital', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    local_revenue = models.FloatField(db_column='Local Revenue', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_capital = models.FloatField(db_column='Total Capital', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_revenue = models.FloatField(db_column='Total Revenue', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid_capital = models.FloatField(db_column='Foreign Aid Capital', blank=True,
                                            null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid_revenue = models.FloatField(db_column='Foreign Aid Revenue', blank=True,
                                            null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    foreign_aid_total = models.FloatField(db_column='Foreign Aid Total', blank=True,
                                          null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cost = models.FloatField(db_column='Total Cost', blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    allocation = models.FloatField(db_column='Allocation', blank=True, null=True)  # Field name made lowercase.
    release = models.FloatField(db_column='Release', blank=True, null=True)  # Field name made lowercase.
    utilization = models.FloatField(db_column='Utilization', blank=True, null=True)  # Field name made lowercase.
    expense_upto_june = models.FloatField(db_column='Expense Upto June', blank=True,
                                          null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    projection_one = models.FloatField(db_column='Projection One', blank=True,
                                       null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    projection_two = models.FloatField(db_column='Projection Two', blank=True,
                                       null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    throw_forward = models.FloatField(db_column='Throw Forward', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'adp_schemes_10_18'


class TblLocalBriefs(models.Model):
    id = models.AutoField(primary_key=True)
    scheme_name = models.CharField(max_length=5000, blank=True, null=True)
    districts = models.CharField(max_length=5000, blank=True, null=True)
    tehsils = models.CharField(max_length=5000, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    sector = models.CharField(max_length=500, blank=True, null=True)
    scheme_type = models.CharField(max_length=100, blank=True, null=True)
    scheme_sub_type = models.CharField(max_length=500, blank=True, null=True)
    currently_assigned_to = models.CharField(max_length=100, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modifed_date = models.CharField(max_length=100, blank=True, null=True)
    pp_no = models.CharField(max_length=5000, blank=True, null=True)
    approval_revision_date = models.CharField(max_length=500, blank=True, null=True)
    major_components = models.CharField(max_length=5000, blank=True, null=True)
    major_targets = models.CharField(max_length=5000, blank=True, null=True)
    scheme_no = models.CharField(max_length=100, blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    local_cost = models.FloatField(blank=True, null=True)
    foreign_cost = models.FloatField(blank=True, null=True)
    expense_upto_june = models.FloatField(blank=True, null=True)
    local_capital = models.FloatField(blank=True, null=True)
    local_revenue = models.FloatField(blank=True, null=True)
    foreign_capital = models.FloatField(blank=True, null=True)
    foreign_revenue = models.FloatField(blank=True, null=True)
    total_capital = models.FloatField(blank=True, null=True)
    total_revenue = models.FloatField(blank=True, null=True)
    total_capital_revenue = models.FloatField(blank=True, null=True)
    projection_one = models.FloatField(blank=True, null=True)
    projection_two = models.FloatField(blank=True, null=True)
    throw_forward = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_local_briefs'


class MainSector(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'main_sector'


class MeetingsInitiatives(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_agenda = models.ForeignKey('TblMeetings', models.DO_NOTHING, db_column='meeting_agenda')
    assignment = models.CharField(max_length=5000, blank=True, null=True)
    nature = models.ForeignKey('TblTaskNature', models.DO_NOTHING, db_column='nature', blank=True, null=True)
    sector = models.ForeignKey('MainSector', models.DO_NOTHING, db_column='sector', blank=True, null=True)
    sub_sector = models.ForeignKey('SubSector', models.DO_NOTHING, db_column='sub_sector', blank=True, null=True)
    department = models.ForeignKey('TblDepartments', models.DO_NOTHING, db_column='department', blank=True, null=True)
    referred_by = models.CharField(max_length=5000, blank=True, null=True)
    assigned_to = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='assigned_to', blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.ForeignKey('TblTaskStatus', models.DO_NOTHING, db_column='status', default=1, blank=True, null=True)
    priority = models.ForeignKey('TblTaskPriority', models.DO_NOTHING, db_column='priority', blank=True, null=True)
    remarks = models.CharField(max_length=5000, blank=True, null=True)
    is_important = models.NullBooleanField()
    term = models.ForeignKey('TblTaskTerm', models.DO_NOTHING, db_column='term', blank=True, null=True)
    attachments = models.CharField(max_length=5000, blank=True, null=True)
    pics = models.CharField(max_length=5000, blank=True, null=True)
    # calendar_id = models.CharField(max_length=50, blank=True, null=True)
    history = HistoricalRecords(table_name='meetings_initiatives_history')

    class Meta:
        managed = False
        db_table = 'meetings_initiatives'


class MeetingsInitiativesHistroy(models.Model):
    id = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    meeting_agenda = models.CharField(max_length=5000, blank=True, null=True)
    assignment = models.CharField(max_length=5000, blank=True, null=True)
    nature = models.CharField(max_length=5000, blank=True, null=True)
    sector = models.CharField(max_length=5000, blank=True, null=True)
    sub_sector = models.CharField(max_length=5000, blank=True, null=True)
    department = models.CharField(max_length=5000, blank=True, null=True)
    referred_by = models.CharField(max_length=5000, blank=True, null=True)
    assigned_to = models.CharField(max_length=5000, blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=5000, blank=True, null=True)
    priority = models.CharField(max_length=5000, blank=True, null=True)
    remarks = models.CharField(max_length=5000, blank=True, null=True)
    is_important = models.NullBooleanField()
    term = models.CharField(max_length=5000, blank=True, null=True)
    remarks_date = models.DateField(blank=True, null=True, db_column='history_date')
    attachments = models.CharField(max_length=5000, blank=True, null=True)
    # calendar_id = models.CharField(max_length=50, blank=True, null=True)
    pics = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meetings_initiatives_history'


class SubSector(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    sector = models.CharField(db_column='Sector', max_length=255)  # Field name made lowercase.

    def __str__(self):
        return str(self.sector)

    class Meta:
        managed = False
        db_table = 'sector'


class TblTaskNature(models.Model):
    id = models.AutoField(primary_key=True)
    nature = models.CharField(max_length=255)

    def __str__(self):
        return str(self.nature)

    class Meta:
        managed = False
        db_table = 'tbl_task_nature'


class TblTaskPriority(models.Model):
    id = models.AutoField(primary_key=True)
    priority = models.CharField(max_length=255)

    def __str__(self):
        return str(self.priority)

    class Meta:
        managed = False
        db_table = 'tbl_task_priority'


class TblTaskStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return str(self.status)

    class Meta:
        managed = False
        db_table = 'tbl_task_status'


class TblTaskTerm(models.Model):
    id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=255)

    def __str__(self):
        return str(self.term)

    class Meta:
        managed = False
        db_table = 'tbl_task_term'


class TblDepartments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'tbl_departments'


class TblUsers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=False, max_length=500, blank=True, null=True)
    designation = models.CharField(max_length=500, blank=True, null=True)
    email_id = models.CharField(max_length=500, blank=True, null=True)
    contact_no = models.CharField(max_length=500, blank=True, null=True)
    pic_path = models.CharField(max_length=500, blank=True, null=True)
    is_synced = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(default=server_current_datetime, blank=True, null=True)
    department = models.ForeignKey('TblDepartments', models.DO_NOTHING, db_column='department', blank=True, null=True)
    country = models.ForeignKey('TblCountry', models.DO_NOTHING, db_column='country', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        ordering = ('name',)
        db_table = 'tbl_users'


class TblCountry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        ordering = ('name',)
        db_table = 'tbl_countries'


class TblQuickTasks(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='assigned_to')
    task_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_synced = models.BooleanField(default=False)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    history = HistoricalRecords(table_name='tbl_quick_tasks_new_history')

    def __str__(self):
        return str(self.task_name)

    class Meta:
        managed = False
        db_table = 'tbl_quick_tasks'
        app_label = 'meeting_management'


class TblDonorAgencies(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'tbl_donor_agencies'


class TblForeignBriefs(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    districts = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    donor_agency = models.ForeignKey('TblDonorAgencies', models.DO_NOTHING, db_column='donor_agency')
    implementing_agency = models.CharField(max_length=255, blank=True, null=True)
    funding_mode = models.CharField(max_length=255, blank=True, null=True)
    local_share = models.CharField(db_column='local_cost', max_length=255, blank=True, null=True)
    foreign_share = models.CharField(db_column='foreign_cost', max_length=255, blank=True, null=True)
    total_cost = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    project_start_date = models.DateField(blank=True, null=True)
    project_end_date = models.DateField(blank=True, null=True)
    loan_negotiation_date = models.DateField(blank=True, null=True)
    loan_signing_date = models.DateField(blank=True, null=True)
    loan_effectiveness_date = models.DateField(blank=True, null=True)
    loan_closing_date = models.DateField(blank=True, null=True)
    is_in_adp = models.BooleanField(default=True)
    time_lapsed_percent = models.IntegerField(blank=True, null=True)
    cy_allocation = models.DecimalField(max_digits=50, decimal_places=3, blank=True, null=True)
    cy_disbursement = models.DecimalField(max_digits=50, decimal_places=3, blank=True, null=True)
    cy_utilization = models.DecimalField(max_digits=50, decimal_places=3, blank=True, null=True)
    cumulative_allocation = models.DecimalField(max_digits=50, decimal_places=3, blank=True, null=True)
    cumulative_disbursement = models.DecimalField(max_digits=50, decimal_places=3, blank=True, null=True)
    cumulative_utilization = models.DecimalField(max_digits=50, decimal_places=3, blank=True, null=True)
    scope_objectives = HTMLField(blank=True, null=True)
    components_dli = HTMLField(blank=True, null=True)
    physical_progress = HTMLField(blank=True, null=True)
    issues_way_forward = HTMLField(blank=True, null=True)
    scheme_description = HTMLField(blank=True, null=True)

    def __str__(self):
        return str(self.project_name)

    class Meta:
        managed = False
        db_table = 'tbl_foreign_briefs'


class TblMeetings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    meeting_date = models.DateField()
    meeting_start_time = models.TimeField()
    meeting_end_time = models.TimeField()
    venue = models.CharField(max_length=255, blank=True, null=True)
    decisions = HTMLField(blank=True, null=True)
    calendar_id = models.CharField(max_length=255)
    attachments = models.CharField(max_length=5000, blank=True, null=True)
    pics = models.CharField(max_length=5000, blank=True, null=True)
    participants = models.ManyToManyField(TblUsers, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = True
        db_table = 'tbl_meetings'


class TblCalenderSync(models.Model):
    id = models.AutoField(primary_key=True)
    initiative_type = models.CharField(max_length=255)
    sync_to = models.CharField(max_length=50)
    sync_by = models.ForeignKey('socialaccount.SocialAccount', models.DO_NOTHING, db_column='sync_by', blank=True,
                                null=True)
    syncing = models.BooleanField(default=True)

    def __str__(self):
        return str(self.initiative_type)

    class Meta:
        managed = False
        db_table = 'tbl_calender_sync'


class ShortMeetingsInitiativesVw(models.Model):
    id = models.IntegerField(primary_key=True)
    assignment = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=254, blank=True, null=True)
    assignment_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    sub_sector = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True)
    nature = models.CharField(max_length=254, blank=True, null=True)
    meeting_agenda = models.TextField(blank=True, null=True)
    referred_by = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    priority = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    term = models.CharField(max_length=50, blank=True, null=True)
    is_important = models.NullBooleanField()
    attachments = models.CharField(max_length=254, blank=True, null=True)
    pics = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'short_meetings_initiatives_vw_android'


class LongMeetingsInitiativesVw(models.Model):
    id = models.IntegerField(primary_key=True)
    assignment = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=254, blank=True, null=True)
    assignment_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    sub_sector = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True)
    nature = models.CharField(max_length=254, blank=True, null=True)
    meeting_agenda = models.TextField(blank=True, null=True)
    referred_by = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    priority = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    term = models.CharField(max_length=50, blank=True, null=True)
    is_important = models.NullBooleanField()
    attachments = models.CharField(max_length=254, blank=True, null=True)
    pics = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'long_meetings_initiatives_vw_android'


class ImportantMeetingsInitiativesVw(models.Model):
    id = models.IntegerField(primary_key=True)
    assignment = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=254, blank=True, null=True)
    assignment_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    sub_sector = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True)
    nature = models.CharField(max_length=254, blank=True, null=True)
    meeting_agenda = models.TextField(blank=True, null=True)
    referred_by = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    priority = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    term = models.CharField(max_length=50, blank=True, null=True)
    is_important = models.NullBooleanField()
    attachments = models.CharField(max_length=254, blank=True, null=True)
    pics = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'important_meetings_initiatives_vw_android'


class AllMeetingsInitiativesVw(models.Model):
    id = models.IntegerField(primary_key=True)
    assignment = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=254, blank=True, null=True)
    assignment_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    sub_sector = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True)
    nature = models.CharField(max_length=254, blank=True, null=True)
    meeting_agenda = models.TextField(blank=True, null=True)
    referred_by = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    priority = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    term = models.CharField(max_length=50, blank=True, null=True)
    is_important = models.NullBooleanField()
    attachments = models.CharField(max_length=254, blank=True, null=True)
    pics = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_meetings_initiatives_vw_android'


# class TblMeetingParticipants(models.Model):
#     id = models.AutoField(primary_key=True)
#     meeting_id = models.IntegerField()
#     user_id = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_meeting_participants'


class TblUsersToSync(models.Model):
    id = models.AutoField(primary_key=True)
    auth_user_id = models.ForeignKey(User, db_column='user_id')
    calendar_link = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_users_to_sync_calendar'


class TblMeetingsUsersEvents(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_id = models.IntegerField()
    user_id = models.IntegerField()
    calendar_event_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_meetings_users_calendarevents'


class TblMeetingsParticipants(models.Model):
    meeting_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'tbl_meeting_participants'
        app_label = 'meeting_management'

# class TblMeetingsParticipants(models.Model):
#     tblmeetings_id = models.BigIntegerField(blank=True, null=True)
#     tblusers_id = models.IntegerField(blank=True, null=True)
#     id = models.BigAutoField(primary_key=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_meetings_participants'
#         app_label = 'meeting_management'
