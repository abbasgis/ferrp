from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^app/$', app_integration, name='app_integration'),
    url(r'^datamatrs_browser/$', datamarts_browser, name='datamarts_browser'),
    url(r'^conn_params/$', conn_params_view, name='conn_params'),
    url(r'^test_conn/$', test_connection, name='test_conn'),
    url(r'^add_or_get_conn_details/$', add_or_get_connection_details, name='add_conn'),
    url(r'^add_tables/$', add_tables, name='add_tables'),
    url(r'^del_table/$', delete_table, name='del_tables'),
    url(r'^view_datasets/$', view_datasets, name='view_datasets'),
    url(r'^view_table/$', view_aspatial_table, name='view_table'),

    # url(r'^add_datasets/$', add_datasets, name='add_datasets'),

]
