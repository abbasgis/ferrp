from django import forms
from django.forms import BoundField

from ferrp.layers.models import Projection


class ShapeFileFieldForm(forms.Form):
    select_shapefile = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'id': "mulFileField", 'multiple': True, 'accept': '.shp,.shx,.dbf,.prj'}))


class LayerViewForm(forms.Form):
    title = forms.CharField()
    file_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    layer_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    layer_type = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    geometry_type = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    created_at = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yyyy'}))

    SRS = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))  # widget=forms.Textarea
    SRID = forms.CharField(max_length=7, widget=forms.TextInput())
    MinX = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    MaxX = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    MinY = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    MaxY = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # layer_type = forms.CharField(widget=forms.HiddenInput(attrs={vals}))


class FieldSet(object):
    def __init__(self, form, fields, legend='', cls=None):
        self.form = form
        self.legend = legend
        self.fields = fields
        self.cls = cls

    def __iter__(self):
        for name in self.fields:
            field = self.form.fields[name]
            yield BoundField(self.form, field, name)


class RasterFieldForm(forms.Form):
    TYPE_CHOICES = (
        ('single', 'Single'),
        ('tile', 'Tile'),
    )
    raster_type = forms.CharField(widget=forms.RadioSelect(choices=TYPE_CHOICES,
                                                           attrs={'id': 'rdo_raster_type', 'class': "radio-inline"}))

    # SRID_CHOICES = (('Option 1', 'Option 1'), ('Option 2', 'Option 2'),)
    SRID_CHOICES= list(Projection.objects.all().values_list('srid','name')) #.order_by('-name')
    SRID_CHOICES.insert(0, ('', '----'))
    select_srid = forms.ChoiceField(choices=SRID_CHOICES)
    raster_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'txt_raster_name'}))
    select_raster = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'id': "mul_file_field", 'accept': '.tif,.img,.jp2'}))  # 'multiple': True,
