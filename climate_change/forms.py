import datetime

from django import forms

from ferrp.climate_change.models import TemperatureRcp4525KmPunjab

LAYER_CHOICES = [
    ('temperature', 'Temperature'),
    ('precipitation', 'Precipitation'),
]
YEAR_CHOICES = TemperatureRcp4525KmPunjab.objects.all().distinct('year').order_by('year').values_list('year', 'year')
MONTH_CHOICE = [(m, m) for m in range(1, 13)]


class HeatMapInputsForm(forms.Form):
    layer = forms.CharField(label='Layer', widget=forms.Select(choices=LAYER_CHOICES), )
    year = forms.IntegerField(label='Year', widget=forms.Select(choices=YEAR_CHOICES),
                              initial=datetime.datetime.now().year, )
    month = forms.IntegerField(label='Month', widget=forms.Select(choices=MONTH_CHOICE),
                               initial=datetime.datetime.now().month, )

    def __init__(self, *args, **kwargs):
        super(HeatMapInputsForm, self).__init__(*args, **kwargs)
        self.fields['layer'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'
        self.fields['month'].widget.attrs['class'] = 'form-control'
