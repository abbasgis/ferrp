from django.conf.urls import url

from ferrp.meeting_management import mobile_controller

urlpatterns = [
    url(r'^mb_test/$', mobile_controller.for_testing, name='mb_test'),
    url(r'^mb_chk_email/$', mobile_controller.checkIsEmailRegistered, name='mb_chk_email'),
    url(r'^mb_login/$', mobile_controller.authenticate_mobile_user, name='mb_login'),
    url(r'^mb_get_assignments_data/$', mobile_controller.get_assignments_data, name='mb_get_assignments_data'),
    url(r'^mb_get_assignment_detail/$', mobile_controller.get_assignment_detail, name='mb_get_assignment_detail'),
    url(r'^mb_get_remarks_history/$', mobile_controller.get_remarks_history, name='mb_get_remarks_history'),
    url(r'^mb_save_task/$', mobile_controller.save_task, name='mb_save_task'),
    url(r'^mb_delete_task/$', mobile_controller.delete_task, name='mb_delete_task'),
    url(r'^mb_users_list/$', mobile_controller.get_users_list, name='mb_users_list'),
    url(r'^mb_sync_quick_task/$', mobile_controller.sync_quick_tasks, name='mb_sync_quick_task'),


]
