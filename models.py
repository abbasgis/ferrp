import datetime

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField

from ferrp.local_settings import ENTITY_TYPE, PERMISSION_TYPE


class RightsSupport(models.Model):
    class Meta:
        managed = False
        permissions = (
            ('fileupload', 'File Upload Rights'),
        )


class Activity_Log(models.Model):
    user_name = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=100, null=True)
    app_label = models.CharField(max_length=100)
    view_name = models.CharField(max_length=100)
    view_des = models.CharField(max_length=600, null=True, blank=True)
    error_des = models.CharField(max_length=600, null=True, blank=True)
    access_date = models.DateField(blank=True, null=True)
    access_time = models.TimeField(blank=True, null=True)
    url = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    params_get = JSONField(null=True, blank=True)
    params_post = JSONField(null=True, blank=True)

    def insert_into_activity_log(self, request, app_label, view_name, view_des=None, url=None, completed=False):
        self.user_name = request.user.username
        self.dept_name = request.user.groups.name
        self.app_label = app_label
        self.view_name = view_name
        self.view_des = view_des
        self.url = url
        now = datetime.datetime.now()
        self.access_date = now.strftime("%Y-%m-%d")
        self.access_time = now.strftime("%H:%M:%S-%Z")
        self.completed = completed
        self.params_get = request.GET
        self.params_post = request.POST
        # act_log = Activity_Log(user_name=user_name,dept_name=dept_name, app_label=app_label, view_name=view_name, view_des=view_des,
        #                        url=url, completed=completed, params_get=params_get,params_post=params_post)
        # act_log.save()
        self.save()
        pass

    def update_error_desc(self, error_message):
        self.error_des = error_message
        self.save()

    def update_complete_status(self):
        self.completed = True
        self.save()


class Items_Permission(models.Model):
    id = models.AutoField(primary_key=True)
    # info_id = models.PositiveIntegerField() #models.ForeignKey(Save_Info, on_delete=models.CASCADE)
    # info_app_label =models.CharField(max_length=100)
    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField()
    item_object = GenericForeignKey('item_type', 'item_id')
    item_name = models.CharField(max_length=300)
    entity_name = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE)
    permission_type = models.CharField(max_length=25, choices=PERMISSION_TYPE)

    @classmethod
    def insert_or_update_row(cls, item_object, item_name, entity_name, entity_type, permission_type):
        ip_list = Items_Permission.get_rows_list(item_object, item_name, entity_name, entity_type, permission_type)

        if len(ip_list) == 0:
            Items_Permission().insert_row(item_object, item_name, entity_name, entity_type, permission_type)
        else:
            ip_obj = ip_list[0]
            ip_obj.permission_type = permission_type
            ip_obj.save()

    @classmethod
    def get_rows_list(cls, item_object, item_name, entity_name, entity_type, permission_type):
        item_type = ContentType.objects.get_for_model(item_object)
        ip_list = list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                       item_name=item_name, entity_name=entity_name,
                                                       entity_type=entity_type, permission_type=permission_type))
        # if len(ip_list)==0:
        #     ip_obj = Items_Permission()
        # else:
        #     ip_obj =ip_list[0]
        return ip_list

    def insert_row(self, item_info, item_name, entity_name, entity_type, permission_type):
        self.item_object = item_info
        self.item_name = item_name
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.permission_type = permission_type
        self.save()
        return self

    @classmethod
    def delete_item_permission(cls, item_object, item_name, request, d_or_s_permission_type='D'):
        view_users = request.GET.get("view_users_remove").split(',')
        view_depts = request.GET.get("view_depts_remove").split(',')
        download_users = request.GET.get("download_users_remove").split(',')
        download_departs = request.GET.get("download_depts_remove").split(',')
        item_type = ContentType.objects.get_for_model(item_object)
        for vu in view_users:
            if vu != "-1":
                permission_type = 'V'
                # if vu == "Public": permission_type = 'P'
                obj = list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                           item_name=item_name,
                                                           entity_name=vu,
                                                           entity_type='U', permission_type=permission_type))
                if len(obj) > 0: obj[0].delete()
        for vd in view_depts:
            if vd != "-1":
                permission_type = 'V'
                # if vd == "Public": permission_type = 'P'
                obj = list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                           item_name=item_name,
                                                           entity_name=vd,
                                                           entity_type='D', permission_type=permission_type))
                if len(obj) > 0: obj[0].delete()
        for du in download_users:
            if du != "-1":
                # if du == "Public": d_or_s_permission_type = 'P'
                obj = list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                           item_name=item_name,
                                                           entity_name=du,
                                                           entity_type='U',
                                                           permission_type=d_or_s_permission_type))
                if len(obj) > 0: obj[0].delete()
        for dd in download_departs:
            if dd != "-1":
                # if dd == "Public": d_or_s_permission_type = 'P'
                obj = list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                           item_name=item_name,
                                                           entity_name=dd,
                                                           entity_type='D',
                                                           permission_type=d_or_s_permission_type))
                if len(obj) > 0: obj[0].delete()


    @classmethod
    def set_item_permission(cls, item_object, item_name, request, d_or_s_permission_type='D'):
        view_users = request.GET.get("view_users_add").split(',')
        view_depts = request.GET.get("view_depts_add").split(',')
        download_users = request.GET.get("download_users_add").split(',')
        download_departs = request.GET.get("download_depts_add").split(',')
        item_type = ContentType.objects.get_for_model(item_object)
        # perms_list = list(Permission.objects.filter(layer_name=layer_name))
        for vu in view_users:
            if vu != "-1":
                permission_type = 'V'
                # if vu == "Public": permission_type = 'P'
                available = len(list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                                     item_name=item_name,
                                                                     entity_name=vu,
                                                                     entity_type='U',
                                                                     permission_type=permission_type))) > 0
                if not available:
                    Items_Permission().insert_row(item_info=item_object, item_name=item_name, entity_name=vu,
                                                  entity_type='U', permission_type=permission_type)
        for vd in view_depts:
            if vd != "-1":
                permission_type = 'V'
                # if vd == "Public": permission_type = 'P'
                available = len(list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                                     item_name=item_name,
                                                                     entity_name=vd,
                                                                     entity_type='D',
                                                                     permission_type=permission_type))) > 0
                if not available:
                    Items_Permission().insert_row(item_info=item_object, item_name=item_name, entity_name=vd,
                                                  entity_type='D', permission_type=permission_type)
        for du in download_users:
            if du != "-1":
                # if du == "Public": d_or_s_permission_type = 'P'
                available = len(list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                                     item_name=item_name,
                                                                     entity_name=du,
                                                                     entity_type='U',
                                                                     permission_type=d_or_s_permission_type))) > 0
                if not available:
                    Items_Permission().insert_row(item_info=item_object, item_name=item_name, entity_name=du,
                                                  entity_type='U', permission_type=d_or_s_permission_type)
        for dd in download_departs:
            if dd != "-1":
                # if dd == "Public": d_or_s_permission_type = 'P'
                available = len(list(Items_Permission.objects.filter(item_type__pk=item_type.id, item_id=item_object.id,
                                                                     item_name=item_name,
                                                                     entity_name=dd,
                                                                     entity_type='D',
                                                                     permission_type=d_or_s_permission_type))) > 0
                if not available:
                    Items_Permission().insert_row(item_info=item_object, item_name=item_name, entity_name=dd,
                                                  entity_type='D', permission_type=d_or_s_permission_type)
