import base64
import json

import zlib

from ferrp.survey_stats_app.utils import getQueryResultAsJson, date_handler

def get_admin_hierarchy_json():
    str_district_query = 'select district_id, district_name, extent from district ORDER by district_name;'
    district_resultset = getQueryResultAsJson(str_district_query, False)
    str_ext_hierarchy = '[{\
                            text: "All Districts",\
                            code: "punjab", \
                            extent: "68.637405,27.649300,75.411542,33.205432", \
                            handler: Ext.bind(me.onItemClick, this, me, true) \
                        },'
    for dist_row in district_resultset:
        district_id = dist_row['district_id']
        district_name = dist_row['district_name']
        district_extent = dist_row['extent']
        str_tehsil_query = 'select tehsil_id, tehsil_name, extent from tehsil WHERE district_id = '+str(district_id)+' order by tehsil_name;'
        str_ext_hierarchy = str_ext_hierarchy + '{\
                                text: "' + district_name + '", ' \
                                'code: "district_' + str(district_id) + '", ' \
                                'extent: "' + parse_extent(district_extent) + '", ' \
                                'handler: Ext.bind(me.onItemClick, this, me, true),' \
                                'menu:{' \
                                    'items:['
        tehsil_resultset = getQueryResultAsJson(str_tehsil_query, False)
        str_ext_hierarchy = str_ext_hierarchy + '{\
                                text: "All Tehsils",\
                                code: "district_, '+ str(district_id)+ '",  \
                                extent: "'+ parse_extent(district_extent)+ '",  \
                                handler: Ext.bind(me.onItemClick, this, me, true) \
                            },'
        for teh_row in tehsil_resultset:
            tehsil_id = teh_row['tehsil_id']
            tehsil_name = teh_row['tehsil_name']
            tehsil_extent = teh_row['extent']
            str_ext_hierarchy = str_ext_hierarchy + '{\
                                        text: "' + tehsil_name + '", ' \
                                        'code: "tehsil_' + str(tehsil_id) + '", ' \
                                        'extent: "' + parse_extent(tehsil_extent )+ '", ' \
                                        'handler: Ext.bind(me.onItemClick, this, me, true),' \
                                        'menu:{' \
                                            'items:['
            str_qanungoi_halqa_query = 'select qanungoi_halqa_id, qanungoi_halqa_name, extent from qanungoi_halqa WHERE tehsil_id = '+str(tehsil_id)+' order by qanungoi_halqa_name;'
            qanungoi_halqa_resultset = getQueryResultAsJson(str_qanungoi_halqa_query, False)
            str_ext_hierarchy = str_ext_hierarchy + '{\
                                    text: "All Qanungoi Halqas",\
                                    code: "tehsil_, '+ str(tehsil_id)+ '",  \
                                    extent: "' + parse_extent(tehsil_extent) + '",  \
                                    handler: Ext.bind(me.onItemClick, this, me, true) \
                                },'
            for qanungoi_halqa_row in qanungoi_halqa_resultset:
                qanungoi_halqa_id = qanungoi_halqa_row['qanungoi_halqa_id']
                qanungoi_halqa_name = qanungoi_halqa_row['qanungoi_halqa_name']
                qanungoi_halqa_extent = qanungoi_halqa_row['extent']
                str_ext_hierarchy = str_ext_hierarchy + '{\
                                    text: "' + qanungoi_halqa_name + '", ' \
                                    'code: "qanungoi_' + str(qanungoi_halqa_id) + '", ' \
                                    'extent: "' + parse_extent(qanungoi_halqa_extent) + '", ' \
                                    'handler: Ext.bind(me.onItemClick, this, me, true),' \
                                    'menu:{' \
                                        'items:['
                str_patwar_circle_query = 'select patwar_circle_id, patwar_circle_name, extent from patwar_circle WHERE qanungoi_halqa_id = '+str(qanungoi_halqa_id)+' order by patwar_circle_name;'
                patwar_circle_resultset = getQueryResultAsJson(str_patwar_circle_query, False)
                str_ext_hierarchy = str_ext_hierarchy + '{\
                                    text: "All Patwar Circles",\
                                    code: "qanungoi_, '+ str(qanungoi_halqa_id)+ '",  \
                                    extent: "'+ parse_extent(qanungoi_halqa_extent) + '",  \
                                    handler: Ext.bind(me.onItemClick, this, me, true) \
                                },'
                for patwar_circle_row in patwar_circle_resultset:
                    patwar_circle_id = patwar_circle_row['patwar_circle_id']
                    patwar_circle_name = patwar_circle_row['patwar_circle_name']
                    patwar_circle_extent = patwar_circle_row['extent']
                    str_ext_hierarchy = str_ext_hierarchy + '{\
                                         text: "' + patwar_circle_name.replace('"', '') + '", ' \
                                         'code: "patwar_' + str(patwar_circle_id) + '", ' \
                                         'extent: "' + parse_extent(patwar_circle_extent) + '", ' \
                                         'handler: Ext.bind(me.onItemClick, this, me, true),' \
                                         'menu:{' \
                                             'items:['
                    str_mauza_query = 'select mauza_id, mauza_name, extent from mauza where patwar_circle_id = \'' + str(patwar_circle_id) + '\';'
                    mauza_resultset = getQueryResultAsJson(str_mauza_query, False)
                    str_ext_hierarchy = str_ext_hierarchy + '{\
                                            text: "All Mauzas",\
                                            code: "patwar_, '+ str(patwar_circle_id)+ '",  \
                                            extent: "' + parse_extent(patwar_circle_extent) + '",  \
                                            handler: Ext.bind(me.onItemClick, this, me, true) \
                                        },'
                    for mauza_row in mauza_resultset:
                        mauza_id = mauza_row['mauza_id']
                        mauza_name = mauza_row['mauza_name']
                        mauza_extent = mauza_row['extent']
                        str_ext_hierarchy = str_ext_hierarchy + '{\
                                            text: "' + mauza_name.replace('"', '') + '", ' \
                                            'code: "mauza_' + str(mauza_id) + '", ' \
                                            'extent: "' + parse_extent(mauza_extent) + '", ' \
                                            'handler: Ext.bind(me.onItemClick, this, me, true),'
                        str_ext_hierarchy = str_ext_hierarchy + '},'
                    str_ext_hierarchy = str_ext_hierarchy + ']},'
                    str_ext_hierarchy = str_ext_hierarchy + '},'
                str_ext_hierarchy = str_ext_hierarchy + ']},'
                str_ext_hierarchy = str_ext_hierarchy + '},'
            str_ext_hierarchy = str_ext_hierarchy + ']},'
            str_ext_hierarchy = str_ext_hierarchy + '},'
        str_ext_hierarchy = str_ext_hierarchy + ']},'
        str_ext_hierarchy = str_ext_hierarchy + '},'
    str_ext_hierarchy = str_ext_hierarchy + ']'
    hierarchy_json = json.dumps(str_ext_hierarchy, default=date_handler)
    # compressed_json = base64.b64encode(zlib.compress(str.encode(hierarchy_json), 9))
    return str_ext_hierarchy

def parse_extent(extent):
    if extent:
        return extent
    else:
        return ''
