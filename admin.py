from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from ferrp.layers.models import Info
from ferrp.models import Items_Permission
from ferrp.maps.models import Map_Info

admin.site.login_template = 'registration/login.html'

# add_missing_owner_permission.short_description = "Add Missing Owner Permissions"

@admin.register(Items_Permission)
class ItemsPermissionAdmin(admin.ModelAdmin):
    list_display = ('item_object','item_name', 'entity_name','entity_type','permission_type')
    search_fields = ('item_name', 'entity_name')
    list_filter = ('item_name', 'entity_name')
    # actions = [add_missing_owner_permission]
    change_list_template = "admin/items_permission_change_list.html"

    def get_urls(self):
        urls = super(ItemsPermissionAdmin, self).get_urls()
        my_urls = [url(r'^missing_owner_permission/$',self.add_missing_owner_permission,name='add_missing_owners_permission')]
        return my_urls + urls

    # @staff_member_required
    def add_missing_owner_permission(self, request):
        layer_items = Info.objects.all()
        for item_info in layer_items:
            Items_Permission.insert_or_update_row(item_info, item_info.layer_name, entity_name=item_info.created_by,
                                                  entity_type='U', permission_type='O')
        map_items = Map_Info.objects.all()
        for item_info in map_items:
            Items_Permission.insert_or_update_row(item_info, item_info.name, entity_name=item_info.created_by,
                                                  entity_type='U', permission_type='O')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
