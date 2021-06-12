from decimal import Decimal
from django.contrib import admin, messages

# Register your models here.
from django.contrib.admin import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from simple_history.admin import SimpleHistoryAdmin

from ferrp.projects.models import Projects, Directory, DirectoryTemplate, Files
from ferrp.projects.views import add_project_in_db_from_admin


class DCHAdminSite(AdminSite):
    site_header = 'Data Clearinghouse Administration'
    login_template = 'registration/login.html'
    # app_index_template = 'admin/app_index_template.html'
    # index_template = 'admin/index_template.html'


admin_site = DCHAdminSite(name='admin_dch')


class TblProjectsAdmin(SimpleHistoryAdmin):
    change_form_template = 'admin/tbl_add_project_template.html'
    # prepopulated_fields = {"project_name": ("project_id",)}
    list_display = (
        'project_id', 'set_directories', 'project_name', 'project_name_short')
    history_list_display = ['project_id', 'project_name', 'project_name_short']
    search_fields = ('project_name', 'project_id')
    list_filter = ('project_id', 'project_name',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    fields = (
        'project_id', 'project_name', 'project_name_short')
    readonly_fields = ('project_id',)
    actions = None

    def set_directories(self, obj):
        # url = 'http://localhost:88/admin/ppms/tblusersprojects/?gs_no__project_id=1910'
        url = '/admin_dch/projects/directory/?project_id=' + obj.project_id
        return '<a href="' + url + '" target="_blank">Click for Directories</a>'

    set_directories.allow_tags = True

    # def get_fields(self, request, obj=None):
    #     if obj.project_id == '8119':
    #         return ('project_id', 'project_name',)
    #     return ('project_id', 'project_name', 'project_startdate', 'project_enddate', 'project_disbursement_total',
    #             'project_expenditure_total',)

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.project_addby:
            instance.project_addby = user.id
            add_project_in_db_from_admin(instance, request)
        instance.updated_by = user.id
        instance.save()
        form.save_m2m()
        return instance

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        return True

    def set_permission(self, obj):
        # url = 'http://localhost:88/admin/ppms/tblusersprojects/?gs_no__project_id=1910'
        url = '/ppms/permission_assign/?project_id=' + obj.project_id
        return '<a href="' + url + '" target="_blank">Click for Permissions</a>'

    set_permission.allow_tags = True
    app_index = 'admin/app_index_template.html'
    app_index_template = 'admin/app_index_template.html'
    index_template = 'admin/index_template.html'

    # def get_queryset(self, request):
    #     qs = super(TblProjectsAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(project_addby=request.user.id)


admin.site.register(Projects, TblProjectsAdmin)
admin_site.register(Projects, TblProjectsAdmin)


class DirectoryAdmin(DraggableMPTTAdmin, SimpleHistoryAdmin):
    # resource_class = TblActivitiesResource
    list_display = ('tree_actions', 'dir_name_tree', 'add', 'edit', 'dir_level', 'file_size', 'file_type')
    history_list_display = ['dir_name', 'dir_level', "status"]
    list_display_links = ('edit',)
    list_filter = ('dir_level',)
    search_fields = ('dir_name', 'dir_id',)
    edit_fieldsets = (
        'parent_dir_id', 'dir_name',)
    add_fieldsets = ('parent_dir_id', 'dir_name',)
    readonly_fields = ('parent_dir_id', 'dir_id', 'project_id',)
    # ordering = ('tree_id',)
    mptt_level_indent = 25
    save_as_continue = False
    actions = ['view_file', 'download_file', 'upload_documents_action', 'upload_shapefile_action',
               'upload_raster_action', 'upload_map_action']

    # def view_file(self, obj):
    #     # url = 'http://localhost:88/admin/ppms/tblusersprojects/?gs_no__project_id=1910'
    #     url = str(obj.dir_path)
    #     return '<a href="' + url + '" target="_blank">Click for Permissions</a>'
    #
    # view_file.allow_tags = True

    def dir_name_tree(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.dir_name,  # Or whatever you want to put here
        )

    def add(self, obj):
        url = 'add/?dir_id=' + str(obj.dir_id)
        return '<b><a href="' + url + '"><img src="/static/assets/img/add.png" alt="Add"></a></b>'

    def edit(self, obj):
        if obj.is_leaf_node():
            url = 'add/?dir_id=' + str(obj.dir_id)
            return '<img src="/static/assets/img/pencil.png" alt="Edit">'
        else:
            return ''

    add.allow_tags = True
    edit.allow_tags = True

    def view_file(self, request, queryset):
        project_id = self.project_id
        rs = list(queryset)
        selected = len(rs)
        if selected == 0 or selected > 1:
            self.message_user(request, "You Have Selected " + str(selected) + ' rows, please select only one row',
                              level=messages.WARNING)
        else:
            file = Files.objects.filter(file_name=rs[0].file_name).get()
            file_type = file.file_type.model
            url = ''
            if file_type == 'doc_info':
                url = reverse("view_document") + "?doc_name=" + rs[0].file_name
            if file_type == 'info':
                url = reverse("view_layer") + "?layer_name=" + rs[0].file_name

            return HttpResponseRedirect(url)
            # self.message_user(request, "Picture Updated Successfully", level=messages.INFO)

    view_file.short_description = "View File"
    view_file.acts_on_all = True

    def download_file(self, request, queryset):
        project_id = self.project_id
        rs = list(queryset)
        selected = len(rs)
        if selected == 0 or selected > 1:
            self.message_user(request, "You Have Selected " + str(selected) + ' rows, please select only one row',
                              level=messages.WARNING)
        else:
            file = Files.objects.filter(file_name=rs[0].file_name).get()
            file_type = file.file_type.model
            url = ''
            if file_type == 'doc_info':
                url = reverse("download_document") + "?doc_name=" + rs[0].file_name
            if file_type == 'info':
                url = reverse("lyr_download") + "?layer_name=" + rs[0].file_name
            return HttpResponseRedirect(url)
            # self.message_user(request, "Picture Updated Successfully", level=messages.INFO)

    download_file.short_description = "Download File"
    download_file.acts_on_all = True

    def upload_documents_action(self, request, queryset):
        project_id = self.project_id
        rs = list(queryset)
        selected = len(rs)
        if selected == 0 or selected > 1:
            self.message_user(request, "You Have Selected " + str(selected) + ' rows, please select only one row',
                              level=messages.WARNING)
        else:
            return HttpResponseRedirect(
                "/documents/doc_upload/?project_id=" + rs[0].project_id + '&dir_id=' + str(rs[0].dir_id))
            # self.message_user(request, "Picture Updated Successfully", level=messages.INFO)

    upload_documents_action.short_description = "Upload Document"
    upload_documents_action.acts_on_all = True

    def upload_shapefile_action(self, request, queryset):
        project_id = self.project_id
        rs = list(queryset)
        selected = len(rs)
        if selected == 0 or selected > 1:
            self.message_user(request, "You Have Selected " + str(selected) + ' rows, please select only one row',
                              level=messages.WARNING)
        else:
            return HttpResponseRedirect(
                "/layers/upload/shp/?project_id=" + rs[0].project_id + '&dir_id=' + str(rs[0].dir_id))
            # self.message_user(request, "Picture Updated Successfully", level=messages.INFO)

    upload_shapefile_action.short_description = "Upload Shapefile"
    upload_shapefile_action.acts_on_all = True

    def upload_raster_action(self, request, queryset):
        project_id = self.project_id
        rs = list(queryset)
        selected = len(rs)
        if selected == 0 or selected > 1:
            self.message_user(request, "You Have Selected " + str(selected) + ' rows, please select only one row',
                              level=messages.WARNING)
        else:
            return HttpResponseRedirect(
                "/layers/upload/raster/?project_id=" + rs[0].project_id + '&dir_id=' + str(rs[0].dir_id))
            # self.message_user(request, "Picture Updated Successfully", level=messages.INFO)

    upload_raster_action.short_description = "Upload Raster"
    upload_raster_action.acts_on_all = True

    def upload_map_action(self, request, queryset):
        project_id = self.project_id
        rs = list(queryset)
        selected = len(rs)
        if selected == 0 or selected > 1:
            self.message_user(request, "You Have Selected " + str(selected) + ' rows, please select only one row',
                              level=messages.WARNING)
        else:
            return HttpResponseRedirect(
                "/maps/create_map/?project_id=" + rs[0].project_id + '&dir_id=' + str(rs[0].dir_id))
            # self.message_user(request, "Picture Updated Successfully", level=messages.INFO)

    upload_map_action.short_description = "Create Map"
    upload_map_action.acts_on_all = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        # if 'delete_selected' in actions:
        #    del actions['delete_selected']
        return actions

    project_id = ''

    def get_form(self, request, obj=None, **kwargs):
        form = super(DirectoryAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            dir_id = request.GET.get('dir_id')
            form.base_fields['parent_dir_id'].initial = dir_id
            #    self.readonly_fields=['parent_dir_id']
            # return ActivityAddForm
        return form

    def get_queryset(self, request):
        project_id = request.GET.get('project_id', '1')
        if self.project_id is None or self.project_id != project_id and project_id != '1':
            self.project_id = project_id
        else:
            project_id = self.project_id
        qs = super(DirectoryAdmin, self).get_queryset(request)
        if request.user.is_superuser and project_id == '1':
            return qs
        else:
            if project_id == 1 or project_id == '':
                arr_project_id = ['9356']  # get_projects_list_assign_to_users_or_groups(request.user.id)
                # return qs.filter(project_id__in=arr_project_id)
                return qs
            else:
                return qs.filter(project_id=project_id)

    def changelist_view(self, request, extra_context=None):
        project_id = request.GET.get('_changelist_filters', '1')
        project_id = project_id.replace("project_id=", "")
        post = request.POST.copy()
        if admin.helpers.ACTION_CHECKBOX_NAME not in post:
            post.update({admin.helpers.ACTION_CHECKBOX_NAME: None})
            request._set_post(post)
        project_id = request.GET.get('project_id', '1')
        if project_id == '1':
            project_id = self.project_id
        extra_context = extra_context or {}
        extra_context['project_id'] = project_id
        return super(DirectoryAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = self.add_fieldsets
        self.readonly_fields = []
        if not 'dir_id' in request.GET:
            self.message_user(request,
                              "Items must be selected in order to perform actions on them. No items have been changed",
                              level=messages.ERROR)
            return HttpResponseRedirect("/admin/projects/directory/")

        project_id = request.GET.get('project_id', '1')
        if project_id == '1':
            project_id = self.project_id
        extra_context = extra_context or {}
        extra_context['project_id'] = project_id
        return super(DirectoryAdmin, self).add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = self.edit_fieldsets
        self.readonly_fields = ['parent_dir_id']
        project_id = request.GET.get('project_id', '1')
        if project_id == '1':
            project_id = self.project_id
        extra_context = extra_context or {}
        extra_context['project_id'] = project_id
        return super(DirectoryAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def history_view(self, request, object_id, extra_context=None):
        project_id = request.GET.get('_changelist_filters', '1')
        project_id = project_id.replace("project_id__project_id__exact=", "")
        if project_id == '1':
            project_id = self.project_id
        extra_context = extra_context or {}
        extra_context['project_id'] = project_id
        return super(DirectoryAdmin, self).history_view(request, object_id, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user.id
        if change == False:
            obj.created_by = request.user.id
            parent_obj = Directory.objects.filter(dir_id=obj.parent_dir_id_id).get()
            obj.created_by = request.user.id
            obj.project_id = parent_obj.project_id
            obj.dir_level = parent_obj.dir_level + 1
        obj.save()

    class Media:
        js = ('/static/assets/js/admin_model.js',)
        css = {
            'all': ('/static/assets/css/admin_model.css',)
        }


admin.site.register(Directory, DirectoryAdmin)
admin_site.register(Directory, DirectoryAdmin)


class DirectoryTemplateAdmin(DraggableMPTTAdmin, SimpleHistoryAdmin):
    # resource_class = TblActivitiesResource
    list_display = ('tree_actions', 'dir_name_tree', 'add', 'edit', 'dir_level')
    history_list_display = ['dir_name', 'dir_level', "status"]
    list_display_links = ('edit',)
    list_filter = ('dir_level',)
    search_fields = ('dir_name', 'dir_id',)
    fields = ('parent_dir_id', 'dir_name',)
    edit_fieldsets = (
        'parent_dir_id', 'dir_name',)
    add_fieldsets = ('parent_dir_id', 'dir_name',)
    readonly_fields = ('dir_id',)
    # ordering = ('tree_id',)
    mptt_level_indent = 25
    save_as_continue = False
    actions = []

    def dir_name_tree(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.dir_name,  # Or whatever you want to put here
        )

    def add(self, obj):
        url = 'add/?dir_id=' + str(obj.dir_id)
        return '<b><a href="' + url + '"><img src="/static/assets/img/add.png" alt="Add"></a></b>'

    def edit(self, obj):
        if obj.is_leaf_node():
            url = 'add/?dir_id=' + str(obj.dir_id)
            return '<img src="/static/assets/img/pencil.png" alt="Edit">'
        else:
            return ''

    add.allow_tags = True
    edit.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user.id
        if change == False:
            obj.created_by = request.user.id
            obj.dir_level = 0
            obj.act_addby = request.user.id
            parent_obj = Directory.objects.filter(dir_id=obj.parent_dir_id_id)
            if parent_obj.count() > 0:
                parent_obj = parent_obj.get()
                obj.dir_level = parent_obj.dir_level + 1
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(DirectoryTemplateAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            dir_id = request.GET.get('dir_id')
            form.base_fields['parent_dir_id'].initial = dir_id
            #    self.readonly_fields=['parent_dir_id']
            # return ActivityAddForm
        return form


admin.site.register(DirectoryTemplate, DirectoryTemplateAdmin)
admin_site.register(DirectoryTemplate, DirectoryTemplateAdmin)
