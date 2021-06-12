from django.contrib import admin

# Register your models here.
from ferrp.integration.models import DatabaseConnections


@admin.register(DatabaseConnections)
class DBConnectionAdmin(admin.ModelAdmin):
    list_display = ('name','title','integrated_data')
    search_fields = ('name','title','integrated_data')
    list_filter = ('name','title','integrated_data')
