import urllib
from operator import itemgetter
import json
import PIL, numpy, os
from PIL import ImageDraw, ImageFont
from PIL.Image import Image

from django.apps import apps
from django.contrib.gis.db.models import RasterField, Transform, MultiPolygonField
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon, MultiPoint, MultiLineString, Polygon, Point, LinearRing, LineString, \
    GeometryCollection
from io import BytesIO

from django.db.models.expressions import RawSQL
from pyheatmap.heatmap import HeatMap

from ferrp.layers.gis_migration import transform_geometry
from ferrp.layers.models import Info, Raster_Info
from ferrp.settings import ICON_PATH, MEDIA_ROOT
from ferrp.utils import Log_Error, DB_Query, Common_Utils

from ferrp.web_services.layer_styling import Layer_Styling


class WMS_Service():
    def get_map_service(self, request):
        self.styles = None
        self.project_id = request.GET.get('project_id') if 'project_id' in request.GET else request.GET.get(
            'project_id'.upper())
        self.result_table = request.GET.get('RESULT_TABLE') if 'RESULT_TABLE' in request.GET else None
        self.bbox = request.GET.get('bbox') if 'bbox' in request.GET else request.GET.get('bbox'.upper())
        self.styles = request.GET.get('styles') if 'styles' in request.GET else request.GET.get('styles'.upper())
        self.width = request.GET.get('width') if 'width' in request.GET else request.GET.get('width'.upper())
        self.height = request.GET.get('height') if 'height' in request.GET else request.GET.get('height'.upper())
        # map_srs = request.GET.get('srs'.upper())
        self.map_srs = request.GET.get('srs') if 'srs' in request.GET else request.GET.get('CRS')
        self.layer_name = request.GET.get('layers') if 'layers' in request.GET else request.GET.get('layers'.upper())
        self.format = request.GET.get('format') if 'format' in request.GET else request.GET.get('format'.upper())
        self.format_option = request.GET.get('format_options') if 'format_option' in request.GET else request.GET.get(
            'format_option'.upper())
        # self.style = request.GET.get('styles'.upper())


        if self.bbox is None or self.layer_name is None: pass
        self.bbox = self.bbox.split(',')

        self.layer_name_part = self.layer_name.split(":")
        self.layer_name = self.layer_name_part[len(self.layer_name_part) - 1]
        # if map_srs is None: pass
        self.map_srid = self.map_srs.split(':')[1]
        if self.result_table is None:
            self.layer_info = list(Info.objects.filter(layer_name=self.layer_name))[0]
            self.layer_extent = self.layer_info.extent
            self.layer_srid = self.layer_info.srid
            self.table_name = self.layer_info.table_name
            self.app_label = self.layer_info.app_label
            if self.app_label == 'remote_app':
                from ferrp import settings
                settings.REMOTE_CONN_NAME = self.layer_info.remote_conn_name.name
        else:
            q = "select st_srid(rast) from %s where layer_name='%s'" % (self.result_table, self.layer_name)
            self.layer_srid = DB_Query.execute_query_as_one(q)
            self.layer_info = Info()
            self.layer_info.layer_type = "Raster"
            q = "select st_envelope(rast) from %s where layer_name='%s'" % (self.result_table, self.layer_name)
            self.layer_extent = DB_Query.execute_query_as_one(q)
            self.app_label = 'gis'
            self.table_name = self.result_table
        if self.app_label == None:
            self.app_label = 'gis'
        if self.layer_srid is None: self.layer_srid = '4326'
        self.pixel_size_x = (float(self.bbox[2]) - float(self.bbox[0])) / float(self.width)
        self.pixel_size_y = (float(self.bbox[3]) - float(self.bbox[1])) / float(self.height)
        self.pixel_size_map = self.pixel_size_x if self.pixel_size_x < self.pixel_size_y else self.pixel_size_y
        self.pixel_size = self.pixel_size_map

        self.map_envelop = Polygon.from_bbox(self.bbox)
        self.map_envelop.srid = int(self.map_srid)
        if self.layer_extent is not None:
            layer_bbox = self.layer_extent.split(',')
            if len(layer_bbox) >= 4:
                self.layer_envelop = Polygon.from_bbox(layer_bbox)
                self.layer_envelop.srid = int(self.layer_srid)
            else:
                self.layer_envelop = None

        self.map_envelop.set_srid(int(self.map_srid))
        if self.layer_srid not in (3857, 900913):
            self.map_envelop_layer_srid = self.map_envelop.transform(self.layer_srid, True)
        else:
            self.map_envelop_layer_srid = self.map_envelop

        if self.app_label == 'layers':
            self.app_label = 'gis'
        if self.layer_info is not None:
            if self.styles != "":
                self.styles = json.loads(self.styles)
                if not 'style' in self.styles.keys():
                    self.styles['style'] = self.layer_info.style
                if not 'label' in self.styles.keys():
                    self.styles['label'] = None
            else:
                self.styles = {}
                self.styles['style'] = self.layer_info.style
                self.styles['label'] = None

        if self.layer_info.layer_type == "Raster":

            content = self.create_raster_tile_image(self.layer_name, self.pixel_size, self.width, self.height,
                                                    self.map_envelop, self.map_srid, self.layer_srid,
                                                    self.bbox, table_name=self.table_name, app_label=self.app_label,
                                                    result_table=self.result_table)
            # create_tile_GDALRaster(layer_name, map_envelope, pixel_size, width, height, map_srid, layer_srid)
            # response.write(content)
            return content

        elif self.layer_info.layer_type == "Vector":
            geom_type = self.layer_info.geom_type
            content = self.create_vector_tile_image(self.layer_name, int(self.width), int(self.height),
                                                    self.map_envelop, int(self.map_srid), self.pixel_size,
                                                    layer_info=self.layer_info, layer_style=self.styles,
                                                    # self.layer_info.style,
                                                    layer_srid=self.layer_srid, table_name=self.table_name,
                                                    app_label=self.app_label)
            size = len(content) / 1024
            return content
        elif self.layer_info.layer_type == "HeatMap":
            args = {
                'width': int(self.width),
                'height': int(self.height),
                'map_envelop': self.map_envelop_layer_srid,
                'layer_envelop': self.layer_envelop,
                'layer_info': self.layer_info,
                'style': self.styles,
                # 'layer_envelop': self.layer_envelop,
                # 'table_name': self.table_name,
                # 'app_label': self.app_label,
                # 'model_name': self.model_name,
                # 'property_name': self.property_name,
            }
            v2hm = Vector2HeatMap(args)
            content = v2hm.get_img_content()
            return content

    def create_empty_raster(self):
        width = int(self.width)
        height = int(self.height)
        img = PIL.Image.new('RGBA', (width, height), color=(0, 0, 0, 110))
        # img_draw = ImageDraw.Draw(img)
        # fill_color = (255, 0,0, 125)
        # img_draw.polygon([(0,0),(0, height),(width, height),(width,0)],fill_color)
        content = BytesIO()
        format_split = self.format.split("/")
        img_format = "png"
        if len(format_split) > 0:
            img_format = format_split[1]
        img.save(content, img_format, optimize=True)
        return content.getvalue()

    def create_raster_tile_image(self, layer_name, pixel_size, width, height, map_envelop, map_srid, layer_srid, bbox,
                                 table_name, app_label, result_table):
        r2map = Raster2Map(
            {"layer_name": layer_name, "width": width, "height": height, "map_envelop": map_envelop,
             "pixel_size": pixel_size, "map_srid": map_srid,
             "layer_srid": layer_srid, "table_name": table_name, "app_label": app_label, "result_table": result_table})

        r2map.create_empty_raster()
        r2map.create_union_raster()
        if not r2map.union_raster is None:
            r2map.create_final_raster()
        content = r2map.create_image()
        return content

    def create_vector_tile_image(self, layer_name, width, height, map_envelop, map_srid, pixel_size, layer_info,
                                 layer_style=None, layer_srid=3857, table_name=None, app_label=None):
        if map_srid != layer_srid:
            # layer_envelop = map_envelop.transform(layer_srid, clone=True)  # transform_geometry(map_envelop, map_srid, des_srid=layer_srid, response_asText=False)
            query = "Select st_transform(st_geomfromtext('%s',%s),%s)" % (map_envelop.wkt, map_srid, layer_srid)
            layer_envelop = GEOSGeometry(DB_Query.execute_query_as_one(query))
        else:
            layer_envelop = map_envelop

        v2r = Vector2Map({"width": width, "height": height, "pixel_size": pixel_size, "map_envelop": map_envelop,
                          "layer_envelop": layer_envelop, "layer_style": layer_style['style'],
                          "layer_label": layer_style['label'],
                          "layer_info": layer_info, "layer_name": layer_name, "layer_srid": layer_srid,
                          "map_srid": map_srid, "table_name": table_name, "app_label": app_label})

        v2r.perform_vector_2_raster_operation()
        # v2r.perform_query(query)
        # content = v2r.get_img_content()
        # save_as_png(content)

        # v2r.draw_boundary_in_polygon()
        content = v2r.get_img_content()
        return content

    @classmethod
    def save_as_png(cls, content, image_name="test.png"):
        file_path_name = os.path.join(MEDIA_ROOT, image_name)
        with open(file_path_name, 'wb+') as destination:
            destination.write(content)

    @classmethod
    def create_affine_transformation(cls, width, height, bbox):
        Istr = '0 %s %s; 0 0 %s; 1 1 1' % (width, width, height)
        Imatrix = numpy.matrix(Istr)
        Mstr = '%s %s %s;%s %s %s;1 1 1' % (bbox[0], bbox[2], bbox[2], bbox[3], bbox[3], bbox[1])
        Mmatrix = numpy.matrix(Mstr)
        affine = Imatrix * Mmatrix.getI()
        return affine


class Raster2Map():
    layer_name = None
    empty_raster = None
    width = None
    height = None
    map_envelop = None
    layer_envelop = None
    pixel_size = None
    map_srid = None
    layer_srid = None
    rast_info = None
    union_raster = None
    final_raster = None
    num_bands = None

    def __init__(self, *args, **kwargs):
        self.layer_name = args[0]['layer_name']
        self.width = args[0]['width']
        self.height = args[0]['height']
        self.map_envelop = args[0]['map_envelop']
        self.pixel_size = args[0]['pixel_size']
        self.map_srid = args[0]['map_srid']
        self.layer_srid = args[0]['layer_srid']
        self.table_name = args[0]['table_name']
        self.app_label = args[0]['app_label']
        self.create_layer_envelop()
        self.layer_styling = Layer_Styling(self.layer_name)
        self.result_table = args[0]['result_table']

    def create_image(self):
        if self.final_raster is not None:
            content = self.convert_raster_to_png(self.final_raster, 'tiled_raster.png')
        else:
            color_map = '0:0:0:0:0\n' \
                        'nv:0:0:0:0'
            content = self.convert_raster_to_png(self.empty_raster, 'final_union_raster.png', color_map)
        return content

    def create_empty_raster(self):
        bbox = self.map_envelop.extent
        rast_info_list = \
            list(Raster_Info.objects.filter(res_x__lte=self.pixel_size, main_table_name=self.layer_name).order_by(
                '-res_x'))

        if len(rast_info_list) > 0:
            self.rast_info = rast_info_list[0]
        else:
            rast_info_list = Raster_Info.objects.filter(table_name=self.layer_name)
            if rast_info_list.count() > 0:
                self.rast_info = rast_info_list[0]
            else:
                self.rast_info = Raster_Info
                pixeltype_query = 'Select Distinct(ST_BandPixelType(rast)) from %s where layer_name=\'%s\'' % (
                    self.result_table, self.layer_name)
                self.rast_info.pixel_type = DB_Query.execute_query_as_one(pixeltype_query)
                query = 'SELECT max(st_numbands(rast)) As num_bands, max(ST_PixelWidth(st_transform(rast, 3857))) As pixwidth, max(ST_PixelHeight(st_transform(rast, 3857))) As pixheight ' \
                        'from "%s" where layer_name=\'%s\'' % (self.result_table, self.layer_name)

                self.rast_info.num_bands = DB_Query.execute_query_as_one(query)
                self.rast_info.table_name = self.result_table
        self.num_bands = self.rast_info.num_bands
        bands = ""
        for i in range(0, self.num_bands):
            bands = bands + "ROW(%s, '%s'::text, 0, NULL)," % (str(i + 1), self.rast_info.pixel_type)
        bands = bands[:len(bands) - 1]
        query = "SELECT st_setSRID(ST_AddBand(ST_MakeEmptyRaster(%s,%s,%s,%s,%s),ARRAY[%s]::addbandarg[])" \
                ",%s) as rast" % (self.width, self.height, bbox[0], bbox[3], self.pixel_size, bands, self.map_srid)
        self.empty_raster = DB_Query.execute_query_as_one(query, app_label=self.app_label)

    def create_layer_envelop(self):
        self.layer_envelop = transform_geometry(self.map_envelop, self.map_srid, self.layer_srid, response_asText=False)
        # if self.map_srid != self.layer_srid:
        #     self.layer_envelop = self.map_envelop.transform(self.layer_srid)
        # else:
        #     self.layer_envelop = self.map_envelop

    def create_union_raster(self):
        num_bands = self.rast_info.num_bands
        if self.result_table is None:
            intersect_query = "Select rast as rast from %s where st_intersects(envelope,'%s')" % (
                self.rast_info.table_name, self.layer_envelop)
        else:
            intersect_query = "Select rast as rast from %s where st_intersects(envelope,'%s') and layer_name='%s'" % (
                self.result_table, self.layer_envelop, self.layer_name)
        # intersect_query = "Select rast as rast from %s" % (self.rast_info.table_name)
        with_query = "With trans_rast as( " + intersect_query + \
                     ") , retile_rast as(" \
                     "	Select st_tile(rast,100,100, TRUE, 0) rast from trans_rast" \
                     "), resample_rast as(" \
                     "   Select st_resample(rast,(Select rast from retile_rast limit 1)) rast from retile_rast" \
                     ")"

        query = "%s Select st_union(rast) from resample_rast" % with_query
        # query = "Select st_union(rast) from %s where st_intersects(envelope,'%s')" % (rast_info.table_name, eg_ext_geom)

        self.union_raster = DB_Query.execute_query_as_one(query, app_label=self.app_label)

    def create_final_raster(self):
        query = "select st_transform(CAST('%s' AS Raster),%s)" % (self.union_raster, self.map_srid)
        transformed_raster = DB_Query.execute_query_as_one(query, app_label=self.app_label)

        query = "select st_resample(CAST('%s' AS Raster),CAST('%s' As Raster))" % (
            transformed_raster, self.empty_raster)
        resample_raster = DB_Query.execute_query_as_one(query, app_label=self.app_label)

        query = "with unionResult as(" \
                "SELECT  CAST('%s' AS Raster) as rast union SELECT CAST('%s' AS Raster) as rast" \
                ")" % (self.empty_raster, resample_raster)
        # query = query + "\n SELECT st_union(unionResult.rast,ARRAY[ROW(1, 'SUM')]::unionarg[]) from unionResult"
        band_op = ""
        for i in range(0, self.rast_info.num_bands):
            band_op = band_op + "ROW(%s, 'SUM')," % (str(i + 1))
        band_op = band_op[:len(band_op) - 1]
        query = query + "SELECT st_union(unionResult.rast, ARRAY[%s]::unionarg[]) from unionResult" % band_op

        final_union_raster = DB_Query.execute_query_as_one(query, app_label=self.app_label)

        query = "select st_clip(CAST('%s' AS Raster),st_geomfromtext('%s',%s))" % (
            final_union_raster, self.map_envelop.wkt, self.map_srid)
        self.final_raster = DB_Query.execute_query_as_one(query)

    def convert_raster_to_png(self, raster, image_name, color_map=None):
        # query = "Select St_numbands(CAST('%s' AS Raster))" % (raster)
        # num_band = DB_Query.execute_query_as_one(query)
        if color_map is None:
            if self.num_bands >= 3:
                stretch_raster = self.minmax_stretch(raster)
                query = "SELECT St_AsPng(CAST('%s' AS Raster),ARRAY[1,2,3])" % (stretch_raster)
            else:
                color_map = self.create_color_map(self.layer_name)
                query = "SELECT ST_AsPNG(ST_ColorMap(CAST('%s' AS Raster),1, '%s'))" % (raster, color_map)
        else:
            query = "SELECT ST_AsPNG(ST_ColorMap(CAST('%s' AS Raster),1, '%s'))" % (raster, color_map)
        final_image = DB_Query.execute_query_as_one(query, app_label=self.app_label)
        content = bytes(final_image)
        # wirte_to_new_file("uploaded/" + image_name, content)
        return content

    def get_layer_stats(self, layer_name):
        query = "With ss as (" \
                "SELECT rid, band, ST_SummaryStats(rast, band) As stats FROM %s CROSS JOIN generate_series(1,4) As band) " \
                "Select ss.band, sum((stats).\"count\"), sum((stats).\"sum\"),avg((stats).\"mean\"),avg((stats).\"stddev\"),min((stats).\"min\"),max((stats).\"max\") " \
                "from ss GROUP BY ss.band ORDER BY ss.band" % layer_name
        stats = DB_Query.execute_query_as_dict(query, app_label=self.app_label)
        return stats

    def get_raster_stats(self, raster):
        query = "With ss as (" \
                "SELECT rid, band, ST_SummaryStats(CAST('%s' as Raster), band) As stats FROM generate_series(1,4) As band) " \
                "Select ss.band, sum((stats).\"count\"), sum((stats).\"sum\"),avg((stats).\"mean\"),avg((stats).\"stddev\"),min((stats).\"min\"),max((stats).\"max\") " \
                "from ss GROUP BY ss.band ORDER BY ss.band" % raster
        stats = DB_Query.execute_query_as_dict(query, app_label=self.app_label)
        return stats

    def apply_map_algebra_expr(self, raster, expr, band=1):
        query = "WITH foo AS (Select st_band(CAST('%s' AS Raster),%s) rast) " \
                "SELECT ST_MapAlgebra(rast, '8BUI', '%s' ,0)FROM foo" % (raster, band, expr)
        # query = "SELECT ST_MapAlgebra(CAST('%s' AS Raster) rast, band, NULL, '%s')" %(raster,expr)
        rast = DB_Query.execute_query_as_one(query, app_label=self.app_label)
        return rast

    def minmax_expr(self, min, max):
        m = (254 - 25) / (max - min)
        c = 254 - m * max
        expr = 'ceil(%s * [rast.val] + %s)' % (m, c)
        return expr

    def minmax_stretch(self, raster):
        stats = self.get_layer_stats(self.layer_name)
        # bands_sub_query = []
        # bands_color_map = []
        bands = []
        for i in range(3):
            min_val = float(stats[i]['min'])
            max_val = float(stats[i]['max'])

            expr = self.minmax_expr(min_val, max_val)
            # rast_band = execute_query_as_one("Select st_band(CAST('%s' AS Raster),%s)" %(raster,(i+1)))
            stretch_band = self.apply_map_algebra_expr(raster, expr, (i + 1))
            bands.append(stretch_band)


            # sub_query = "Select ST_ColorMap(CAST('%s' AS Raster),%s, '%s')" %(raster,(i+1),'grayscale')
            # bands.append(DB_Query.execute_query_as_one(sub_query))
            # bands_sub_query.append(sub_query)
        query = "Select st_addband(CAST('%s' AS RASTER), ARRAY[CAST('%s' AS RASTER),CAST('%s' AS RASTER)])" % (
            bands[0], bands[1], bands[2])
        strech_raster = DB_Query.execute_query_as_one(query, app_label=self.app_label)
        return strech_raster

    def create_color_map(self, layer_name):
        # no_of_bands = self.num_bands
        color_map = None
        rules = []
        layer_info_list = Info.objects.filter(layer_name=self.layer_name)
        if layer_info_list.count() > 0:
            layer_info = layer_info_list[0]
            if layer_info.style is None:
                query = "SELECT rid, band, (stats).* " \
                        "FROM (SELECT rid, band, ST_SummaryStats(rast, band) As stats " \
                        "FROM %s CROSS JOIN generate_series(1,%s) As band WHERE rid=1) As foo" % (
                            self.layer_name, self.num_bands)
                stats = DB_Query.execute_query_as_dict(query)
                style = self.layer_styling.get_default_raster_style(stats)
                rules = style['rules']
            else:
                rules = layer_info.style['rules']
        elif layer_name.endswith("_ssa_"):
            # query = "SELECT rid, band, (stats).* " \
            #         "FROM (SELECT rid, band, ST_SummaryStats(rast, band) As stats " \
            #         "FROM %s CROSS JOIN generate_series(1,%s) As band WHERE layer_name = '%s') As foo" % (
            #             self.result_table, self.num_bands, self.layer_name)
            # stats = DB_Query.execute_query_as_dict(query)
            # stats[0]['max'] = 1
            # stats[0]['min'] = 0
            # stats[0]['mean'] = 0.5
            style = Layer_Styling.get_functional_layer_style('ssa')
            rules = style['rules']
        for rule in rules:
            raster_symbolizer = rule['raster_symbolizer']
            color_map_entries = raster_symbolizer["color_map"]
            arr_color_map = []
            color_map_entries = sorted(color_map_entries, key=itemgetter('quantity'), reverse=True)
            for cm_ent in color_map_entries:
                # for i in range(len(color_map_entries)-1,0,-1):
                #     cm_ent = color_map_entries[i]
                color_hex = cm_ent["color"]
                rgb = tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5))
                op = float(cm_ent["opacity"]) * 255
                value = cm_ent["quantity"]
                arr_color_map.append("%s  %s  %s   %s   %s" % (value, rgb[0], rgb[1], rgb[2], op))
            arr_color_map.append("0  0    0    0   0")
            arr_color_map.append("nv 0    0    0   0")
            color_map = "\n".join(arr_color_map)
        return color_map

    def create_tile_GDALRaster(self, layer_name, map_envelope, pixel_size, width, height, map_srid, layer_srid):
        layer_envelope = transform_geometry(map_envelope, map_srid, des_srid=layer_srid, response_asText=False)
        rast_info = Raster_Info.objects.filter(res_x__lte=pixel_size, main_table_name=layer_name).order_by('-res_x')[0]
        query = "Select st_width(rast) width, st_height(rast) height, st_srid(rast) srid," \
                "  rast, st_astext(envelope) wkt from %s where st_intersects(envelope,'%s')" % (
                    rast_info.table_name, layer_envelope)
        rast_list = DB_Query.execute_query_as_dict(query, app_label=self.app_labely)

        for rastObj in rast_list:
            raster = GDALRaster({
                "srid": rastObj["srid"],
                "width": rastObj["width"],
                "height": rastObj["height"],
                "bands": [{"data": rastObj["rast"], "nodata_value": 0}]
            });

            # print("width:" + raster.width + " height:" + raster.height)
            raster = RasterField(rastObj['rast'])
        pass


class Vector2Map():
    img = None
    img_text = None
    img_draw = None
    img_draw_text = None
    format = "PNG"
    affine = None
    layer_style = None
    # symbolizer = {"fill": "#ffffb2",
    #               "stroke": "#000001",
    #               "stroke-width": "1",
    #               "stroke-linejoin": "bevel"}
    fill_color = (52, 37, 138, 150)
    stroke_color = (38, 34, 65, 255)
    stroke_width = 2
    stroke_linejoin = 'bevel'
    point_size = 3
    bitmap = 'glyphicons/png/glyphicons-21-home.png'  # 'googleicons/maps/ic_add_location_black_24dp_2x.png'
    bitmap_icon = None
    bitmap_color = (52, 37, 138)
    literals = []
    filter_column_name = None

    def __init__(self, *args, **kwargs):
        width = args[0]['width']
        height = args[0]['height']
        self.map_envelop = args[0]['map_envelop']
        self.layer_envelop = args[0]['layer_envelop']
        self.map_srid = args[0]['map_srid']
        self.layer_srid = args[0]['layer_srid']
        self.layer_name = args[0]['layer_name']
        self.layer_info = args[0]['layer_info']
        self.layer_style = args[0]['layer_style']
        self.layer_label = args[0]['layer_label']
        self.pixel_size = args[0]['pixel_size']
        self.table_name = args[0]['table_name']
        self.app_label = args[0]['app_label']
        self.model_name = self.layer_info.lyr_model_name;

        layer_bbox = self.layer_envelop.extent
        bitmap_file = os.path.join(ICON_PATH, self.bitmap)
        icon = PIL.Image.open(bitmap_file)
        self.bitmap_icon = icon
        # self.bitmap_icon = icon.resize((icon.size[0]*2, icon.size[1]*2),PIL.Image.ANTIALIAS)

        # if not self.layer_style in [None, []]:
        #     style = self.layer_style[0] #['styles']
        #     self.set_fill_color(style)
        #     self.set_stroke_color(style)

        self.img = PIL.Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
        # self.img = PIL.Image.new('RGB', (width, height), color=(0, 0, 0))
        self.img_draw = ImageDraw.Draw(self.img)
        if self.layer_label is not None:
            self.img_text = PIL.Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
            self.img_mask = PIL.Image.new('RGBA', (width, height), color=(0, 0, 0, 255))
            self.img_draw_text = ImageDraw.Draw(self.img_text)
        self.affine = WMS_Service.create_affine_transformation(width, height, layer_bbox)

    def perform_query(self, query):
        try:
            rs_list = DB_Query.execute_query_as_dict(query, app_label=self.app_label, model_name=self.model_name)
            for rs in rs_list:
                if not rs['geom'] is None:
                    ggeom = GEOSGeometry(rs['geom'])
                    if ggeom != None:
                        self.draw_geometry(ggeom)
                        if self.layer_label is not None:
                            col_name = self.layer_label['colName']
                            self.draw_label(ggeom, rs[col_name])
        except Exception as e:
            Log_Error.log_error_message(e);
            error_message = str(e)
            print("Erorr in Query:" + error_message + " \n query:" + query)

    def draw_text(self, ggeom, text, fill_color, font=None):
        text = str(text)
        try:
            font = self.get_img_font(text)
            points = []
            geom_type = ggeom.geom_type.lower()
            extent = None
            if "multi" in geom_type:
                if "point" in geom_type:
                    for point in ggeom:
                        points.append(point)
                else:
                    for geom in ggeom:
                        points.append(geom.centroid)
            elif geom_type != "point":
                points.append(ggeom.centroid)
                extent = ggeom.extent
            else:
                points.append(ggeom)
            size = self.img_draw_text.textsize(text, font)
            direction = None
            # if extent:
            #     if  (extent[3] - extent[1]) > (extent[2] - extent[0]):
            #         direction = 'btt'
            for point in points:
                screen_coord = [point.coords[0] - size[0] / 2, point.coords[1] - size[1] / 2]
                self.img_draw_text.text(screen_coord, text, fill=fill_color, font=font, direction=direction)
        except Exception as e:
            Log_Error.log_error_message(e);
            error_message = str(e)
            # print("Erorr in adding text:" + error_message )

    def get_img_font(self, txt):
        # font_size = 10  # starting font size
        font_size = int(self.layer_label['fontSize'])
        # portion of image width you want text width to be
        img_fraction = 0.50
        # font = ImageFont.load_default().font
        # font.setsize()
        font = ImageFont.truetype("arial.ttf", font_size)
        # while font.getsize(txt)[0] < img_fraction * self.img.size[0]:
        #     # iterate until the text size is just larger than the criteria
        #     fontsize += 1
        #     font = ImageFont.truetype("arial.ttf", fontsize)
        return font

    def set_fill_color(self, fill_color, fill_opacity=125):
        if fill_color is not None:
            self.fill_color = (int(fill_color[0]), int(fill_color[1]), int(fill_color[2]), int(fill_opacity))
            # if style['fill_color'] is not None:
            #     fill_color = style['fill_color'].split('(')[-1].split(')')[0].split(",")
            #     fill_opacity = float(style['fill_opacity']) * 255
            #     self.fill_color = (int(fill_color[0]), int(fill_color[1]), int(fill_color[2]), int(fill_opacity))

    def set_stroke_color(self, stroke_color, stroke_width, stroke_linejoin='bevel'):
        if stroke_color is not None:
            # stroke_color = style['stroke_color'].split('(')[-1].split(')')[0].split(",")
            self.stroke_color = (int(stroke_color[0]), int(stroke_color[1]), int(stroke_color[2]))
            self.stroke_width = int(stroke_width)
            self.stroke_linejoin = stroke_linejoin

    def get_img_content(self):
        content = BytesIO()
        self.img.save(content, self.format, optimize=True)
        return content.getvalue()

    # def create_affine_transformation(self, width, height, bbox):
    #     Istr = '0 %s %s; 0 0 %s; 1 1 1' % (width, width, height)
    #     Imatrix = numpy.matrix(Istr)
    #     Mstr = '%s %s %s;%s %s %s;1 1 1' % (bbox[0], bbox[2], bbox[2], bbox[3], bbox[3], bbox[1])
    #     Mmatrix = numpy.matrix(Mstr)
    #     self.affine = Imatrix * Mmatrix.getI()
    #     return self.affine

    def get_affine_as_list(self):
        return self.affine.tolist()

    def convert_map_geom_2_screen_geom(self, map_geom):
        screen_geom = []
        # coords = map_geom.coords
        for coord in map_geom:
            screen_tuple = self.convert_map_point_2_screen_point(coord)
            screen_geom.append(screen_tuple)
        return screen_geom

    def convert_map_point_2_screen_point(self, coord):
        map_matrix = numpy.matrix('%s;%s;1' % (coord[0], coord[1]))
        screen_matrix = self.affine * map_matrix
        screen_tuple = tuple(i[0] for i in numpy.array(screen_matrix[:2]))
        return screen_tuple

    def draw_label(self, ggeom, text):
        # label_col = ', "' + self.layer_label['colName'] + '"'
        color = self.convert_hex_2_rgb(self.layer_label['labelColor'])
        font_fill_color = (int(color[0]), int(color[1]), int(color[2]))
        font_type = self.layer_label['fontType']
        font_size = self.layer_label['fontSize']
        # font = ImageFont.truetype(font_type + ".ttf", int(font_size))
        self.draw_text(ggeom, text, font_fill_color)

    def draw_geometry(self, ggeom):
        if ggeom.geom_type == "MultiPolygon":
            self.draw_multi_polygon(ggeom)
        elif ggeom.geom_type == "MultiLineString":
            self.draw_multi_linestring(ggeom)
        elif ggeom.geom_type == "MultiPoint":
            self.draw_multi_point(ggeom)
        elif ggeom.geom_type == "Polygon":
            self.draw_polygon(ggeom)
        elif ggeom.geom_type == "LinearRing":
            self.draw_linear_ring(ggeom)
        elif ggeom.geom_type == "LineString":
            self.draw_linestring(ggeom)
        elif ggeom.geom_type == "Point":
            self.draw_point(ggeom)

    def draw_point(self, point):
        # map_coord = point.coords
        r = int(self.point_size)
        screen_coord = [point.coords[0] - r, point.coords[1] - r, point.coords[0] + r, point.coords[1] + r]
        # screen_coord = self.convert_map_point_2_screen_point(point)
        # self.img_draw.bitmap(screen_coord, self.bitmap_icon, fill=self.bitmap_color)

        self.img_draw.ellipse(screen_coord, fill=self.fill_color, outline=self.stroke_color)
        # self.img_draw.point(screen_coord,fill=self.fill_color)
        pass

    def draw_linestring(self, polyline):
        map_coords = polyline.coords
        screen_coords = map_coords  # self.convert_map_geom_2_screen_geom(map_coords)
        self.img_draw.line(screen_coords, fill=self.stroke_color, width=self.stroke_width)
        pass

    def draw_linear_ring(self, linear_ring):
        xy = []
        for coord in linear_ring:
            screen_coord = coord  # self.convert_map_geom_2_screen_geom(coord)
            xy.append(screen_coord)
        self.img_draw.polygon(xy, fill=self.fill_color, outline=self.stroke_color)
        pass

    def draw_polygon(self, polygon):
        xy = []
        for coord in polygon.coords:
            # self.draw_linear_ring(linear_ring)
            xy = coord  # self.convert_map_geom_2_screen_geom(coord)
            self.img_draw.polygon(xy, fill=self.fill_color, outline=self.stroke_color)
        pass

    def draw_multi_point(self, multi_point):
        for point in multi_point:
            self.draw_point(point)
        pass

    def draw_multi_linestring(self, multi_linestring):
        for linestring in multi_linestring:
            self.draw_linestring(linestring)
        pass

    def draw_multi_polygon(self, multi_polygon):
        for polygon in multi_polygon:
            # polygon = multi_polygon[1]
            self.draw_polygon(polygon)
        pass

    def calculate_simplify_stem(self):
        if self.layer_srid == 4326:
            simplify_step = float(self.pixel_size) / (110 * 1000)
        else:
            simplify_step = self.pixel_size
        return simplify_step

    def get_geom_query(self, geom_type, size, filter_value=""):
        affine_list = self.get_affine_as_list()
        label_col = ''
        group_by_clause = ''
        if self.layer_label is not None:
            # label_col = ', "' + self.layer_label['colName'] + '"'
            label_col = ', "%s"' % self.layer_label['colName']
            group_by_clause = 'GROUP BY "%s"' % self.layer_label['colName']

        simplify_step = self.calculate_simplify_stem()

        if 'point' in geom_type.lower():

            simplify_step = str(simplify_step * int(self.point_size))

            query = "With tblgeom1 as (Select ST_RemoveRepeatedPoints(ST_Collect(geom),%s) geom %s from %s " \
                    "where st_intersects(st_setsrid(geom,%s), st_geomfromtext('%s',%s)) %s %s)" \
                    % (simplify_step, label_col, self.table_name, self.layer_srid,
                       self.layer_envelop.wkt, self.layer_srid, filter_value, group_by_clause)
        elif 'linestring' in geom_type.lower():
            simplify_step = str(simplify_step)
            query = "With tblgeom1 as (Select ST_Intersection(ST_SimplifyPreserveTopology(geom,%s),st_geomfromtext('%s',%s) ) geom %s from %s where st_intersects(st_setsrid(geom,%s), st_geomfromtext('%s',%s)) %s )" \
                    % (
                        simplify_step, self.layer_envelop.wkt, self.layer_srid, label_col, self.table_name,
                        self.layer_srid,
                        self.layer_envelop.wkt, self.layer_srid,
                        filter_value)
        else:
            simplify_step = str(simplify_step)
            query = "With tblgeom1 as (Select ST_SimplifyPreserveTopology(geom,%s) geom %s from %s where st_intersects(st_setsrid(geom,%s), st_geomfromtext('%s',%s)) %s )" \
                    % (
                        simplify_step, label_col, self.table_name, self.layer_srid,
                        self.layer_envelop.wkt, self.layer_srid,
                        filter_value)

        query += "Select st_affine(geom,%s,%s,%s,%s,%s,%s) geom %s from tblgeom1" \
                 % (affine_list[0][0], affine_list[0][1], affine_list[1][0], affine_list[1][1],
                    affine_list[0][2], affine_list[1][2], label_col)
        return query

    def get_size_of_layer(self):
        try:
            query = "Select sum(st_memsize(geom))/1024 size, count(*) count from %s where st_intersects(geom, st_geomfromtext('%s',%s))" \
                    % (self.table_name, self.layer_envelop.wkt, self.layer_srid)
            res = DB_Query.execute_query_as_dict(query, app_label=self.app_label)
            if res[0]['size'] is None: res[0]['size'] = 0
            return res[0]['size']
        except Exception as e:
            print(e)
        return 0

    def perform_vector_2_raster_operation(self):
        # size = self.get_size_of_layer()
        size = 0
        geom_type = self.layer_info.geom_type
        if self.layer_style is None:

            # query = self.get_geom_query(geom_type, size)
            # self.perform_query(query)
            ls = Layer_Styling(self.layer_name)
            style = ls.get_default_vector_layer_style(geom_type)
            # if "point" in geom_type.lower():
            #     style = ls.get_default_point_style()
            # elif "line" in geom_type.lower():
            #     style = ls.get_default_linestring_style();
            # else:
            #     style = ls.get_default_polygon_style()

            style_rules = style["rules"]
        else:
            if type(self.layer_style) is str:
                self.layer_style = json.loads(self.layer_style)
            if 'style' in self.layer_style:
                self.layer_style = self.layer_style['style']
            if 'style' in self.layer_style:
                self.layer_style = self.layer_style['style']
            style_rules = self.layer_style['rules']
        if self.model_name is None or self.model_name == '':
            for rule in style_rules:
                filter_value = self.get_style_filter(rule['filter'], with_and_op=True)
                # property_name = rule['filter']['property_name']

                if filter_value == '' and len(self.literals) > 0 and self.filter_column_name is not None:
                    filter_value = ' and "%s" not in (%s)' % (
                        self.filter_column_name, ",".join("'{0}'".format(w) for w in self.literals))
                symbolizer = self.get_symbolizer(rule, geom_type)
                if symbolizer is not None:
                    query = self.get_geom_query(geom_type, size, filter_value)
                    self.perform_query(query)
        else:
            django_model = apps.get_model(app_label=self.app_label, model_name=self.model_name)
            affine_list = self.get_affine_as_list()
            simplify_step = str(self.calculate_simplify_stem())
            geom_type = self.layer_info.geom_type
            if "point" in geom_type.lower():
                # req_geom = "ST_RemoveRepeatedPoints(ST_Collect(geom), %s)" % simplify_step
                objs = django_model.objects.annotate(
                    # g=RawSQL("Select st_affine(ST_RemoveRepeatedPoints(ST_Collect(geom), %s), %s,%s,%s,%s,%s,%s)",
                    g=RawSQL("Select st_affine(geom, %s,%s,%s,%s,%s,%s)",
                             # (simplify_step, affine_list[0][0], affine_list[0][1],
                             (affine_list[0][0], affine_list[0][1],
                              affine_list[1][0],
                              affine_list[1][1],
                              affine_list[0][2], affine_list[1][2],))) \
                    .filter(geom__intersects=self.layer_envelop)  # .values('g','pk')

            else:

                objs = django_model.objects.annotate(
                    g=RawSQL("Select st_affine(ST_SimplifyPreserveTopology(geom,%s), %s,%s,%s,%s,%s,%s)",
                             (simplify_step, affine_list[0][0], affine_list[0][1],
                              affine_list[1][0],
                              affine_list[1][1],
                              affine_list[0][2], affine_list[1][2],))) \
                    .filter(geom__intersects=self.layer_envelop)  # .values('g','pk')

            for obj in objs:
                symbolizer = None
                prev_prop_name = None
                for rule in style_rules:
                    # rule = style_rules[0]
                    # com_obj = django_model.objects.get(pk = obj['pk']).values('plot_complaint_count')
                    filter = rule['filter']
                    prop_name = None
                    if 'property_name' in filter: prop_name = filter['property_name']

                    res = True
                    if prop_name is not None:
                        if prev_prop_name is None or prev_prop_name != prop_name:
                            prop_value = getattr(obj, prop_name, False)
                            # if prop_value > 0:
                            #     print (prop_value)
                        res = self.check_condition(filter, prop_value)
                    if res:
                        symbolizer = self.get_symbolizer(rule, geom_type)
                        break
                    prev_prop_name = prop_name
                if symbolizer is not None:
                    geom = GEOSGeometry(obj.g)
                    self.draw_geometry(geom)
                    try:
                        if self.layer_label is not None:
                            col_name = self.layer_label['colName']
                            # text_query = 'Select \'%s\' from "%s" where "%s"=\'%s\'' %()
                            text = Common_Utils.get_model_attribute(obj, col_name)
                            if text is not None:
                                self.draw_label(geom, str(text))
                    except Exception as e:
                        Log_Error.log_error_message(e)
        if self.layer_label is not None:
            #     self.img = PIL.Image.alpha_composite(self.img_text, self.img)
            self.img = PIL.Image.composite(self.img_text, self.img, self.img_text)
            # # self.img.paste(self.img_text)
            #     # self.img_text.paste(self.img)

    def check_condition(self, filter, prop_value):
        res = False
        import operator
        ops = {"=": operator.eq, "<": operator.lt, "<=": operator.le,
               ">": operator.gt, "<=": operator.ge}
        fil_op = filter['op']
        fil_val = filter['literal']
        if fil_op == "between":
            range = fil_val.split('-')
            min = float(range[0])
            max = float(range[1])
            val = float(prop_value)
            if val >= min and val <= max:
                res = True
        else:
            res = ops[fil_op](fil_val, prop_value)
        return res

    def map_2_screen_coordinate(self, geom):
        for coord in geom.coords:
            geom.coord = [0, 0]
        return geom

    def draw_boundary_in_polygon(self):
        affine_list = self.get_affine_as_list()
        if self.layer_info.geom_type == 'Polygon' and self.pixel_size < 10:
            query = "Select st_affine(st_boundary(geom),%s,%s,%s,%s,%s,%s) geom from %s " \
                    "where st_intersects(geom, st_geomfromtext('%s',%s)) and " \
                    " st_length(st_boundary(geom)) > %s " \
                    % (affine_list[0][0], affine_list[0][1], affine_list[1][0], affine_list[1][1], affine_list[0][2],
                       affine_list[1][2], self.table_name, self.layer_envelop.wkt, self.layer_srid, self.pixel_size)
            self.perform_query(query)
        pass

    def get_style_filter(self, filter, with_and_op=False):
        filter_value = ""
        if filter not in [None, {}] and filter["property_name"] != "-1":
            property_name = filter['property_name'] if 'property_name' in filter else ''
            self.filter_column_name = property_name
            literal = filter['literal'] if 'literal' in filter else ''
            if str.lower(filter['op']) == "between":
                literals = literal.split(" - ")
                filter_value = "\"%s\" %s %s and %s" % (filter['property_name'], filter['op'], literals[0], literals[1])
            else:
                self.literals.append(literal)
                filter_value = "\"%s\" %s '%s'" % (filter['property_name'], filter['op'], literal)

            if with_and_op: filter_value = " and " + filter_value
        return filter_value

    def get_symbolizer(self, rule, geom_type):
        symbolizer = None
        try:
            if geom_type.find("Polygon") != -1:
                symbolizer = rule['polygon_symbolizer']
                fill_rgb = self.convert_hex_2_rgb(symbolizer['fill'])
                fill_opacity = symbolizer['fill_opacity']
                if fill_opacity:
                    fill_opacity = float(fill_opacity) * 255
                else:
                    fill_opacity = 125
                self.set_fill_color(fill_rgb, fill_opacity)
                stroke_rgb = self.convert_hex_2_rgb(symbolizer['stroke'])
                stroke_width = symbolizer['stroke-width']
                if 'stroke-linejoin' in symbolizer:
                    stroke_line_join = symbolizer['stroke-linejoin']
                else:
                    stroke_line_join = 'bevel'
                self.set_stroke_color(stroke_rgb, stroke_width, stroke_line_join)

            elif geom_type.find('LineString') != -1:
                symbolizer = rule['line_symbolizer']
                stroke_rgb = self.convert_hex_2_rgb(symbolizer['stroke'])
                stroke_width = symbolizer['stroke-width']
                stroke_linejoin = symbolizer['stroke-linejoin']
                stroke_linecap = symbolizer['stroke-linecap']
                self.set_stroke_color(stroke_rgb, stroke_width, stroke_linejoin)

            elif geom_type.find("Point") != -1:
                symbolizer = rule['point_symbolizer']
                stroke_rgb = self.convert_hex_2_rgb(symbolizer['stroke'])
                stroke_width = symbolizer['stroke-width']
                if stroke_width is None or stroke_width == '': stroke_width = 1;
                self.set_stroke_color(stroke_rgb, stroke_width, "bevel")
                self.point_size = symbolizer['size']
                fill_rgb = self.convert_hex_2_rgb(symbolizer['fill'])
                self.set_fill_color(fill_rgb, 255)
        except Exception as e:
            Log_Error.log_error_message(e)
            symbolizer = None
        return symbolizer

    def convert_hex_2_rgb(self, color_hex):
        rgb = tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5))
        return rgb


class Vector2HeatMap():
    fill_color = (255, 0, 0, 255)
    format = "PNG"
    stroke_color = (38, 34, 65, 255)
    content = None

    def __init__(self, *args, **kwargs):
        self.width = args[0]['width']
        self.height = args[0]['height']
        self.map_envelop = args[0]['map_envelop']
        self.layer_envelop = args[0]['layer_envelop']
        # self.map_srid = args[0]['map_srid']
        # self.layer_srid = args[0]['layer_srid']
        # self.layer_name = args[0]['layer_name']
        self.layer_info = args[0]['layer_info']
        self.style = args[0]['style']['style']
        # self.layer_label = args[0]['layer_label']
        # self.pixel_size = args[0]['pixel_size']

        # if 'table_name' in args[0]: self.table_name = args[0]['table_name']
        # if 'app_label' in args[0]: self.app_label = args[0]['app_label']
        # if 'model_name' in args[0]: self.model_name = args[0]['model_name']
        # if 'property_name' in args[0]: self.property_name = args[0]['property_name']
        self.table_name = self.layer_info.table_name
        self.app_label = self.layer_info.app_label
        self.model_name = self.layer_info.lyr_model_name

        self.property_name = self.style['property_name']
        # self.layer_envelop = self.layer_info['extent']

        map_bbox = self.map_envelop.extent
        # self.layer_envelop.srid = '3857'
        self.img = PIL.Image.new('RGBA', (self.width, self.height), color=(255, 255, 255, 255))
        # self.img = PIL.Image.new('RGB', (width, height), color=(0, 0, 0))
        self.img_draw = ImageDraw.Draw(self.img)

        self.affine = WMS_Service.create_affine_transformation(self.width, self.height, map_bbox)
        if self.model_name is not None:
            self.content = self.createHeatMapFromModel()

    def get_img_content(self):
        if self.content == None:
            content = BytesIO()
            self.img.save(content, self.format, optimize=True)
            return content.getvalue()
        else:
            return self.content

    def get_affine_as_list(self):
        return self.affine.tolist()

    def createHeatMapFromModel(self):
        django_model = apps.get_model(app_label=self.app_label, model_name=self.model_name)
        # geom= self.layer_envelop.transform(3857,True)
        # self.map_envelop.srid = 3857
        objs = django_model.objects.filter(geom__intersects=self.map_envelop)
        # objs = django_model.objects.annotate(geom_srid=Transform('area', 3857, output_field=MultiPolygonField(srid=3857))).filter(geom_srid__intersects=self.layer_envelop)
        # objs = django_model.objects.all()[:3]
        data = []
        for obj in objs:
            res = getattr(obj, self.property_name)
            if res > 0:
                pnt = obj.geom.centroid
                sCoords = self.mapPoint_2_screenCoords(pnt)
                res = int(res)
                sCoords.append(res)
                data.append(sCoords)
                # self.draw_point(sCoords.tolist(), res)

                # heatmapper = Heatmapper()
                # print("count:" + str(res))
        # content = self.get_img_content()
        # WMS_Service.save_as_png(content)

        # s = '92,52 302,104 67,225 290,101'
        # sdata = s.split(" ")
        # data = []
        # for ln in sdata:
        #     a = ln.split(",")
        #     if len(a) != 2:
        #         continue
        #     a = [int(i) for i in a]
        #     data.append(a)

        # start painting
        hm = HeatMap(data=data, width=self.width, height=self.height)
        # # hm.clickmap(save_as="hit.png")
        # hm.heatmap(save_as="heat.png")
        self.img = hm.heatmap()
        #
        content = self.get_img_content()
        # WMS_Service.save_as_png(content, image_name="test2.png")
        return content

    def mapPoint_2_screenCoords(self, point):

        # Istr = '0 %s %s; 0 0 %s; 1 1 1' % (width, width, height)
        pStr = '%s;%s;1' % (point.coords[0], point.coords[1])
        p_matrix = numpy.matrix(pStr)
        sp_matrix = self.affine * p_matrix
        sp_list = sp_matrix.tolist()
        sCoords = [int(sp_list[0][0]), int(sp_list[1][0])]
        return sCoords

    def draw_point(self, coords, point_size):
        # map_coord = point.coords
        r = int(point_size)
        image_coord = [coords[0] - r, coords[1] - r, coords[0] + r, coords[1] + r]
        # image_coord = [coords[0][0] - r, coords[1][0] - r, coords[0][0] + r, coords[1][0] + r]
        # screen_coord = self.convert_map_point_2_screen_point(point)
        # self.img_draw.bitmap(screen_coord, self.bitmap_icon, fill=self.bitmap_color)

        self.img_draw.ellipse(image_coord, fill=self.fill_color, outline=self.stroke_color)  #
        # self.img_draw.point(screen_coord,fill=self.fill_color)

    def get_img_content(self):
        content = BytesIO()
        self.img.save(content, self.format, optimize=True)
        return content.getvalue()
