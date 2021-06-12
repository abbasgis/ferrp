import base64
import json
import os

import zlib

import subprocess
from django.apps import apps
from django.db import connections
from django.forms import model_to_dict

from ferrp import settings

from ferrp.db_connections.models import ConnectionsList, GenericTableModel
from ferrp.settings import BASE_DIR


def get_databse_engines_list():
    db_engines_model_class = apps.get_model(app_label='db_connections', model_name='DatabaseEngines')
    table_rows = list(db_engines_model_class.objects.all().order_by('id'))
    data_array = get_model_dict_array(table_rows)
    json_data = json.dumps(data_array)
    compressed = base64.b64encode(zlib.compress(str.encode(json_data), 9))
    return json_data

database_id = None
connection = None
def get_insert_connection_in_db(request):
    db_provider = request.POST.get('cmbDbProviders')
    txtHost = request.POST.get('txtHost')
    txtPort = request.POST.get('txtPort')
    txtDBName = request.POST.get('txtDBName')
    txtUserName = request.POST.get('txtUserName')
    txtPassword = request.POST.get('txtPassword')
    # json_data = json.loads('')
    # manage_file_path = BASE_DIR + '\\manage.py'
    # model_file_path = BASE_DIR + '\\ferrp\\db_connections\\'+json_data['server'] + '_' + json_data['db_engine']  + '_' + json_data['database'] + '_' + json_data['username'] +'_models.py'
    database_id = get_db_connections(db_provider, txtHost, txtPort, txtDBName, txtUserName, txtPassword)
    connection = connections[database_id]
    # cursor = connection.cursor()
    tables = connection.introspection.table_names()
    connection_name = txtHost + '_' + txtPort + '_' + txtDBName + '_' + txtUserName
    result = {}
    result['tables'] = tables
    result['connection_name'] = connection_name
    connections_model_class = apps.get_model(app_label='db_connections', model_name='ConnectionsList')
    connection_list = connections_model_class()
    if tables:
        connection_list.connection_name = connection_name
        connection_list.database_host = txtHost
        connection_list.database_name = txtDBName
        connection_list.database_user = txtUserName
        connection_list.database_password = txtPassword
        connection_list.database_port = txtPort
        connection_list.engine_id = db_provider
        connection_list.save()

    # table_description = connection.introspection.get_table_description(cursor, tables[0])
    #table_name = tables[0]
    # for table in tables:
    #     spatial_column_name = is_spatial_table(connection, table)
    #     # print('Table Name: ' + table + ', Is_Spatial: ' + str(is_spatial) )
    #     if spatial_column_name != None:
    #         RemoteTableModel._meta.db_table = table
    #         RemoteTableModel.geom.db_column = spatial_column_name
    #         obj = RemoteTableModel.objects.all()[:1]
    #         print(obj)


    # seen_models = connection.introspection.installed_models(tables)
    # manage_file_path = os.path.join(BASE_DIR,"manage.py")
    # cmd = 'python "%s" inspectdb --database %s' %(manage_file_path, database)
    # output = execute_command_line(cmd)
    # command_to_execute = 'python "' + manage_file_path + '" inspectdb --database "test_ferrp" > "' + model_file_path + '"'
    # command_line_data = execute_command_line(command_to_execute)
    #
    return result

def get_spatial_and_key_column(conn, table):
    cursor = conn.cursor()
    table_description = conn.introspection.get_table_description(cursor, table)
    result = {}
    result['is_spatial'] = False
    result['id'] = None
    # with connection.schema_editor() as schema_editor:

    # for i in table_description:
    #     field_type=conn.introspection.get_field_type(table_description[i][1], table_description[i])
    for key in table_description:
        record = list(key)
        if record[1] in [16400]:
            result['geom_field'] = record[0]
            result['is_spatial'] = True
        # if record[0] == 'id' or record[0] == 'gid' or record[0] == 'fid':
        #     result['id'] = record[0]
        result['id'] = conn.introspection.get_primary_key_column(cursor, table)
    return result

def get_model_dict_array(rows):
    data_array = []
    for row in rows:
        row_dict = model_to_dict(row)
        data_array.append(row_dict)
    return data_array

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def execute_command_line(cmds):
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE, shell=True)
    data = ""
    for ln in proc.stdout:
        db_query = ln.decode("utf-8")
        data = data + db_query
    proc.kill()
    return data

def get_db_connections(db_provider, txtHost, txtPort, txtDBName, txtUserName, txtPassword):
    newDatabase = {}
    database_id = 'test_ferrp' #params['db_engine']
    settings.DATABASES[database_id] = {}

    # newDatabase['ENGINE'] = get_engine(params['db_engine'])
    # newDatabase['NAME'] = params['database']
    # newDatabase['USER'] = params['username']
    # newDatabase['PASSWORD'] = params['password']
    # newDatabase['HOST'] = params['server']
    # newDatabase['PORT'] = params['port']

    # newDatabase['ATOMIC_REQUESTS']: False
    # newDatabase['AUTOCOMMIT']: True
    # newDatabase['CONN_MAX_AGE']: 0
    # newDatabase['OPTIONS']: {}
    # newDatabase['TIME_ZONE']: None
    # newDatabase['TEST']: {'CHARSET': None, 'COLLATION': None, 'NAME': None, 'MIRROR': None}

    settings.DATABASES[database_id]['ENGINE'] = get_engine(db_provider)
    settings.DATABASES[database_id]['HOST'] = txtHost
    settings.DATABASES[database_id]['PORT'] = txtPort
    settings.DATABASES[database_id]['NAME'] = txtDBName
    settings.DATABASES[database_id]['USER'] = txtUserName
    settings.DATABASES[database_id]['PASSWORD'] = txtPassword


    # settings.DATABASES[database_id] = newDatabase
    return database_id

def get_engine(engine):
    if engine == '1':
        return 'django.contrib.gis.db.backends.postgis'
    elif engine == '2':
        return 'django.db.backends.mysql'
    elif engine == '3':
        return 'django.db.backends.sqlite3'
    elif engine == '4':
        return 'django.db.backends.oracle'
    else:
        return None

def get_insert_table_in_db(request):
    data = request.POST.get('data')
    json_data = json.loads(data)
    connection = connections['irrigation']
    queries = connection.queries
    for table in json_data:
        spatial_key_column = get_spatial_and_key_column(connection, table)
        GenericTableModel._meta.app_label = 'test_gis'
        GenericTableModel._meta.db_table = table
        if spatial_key_column['is_spatial'] == True:
            GenericTableModel.geom.db_column = spatial_key_column['geom_field']
            GenericTableModel.id.db_column = spatial_key_column['id']
            obj = GenericTableModel.objects.all()[:1]
            print(obj)
    print('abc')

