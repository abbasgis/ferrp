import os

import datetime
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.db import connections

from ferrp.layers.forms import FieldSet, LayerViewForm
from ferrp.layers.gis_migration import set_layer_or_table_name, Vector, raster_table_list_with_overview
from ferrp.layers.models import Projection, Info, Raster_Info
from ferrp.local_settings import SPATIAL_DB
from ferrp.models import Items_Permission
from ferrp.settings import SHAPEFILE_PATH
from ferrp.utils import DB_Query


def info_layer_context(layer_params, layer_type="Vector"):
    form = LayerViewForm()
    table_name_token = layer_params['table_name'].split("_")
    title = ''
    for i in range(0, len(table_name_token) - 1):
        title = title + table_name_token[i] + "_"
    title = title[:-1]
    form.fields['title'].initial = title
    form.fields['file_name'].initial = layer_params['file_name']
    form.fields['layer_name'].initial = layer_params['table_name']

    form.fields['layer_type'].initial = layer_type
    form.fields['geometry_type'].initial = layer_params['geomtype']
    form.fields['created_at'].initial = datetime.datetime.now().strftime("%Y-%m-%d")
    form.fields['SRS'].initial = layer_params['srs']['wkt']
    form.fields['SRID'].initial = layer_params['srs']['srid']
    form.fields['MinX'].initial = layer_params['envelop'][0]
    form.fields['MinY'].initial = layer_params['envelop'][1]
    form.fields['MaxX'].initial = layer_params['envelop'][2]
    form.fields['MaxY'].initial = layer_params['envelop'][3]
    fieldsets = (FieldSet(form, ('title', 'file_name', 'layer_name', 'layer_type', 'geometry_type', 'created_at'),
                          legend='General',
                          cls="fieldset"),
                 FieldSet(form, ('SRS', 'SRID'), legend='Spatial Reference System', cls="fieldset"),

                 FieldSet(form, ('MinX', 'MinY', 'MaxX', 'MaxY'),
                          legend="Envelope",
                          cls="fieldset"))
    context = {'form_layer_view': form,
               'fieldsets': fieldsets, 'isExisting': 1,
               'fields': layer_params['fields']}
    return context


def read_shapefile(file_name):
    file_path = os.path.join(SHAPEFILE_PATH, file_name)
    file_path_name = os.path.join(file_path, file_name + ".shp")
    ds = DataSource(file_path_name)
    # ds = DataSource('uploaded/shp/' + filename)
    # ds =DataSource('uploaded/shp/PH-II_Road_Line_20171229173425720314.shp')
    layer = ds[0]
    shpParam = read_layer_parameters(layer, "shp")
    shpParam['file_name'] = file_name
    return shpParam


def read_layer_parameters(layer, layer_type, layer_name=None):
    dict = {}
    if layer_name is None: layer_name = layer.name
    dict['table_name'] = set_layer_or_table_name(layer_name, layer_type)
    dict['fields'] = layerFieldsDetails(layer)
    dict['geomtype'] = layer.geom_type.name
    dict['srs'] = layerSRSDetails(layer)
    dict['envelop'] = layer.extent.tuple
    return dict


def layerFieldsDetails(layer):
    fields_name = layer.fields
    fields_type = [fld.__name__ for fld in layer.field_types]
    fields_width = layer.field_widths
    fields_precision = layer.field_precisions
    fields = [];
    for i in range(len(fields_name)):
        info = {}

        info['field_name'] = fields_name[i]
        info['field_type'] = fields_type[i]
        info['field_width'] = fields_width[i]
        info['field_precision'] = fields_precision[i]
        fields.append(info)
    return fields


def layerSRSDetails(layer):
    res = getSRIDFromAOI(layer.extent.wkt)
    if res is None:
        srs = layer.srs.wkt
        srid = layer.srs.srid
        res = {'wkt': srs, 'srid': srid}
    return res


def getSRIDFromAOI(extentwkt):
    poly = GEOSGeometry(extentwkt)
    rs = Projection.objects.filter(extent__intersects=poly)
    if rs.exists():
        res = {'wkt': rs[0].srs, 'srid': rs[0].srid}
    else:
        res = {'wkt': "Unknown", 'srid': 0}
    return res


def read_shapefile_from_layer(layer, srid=None, srs=None):
    dict = {}
    dict['table_name'] = layer.name
    dict['fields'] = layer_fields_details(layer)
    dict['geomtype'] = layer.geom_type.name
    dict['srs'] = layerSRSDetails(layer)
    dict['envelop'] = layer.extent.tuple
    return dict


def layer_fields_details(layer):
    fields_name = layer.fields
    fields_type = [fld.__name__ for fld in layer.field_types]
    fields_width = layer.field_widths
    fields_precision = layer.field_precisions
    fields = [];
    for i in range(len(fields_name)):
        info = {}
        info['field_name'] = fields_name[i]
        info['field_type'] = fields_type[i]
        info['field_width'] = fields_width[i]
        info['field_precision'] = fields_precision[i]
        fields.append(info)
    return fields


def importShapefile(file_path_name, table_name, srid, srs):
    ds = DataSource(file_path_name)
    layer = ds[0]
    table_name = table_name.lower()
    shpParams = read_shapefile_from_layer(layer, srid, srs)
    # shpParams['file_name'] = filename
    shpParams['table_name'] = 'gis_' + table_name
    # shpParams['srs']['srid'] = srid
    shpParams['srs'] = {'srs': srs, 'srid': 3857, 'orig_srid': srid}
    # if not srid in ['0', '3857', '4326']:
    #     rows = Projection.objects.filter(srid='3857')
    #     if rows.exists():
    #         row = rows[0]
    #         shpParams['srs'] = {'srs': row.srs, 'srid': row.srid, 'orig_srid': srid}

    vector = Vector(shpParams)  # fields,fields_type

    result = vector.set_up_model(table_name)
    if result != -1:
        vector.shp_2_db(layer, shpParams)
    return {'table_name': shpParams['table_name'], 'srs': shpParams['srs']['srid'],
            'geomtype': shpParams['geomtype'].lower()}




def create_raster_info(table_name, file_name_path, user):
    connection = connections[SPATIAL_DB]
    with connection.cursor() as cursor:
        srid_query = "Select st_srid(rast) from " + table_name
        cursor.execute(srid_query)
        srid = str(cursor.fetchone()[0])
        extent_query = "Select st_extent(envelope) from " + table_name
        cursor.execute(extent_query)
        extent = str(cursor.fetchone()[0])
    layer_name = table_name
    # title = layer_name.rsplit('_', 1)[0][4:]  # [0]
    layer_name_parts = layer_name.split('_');
    title = ""
    for i in range(1,len(layer_name_parts)-1):
        title = title + layer_name_parts[i]+" "
    title  = title[:len(title)-1]
    # title = layer_name.replace("_", " ")[4:]
    created_at = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    layer_info = Info.insert_into_layer_info(layer_name=layer_name, title=title, table_name=table_name,
                                             layer_type="Raster", orig_extent=extent, file_path_name=file_name_path, user=user,
                                             srid=srid,
                                             created_at=created_at)

    insert_into_raster_info(layer_info, table_name)
    return layer_name

def insert_into_raster_info(layer_info, table_name):
    srid = layer_info.srid
    list_table_names = raster_table_list_with_overview(table_name)
    for tab_name in list_table_names:
        if srid == 3857:
            query = 'SELECT max(st_numbands(rast)) As num_bands, max(ST_PixelWidth(rast)) As pixwidth, max(ST_PixelHeight(rast)) As pixheight ' \
                    'from "%s"' % (tab_name)
        else:
            query = 'SELECT max(st_numbands(rast)) As num_bands, max(ST_PixelWidth(st_transform(rast, 3857))) As pixwidth, max(ST_PixelHeight(st_transform(rast, 3857))) As pixheight ' \
                    'from "%s"' % (tab_name)

        res = DB_Query.execute_query_as_dict(query)
        pixeltype_query = 'Select Distinct(ST_BandPixelType(rast)) from %s' % tab_name
        pixeltype = DB_Query.execute_query_as_one(pixeltype_query)
        ras_info = Raster_Info(Info_id=layer_info, table_name=tab_name, main_table_name=table_name,
                               res_x=res[0]['pixwidth'], res_y=res[0]['pixheight'], num_bands=res[0]['num_bands'],
                               pixel_type=pixeltype)
        ras_info.save()
