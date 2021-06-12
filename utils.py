import base64
import datetime
import json
import os
import io

import logging
import re
import traceback
import zipfile

from urllib.parse import quote
from django.core.mail import EmailMultiAlternatives
import urllib.request as urllib2

import PyPDF2
from PIL.Image import Image
from django.apps import apps
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import Extent
from django.contrib.gis.geos import GEOSGeometry
from django.db import connections, connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import resolve

from ferrp import settings
from ferrp.integration.models import DatabaseConnections

from ferrp.local_settings import *
from ferrp.models import Items_Permission
from ferrp.settings import THUMBNAILS_PATH, THUMBNAILS_URL


class Common_Utils():
    @classmethod
    def check_if_email_exist(cls, user):
        # user = request.user
        res = False
        message = "Email address is not available, Please provide your email before further processing"
        # user_name = user.username
        # user_obj = User.objects.get(user_name=user_name)
        user_email = user.email
        if not (user_email is None or user_email == ''):
            res = True
            message = user_email
        return {"status": res, "msg": message}

    @classmethod
    def test_column_exist(cls, table_name, column_name):
        test_query = "SELECT column_name FROM information_schema.columns " \
                     "WHERE table_name='%s' and " \
                     "column_name='%s'" % (table_name, column_name)
        result = DB_Query.execute_query_as_one(query=test_query)
        return result

    @classmethod
    def bad_request(message):
        response = HttpResponse(json.dumps({'message': message}),
                                content_type='application/json')
        response.status_code = 400
        return response

    @classmethod
    def get_info_item_content_type(cls, app_label, info_name):
        item_type = None
        item_type_list = list(
            ContentType.objects.filter(app_label=app_label, model=info_name).values_list('id', flat=True))
        if len(item_type_list) > 0:
            item_type = item_type_list[0]
        return item_type

    @classmethod
    def save_icon(cls, image, img_name):
        if not os.path.exists(THUMBNAILS_PATH):
            os.makedirs(THUMBNAILS_PATH)
            os.chmod(THUMBNAILS_PATH, 0o755)
        img_path_name = os.path.join(THUMBNAILS_PATH, img_name + '.png')
        icon_url = os.path.join(THUMBNAILS_URL, img_name + '.png')

        img_b64 = image.split(',')[1]
        img = base64.b64decode(img_b64)
        # handle_uploaded_file()
        Common_Utils.wirte_to_new_file(img_path_name, img)
        return icon_url

    @classmethod
    def pdf_page_to_png(pdf_path_name, pagenum=0, resolution=72, ):
        """
        Returns specified PDF page as wand.image.Image png.
        :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
        :param int pagenum: Page number to take.
        :param int resolution: Resolution for resulting png in DPI.
        """
        # file = open(pdf_path_name, "r", encoding="utf-8")
        file = open(pdf_path_name)
        src_pdf = PyPDF2.PdfFileReader(file)
        dst_pdf = PyPDF2.PdfFileWriter()
        dst_pdf.addPage(src_pdf.getPage(pagenum))

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=resolution)
        img.convert("png")

        return img

    @classmethod
    def convert_file_name_2_title(cls, file_name):
        title = file_name
        special_char = ['_', '-']
        for char in special_char:
            title = title.replace(char, ' ')
        return title

    @classmethod
    def get_app_label(self, raw_uri):
        view_func = resolve(raw_uri)[0]
        app_label = view_func.__module__.rsplit('.', 1)[1]
        view_name = view_func.__name__
        return app_label

    @classmethod
    def zip_files(self, zip_subdir, filenames):
        # The zip compressor
        s = io.BytesIO()
        zf = zipfile.ZipFile(s, "w")

        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            # Add file, at correct path
            zf.write(fpath, zip_path)
            # Must close zip for all contents to be written
        zf.close()
        return s

    @classmethod
    def add_timestamp_to_string(self, str):
        dt_val = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # remove_char= ['-',' ',':','.']
        # for c in remove_char:
        #     dt_val = dt_val.replace(c,' ')
        str = str.replace(" ", "_") + "_" + dt_val;
        return str

    @classmethod
    def handle_uploaded_file(self, f, file_path_name=None):
        if file_path_name is None: file_path_name = f.name.replace(" ", "_")

        with open(file_path_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        os.chmod(file_path_name, 0o755)

    @classmethod
    def wirte_to_new_file(self, file_path_name, content):
        try:
            os.remove(file_path_name)
        except OSError:
            pass
        with open(file_path_name, 'wb+') as destination:
            destination.write(content)

    @classmethod
    def escape_special_chars_4_db(self, text):
        text = text.replace("'", "''")
        return text;

    @classmethod
    def prepare_relation_name_4_db(cls, text):
        text = text.replace("'", " ")
        text = text.replace("'", "")
        text = text.replace("@", "")
        text = text.replace('"', "")
        text = text.replace(" ", "_")
        text = text.lower()
        return text

    @classmethod
    def get_geom_extent(cls, table_name, layer_type="Vector"):
        query = None
        if layer_type == "Vector":
            query = "Select st_extent(geom) from %s" % table_name
        elif layer_type == "Raster":
            query = "Select st_extent(envelope) from %s" % table_name
        if query is not None:
            res = DB_Query.execute_query_as_one(query)

            res = res.replace(" ", ",")[4:len(res) - 1]
        else:
            res = None
        return res

    @classmethod
    def str_2_bool(cls, val):
        return val.lower() in ("yes", "true", "t", "1")

    @classmethod
    def get_raster_paramenters(cls, table_name):
        query = "SELECT ST_PixelWidth(rast) As pixwidth, ST_PixelHeight(rast) As pixheight, " \
                "ST_NumBands(rast) As numbands, ST_BandPixelType(rast,1) As ptype from %s limit 1" % table_name
        res = DB_Query.execute_query_as_dict(query)[0]

    @classmethod
    def send_sms(self, contact_no, msg_body):
        try:
            quoted_text = quote(msg_body)
            sms_url = 'http://api.bizsms.pk/api-send-branded-sms.aspx?username=pnd@bizsms.pk&pass=p5890hg99&text=' + \
                      quoted_text + '&masking=P&DD-FERRP&destinationnum=' + contact_no + '&language=English'
            response = urllib2.urlopen(sms_url)
            html = response.msg
            if html == 'OK':
                return 'SMS sent!'
            else:
                return 'SMS not sent!'
        except Exception as e:
            return e

    # msg body accepts plain text and html also
    @classmethod
    def send_email(self, email_id, subject, msg_body):
        try:
            msg = EmailMultiAlternatives(subject, msg_body, None, [email_id])
            msg.attach_alternative(msg_body, "text/html")
            msg.send()
            return {"Email sent."}
        except Exception as e:
            return e

    @classmethod
    def get_jqx_colinfo_fieldinfo(cls, col, grid_width, total_width, number_fields=[], date_fields=[], decimal_fields=[] ):
        align = "left"
        data_type = "string"
        filter_type = 'checkedlist'  # 'input'
        cellsformat = None
        if col["data_type"] in number_fields:
            align = "right"
            data_type = 'number'  # numeric_data_type_names[str(col[1])]
            filter_type = 'number'
            # if re.search("price", col[0], re.IGNORECASE):
            #     cellsformat = 'c2'
            # else:
            cellsformat = 'F2' if col["data_type"] in decimal_fields else "n"
        elif col["data_type"] in date_fields:
            data_type = 'date'
            filter_type = 'range'
            cellsformat = 'dd-MMMM-yyyy'
        field_info = {
            "name": col["name"],
            "type": data_type,
            # "values": {"width": col_width, "align": align}
        }
        # data_fields.append(data_field)
        if total_width >= grid_width:
            col_width = grid_width / total_width * col["width"];
        else:
            col_width = col["width"]
        if col_width < 100:
            col_width = 100
        col_info = {
            "text": col["name"],
            "datafield": col["name"],
            'datatype': data_type,
            "cellsalign": align,
            "align": 'center',  # align,
            'filtertype': filter_type,
            "width": col_width,
            "resizable": True,
            "cellsformat": cellsformat
            # "draggable":True,
        }
        return {"col_info": col_info, "field_info": field_info}


class Log_Error():
    @classmethod
    def log_view_error_message(self, request, e, act_log=None, redirect_path=None):
        error_message = str(e)
        self.log_error_message(e, act_log)
        messages.add_message(request, messages.ERROR, error_message)
        if redirect_path is None:
            redirect_path = request.META.get('HTTP_REFERER', '')
            if redirect_path == '':
                redirect_path = "/"
        return redirect(redirect_path)
        # response.write(error_message)

    @classmethod
    def log_error_message(self, e, act_log=None):
        error_message = str(e)
        logger = logging.getLogger()
        if act_log is not None: act_log.update_error_desc(error_message)
        logger.error(traceback.format_exc())
        return error_message

    @classmethod
    def log_message(cls, msg):
        logger = logging.getLogger()
        logger.error(msg)


class DB_Query():
    @classmethod
    def get_connnection_name_4_layer(cls, layer_info):
        if layer_info.app_label == 'remote_app': settings.REMOTE_CONN_NAME = layer_info.remote_conn_name.name
        return DB_Query.get_connection_name(app_label=layer_info.app_label, model_name=layer_info.lyr_model_name)

    @classmethod
    def get_connection_name(cls, app_label, model_name=None):
        if app_label in SPATIAL_APPS or model_name in SPATIAL_TABLES:
            return SPATIAL_DB
        elif app_label in ADP_APP or model_name in ADP_TABLES:
            return ADP_DB
        elif app_label in IRRIGATION_APP or model_name in IRRIGATION_TABLES:
            return IRRIGATION_DB
        elif app_label in DELSAP_APP or model_name in DELSAP_TABLES:
            return DELSAP_DB
        elif app_label in DIA_APP or model_name in DIA_TABLES:
            return DIA_DB
        # elif app_label in INDUS_BASIN_APP and model_name in INDUS_BASIN_TABLES:
        #     return INDUS_BASIN_DB
        elif app_label in SURVEY_STATS_APPS or model_name in SURVEY_STATS_TABLES:
            return SURVEY_STATS_DB
        # elif app_label in PC1_APP or model_name in PC1_TABLES:
        #     return PC1_DB

        elif app_label in MEETINGS_APP or model_name in MEETINGS_TABLES:
            return MEETINGS_DB
        elif app_label == 'remote_app':
            if settings.REMOTE_CONN_NAME not in settings.DATABASES.keys():
                connection_info = DatabaseConnections.objects.filter(name=settings.REMOTE_CONN_NAME).values(
                    'con_string').get()
                settings.DATABASES[settings.REMOTE_CONN_NAME] = connection_info["con_string"]
            return settings.REMOTE_CONN_NAME
        return 'default'

    @classmethod
    def get_spatial_and_key_column(cls, app_label, table_name):
        conn = connections[DB_Query.get_connection_name(app_label)]
        cursor = conn.cursor()
        table_description = conn.introspection.get_table_description(cursor, table_name)
        result = {}
        result['is_spatial'] = False
        result['id'] = None
        # with connection.schema_editor() as schema_editor:

        # for i in table_description:
        #     field_type=conn.introspection.get_field_type(table_description[i][1], table_description[i])

        for col_description in table_description:
            record = list(col_description)
            field_type = conn.introspection.get_field_type(col_description[1], col_description)
            if field_type in [16400, 'GeometryField']:
                result['geom_field'] = record[0]
                result['is_spatial'] = True
                # if record[0] == 'id' or record[0] == 'gid' or record[0] == 'fid':
                #     result['id'] = record[0]
        result['id'] = conn.introspection.get_primary_key_column(cursor, table_name)
        return result

    @classmethod
    def execute_query_as_list(self, query, app_label="gis"):
        connection_name = DB_Query.get_connection_name(app_label)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            result_list = list(cursor.fetchall())
            cursor.close()
        return result_list

    @classmethod
    def execute_query_as_dict(self, query, is_geom_include=True, app_label="gis", model_name=None):
        connection_name = DB_Query.get_connection_name(app_label, model_name)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            if is_geom_include:
                result_dict = DB_Query.dictfetchall(cursor)
            else:
                result_dict = DB_Query.dictfetchallXGeom(cursor)
            cursor.close()
        return result_dict

    @classmethod
    def execute_query_as_one(self, query, is_one=True, app_label="gis", model_name=None):
        connection_name = DB_Query.get_connection_name(app_label, model_name)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            cur_res = cursor.fetchone()
            if cur_res is not None:
                result = cur_res[0]
            cursor.close()
        return result

    @classmethod
    def execute_dml(self, query, app_label="gis"):
        connection_name = DB_Query.get_connection_name(app_label)
        connection = connections[connection_name]
        cursor = connection.cursor()
        res = cursor.execute(query)
        return res

    @classmethod
    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def dictfetchallXGeom(self, cursor):
        columns = []
        for col in cursor.description:
            if col[0] != "geom":
                columns.append(col[0])
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def execute_query_as_geojson(cls, query, app_label='gis', geom_col='geom'):
        geo_json_query = "SELECT jsonb_build_object(" \
                         "'type',     'FeatureCollection'," \
                         "'features', jsonb_agg(feature)) " \
                         "FROM ( " \
                         "SELECT jsonb_build_object( " \
                         "'type', 'Feature', " \
                         "'geometry',   ST_AsGeoJSON(%s)::jsonb," \
                         "'properties', to_jsonb(row) - 'geom' -'geometry'" \
                         ") AS feature " \
                         "FROM (%s) row) features;" % (geom_col, query)
        result = DB_Query.execute_query_as_one(geo_json_query, app_label=app_label)
        return result

    @classmethod
    def get_geojson(cls, table_name, geom=None, layer_info=None):
        where_clause = ""
        layer_type = layer_info.layer_type
        layer_srid = layer_info.srid
        if geom is not None:
            if layer_type == "Vector":
                if geom.srid != layer_srid:
                    geom.transform(layer_srid)
                pggeom = "st_geomfromtext('%s',%s)" % (geom.wkt, layer_srid)
                where_clause = "where st_intersects(geom, %s)" % (pggeom)
                query = "SELECT jsonb_build_object(" \
                        "'type',     'FeatureCollection'," \
                        "'features', jsonb_agg(feature)) " \
                        "FROM ( " \
                        "SELECT jsonb_build_object( " \
                        "'type', 'Feature', " \
                        "'geometry',   ST_AsGeoJSON(geom)::jsonb," \
                        "'properties', to_jsonb(row) - 'geom' -'geometry'" \
                        ") AS feature " \
                        "FROM (SELECT * FROM %s %s) row) features;" % (table_name, where_clause)
            elif layer_type == "Raster":
                # if layer_srid != 3857:
                #     pnt.srid = 3857
                #     pnt.transform(layer_srid)
                query = "Select st_numbands(rast) from %s limit 1" % table_name
                bands = DB_Query.execute_query_as_one(query)
                # rast_info = Raster_Info.objects.filter(table_name=table_name)[0]
                # bands = rast_info.num_bands
                if "point" not in geom.geom_type.lower():
                    geom = geom.centroid
                if geom.srid != layer_srid:
                    geom.transform(layer_srid)
                pggeom = "st_geomfromtext('%s',%s)" % (geom.wkt, layer_srid)
                if layer_srid != 3857:
                    res_geom = "st_transform(%s,%s)" % (pggeom, 3857)
                else:
                    res_geom = pggeom
                where_clause = "where st_intersects(st_envelope(rast), %s)" % (pggeom)
                sub_query = "Select "
                for i in range(1, bands + 1):
                    sub_query = sub_query + 'st_value(rast, %s, %s,true) "band_%s",' % (i, pggeom, i)
                sub_query = sub_query[:len(sub_query) - 1]
                sub_query = '%s from %s %s' % (sub_query, table_name, where_clause)
                query = "SELECT jsonb_build_object(" \
                        "'type',     'FeatureCollection'," \
                        "'features', jsonb_agg(feature)) " \
                        "FROM ( " \
                        "SELECT jsonb_build_object( " \
                        "'type', 'Feature', " \
                        "'geometry',   ST_AsGeoJSON(%s)::jsonb," \
                        "'properties', to_jsonb(row) - 'geom' -'geometry'" \
                        ") AS feature " \
                        "FROM (%s) row) features;" % (res_geom, sub_query)
        else:
            res = {'type': 'FeatureCollection', 'features': None}
            return res

        result = DB_Query.execute_query_as_one(query, app_label=layer_info.app_label)
        return result

    @classmethod
    def get_table_description(cls, table_name, app_label, conn=None, is_geom_included=True):

        if conn is None: conn = connections[DB_Query.get_connection_name(app_label=app_label)]
        table_description = conn.introspection.get_table_description(conn.cursor(), table_name)
        cols = []
        table_width = 0
        for col in table_description:
            try:
                # record = list(col_description)
                # field_type = conn.introspection.get_field_type(col_description[1], col_description)
                data_type = conn.introspection.get_field_type(col[1], col)
                if not is_geom_included and data_type == "GeometryField":
                    continue
                c_width = 200 if col[3] == -1 else col[3]
                if col[0] == 'assignment': c_width = 500
                col = {"name": col[0], "width": c_width, "data_type": data_type}
                cols.append(col)
                table_width = table_width + c_width
            except Exception as e:
                print(str(e))
        return {"cols": cols, "tabLe_width": table_width}

    @classmethod
    def get_jqx_columns_info_and_data_of_layer(cls, layer_info, is_geom_included=True, grid_width=1500):
        if layer_info.layer_type == "Raster":
            query = 'SELECT (pvc).* ' \
                    'FROM (SELECT ST_ValueCount(rast) As pvc ' \
                    'FROM "%s") As foo ' \
                    'ORDER BY (pvc).value ' % layer_info.table_name
        else:
            query = 'Select * from "%s"' % layer_info.table_name
        connection = connections[DB_Query.get_connnection_name_4_layer(layer_info)]  # connections[SPATIAL_DB]
        return DB_Query.get_jqx_columns_info_and_data_of_table(layer_info.table_name, layer_info.app_label, query,
                                                               conn=connection,
                                                               is_geom_included=is_geom_included, grid_width=grid_width)

    @classmethod
    def get_jqx_columns_info_and_data_of_table(cls, table_name, app_label, query, conn=None, is_geom_included=True,
                                               grid_width=1500):
        if conn == None: conn = connections[DB_Query.get_connection_name(app_label=app_label)]
        table_info = DB_Query.get_table_description(table_name, app_label, conn=conn,
                                                    is_geom_included=is_geom_included)
        data_fields = []
        grid_cols = []
        data_cols = []
        total_width = table_info["tabLe_width"]
        for col in table_info["cols"]:
            res = Common_Utils.get_jqx_colinfo_fieldinfo(col,grid_width=grid_width, total_width=total_width,
                                                         number_fields=["IntegerField", "DecimalField", "AutoField"],
                                                         date_fields=["DateField", "DateTimeField"],
                                                         decimal_fields=["DecimalField"])
            data_fields.append(res["field_info"])
            grid_cols.append(res["col_info"])
            data_cols.append(col["name"])

        with conn.cursor() as cursor:

            # query = 'Select * from "%s"' %table_name
            cursor.execute(query)

            data = [
                dict(zip(data_cols, row))
                for row in cursor.fetchall()
            ]
        return {"total_width": total_width, "data_fields": data_fields, "columns": grid_cols, "data": data}

    @classmethod
    def get_jqx_columns_info_with_data(self, query, app_label, is_geom_include=True, grid_width=-1):

        # app_label = layer_info.app_label

        connection = connections[DB_Query.get_connection_name(app_label=app_label)]  # connections[SPATIAL_DB]
        result = None
        grid_cols = []
        data_cols = []
        data_fields = []
        numeric_data_type_names = ["23", "701"]  # {"23": "int", "701": "float"}
        date_data_type_names = ['1082', 'date', 'datetime', 'timez']
        row_count = 0
        with connection.cursor() as cursor:
            cursor.execute(query)

            total_width = 0;
            for col in cursor.description:
                if is_geom_include == False and col[1] == 47806:
                    continue
                c_width = 200 if col[3] == -1 else col[3]
                if col[0] == 'assignment': c_width = 500
                total_width = total_width + c_width

            for col in cursor.description:
                # if row_count == 20: break;
                if is_geom_include == False and col[0] == "geom":
                    continue
                if col[0] in data_cols:
                    continue
                if col[0] == "pop":
                    continue
                align = "left"
                data_type = "string"
                filter_type = 'checkedlist'  # 'input'
                cellsformat = None
                if str(col[1]) in numeric_data_type_names:
                    align = "right"
                    data_type = 'number'  # numeric_data_type_names[str(col[1])]
                    filter_type = 'number'
                    # if re.search("price", col[0], re.IGNORECASE):
                    #     cellsformat = 'c2'
                    # else:
                    cellsformat = 'F2'
                elif str(col[1]) in date_data_type_names:
                    data_type = 'date'
                    filter_type = 'range'
                    cellsformat = 'D'
                col_width = 200 if col[3] == -1 else col[3]
                # col_width = int(col[3])
                if col[0] == 'assignment':
                    col_width = 500
                if total_width >= grid_width:
                    col_width = grid_width / total_width * col_width;
                if col_width < 100:
                    col_width = 100
                # total_width = total_width + col_width
                if data_type == 'date':
                    data_field = {
                        "name": col[0],
                        "type": data_type,
                        "format": 'dd.MM.yyyy'
                    }
                else:
                    data_field = {
                        "name": col[0],
                        "type": data_type,
                        # "values": {"width": col_width, "align": align}
                    }

                data_fields.append(data_field)
                if data_type == 'date':
                    col_info = {
                        "text": col[0],
                        "datafield": col[0],
                        'datatype': data_type,
                        "cellsalign": align,
                        "align": align,
                        'filtertype': filter_type,
                        "width": col_width,
                        "resizable": True,
                        'cellsformat': 'dd.MM.yyyy'
                    }
                else:
                    col_info = {
                        "text": col[0],
                        "datafield": col[0],
                        'datatype': data_type,
                        "cellsalign": align,
                        "align": align,
                        'filtertype': filter_type,
                        "width": col_width,
                        "resizable": True,
                        # "draggable":True,
                    }
                grid_cols.append(col_info)
                data_cols.append(col[0])
                row_count = row_count + 1
            data = [
                dict(zip(data_cols, row))
                for row in cursor.fetchall()
            ]
            return {"total_width": total_width, "data_fields": data_fields, "columns": grid_cols, "data": data}


            # def LayerPermissions_2_ItemsPrmissions():
            #     perm_obj = Permission.objects.all()
            #     print(len(perm_obj))
            #     for obj in perm_obj:
            #         Items_Permission().insert_row(item_info=obj.Info_id,item_name=obj.layer_name,entity_name=obj.entity_name,
            #                                       entity_type=obj.entity_type,permission_type=obj.permission_type)

    @classmethod
    def get_column_names(cls, table_name):
        query = "select column_name, data_type from information_schema.columns where table_name='%s'" % table_name
        cols = DB_Query.execute_query_as_dict(query)
        return cols;

    @classmethod
    def get_column_distinct_value(cls, table_name, col_name):
        query = 'Select distinct("%s") from %s order by "%s"' % (col_name, table_name, col_name)
        distinct_values = DB_Query.execute_query_as_list(query)
        return distinct_values

    @classmethod
    def get_srid(cls, table_name, layer_type="Vector"):
        query = None
        if layer_type == "Vector":
            query = "Select st_srid(geom) from %s" % (table_name)
        elif layer_type == "Raster":
            query = "Select st_srid(rast) from %s" % (table_name)
        if query is not None:
            res = DB_Query.execute_query_as_one(query)
        return res

    @classmethod
    def get_geom_extent_in_3857(cls, table_name, srid, layer_type="Vector", app_label='gis'):
        query = None
        if layer_type == "Vector":
            query = 'Select st_extent(st_transform(st_setsrid(geom,%s),3857)) from "%s"' % (srid, table_name)
        elif layer_type == "Raster":
            query = 'Select st_extent(st_transform(st_setsrid(envelope,%s),3857)) from "%s"' % (srid, table_name)
        if query is not None:
            res = DB_Query.execute_query_as_one(query, app_label=app_label)
            if res is None:
                res = str(SPATIAL_EXTENT_3857)
                res = res[1:len(res) - 1]
            else:
                res = res.replace(" ", ",")[4:len(res) - 1]
        else:
            res = str(SPATIAL_EXTENT_3857)
            res = res[1:len(res) - 1]
        res = res.replace(",", ", ")

        return res

    @classmethod
    def get_raster_summary(cls, table_name):
        query = "Select sum((stats).sum) sum, avg((stats).mean) mean, avg((stats).stddev) stddev," \
                " min((stats).min) min, max((stats).max) max " \
                "FROM (SELECT ST_SummaryStats(rast, 1, TRUE ) As stats " \
                "FROM %s) As foo;" % table_name
        summary_stats = DB_Query.execute_query_as_dict(query)
        return summary_stats

    @classmethod
    def get_raster_valuecount(cls, table_name):
        query = "SELECT (pvc).COUNT as count, (pvc).VALUE as val " \
                "FROM (SELECT ST_ValueCount(rst.rast,1) AS pvc FROM %s rst) f ORDER BY (pvc).VALUE" % table_name
        res = DB_Query.execute_query_as_list(query)

        return res;

    @classmethod
    def addPermissionType2Items(cls, item_list, item_name_field, user, permission_type):

        for item in item_list:
            # if user.is_superuser:
            #     res = True
            # else:
            item_name = item[item_name_field]
            res = len(list(Items_Permission.objects.filter(item_name=item_name, entity_name=user, entity_type='U',
                                                           permission_type=permission_type))) > 0
            # item_type = ContentType.objects.get_for_model(item)
            # res = list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item['id'],
            #                                            item_name=item_name, entity_name=user,
            #                                            entity_type='V', permission_type=permission_type))

            if permission_type == 'O':
                item['is_owner'] = res
            else:
                item["permission_" + permission_type] = res
        return item_list

    @classmethod
    def get_fields_list(cls, table_name, schema_name="public"):
        query = "SELECT column_name, data_type " \
                "FROM information_schema.columns " \
                "WHERE table_schema = '%s' " \
                "AND table_name   = '%s'" % (schema_name, table_name)
        res = DB_Query.execute_query_as_dict(query)
        return res


class Model_Utils():
    @classmethod
    def lyr_2_model(cls, layer, model, layer_mapping, src_srid, des_srid=3857):
        pk_name = model._meta.pk.name
        for feat in layer:
            try:
                feat_geom = feat.geom
                feat_geom.srid = int(src_srid)

                if src_srid != des_srid:
                    feat_geom.transform(des_srid)
                obj = model()
                obj.geom = GEOSGeometry(feat_geom.wkt)

                for key in layer_mapping:
                    if key not in [pk_name, "geom"]:
                        val = feat[str(layer_mapping[key])]
                        if val != "-1":
                            obj.__setattr__(key, val)
                obj.save()
            except Exception as e:
                Log_Error.log_error_message(e)

    @classmethod
    def get_apps_with_model_name(cls):
        apps_list = {}
        inst_apps = settings.INSTALLED_APPS
        inst_apps.append('ferrp.gis')
        for app_name in inst_apps:
            if "ferrp" in app_name:
                app_name = app_name.split(".")
                if len(app_name) > 1:
                    app_label = app_name[len(app_name) - 1]
                    model_names = Model_Utils.get_app_model_name(app_label)
                    if len(model_names) > 0:
                        apps_list[app_label] = model_names
        return apps_list

    @classmethod
    def get_app_model_name(cls, app_name, must_include_geom=True):
        model_names = []
        app_models = apps.get_app_config(app_label=app_name).models
        for key in app_models:
            if must_include_geom == True:
                model_fields = app_models[key]._meta.fields
                # app_models[key]._meta.fields[0].attname
                for field in model_fields:
                    if field.attname == "geom":
                        model_names.append(key)
                        break
        return model_names

    @classmethod
    def get_model_fields_list(cls, app_label, model_name, include_properties=False, include_pk=False,
                              include_geom=False):
        model = apps.get_model(app_label=app_label, model_name=model_name)

        excludedField = []
        if include_pk == False:
            pk_name = model._meta.pk.name
            excludedField.append(pk_name)
        if include_geom == False:
            excludedField.append("geom")
        field_names = []
        for f in model._meta.fields:
            if f.name not in excludedField:
                field_names.append(f.name)
        if include_properties == True:
            property_names = [name for name in dir(model) if isinstance(getattr(model, name), property)]
            # return dict((name, getattr(instance, name) for name in field_names + property_names)
            all_fields = field_names + property_names
            return all_fields
        return field_names

    @classmethod
    def get_model_attribute_value(cls, obj, col_name, default_value=None):
        res = None
        attr = getattr(obj, col_name, default_value)
        if callable(attr):
            res = attr()
        else:
            res = attr
        return res

    @classmethod
    def calculate_model_envelop(cls, model):
        agg_obj = model.objects.aggregate(ext=Extent('geom'))
        extent = agg_obj['ext']
        if extent is None: extent = SPATIAL_EXTENT_3857
        return extent

    @classmethod
    def get_model_geometry_type(cls, model):
        obj = model.objects.all()[:1]
        geom_type = obj[0].geom.geom_type
        return geom_type


def getJSONFromDB(sql, con):
    if con is not None:
        connection = connections[con]
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


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)
