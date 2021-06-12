from decimal import Decimal

import datetime
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db.models import Extent
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models

# Create your models here.
from ferrp.integration.models import GenericGeomModel, DatabaseConnections
from ferrp.models import Items_Permission
from ferrp.utils import Common_Utils, DB_Query, SPATIAL_EXTENT_3857

class layer_categories(models.Model):
    # id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.category

class Info(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    layer_name = models.CharField(null=True, max_length=200)
    table_name = models.CharField(max_length=200)
    layer_type = models.CharField(null=True, max_length=100)
    geom_type = models.CharField(max_length=30, null=True,blank=True)
    srid = models.IntegerField()
    orig_srid = models.IntegerField(null=True, blank=True)
    extent = models.TextField(null=True, blank=True)
    orig_extent = models.CharField(null=True, blank=True, max_length=200)
    created_by = models.CharField(max_length=200)
    upload_at = models.DateField(null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    # icon = models.ImageField(null=True, blank=True)
    lyr_model_name = models.CharField(max_length=200,null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    icon = models.CharField(max_length=500, null=True, blank=True)
    style = JSONField(null=True, blank=True)
    label = JSONField(null=True, blank=True)
    main_category = models.ForeignKey(layer_categories, db_column='main_category', to_field= 'category',max_length=500, null=True,
                                      default='Unspecified', on_delete=models.DO_NOTHING)
    permissions = GenericRelation(Items_Permission, object_id_field='id', content_type_field='item_type')
    app_label = models.CharField(max_length=100, null=True, default='gis')
    rst_overview_list = models.CharField(max_length=100, null=True, blank=True, default='2,4,8')
    isNetwork = models.BooleanField(default=False)
    lyr_col_name = models.CharField(max_length=100, null=True, default="geom")
    remote_conn_name = models.ForeignKey('integration.DatabaseConnections',on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.app_label+":"+ self.table_name


    @classmethod
    def insert_into_layer_info(cls, layer_name, title, table_name, layer_type, orig_extent, file_path_name, user,
                               srid=None, orig_srid=None, geom_type=None,
                               created_at=None, app_label='gis', lyr_model_name=None,
                               main_category='Unspecified', rst_overview_list=None, lyr_col_name=None,
                               remote_conn_name=None, extent=None):
        uploaded_at = datetime.datetime.now().strftime("%Y-%m-%d")
        # if orig_extent == None:
        #     # res = Info.calculate_model_extent_srid(cls, model, geom, model_geom_col_name='geom')
        #     orig_extent = SPATIAL_EXTENT_3857[1:len(SPATIAL_EXTENT_3857)-1]
        #     orig_srid = 3857
        if extent == None:
            extent = DB_Query.get_geom_extent_in_3857(table_name=table_name, srid=orig_srid, layer_type=layer_type,
                                                      app_label=app_label) if orig_srid != 3857 or orig_extent is None else orig_extent

        if layer_type == "Raster" and lyr_col_name is None: lyr_col_name = "rst"
        if layer_type == "Vector" and lyr_col_name is None: lyr_col_name = "rst"
        if layer_type == "Raster" and rst_overview_list is None: rst_overview_list = "2,4,8"
        layer_info = Info(layer_name=layer_name, name=title, table_name=table_name, layer_type=layer_type,
                          geom_type=geom_type, srid=srid, extent=extent, orig_srid=orig_srid, orig_extent=orig_extent,
                          created_by=user,
                          upload_at=uploaded_at, created_at=created_at, file_path=file_path_name,
                          app_label=app_label, lyr_model_name=lyr_model_name, main_category=main_category,
                          rst_overview_list=rst_overview_list, lyr_col_name=lyr_col_name,remote_conn_name=remote_conn_name)

        layer_info.save()

        Items_Permission.insert_or_update_row(layer_info,
                                              layer_name, entity_name=user, entity_type='U', permission_type='O')
        # Items_Permission().insert_row(item_info=layer_info, item_name=layer_info.name,
        #                               entity_name=user, entity_type='U', permission_type='O')

        return layer_info

    @classmethod
    def delete_layer_info(cls, layer_name):
        obj_list = list(Info.objects.filter(layer_name=layer_name))
        if len(obj_list) > 0:
            obj_list[0].delete()

    @classmethod
    def convert_spatial_table_into_layer_info(cls, app_label, table_name, user, main_category, spatial_key_column=None):
        if spatial_key_column is None: spatial_key_column = DB_Query.get_spatial_and_key_column(app_label, table_name)
        g_model = GenericGeomModel.set_spatial_model(app_label, table_name, spatial_key_column)
        objs = g_model.objects.all()[:1]
        obj = objs[0] if objs.count() > 0 else None
        layer_name = None
        if obj is not None:
            layer_name = Common_Utils.add_timestamp_to_string(table_name)
            title = table_name.replace("_", " ")
            layer_type = "Vector"
            res = Info.calculate_model_extent_srid(g_model, obj.geom)
            orig_extent = res['orig_extent']  # GenericGeomModel.objects.aggregate(Extent('geom'))
            orig_srid = res['orig_srid']
            srid = orig_srid
            extent = orig_extent
            geom_type = obj.geom.geom_type
            created_at = datetime.datetime.now().strftime(
                "%Y-%m-%d")  # str(datetime.datetime.now().strftime('YYYY-MM-DD'))
            # app_label = GenericGeomModel._meta.app_label
            from ferrp import settings
            db_obj = DatabaseConnections.objects.filter(name = settings.REMOTE_CONN_NAME).first()
            lyr_col_name = spatial_key_column['geom_field']
            Info.insert_into_layer_info(layer_name, title, table_name, layer_type, orig_extent, None,
                                        user, srid, orig_srid, geom_type, created_at, app_label, None,
                                        main_category, None, lyr_col_name,db_obj, extent=extent)
        return layer_name

    @classmethod
    def calculate_model_extent_srid(cls, model, geom, model_geom_col_name='geom'):

        res = {}
        objs = []
        extent = model.objects.aggregate(Extent(model_geom_col_name))
        srid = geom.srid
        if srid is None or srid in ['0']:
            try:
                extent_polygon = Polygon.from_bbox(extent["geom__extent"])
                objs = Projection.objects.filter(extent__contains=extent_polygon)
            except Exception as e:
                objs = Projection.objects.filter(srid=geom.srid)
                if objs.count() > 0:
                    val = str(objs[0].extent.extent)
                    extent = val[1:len(val) - 1]
            if objs.count() > 0:
                obj = objs[0]
                res['orig_extent'] = extent
                res['orig_srid'] = obj.srid
            else:
                val = str(SPATIAL_EXTENT_3857)
                res['orig_extent'] = val[1:len(val) - 1]

                res['orig_srid'] = 3857
        else:
            val = str(extent["geom__extent"])
            res['orig_extent'] = val[1:len(val) - 1]
            res['orig_srid'] = geom.srid
        return res


# class Permission(models.Model):
#     id = models.AutoField(primary_key=True)
#     Info_id = models.ForeignKey(Info, on_delete=models.CASCADE, blank=True, null=True)
#     layer_name = models.CharField(max_length=300)
#     entity_name = models.CharField(max_length=100)
#     entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE)
#     permission_type = models.CharField(max_length=25, choices=PERMISSION_TYPE)


class Projection(models.Model):
    id = models.AutoField(primary_key=True)
    srid = models.IntegerField()
    name = models.CharField(max_length=100)
    proj4 = models.CharField(max_length=300)
    srs = models.TextField()
    extent = models.PolygonField(srid=0)
    units = models.CharField(max_length=100, null=True, blank=True)
    meter_per_unit = models.FloatField(null=True, blank=True)


class Raster_Info(models.Model):
    id = models.AutoField(primary_key=True)
    Info_id = models.ForeignKey(Info, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=200)
    main_table_name = models.CharField(max_length=200)
    res_x = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal('0.0000'))
    res_y = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal('0.0000'))
    num_bands = models.IntegerField(blank=True, null=True)
    pixel_type = models.CharField(max_length=30, blank=True, null=True)

    def insert_into_raster_info(self, Info, table_name, main_table_name):
        res = Common_Utils.get_raster_paramenters(table_name)
        if Info.srid == 4326:
            pixwidth = float(res['pixwidth']) * 110 * 1000
            pixheight = float(res['pixheight']) * 110 * 1000
        else:
            pixheight = res['pixheight']
            pixwidth = res['pixwidth']
        self.Info_id = Info
        self.table_name = table_name
        self.main_table_name = main_table_name
        self.res_x = pixwidth
        self.res_y = pixheight
        self.num_bands = res['numbands']
        self.pixel_type = res['ptype']
        self.save()
