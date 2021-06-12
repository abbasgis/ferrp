# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-04 12:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdpSchemes1018',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scheme_name', models.CharField(blank=True, db_column='Scheme Name', max_length=2500, null=True)),
                ('year', models.TextField(blank=True, db_column='Year', null=True)),
                ('gs_no', models.IntegerField(blank=True, db_column='GS No', null=True)),
                ('district', models.CharField(blank=True, db_column='District', max_length=5000, null=True)),
                ('sector', models.CharField(blank=True, db_column='Sector', max_length=255, null=True)),
                ('main_sector', models.CharField(blank=True, db_column='Main Sector', max_length=255, null=True)),
                ('type', models.CharField(blank=True, db_column='Type', max_length=255, null=True)),
                ('approval', models.TextField(blank=True, db_column='Approval', null=True)),
                ('local_capital', models.FloatField(blank=True, db_column='Local Capital', null=True)),
                ('local_revenue', models.FloatField(blank=True, db_column='Local Revenue', null=True)),
                ('total_capital', models.FloatField(blank=True, db_column='Total Capital', null=True)),
                ('total_revenue', models.FloatField(blank=True, db_column='Total Revenue', null=True)),
                ('foreign_aid_capital', models.FloatField(blank=True, db_column='Foreign Aid Capital', null=True)),
                ('foreign_aid_revenue', models.FloatField(blank=True, db_column='Foreign Aid Revenue', null=True)),
                ('foreign_aid_total', models.FloatField(blank=True, db_column='Foreign Aid Total', null=True)),
                ('total_cost', models.FloatField(blank=True, db_column='Total Cost', null=True)),
                ('allocation', models.FloatField(blank=True, db_column='Allocation', null=True)),
                ('release', models.FloatField(blank=True, db_column='Release', null=True)),
                ('utilization', models.FloatField(blank=True, db_column='Utilization', null=True)),
                ('expense_upto_june', models.FloatField(blank=True, db_column='Expense Upto June', null=True)),
                ('projection_one', models.FloatField(blank=True, db_column='Projection One', null=True)),
                ('projection_two', models.FloatField(blank=True, db_column='Projection Two', null=True)),
                ('throw_forward', models.FloatField(blank=True, db_column='Throw Forward', null=True)),
            ],
            options={
                'db_table': 'adp_schemes_10_18',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AllMeetingsInitiativesVw',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('assignment', models.TextField(blank=True, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=254, null=True)),
                ('assignment_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_sector', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.CharField(blank=True, max_length=254, null=True)),
                ('nature', models.CharField(blank=True, max_length=254, null=True)),
                ('meeting_agenda', models.TextField(blank=True, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('priority', models.CharField(blank=True, max_length=254, null=True)),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('term', models.CharField(blank=True, max_length=50, null=True)),
                ('is_important', models.NullBooleanField()),
                ('attachments', models.CharField(blank=True, max_length=254, null=True)),
                ('pics', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'all_meetings_initiatives_vw_android',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImportantMeetingsInitiativesVw',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('assignment', models.TextField(blank=True, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=254, null=True)),
                ('assignment_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_sector', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.CharField(blank=True, max_length=254, null=True)),
                ('nature', models.CharField(blank=True, max_length=254, null=True)),
                ('meeting_agenda', models.TextField(blank=True, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('priority', models.CharField(blank=True, max_length=254, null=True)),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('term', models.CharField(blank=True, max_length=50, null=True)),
                ('is_important', models.NullBooleanField()),
                ('attachments', models.CharField(blank=True, max_length=254, null=True)),
                ('pics', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'important_meetings_initiatives_vw_android',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LongMeetingsInitiativesVw',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('assignment', models.TextField(blank=True, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=254, null=True)),
                ('assignment_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_sector', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.CharField(blank=True, max_length=254, null=True)),
                ('nature', models.CharField(blank=True, max_length=254, null=True)),
                ('meeting_agenda', models.TextField(blank=True, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('priority', models.CharField(blank=True, max_length=254, null=True)),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('term', models.CharField(blank=True, max_length=50, null=True)),
                ('is_important', models.NullBooleanField()),
                ('attachments', models.CharField(blank=True, max_length=254, null=True)),
                ('pics', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'long_meetings_initiatives_vw_android',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MainSector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
            ],
            options={
                'db_table': 'main_sector',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingsInitiatives',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment', models.CharField(blank=True, max_length=5000, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=5000, null=True)),
                ('meeting_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=5000, null=True)),
                ('is_important', models.NullBooleanField()),
                ('attachments', models.CharField(blank=True, max_length=5000, null=True)),
                ('pics', models.CharField(blank=True, max_length=5000, null=True)),
            ],
            options={
                'db_table': 'meetings_initiatives',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingsInitiativesHistroy',
            fields=[
                ('id', models.IntegerField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('meeting_agenda', models.CharField(blank=True, max_length=5000, null=True)),
                ('assignment', models.CharField(blank=True, max_length=5000, null=True)),
                ('nature', models.CharField(blank=True, max_length=5000, null=True)),
                ('sector', models.CharField(blank=True, max_length=5000, null=True)),
                ('sub_sector', models.CharField(blank=True, max_length=5000, null=True)),
                ('department', models.CharField(blank=True, max_length=5000, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=5000, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=5000, null=True)),
                ('meeting_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=5000, null=True)),
                ('priority', models.CharField(blank=True, max_length=5000, null=True)),
                ('remarks', models.CharField(blank=True, max_length=5000, null=True)),
                ('is_important', models.NullBooleanField()),
                ('term', models.CharField(blank=True, max_length=5000, null=True)),
                ('remarks_date', models.DateField(blank=True, db_column='history_date', null=True)),
                ('attachments', models.CharField(blank=True, max_length=5000, null=True)),
                ('pics', models.CharField(blank=True, max_length=5000, null=True)),
            ],
            options={
                'db_table': 'meetings_initiatives_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShortMeetingsInitiativesVw',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('assignment', models.TextField(blank=True, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=254, null=True)),
                ('assignment_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_sector', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.CharField(blank=True, max_length=254, null=True)),
                ('nature', models.CharField(blank=True, max_length=254, null=True)),
                ('meeting_agenda', models.TextField(blank=True, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('priority', models.CharField(blank=True, max_length=254, null=True)),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('term', models.CharField(blank=True, max_length=50, null=True)),
                ('is_important', models.NullBooleanField()),
                ('attachments', models.CharField(blank=True, max_length=254, null=True)),
                ('pics', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'short_meetings_initiatives_vw_android',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubSector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sector', models.CharField(db_column='Sector', max_length=255)),
            ],
            options={
                'db_table': 'sector',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblCalenderSync',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('initiative_type', models.CharField(max_length=255)),
                ('sync_to', models.CharField(max_length=50)),
                ('syncing', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tbl_calender_sync',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblDepartments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_departments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblDonorAgencies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_donor_agencies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblForeignBriefs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(blank=True, max_length=255, null=True)),
                ('funding_mode', models.CharField(blank=True, max_length=255, null=True)),
                ('local_share', models.CharField(blank=True, db_column='local_cost', max_length=255, null=True)),
                ('foreign_share', models.CharField(blank=True, db_column='foreign_cost', max_length=255, null=True)),
                ('total_cost', models.CharField(blank=True, max_length=255, null=True)),
                ('duration', models.CharField(blank=True, max_length=255, null=True)),
                ('implementing_agency', models.CharField(blank=True, max_length=255, null=True)),
                ('loan_effectiveness_date', models.DateField(blank=True, null=True)),
                ('loan_closing_date', models.DateField(blank=True, null=True)),
                ('loan_negotiation_date', models.DateField(blank=True, null=True)),
                ('loan_signing_date', models.DateField(blank=True, null=True)),
                ('is_in_adp', models.BooleanField(default=True)),
                ('scheme_description', models.CharField(blank=True, max_length=100000, null=True)),
            ],
            options={
                'db_table': 'tbl_foreign_briefs_1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblLocalBriefs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scheme_name', models.CharField(blank=True, max_length=5000, null=True)),
                ('districts', models.CharField(blank=True, max_length=5000, null=True)),
                ('tehsils', models.CharField(blank=True, max_length=5000, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('sector', models.CharField(blank=True, max_length=500, null=True)),
                ('scheme_type', models.CharField(blank=True, max_length=100, null=True)),
                ('scheme_sub_type', models.CharField(blank=True, max_length=500, null=True)),
                ('currently_assigned_to', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modifed_date', models.CharField(blank=True, max_length=100, null=True)),
                ('pp_no', models.CharField(blank=True, max_length=5000, null=True)),
                ('approval_revision_date', models.CharField(blank=True, max_length=500, null=True)),
                ('major_components', models.CharField(blank=True, max_length=5000, null=True)),
                ('major_targets', models.CharField(blank=True, max_length=5000, null=True)),
                ('scheme_no', models.CharField(blank=True, max_length=100, null=True)),
                ('total_cost', models.FloatField(blank=True, null=True)),
                ('local_cost', models.FloatField(blank=True, null=True)),
                ('foreign_cost', models.FloatField(blank=True, null=True)),
                ('expense_upto_june', models.FloatField(blank=True, null=True)),
                ('local_capital', models.FloatField(blank=True, null=True)),
                ('local_revenue', models.FloatField(blank=True, null=True)),
                ('foreign_capital', models.FloatField(blank=True, null=True)),
                ('foreign_revenue', models.FloatField(blank=True, null=True)),
                ('total_capital', models.FloatField(blank=True, null=True)),
                ('total_revenue', models.FloatField(blank=True, null=True)),
                ('total_capital_revenue', models.FloatField(blank=True, null=True)),
                ('projection_one', models.FloatField(blank=True, null=True)),
                ('projection_two', models.FloatField(blank=True, null=True)),
                ('throw_forward', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_local_briefs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMeetingParticipants',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('meeting_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_meeting_participants',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMeetings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('meeting_date', models.DateField(blank=True, null=True)),
                ('meeting_start_time', models.TimeField(blank=True, null=True)),
                ('meeting_end_time', models.TimeField(blank=True, null=True)),
                ('venue', models.CharField(max_length=255)),
                ('decisions', models.CharField(max_length=255)),
                ('calendar_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tbl_meetings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblQuickTasks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(blank=True, max_length=255, null=True)),
                ('task_date', models.DateField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_synced', models.BooleanField(default=False)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'tbl_quick_tasks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblTaskNature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nature', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tbl_task_nature',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblTaskPriority',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('priority', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tbl_task_priority',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblTaskStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tbl_task_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblTaskTerm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('term', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tbl_task_term',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('designation', models.CharField(blank=True, max_length=500, null=True)),
                ('email_id', models.CharField(blank=True, max_length=500, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=500, null=True)),
                ('pic_path', models.CharField(blank=True, max_length=500, null=True)),
                ('is_synced', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default='2019-01-04 17:50:43', null=True)),
            ],
            options={
                'db_table': 'tbl_users',
                'ordering': ('name',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalMeetingsInitiatives',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('assignment', models.CharField(blank=True, max_length=5000, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=5000, null=True)),
                ('meeting_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=5000, null=True)),
                ('is_important', models.NullBooleanField()),
                ('attachments', models.CharField(blank=True, max_length=5000, null=True)),
                ('pics', models.CharField(blank=True, max_length=5000, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assigned_to', models.ForeignKey(blank=True, db_column='assigned_to', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblUsers')),
                ('department', models.ForeignKey(blank=True, db_column='department', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblDepartments')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('meeting_agenda', models.ForeignKey(blank=True, db_column='meeting_agenda', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblMeetings')),
                ('nature', models.ForeignKey(blank=True, db_column='nature', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblTaskNature')),
                ('priority', models.ForeignKey(blank=True, db_column='priority', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblTaskPriority')),
                ('sector', models.ForeignKey(blank=True, db_column='sector', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.MainSector')),
                ('status', models.ForeignKey(blank=True, db_column='status', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblTaskStatus')),
                ('sub_sector', models.ForeignKey(blank=True, db_column='sub_sector', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.SubSector')),
                ('term', models.ForeignKey(blank=True, db_column='term', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblTaskTerm')),
            ],
            options={
                'verbose_name': 'historical meetings initiatives',
                'db_table': 'meetings_initiatives_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTblQuickTasks',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('task_name', models.CharField(blank=True, max_length=255, null=True)),
                ('task_date', models.DateField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_synced', models.BooleanField(default=False)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assigned_to', models.ForeignKey(blank=True, db_column='assigned_to', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='meeting_management.TblUsers')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical tbl quick tasks',
                'db_table': 'tbl_quick_tasks_new_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
