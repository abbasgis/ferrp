from django.contrib import admin

# Register your models here.
from ferrp.maps.models import Map_Info


@admin.register(Map_Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('name','title', 'params','created_by','created_at','created_time')
    search_fields = ('name', 'title','created_by')
    list_filter = ('name', 'title','created_by')