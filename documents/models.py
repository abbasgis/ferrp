import datetime
import os

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from ferrp.local_settings import ENTITY_TYPE, PERMISSION_TYPE
from ferrp.models import Items_Permission
from ferrp.settings import THUMBNAILS_PATH, THUMBNAILS_URL
from ferrp.utils import Common_Utils


class Doc_Info(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=500)

    file_extension = models.CharField(max_length=100, default='pdf')

    upload_date = models.DateField()
    upload_time = models.TimeField()
    icon = models.CharField(max_length=500, null=True)

    created_by = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateField(null=True, blank=True)
    permissions = GenericRelation(Items_Permission, object_id_field='id', content_type_field='item_type')

    def insert_row(self, name, title, path, created_by, created_at=None, icon_path=None, extension="pdf"):
        # obj = self(name=name,title=title,path=path,icon_path=icon_path)
        self.name = name
        self.title = title
        self.path = path
        now = datetime.datetime.now()
        self.upload_date = now.strftime("%Y-%m-%d")
        self.upload_time = now.strftime("%H:%M:%S-%Z")
        self.created_by = created_by
        self.create_at = created_at
        self.icon = icon_path
        self.file_extension = extension
        self.save()
        Items_Permission().insert_row(item_info=self, item_name=self.name, entity_name=self.created_by,
                                entity_type='U', permission_type='O')

    def update_icon(self, document_name, document_path):
        img = Common_Utils.pdf_page_to_png(document_path)
        icon_path_name = os.path.join(THUMBNAILS_PATH, document_name)
        icon_url = os.path.join(THUMBNAILS_URL, document_name + '.png')

        img.save(icon_path_name, 'png')
        objs = list(self.objects.filter(name=document_name))
        if len(objs) > 0:
            obj = objs[0]
            obj.icon_path = icon_path_name
            obj.save()


# class Permission(models.Model):
#     id = models.AutoField(primary_key=True)
#     info_id = models.ForeignKey(Info, on_delete=models.CASCADE, blank=True, null=True)
#     doc_name = models.CharField(max_length=300)
#     entity_name = models.CharField(max_length=100)
#     entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE)
#     permission_type = models.CharField(max_length=25, choices=PERMISSION_TYPE)
#
#     def insert_row(self, info, document_name, entity_name, entity_type, permission_type):
#         self.info_id = info
#         self.doc_name = document_name
#         self.entity_name = entity_name
#         self.entity_type = entity_type
#         self.permission_type = permission_type
#         self.save()