from django.contrib import admin

# Register your models here.
from ferrp.documents.models import Doc_Info


@admin.register(Doc_Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('name','title','created_by','created_at')
    search_fields = ('name', 'title','created_by')
    list_filter = ('name', 'title','created_by')