# from django.db import models
import datetime
from django.contrib.gis.db import models
# Create your models here.
from django.contrib.postgres.fields import JSONField

from ferrp.models import Items_Permission


class GenericGeomModel(models.Model):
    class Meta:
        managed = False
        app_label = 'remote_app'
        db_table = ''

    @classmethod
    def set_spatial_model(cls, app_label, table_name, spatial_key_column):
        attrs = {
            'id': models.AutoField(primary_key=True, db_column=spatial_key_column['id']),
            'geom': models.GeometryField(null=True, blank=True, db_column=spatial_key_column['geom_field']),
            '__module__': 'ferrp.integration'
        }
        g_model = type("GenericGeomModel", (models.Model,), attrs)
        g_model._meta.db_table = table_name
        g_model._meta.app_label = app_label
        return g_model

class DatabaseConnections(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, unique=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    con_string = JSONField()
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(blank=True,null=True)
    integrated_data = JSONField(null=True,blank=True)


    def insert_row(self, name, title, conn_string,user):
        self.name = name
        self.title = title
        self.con_string = conn_string
        self.created_by = user
        self.created_at = datetime.datetime.now()
        self.save()
        Items_Permission().insert_row(item_info=self, item_name=self.name, entity_name=self.created_by,
                                      entity_type='U', permission_type='O')

    def update_integrated_data(self,integrated_info):
        self.integrated_data = integrated_info
        self.save()