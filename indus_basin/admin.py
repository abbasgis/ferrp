from django.contrib import admin

# Register your models here.
from ferrp.indus_basin.models import *


@admin.register(Basin)
class BasinAdmin(admin.ModelAdmin):
    list_display = ('oid', 'basin_name')
    search_fields = ('basin_name',)
    list_filter = ('basin_name',)

    class Media:
        js = ('/static/assets/js/model_basin.js',)
        # css = {
        #     'all': ('/static/assets/css/admin_model.css',)
        # }


@admin.register(Drainage_Basin)
class DrainageBasinAdmin(admin.ModelAdmin):
    list_display = ('oid', 'drainage_basin_name','river_oid')
    search_fields = ('drainage_basin_name',)
    list_filter = ('drainage_basin_name',)

    class Media:
        js = ('/static/assets/js/model_drainage_basin.js',)

@admin.register(Rivers)
class RiversAdmin(admin.ModelAdmin):
    list_display = ('oid', 'river_name')
    search_fields = ('river_name',)
    list_filter = ('river_name',)
    ordering = ('-river_name',)
