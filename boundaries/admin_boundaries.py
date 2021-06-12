from django.contrib import admin
from django.forms import forms

from ferrp.boundaries.models import BoundariesInfo


# class TblBoundariesForm(forms.ModelForm):
#     attachments_field = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))
#     pic_path_field = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))
#
#     class Meta:
#         model = BoundariesInfo
#         fields = ['id', 'bound_name', 'table_name', 'bound_code', 'bound_level']


class BoundariesInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'bound_name', 'table_name', 'bound_code', 'bound_level']
    search_fields = ['bound_name', 'bound_code','bound_level']
    list_filter = ['bound_name', 'bound_code','bound_level']
    # form = TblBoundariesForm
    def save_model(self, request, obj, form, change):
        obj.bound_level = obj.get_boundaries_level()
        super(BoundariesInfoAdmin, self).save_model(request, obj, form, change)
