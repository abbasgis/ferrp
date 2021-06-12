import datetime
import os

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models

# Create your models here.
from ferrp.local_settings import ENTITY_TYPE, PERMISSION_TYPE
from ferrp.models import Items_Permission
from ferrp.settings import THUMBNAILS_PATH
from ferrp.utils import Common_Utils


class Map_Info(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    title = models.CharField(max_length=600)
    params = JSONField()
    created_by = models.CharField(max_length=200)
    created_at = models.DateField(null=True, blank=True)
    created_time = models.TimeField(null=True, blank=True)
    icon = models.CharField(max_length=500, null=True, blank=True)
    permissions = GenericRelation(Items_Permission, object_id_field='id', content_type_field='item_type')

    @classmethod
    def insert_or_update(cls, map_title, map_name, params, user):
        map_info = Map_Info.objects.filter(name=map_name).first()
        if map_info == None:
            map_info = Map_Info().insert_row(map_title,map_name,params,user)
        else:
            map_info.params = params
            map_info.save()

        return map_info

    def insert_row(self, map_title, map_name, params, user):
        # map_name = Common_Utils.add_timestamp_to_string(map_title)
        self.title = map_title
        self.name = map_name
        self.params = params
        self.created_by = user
        now = datetime.datetime.now()
        self.created_at = now.strftime("%Y-%m-%d")
        self.created_time = now.strftime("%H:%M:%S-%Z")
        self.save()
        Items_Permission.insert_or_update_row(self, map_name, user, 'U', 'O')
        return self

    def update_icon(self, icon_url, map_name):
        # img = Common_Utils.pdf_page_to_png(document_path)
        # icon_path_name = os.path.join(THUMBNAILS_PATH, document_name)
        # img.save(icon_path_name, 'png')
        objs = list(self.objects.filter(name=map_name))
        if len(objs) > 0:
            obj = objs[0]
            obj.icon_path = icon_url
            obj.save()


# class Map_Permission(models.Model):
#     id = models.AutoField(primary_key=True)
#     save_info_id = models.ForeignKey(Save_Info, on_delete=models.CASCADE)
#     map_name = models.CharField(max_length=300)
#     entity_name = models.CharField(max_length=100)
#     entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE)
#     permission_type = models.CharField(max_length=25, choices=PERMISSION_TYPE)
#
#     def insert_row(self, save_info, map_name, entity_name, entity_type, permission_type):
#         self.save_info_id = save_info
#         self.map_name = map_name
#         self.entity_name = entity_name
#         self.entity_type = entity_type
#         self.permission_type = permission_type
#         self.save()


class TblAdminHierarchy(models.Model):
    admin_name = models.CharField(max_length=64, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    admin_level = models.IntegerField(blank=True, null=True)
    admin_level_name = models.CharField(max_length=256, blank=True, null=True)
    code_from_table = models.CharField(max_length=256, blank=True, null=True)
    name_from_table = models.CharField(max_length=256, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    extent = models.GeometryField(blank=True, null=True)
    # geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    # extent = models.TextField(blank=True, null=True)  # This field type is a guess.
    level_complete_code = models.CharField(max_length=256, blank=True, null=True)
    extent_boundary = models.CharField(max_length=256, blank=True, null=True)

    # id = models.BigAutoField()

    class Meta:
        managed = False
        db_table = 'tbl_admin_hierarchy'
