from django.conf.urls import url, include

from ferrp.meeting_management.views import *

urlpatterns = [
    url('^', include('ferrp.meeting_management.urls_mobile')),
    url(r'^$', mm_index, name='mm'),
    url(r'^meetings_data/', meetings_list, name='meetings_data'),
    url(r'^grid_data/', meeting_grid_data, name='grid_data'),
    url(r'^history_data/', meeting_remarks_history_data, name='history_data'),
    url(r'^participants_list/', participants_list, name='participants_list'),
    url(r'^initiatives_list/', initiatives_list, name='initiatives_list'),
    url(r'^sms_email_data/', sms_email_data, name='sms_email_data'),
    url(r'^sync_to/', sync_to, name='sync_to'),
    # url(r'^google_callback/', google_callback, name='google_callback'),

]
