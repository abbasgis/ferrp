import os
import subprocess
from django.contrib.gis.db import models
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import Polygon
from django.db import connections, migrations
from django.db.migrations import Migration
from django.db.migrations.state import ProjectState

from ferrp.layers.models import Info
from ferrp.local_settings import SPATIAL_DB, SPATIAL_EXTENT_3857, OVERVIEW_FACTOR
from ferrp.settings import DATABASES, SHAPEFILE_PATH
from ferrp.utils import Log_Error, DB_Query, Common_Utils


class Vector(models.Model):
    available_apps = ['dhaisl.layers']
    # con = connections['spatialds']
    oid = models.AutoField(primary_key=True)

    # geom = models.GeometryField(srid=0, null=True)

    class Meta:
        managed = False

    def __init__(self, shpParams):
        # self._meta.db_table = 'gis_' + shpParams['table_name']
        srid = shpParams['srs']['srid']
        geom = models.GeometryField(srid=srid, null=True)
        self.model_fields = []
        self.model_fields.append(("oid", models.AutoField(primary_key=True)))
        # for i in range(len(shpParams['fields'])):
        for field in shpParams['fields']:
            if field['field_name'] == "oid": continue
            self.model_fields.append((field['field_name'],
                                      self.getModelFieldType(field['field_type'], field['field_width'],
                                                             field['field_precision'])))
        self.model_fields.append(('geom', models.GeometryField(srid=srid, null=True)))

    def __setitem__(self, key, value):
        res = setattr(self, key, value)
        return res

    def __getitem__(self, key):
        res = getattr(self, key)
        return res

    def get_field(self, field_name):
        res = self[field_name]
        return res

        # def layer_mapping(self,ds,dataMapping):
        # lm = LayerMapping(self, ds, dataMapping)
        # lm.save(verbose=True)  # Save the layermap, imports t

    def cad_2_db(self, layer, lyrParams):
        table_name = lyrParams['table_name'].lower()
        srid = lyrParams['srs']['srid']
        orig_srid = lyrParams['srs']['orig_srid']
        iQ2 = ""
        table_names = {}
        for feat in layer:
            try:
                strFields = ""
                strValues = ""
                geom = feat.geom
                res_list = transform_geometry_and_check_inside_extent(geom, src_srid=lyrParams['srs']['orig_srid'],
                                                                      des_srid=lyrParams['srs']['srid'])
                if res_list is not None:
                    res = res_list[0]
                    geom_type = str(geom.geom_type)
                    if res['intersects'] == True:
                        if not geom_type in table_names.keys():
                            table_names[geom_type] = table_name + "_" + geom_type
                            self.set_up_model(table_names[geom_type])
                            table_names[geom_type] = "gis_" + table_names[geom_type]
                        for field in lyrParams['fields']:
                            name = field['field_name']
                            if name == "oid": continue
                            strFields += "\"" + name + "\","
                            val = Common_Utils.escape_special_chars_4_db(str(feat.get(name)))
                            # val = self.escapeChar(str(feat.get(name)))
                            strValues += "'" + val + "',"
                        try:
                            iQ2 = 'Insert into %s(%s "geom") values(%s CAST(\'%s\' As Geometry))' % (
                                table_names[geom_type], strFields, strValues, res['geom'])
                            DB_Query.execute_dml(iQ2)
                        except Exception as e:
                            print("Query:" + iQ2)
                            iQ2 = "Insert into %s(geom) values(CAST('%s' As Geometry))" \
                                  % (table_names[geom_type], res['geom'])
                            DB_Query.execute_dml(iQ2)
            except Exception as e:
                Log_Error.log_error_message(e)
        connections['spatialds'].commit()
        return table_names

    def shp_2_db(self, layer, lyrParams):
        # fields_name = shpParam['fields']['field_name']
        table_name = lyrParams['table_name'].lower()
        srid = lyrParams['srs']['srid']
        orig_srid = lyrParams['srs']['orig_srid']
        iQ2 = ""
        for feat in layer:
            try:
                strFields = ""
                strValues = ""
                geom = feat.geom
                res_list = transform_geometry_and_check_inside_extent(geom, src_srid=lyrParams['srs']['orig_srid'],
                                                                      des_srid=lyrParams['srs']['srid'])
                if res_list is not None:
                    res = res_list[0]
                    if res['intersects'] == True:
                        for field in lyrParams['fields']:
                            name = field['field_name']
                            if name == "oid": continue
                            strFields += "\"" + name + "\","
                            val = Common_Utils.escape_special_chars_4_db(str(feat.get(name)))
                            # val = self.escapeChar(str(feat.get(name)))
                            strValues += "'" + val + "',"
                        final_table_name = table_name
                        try:
                            iQ2 = 'Insert into %s(%s "geom") values(%s CAST(\'%s\' As Geometry))' % (
                                final_table_name, strFields, strValues, res['geom'])
                            DB_Query.execute_dml(iQ2)
                        except Exception as e:
                            print("Query:" + iQ2)
                            iQ2 = "Insert into %s(geom) values(CAST('%s' As Geometry))" \
                                  % (final_table_name, res['geom'])
                            DB_Query.execute_dml(iQ2)
            except Exception as e:
                Log_Error.log_error_message(e)
        connections['spatialds'].commit()
        # return final_table_name

    def escapeChar(self, str):
        return str.replace('"', '\\"').replace("'", "\\'")

    def set_up_model(self, table_name):
        try:
            operations = [
                # migrations.DeleteModel('gis_'+table_name),
                migrations.CreateModel(table_name, self.model_fields),
            ]
            mig_op_res = self.apply_operations('gis', ProjectState(), operations)
        except:
            return -1;

    def apply_operations(self, app_label, project_state, operations):
        migration = Migration('name', app_label)
        migration.operations = operations
        with connections['spatialds'].schema_editor() as editor:
            self.current_state = migration.apply(project_state, editor)
            # return migration.get_model()

    def getModelFieldType(self, field_type, width, precision):
        ft = {
            "OFTBinary": lambda: models.BooleanField(null=True, blank=True),
            "OFTDate": lambda: models.DateField(null=True, blank=True),
            "OFTTime": lambda: models.TimeField(null=True, blank=True),
            "OFTDateTime": lambda: models.DateTimeField(null=True, blank=True),  # (auto_now_add=True)
            "OFTInteger": lambda: models.IntegerField(null=True, blank=True),  # default=0
            "OFTInteger64": lambda: models.BigIntegerField(null=True, blank=True),
            "OFTReal": lambda: models.FloatField(null=True, blank=True),
            "OFTString": lambda: models.CharField(max_length=width, null=True,
                                                  blank=True) if width > 0 else models.TextField(null=True,
                                                                                                 blank=True),
            "OFTWideString": lambda: models.CharField(max_length=width) if width > 0 else models.TextField(
                null=True, blank=True),
        }
        # FIELD_TYPES = {
        #     models.AutoField: OFTInteger,
        #     models.IntegerField: (OFTInteger, OFTReal, OFTString),
        #     models.FloatField: (OFTInteger, OFTReal),
        #     models.DateField: OFTDate,
        #     models.DateTimeField: OFTDateTime,
        #     models.EmailField: OFTString,
        #     models.TimeField: OFTTime,
        #     models.DecimalField: (OFTInteger, OFTReal),
        #     models.CharField: OFTString,
        #     models.SlugField: OFTString,
        #     models.TextField: OFTString,
        #     models.URLField: OFTString,
        #     USStateField: OFTString,
        #     models.BigIntegerField: (OFTInteger, OFTReal, OFTString),
        #     models.SmallIntegerField: (OFTInteger, OFTReal, OFTString),
        #     models.PositiveSmallIntegerField: (OFTInteger, OFTReal, OFTString),
        # }
        model_field = ft[field_type]()
        return model_field


def arz_add_srs_entry(srs, auth_name='EPSG', auth_srid=None, ref_sys_name=None,
                      database=None, proj4=None, wkt=None):
    """
    This function takes a GDAL SpatialReference system and adds its information
    to the `spatial_ref_sys` table of the spatial backend.  Doing this enables
    database-level spatial transformations for the backend.  Thus, this utility
    is useful for adding spatial reference systems not included by default with
    the backend:

    # >>> from django.contrib.gis.utils import add_srs_entry
    # >>> add_srs_entry(3857)

    Keyword Arguments:
     auth_name:
       This keyword may be customized with the value of the `auth_name` field.
       Defaults to 'EPSG'.

     auth_srid:
       This keyword may be customized with the value of the `auth_srid` field.
       Defaults to the SRID determined by GDAL.

     ref_sys_name:
       For SpatiaLite users only, sets the value of the `ref_sys_name` field.
       Defaults to the name determined by GDAL.

     database:
      The name of the database connection to use; the default is the value
      of `django.db.DEFAULT_DB_ALIAS` (at the time of this writing, its value
      is 'default').
    """
    # If argument is not a `SpatialReference` instance, use it as parameter
    # to construct a `SpatialReference` instance.
    if not isinstance(srs, SpatialReference):
        srs = SpatialReference(srs)

    # if srs.srid is None:
    #     raise Exception('Spatial reference requires an SRID to be '
    #                     'compatible with the spatial backend.')

    # Initializing the keyword arguments dictionary for both PostGIS
    # and SpatiaLite.
    kwargs = {'srid': auth_srid or srs.srid,
              'auth_name': auth_name,
              'auth_srid': auth_srid or srs.srid,
              'proj4text': proj4 or srs.proj4,
              }

    if not database:
        database = SPATIAL_DB
    connection = connections[database]

    SpatialRefSys = arz_get_srs_model(connection)
    # Backend-specific fields for the SpatialRefSys model.
    srs_field_names = {f.name for f in SpatialRefSys._meta.get_fields()}
    if 'srtext' in srs_field_names:
        kwargs['srtext'] = wkt or srs.wkt
    if 'ref_sys_name' in srs_field_names:
        # SpatiaLite specific
        kwargs['ref_sys_name'] = ref_sys_name or srs.name

    # Creating the spatial_ref_sys model.
    try:
        # Try getting via SRID only, because using all kwargs may
        # differ from exact wkt/proj in database.
        SpatialRefSys.objects.using(database).get(srid=auth_srid or srs.srid)
    except SpatialRefSys.DoesNotExist:
        SpatialRefSys.objects.using(database).create(**kwargs)


def arz_get_srs_model(connection):
    if not hasattr(connection.ops, 'spatial_version'):
        raise Exception('The `add_srs_entry` utility only works '
                        'with spatial backends.')
    if not connection.features.supports_add_srs_entry:
        raise Exception('This utility does not support your database backend.')
    SpatialRefSys = connection.ops.spatial_ref_sys()
    return SpatialRefSys


def transform_geometry_and_check_inside_extent(geom, src_srid, des_srid=None):
    try:
        if not isinstance(geom, str):
            wkt = geom.wkt
        else:
            wkt = geom

        query = "Select st_transform(st_force2D(st_geomfromtext('" + wkt + "'," + str(
            src_srid) + "))," + str(des_srid) + ")"
        trans_geom = DB_Query.execute_query_as_one(query)
        polygon = Polygon().from_bbox(SPATIAL_EXTENT_3857)
        polygon.srid = des_srid
        query = "Select CAST('%s' AS Geometry) geom, st_dimension(CAST('%s' AS Geometry)) dim , " \
                "st_contains(st_geomfromtext('%s'), CAST('%s' AS Geometry)) intersects" % (
                    trans_geom, trans_geom, polygon, trans_geom)
        res = DB_Query.execute_query_as_dict(query)
        return res
    except Exception as e:
        Log_Error.log_error_message(e)


def transform_geometry(geom, src_srid, des_srid=None, response_asText=True):
    try:
        if not isinstance(geom, str):
            wkt = geom.wkt
        else:
            wkt = geom
        if response_asText == False:
            query = "Select st_transform(st_force2D(st_geomfromtext('" + wkt + "'," + str(
                src_srid) + "))," + str(des_srid) + ")"
        else:
            query = "Select st_astext(st_transform(st_force2D(st_geomfromtext('" + wkt + "'," + str(
                src_srid) + "))," + str(des_srid) + ")) geom"
        cursor = connections['spatialds'].cursor()
        cursor.execute(query);
        row = cursor.fetchone()
        return row[0]

    except:
        return None


def set_layer_or_table_name(layer_name, layer_type=None):
    layer_name = str.lower(layer_name)
    layer_name = layer_name.replace("-", "_").replace(" ", "_")
    # layer_type = str.lower(layer_type)
    if layer_type != None:
        layer_type = str.lower(layer_type)
        if str.lower(layer_type) == "raster":
            layer_name = "rst_" + layer_name
        elif str.lower(layer_type) in ["vector", "shp"]:
            layer_name = layer_name
        elif str.lower(layer_type) == "cad":
            layer_name = "cad_" + layer_name
    return layer_name


def drop_spatial_table(layer_info):
    tokens = layer_info.table_name.split("_")
    token = tokens[len(tokens)-1]
    if token == "vw":
        drop_cmd = "DROP VIEW " + layer_info.table_name
    else:
        drop_cmd = "DROP TABLE " + layer_info.table_name
    connection = connections[SPATIAL_DB]
    with connection.cursor() as cursor:
        try:
            cursor.execute(drop_cmd)
        except Exception as e:
            print(e)
    layer_info.delete()
    # Info.delete_layer_info(layer_info.layer_name)
    return True


def drop_raster_tables(layer_info):
    list_table_names = raster_table_list_with_overview(layer_info.table_name)

    for tab_name in list_table_names:
        drop_cmd = "DROP TABLE " + tab_name
        connection = connections[SPATIAL_DB]
        with connection.cursor() as cursor:
            try:
                cursor.execute(drop_cmd)
            except Exception as e:
                print(e)
    # obj = Info.objects.filter(layer_name=layer_info.layer_name)
    layer_info.delete()

    return True


def raster_table_list_with_overview(table_name):
    list_table_names = [table_name];
    for fact in OVERVIEW_FACTOR:
        list_table_names.append("o_%s_%s" % (fact, table_name))
    return list_table_names;


def get_table_schema(table_name):
    query = "select column_name, data_type, character_maximum_length " \
            "from INFORMATION_SCHEMA.COLUMNS where table_name = '" + table_name + "'";
    connection = connections[SPATIAL_DB]
    with connection.cursor() as cursor:
        cursor.execute(query)
        return DB_Query.dictfetchall(cursor)


def convert_vector_layer_to_shp(layer_info):
    connection_name = DB_Query.get_connection_name(layer_info.app_label)
    database_params = DATABASES[connection_name]
    output_file_path = os.path.join(SHAPEFILE_PATH, layer_info.layer_name)
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)
    output_file_path_name = os.path.join(output_file_path,layer_info.table_name)
    output_file_path_name = output_file_path_name+".shp"
    cmds = 'pgsql2shp -f "%s" -h %s -p %s -u %s -P %s -g geom %s %s' % (output_file_path_name, database_params['HOST'],
                                                                      database_params['PORT'], database_params['USER'],
                                                                      database_params['PASSWORD'],
                                                                      database_params['NAME'], layer_info.table_name)
    execute_command_line(cmds,is_import_to_db=False)
    return output_file_path_name


def create_raster_table_from_files(file_path, raster_name, file_Ext,raster_srid):
    of = ','.join(OVERVIEW_FACTOR)
    table_name = set_layer_or_table_name(raster_name, 'raster').lower()
    table_name = Common_Utils.add_timestamp_to_string(table_name)
    file_path_name = os.path.join(file_path, "*" + file_Ext).lower()
    cmds = 'raster2pgsql -s %s -l %s -d -t 100x100 -C -x -r -e -p  %s %s' % (raster_srid, of, file_path_name, table_name)
    # cmds = 'raster2pgsql -d -t 500x500 -C -x -r -e -p  "%s" %s' % (file_path_name, table_name)
    execute_command_line(cmds)
    # create_extent_column_in_raster_table(table_name)
    return table_name


def save_raster_in_db(file_path_name, table_name, raster_srid):
    of = ','.join(OVERVIEW_FACTOR)
    cmds = 'raster2pgsql -s %s -l %s -a -t 500x500 -e  "%s" %s' % (raster_srid, of, file_path_name.lower(), table_name.lower())  # -C -x -r
    execute_command_line(cmds)
    return table_name


def create_extent_column_in_raster_table(table_name):
    connection = connections[SPATIAL_DB]
    with connection.cursor() as cursor:
        list_table_names = raster_table_list_with_overview(table_name)
        for tab_name in list_table_names:
            try:
                create_column = 'ALTER TABLE "%s" ADD COLUMN envelope geometry' % tab_name
                cursor.execute(create_column)  # add column to table

                update_envelope = 'Update "%s" set envelope =st_envelope(rast)' % tab_name
                cursor.execute(update_envelope)

            except Exception as e:
                print("error in creating extent column of " + tab_name + " \n Error:" + e.args[0])


def execute_command_line(cmds, is_import_to_db=True):
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE, shell=True)  # , stdout=writer
    if is_import_to_db==True:
        con = connections[SPATIAL_DB]
        cursor = con.cursor()
        data = ""
        for ln in proc.stdout:
            ras_query = ln.decode("utf-8")
            data = data + ras_query
            cursor.execute(ras_query)

        cursor.close()
        con.close()

    else:
        # proc.wait()
        for ln in proc.stdout:
            print(ln.decode("utf-8")+"\n")
        # print ("Code:"+ str(proc.returncode))

    proc.kill()