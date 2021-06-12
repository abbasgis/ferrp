import json
from django.db import connections
from django.forms import model_to_dict


def getQueryResultAsJson(strQuery, as_string = True):
    connection = connections['irrigation']
    cursor = connection.cursor()
    cursor.execute(strQuery)
    data = dictfetchall(cursor)
    if as_string == True:
        json_data = json.dumps(data, default=date_handler)
    else:
        json_data = data
    return json_data

def get_query_result_as_array(str_query):
    connection = connections['irrigation']
    cursor = connection.cursor()
    cursor.execute(str_query)
    data = dictfetchall(cursor)
    return data

def execute_query(str_query):
    connection = connections['irrigation']
    cursor = connection.cursor()
    try:
        cursor.execute(str_query)
        return True
    except SyntaxError:
        return False

def get_whereclause_from_filters(filters_array):
    length = len(filters_array)
    where_clause = ''
    index = 0
    for item in filters_array:
        single_clause = get_single_clause(item['property'], item['operator'], item['value'])
        if index == (length - 1):
            where_clause = where_clause + single_clause
        else:
            where_clause = where_clause + single_clause + ' and '
        index += 1
    return where_clause

def get_single_clause(property, oper, value):
    clause = ''
    if oper == 'like':
        clause = property + ' ' + oper + ' \'' + value + '%\' '
    else:
        # if validate_float(value) == True:
        #     clause = property + ' ' + get_operator_symbol(oper) + ' ' + str(value) + ' '
        # else:
        clause = property + ' ' + get_operator_symbol(oper) + ' \'' + str(value) + '\' '
    return clause

def validate_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_operator_symbol(oper):
    if oper == 'gt':
        return '>'
    elif oper == 'lt':
        return '<'
    else:
        return '='

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_model_dict_array(rows):
    data_array = []
    for row in rows:
        row_dict = model_to_dict(row)
        data_array.append(row_dict)
    return data_array
