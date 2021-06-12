from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Projects(models.Model):
    PROJECT_TYPE = (
        ('local', 'Local'),
        ('foreign', 'Foreign'),
    )
    id = models.AutoField(primary_key=True)
    project_id = models.CharField(unique=True, max_length=100)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    project_name_short = models.CharField(max_length=255)
    project_type = models.CharField(max_length=50, blank=True, null=True, choices=PROJECT_TYPE)
    project_addby = models.IntegerField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.project_name

    class Meta:
        managed = True
        # db_table = 'tbl_projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['project_name']


class Directory(MPTTModel):
    dir_id = models.AutoField(primary_key=True)
    dir_name = models.CharField(max_length=255)
    dir_level = models.IntegerField()
    parent_dir_id = TreeForeignKey('self', null=True, blank=True, db_column='parent_dir_id', related_name='children',
                                   db_index=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    project_id = models.CharField(max_length=100)
    dir_path = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_title = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    lft = models.IntegerField(blank=True, null=True)
    rght = models.IntegerField(blank=True, null=True)
    tree_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.dir_name

    def _get_parent_id(self):
        return self.parent_dir_id

    class MPTTMeta:
        level_attr = 'dir_level'
        name_attr = 'dir_name'
        parent_attr = 'parent_dir_id'

    class Meta:
        managed = True
        # db_table = 'tbl_directory'
        verbose_name = 'Directories'
        unique_together = (('dir_id', 'project_id'),)
        # ordering = ['act_enddate', 'act_startdate']


class DirectoryTemplate(MPTTModel):
    dir_id = models.AutoField(primary_key=True)
    dir_name = models.CharField(max_length=255)
    dir_level = models.IntegerField()
    parent_dir_id = TreeForeignKey('self', null=True, blank=True, db_column='parent_dir_id', related_name='children',
                                   db_index=True)
    act_addby = models.IntegerField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    dir_path = models.CharField(max_length=255, blank=True, null=True)
    lft = models.IntegerField(blank=True, null=True)
    rght = models.IntegerField(blank=True, null=True)
    tree_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.dir_name

    def _get_parent_id(self):
        return self.parent_dir_id

    class MPTTMeta:
        level_attr = 'dir_level'
        name_attr = 'dir_name'
        parent_attr = 'parent_dir_id'

    class Meta:
        managed = False
        verbose_name = 'Directory Template'


class Files(models.Model):
    id = models.AutoField(primary_key=True)
    file_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    file_id = models.PositiveIntegerField()
    file_object = GenericForeignKey('file_type', 'file_id')
    file_name = models.CharField(max_length=300)
    file_title = models.CharField(max_length=300)
    dir_id = models.ForeignKey(Directory, models.CASCADE, db_column='dir_id')
    project_id = models.ForeignKey(Projects, models.CASCADE, db_column='project_id')

    @classmethod
    def get_rows_list(cls, item_object, item_name, dir_id):
        item_type = ContentType.objects.get_for_model(item_object)
        ip_list = list(Files.objects.filter(file_type__pk=item_type.id, file_id=item_object.id,
                                            file_name=item_name, dir_id=dir_id))
        # if len(ip_list)==0:
        #     ip_obj = Items_Permission()
        # else:
        #     ip_obj =ip_list[0]
        return ip_list

    def insert_row(self, file_info_obj, file_name, project_id_obj, dir_id_obj):
        self.file_object = file_info_obj
        self.file_name = file_name
        self.dir_id = dir_id_obj
        self.project_id = project_id_obj
        self.save()
        return self

    class Meta:
        managed = True
        verbose_name = 'Files'
