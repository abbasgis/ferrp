from django.apps import apps
from django.conf.urls import url
from django.contrib import admin, messages

# Register your models here.
from django import forms
from django.contrib.gis.db.models import Extent
from django.contrib.gis.db.models.functions import Envelope, AsGeoJSON
from django.contrib.gis.gdal import SpatialReference, DataSource
from django.contrib.gis.geos import Polygon, GEOSGeometry
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ferrp.layers.gis_migration import arz_add_srs_entry, transform_geometry
from ferrp.layers.utils import create_raster_info
from .models import *
from ferrp.local_settings import SPATIAL_EXTENT_3857, DEFAULT_PROJECTION, OVERVIEW_FACTOR
from ferrp.utils import Log_Error, DB_Query, Common_Utils, Model_Utils




@admin.register(layer_categories)
class LayerCategory(admin.ModelAdmin):
    list_display = ['id', 'category']
    search_fields = ['category']
    list_filter = ['category']


class AOIForm(forms.ModelForm):
    extent = forms.Textarea()

    class Meta:
        model = Projection
        fields = ['srid', 'name', 'proj4', 'extent', 'units', 'meter_per_unit', 'srs']


@admin.register(Projection)
class AOIAdmin(admin.ModelAdmin):
    list_display = ['srid', 'name', 'proj4', 'extent', 'units', 'meter_per_unit', 'srs']
    search_fields = ['srid', 'name']
    list_filter = ['srid', 'name']

    form = AOIForm
    save_as = True
    save_as_continue = False
    save_on_top = True
    exclude = ['units', 'meter_per_unit', 'srs']

    def save_model(self, request, obj, form, change):
        # obj.user = request.user
        if request.method == 'POST':
            form = AOIForm(request.POST)
            # if form.is_valid():
            auth_srid = int(request.POST['srid'])
            # crs = pycrs.parser.from_esri_wkt(wk)
            # crs = pycrs.parser.from_ogc_wkt(wkt,strict=True)
            # proj4 = crs.to_proj4()

            proj4 = request.POST['proj4']
            srs = SpatialReference(proj4)
            arz_add_srs_entry(srs, auth_name="ESRI", auth_srid=auth_srid, proj4=srs.proj4, wkt=srs.wkt)

            poly = Polygon.from_bbox(SPATIAL_EXTENT_3857)
            # poly.srid = DEFAULT_PROJECTION
            poly_trans = transform_geometry(poly, DEFAULT_PROJECTION, des_srid=auth_srid)
            # poly_trans.srid = auth_srid
            # poly_trans1 = geometry_transfom(poly,"3857",wkt=proj4)

            obj.srid = auth_srid
            obj.name = request.POST['name']
            obj.proj4 = request.POST['proj4']
            obj.extent = poly_trans
            obj.units = srs.units[1]
            obj.srs = srs.wkt
            obj.meter_per_unit = srs.linear_units

            try:
                super(AOIAdmin, self).save_model(request, obj, form, change)
            except Exception as e:
                Log_Error.log_error_message(e)


class Existing_Model_Info_Form():
    your_name = forms.CharField(label='Your name', max_length=100)


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'app_label', 'layer_name', 'table_name', 'layer_type', 'geom_type',
        'srid', 'orig_srid', 'extent', 'orig_extent', 'created_by', 'main_category')
    search_fields = ('name', 'app_label', 'layer_type', 'layer_name', 'created_by', 'srid')
    list_filter = ('name', 'app_label', 'layer_type', 'layer_name', 'created_by')
    change_list_template = "admin/layer_info_change_list_form.html"
    actions = ['view_layer', 'add_layer_overview']

    def view_layer(self, request, queryset):
        layer_name = queryset[0].layer_name
        return HttpResponseRedirect(reverse('view_layer') + "?layer_name=" + layer_name)

    view_layer.short_description = "View selected layers"

    def add_layer_overview(self, request, queryset):
        # layer_name= queryset[0].layer_name
        table_name = queryset[0].table_name;
        overview_list = queryset[0].rst_overview_list
        lyr_col_name = queryset[0].lyr_col_name
        if overview_list == None: overview_list = ["2"]
        col_list = DB_Query.get_fields_list(table_name)
        col_names = "ov_id SERIAL PRIMARY KEY, %s geometry, " % lyr_col_name
        for obj in col_list:
            if obj["column_name"] != "geom":
                col_names = col_names + obj["column_name"] + " json, "
        col_names = col_names[:-2]
        for level in overview_list:
            query = "Create table o_%s_%s (%s)" % (level, table_name, col_names)
            DB_Query.execute_dml(query)

        pass

    add_layer_overview.short_description = "Add Layer Overview"

    def save_model(self, request, obj, form, change):
        res = DB_Query.get_geom_extent_in_3857(obj.table_name, obj.srid, obj.layer_type)

        obj.extent = res
        try:
            super(InfoAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            Log_Error.log_error_message(e)

    def get_urls(self):
        urls = super(InfoAdmin, self).get_urls()
        my_urls = [
            url(r'^add_existing_models_info_form/$', self.admin_site.admin_view(self.add_existing_models_info_form),
                name='add_existing_models_info_form'),

            url(r'^add_existing_models_info/$', self.admin_site.admin_view(self.add_existing_models_info),
                name='add_existing_models_info'),

            url(r'^add_existing_table_info_form/$', self.admin_site.admin_view(self.add_existing_table_info_form),
                name='add_existing_table_info_form'),

        ]
        return my_urls + urls

    def add_existing_table_info_form(self, request):
        # cat_list = ['Unspecified', 'Water Resource', 'Boundaries', 'POI', 'Soil and Geology',
        #             'Infrastructure', 'Social Infrastructure', 'Climate']
        cat_list = layer_categories.objects.all().values_list('category', flat=True)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            cat_list=cat_list,
        )
        return render(request, "admin/table_add_form.html", context=context)

    def add_existing_models_info_form(self, request):
        # form = Existing_Model_Info_Form()
        app_info = Model_Utils.get_apps_with_model_name()

        cat_list = ['Unspecified', 'Water Resource', 'Boundaries', 'POI', 'Soil and Geology',
                    'Infrastructure', 'Social Infrastructure', 'Climate']
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            # key=value,
            opts=self.model._meta,
            app_info=app_info,
            cat_list=cat_list,
            # form=form
        )

        # AOIAdmin().add_view(
        #     request, '', extra_context=None)
        # return super(InfoAdmin, self).add_view(
        #     request, '', extra_context=None)
        return render(request, "admin/model_add_form.html", context=context)
        # return render(request, 'admin/model_add_form.html',context=data)

    def add_existing_table_info(self, request):
        try:
            title = request.POST.get("title")
            table_name = request.POST.get("table_name")
            main_category = request.POST.get("main_category")
            layer_type = request.POST.get("layer_type")
            col_name = request.POST.get("col_name")
            query = 'Select st_srid("%s") from "%s"' % (col_name, table_name)
            srid = DB_Query.execute_query_as_one(query)
            if layer_type == "Vector":
                query = 'Select ST_GeometryType("%s") from "%s"' % (col_name, table_name)
                geom_type = DB_Query.execute_query_as_one(query)
                layer_name = Common_Utils.add_timestamp_to_string(table_name)
                Info().insert_into_layer_info(layer_name=layer_name, title=title, table_name=table_name,
                                              layer_type=layer_type, orig_extent=None, file_path_name=None,
                                              user=request.user, srid=srid, orig_srid=srid, geom_type=geom_type,
                                              created_at=None, app_label='gis',
                                              main_category=main_category)
            else:
                for next_overview in OVERVIEW_FACTOR:
                    try:
                        query = "SELECT ST_CreateOverview('%s'::regclass, 'rast', %s)" % (table_name, next_overview)
                        res = DB_Query.execute_query_as_one(query)
                    except:
                        query = "select AddRasterConstraints('%s', 'rast')" % (table_name)
                        res = DB_Query.execute_query_as_one(query)
                        query = "SELECT ST_CreateOverview('%s'::regclass, 'rast', %s)" % (table_name, next_overview)
                        res = DB_Query.execute_query_as_one(query)
                    o_table_name = "o_" + str(next_overview) + "_" + table_name
                    query = 'ALTER TABLE %s ADD COLUMN "envelope" geometry' % o_table_name
                    res = DB_Query.execute_dml(query)
                    query = 'UPDATE %s SET "envelope"= st_envelope(rast)' % o_table_name
                    res = DB_Query.execute_dml(query)
                create_raster_info(table_name, "", request.user)

        except Exception as e:
            Log_Error.log_error_message(e)

        return super(InfoAdmin, self).changelist_view(request)

    def add_existing_models_info(self, request):
        try:
            app_label = request.POST.get("app_label")
            model_name = request.POST.get("model_name")
            val = "app_label: %s model_name:%s" % (app_label, model_name)
            if app_label is not None and model_name is not None:
                main_category = request.POST.get("main_category")
                if main_category is None:
                    main_category = 'Unspecified'
                layer_model = apps.get_model(app_label=app_label, model_name=model_name)
                layer_name = app_label + '_' + model_name
                layer_name = Common_Utils.add_timestamp_to_string(layer_name)
                table_name = layer_model._meta.db_table
                # obj_list = list(layer_model.objects.all())
                # obj = layer_model.objects.all().values('geom')[0]
                # agg_obj = layer_model.objects.aggregate(ext=Extent('geom'))
                # extent = agg_obj['ext']
                # if extent is None:
                #     extent =  SPATIAL_EXTENT_3857
                # extent = str(extent)

                objs = layer_model.objects.all()
                for obj in objs:
                    if obj.geom is not None:
                        srid = obj.geom.srid
                        geom_type = obj.geom.geom_type
                        break;
                # else:
                #     srid = 3857
                #     geom_type = None
                # obj_list = list(layer_model.objects.annotate(env=Envelope('geom')))
                # geojson = serialize('geojson', layer_model.objects.all(), geometry_field='geom',fields=('gid',))
                # ds = DataSource(geojson)
                # layer = ds[0]

                Info.insert_into_layer_info(layer_name=layer_name, title=model_name, table_name=table_name,
                                            layer_type='Vector', orig_extent=None, file_path_name=None,
                                            user=request.user, srid=srid, orig_srid=srid, geom_type=geom_type,
                                            created_at=None, app_label=app_label, lyr_model_name=model_name,
                                            main_category=main_category)
        except Exception as e:
            error_message = Log_Error.log_error_message(e)
            messages.add_message(request, messages.ERROR, error_message)
        return super(InfoAdmin, self).changelist_view(request)


@admin.register(Raster_Info)
class Raster_Info_Admin(admin.ModelAdmin):
    list_display = ('table_name', 'main_table_name', 'res_x', 'res_y', 'num_bands', 'pixel_type')
    search_fields = ('main_table_name', 'num_bands', 'pixel_type')
    list_filter = ('main_table_name', 'num_bands', 'pixel_type')

    def add_overview(self, request, queryset):
        # queryset.update(status='p')
        # table_name = request.GET.get('table_name')
        table_name = queryset[0].table_name
        layer_info = Info.objects.filter(table_name=table_name)[0]
        overviews = layer_info.rst_overview_list
        # overview_list = list(map(int, overviews))
        overview_list = list(map(int, overviews.split(",")))
        next_overview = max(overview_list) * 2
        try:
            query = "SELECT ST_CreateOverview('%s'::regclass, 'rast', %s)" % (table_name, next_overview)
            res = DB_Query.execute_query_as_one(query)
        except:
            query = "select AddRasterConstraints('%s', 'rast')" % (table_name)
            res = DB_Query.execute_query_as_one(query)
            query = "SELECT ST_CreateOverview('%s'::regclass, 'rast', %s)" % (table_name, next_overview)
            res = DB_Query.execute_query_as_one(query)
        o_table_name = "o_" + str(next_overview) + "_" + table_name
        query = 'ALTER TABLE %s ADD COLUMN "envelope" geometry' % o_table_name
        res = DB_Query.execute_dml(query)
        query = 'UPDATE %s SET "envelope"= st_envelope(rast)' % o_table_name
        res = DB_Query.execute_dml(query)
        overview_list.append(next_overview)
        Raster_Info().insert_into_raster_info(layer_info, o_table_name, table_name)
        layer_info.rst_overview_list = ','.join([str(i) for i in overview_list])
        layer_info.save()
        self.message_user(request, "successfully add next level overview.")

    add_overview.short_description = "Add Next Level Overview "
    actions = [add_overview]
