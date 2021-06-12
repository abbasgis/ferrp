# Register your models here.
from django.contrib.admin import AdminSite

from ferrp.meeting_management.admin_meeting import *
from ferrp.meeting_management.models import *


class MeetingAdminSite(AdminSite):
    site_title = 'Meetings'
    site_header = 'P&D Department'

meetings_initiatives_site = MeetingAdminSite(name='admin_meetings')
meetings_initiatives_site.register(MeetingsInitiatives, TblMeetingsInitiativesAdmin)

meetings_initiatives_site.register(TblTaskStatus, TblTaskStatusAdmin)
meetings_initiatives_site.register(TblTaskPriority, TblTaskPriorityAdmin)
meetings_initiatives_site.register(TblTaskNature, TblTaskNatureAdmin)
meetings_initiatives_site.register(MainSector, TblMainSectorAdmin)
meetings_initiatives_site.register(SubSector, TblSectorAdmin)
meetings_initiatives_site.register(TblTaskTerm, TblTaskTermAdmin)
meetings_initiatives_site.register(TblDepartments, TblDepartmentsAdmin)
meetings_initiatives_site.register(TblUsers, TblUsersAdmin)
meetings_initiatives_site.register(TblCountry, TblCountryAdmin)
meetings_initiatives_site.register(TblQuickTasks, TblQuickTasksAdmin)
meetings_initiatives_site.register(TblDonorAgencies, TblDepartmentsAdmin)
meetings_initiatives_site.register(TblForeignBriefs, TblForeignBriefsAdmin)
meetings_initiatives_site.register(TblMeetings, TblMeetingsAgendaAdmin)
meetings_initiatives_site.register(TblUsersToSync, TblUsersToSyncAdmin)
