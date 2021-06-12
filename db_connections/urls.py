from django.conf.urls import url

from ferrp.db_connections.views import *

urlpatterns = [
    url(r'^$', external_database_index, name='db_connections'),
    url(r'^engines_list', databse_engines_list, name='engines_list'),
    url(r'^insert_connection_in_db', insert_connection_in_db, name='insert_connection_in_db'),
    url(r'^insert_tables_in_db', insert_table_in_db, name='insert_tables_in_db'),
]