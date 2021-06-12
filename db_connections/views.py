from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from ferrp.db_connections.forms import Table_List_Form
from ferrp.db_connections.utils import *


def external_database_index(request, template=loader.get_template('db_connections.html')):
    return HttpResponse(template.render({}, request))

def databse_engines_list(self):
    engines_list = get_databse_engines_list()
    return HttpResponse(engines_list)

# @csrf_exempt
def insert_connection_in_db(request):
    result = get_insert_connection_in_db(request)
    table_list_form = Table_List_Form(result['tables'])
    return render(request, 'tables_list.html', context={'form':table_list_form})


@csrf_exempt
def insert_table_in_db(request):
    insert_tables = get_insert_table_in_db(request)
    return HttpResponse('')
