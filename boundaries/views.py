import json

from django.db import connection
from django.http import HttpResponse
from django.template import loader

# from boundaries.admin_tree.models import TblAdminHierarchy


def bounaries_browser(request):
    code = request.GET.get('code')
    list_admin_name = ()
    if code == "irb":
        list_admin_name = ('province', 'irrigation_zone', 'irrigation_circle', 'irrigation_division')
    elif code == "bor":
        list_admin_name = ('province','division', 'district', 'tehsil', 'quanghoi', 'patwar_circle', 'mauza')
    elif code == "adb":
        list_admin_name = ('province', 'division', 'district', 'tehsil', 'union_council')
    elif code == "lg":
        list_admin_name = ('province', 'division', 'district', 'district_council', 'municipal_council')
    sql = "select id, parent_id as parentid,concat(admin_name,'(',admin_level_name,')') as text,extent_boundary as value " \
          "from tbl_admin_hierarchy where admin_level_name in" + str(list_admin_name)+" ORDER BY admin_level_name"
    json = getJSONFromDB(sql)
    return HttpResponse(json)



def getJSONFromDB(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    data = dictfetchall(cursor)
    data_json = json.dumps(data, default=date_handler)
    return data_json


def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]



# def get_hierarchy_page(request, template=loader.get_template('hierarchy.html')):
#     # sql = "select id, parent_id as parentid,concat(admin_name,'-',admin_level_name) as text,extent_boundary as value from tbl_admin_hierarchy ORDER BY admin_name"
#     # json = getJSONFromDB(sql)
#     return HttpResponse(template.render({}, request))


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)
