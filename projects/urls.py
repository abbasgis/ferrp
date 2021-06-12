from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', project_browser, name='project_browser'),
    url(r'^proj_view_projects_data/$', get_view_project_page, name='proj_view_projects_data'),
    url(r'^proj_dir_data/$', get_directories_data, name='proj_dir_data'),
    url(r'^proj_action_file/$', perform_action_on_file, name='proj_action_file'),

    # url(r'^doc_upload/$', upload_document, name='upload_document'),
    # url(r'^doc_view/$', view_document, name='view_document'),
    # url(r'^doc_delete/$', delete_document, name='delete_document'),
    # url(r'^doc_download/$', download_document, name='download_document'),
    # url(r'^set_doc_permission/$', set_doc_permission, name='set_doc_permission'),
]
