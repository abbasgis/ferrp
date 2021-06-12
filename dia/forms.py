from django import forms
from django.forms import  ModelForm, Textarea,RadioSelect,TextInput,DecimalField,Select, FileField,ClearableFileInput, CheckboxSelectMultiple
from .import models

CLIMATE_CONDITIONS = (
    ('arid_zone', 'Arid zone'),
    ('semi_arid_zone', 'Semi-Arid Zone'),
    ('humid_zone', 'Humid Zone'),
)

PROJECT_TYPE = (
    ('extension', 'Extension'),
    ('new_construction', 'New construction'),
    ('rehabilitation', 'Rehabilitation'),
)
HAZARD_LEVEL = (
    ('low', 'Low'),
    ('average', 'Average'),
    ('high', 'High'),
)

LOCATION_FEATURES = (
    ('flat_land', 'Flat land'),
    ('hillyarea_plateau', 'Hilly area / Plateau'),
    ('mountain_area', 'Mountain Area'),
    ('riverine_area', 'Riverine area'),
    ('urban_area', 'Urban area'),
    ('rural_area', 'Rural area'),
    ('other', 'Other'),
)

RECOGNIZED_HAZARD = (
    ('landslide', 'Landslide'),
    ('slope_failure', 'Slope Failure'),
    ('flood', 'Flood'),
    ('GLOF', 'GLOF'),
    ('heavy_rain', 'Heavy Rain'),
    ('earthquake', 'Earthquake'),
    ('strong_wind', 'Strong Wind'),
    ('other', 'Other'),
)

FLOOD_AREA = (
    ('urban', 'Urban'),
    ('riverine', 'Riverine'),
    ('Flash', 'Flash'),
)

DATA_AVAILABILITY = (
    ('yes', 'Yes'),
    ('no','No'),

)
RETURN_PEROID=(
    ('5', '5 Years'),
    ('10','10 Years'),
    ('25', '25 Years'),
    ('50','50 Years'),
    ('100','100 Years'),
    ('475','475 Years'),
    ('1000','1000 Years'),
)

SECTION_FOUR_CHECKLIST=(
    ('yes', 'Yes'),
    ('no', 'No'),
    ('partial', 'Partial'),
    ('n/a', 'Not Applicable'),

)

class mhvra_section_one(forms.ModelForm):
    class Meta:
        model=models.MhvraSectionOne
        fields=["project_name","project_type","project_extend","project_climate_condition","rainfall_value","return_period","project_location_features","public_places_nearby"]
        widgets = {
            'project_name': TextInput(attrs={'size': '40'}),
            'project_extend': TextInput(attrs={'size': '40'}),
            'public_places_nearby': TextInput(attrs={'size': '60'}),
            'project_type':RadioSelect(choices=PROJECT_TYPE),
            'project_climate_condition':RadioSelect(choices=CLIMATE_CONDITIONS),
            'project_location_features':RadioSelect(choices=LOCATION_FEATURES)
        }
        labels = {
            'project_name': ('Project Name:'),
            'project_type':('Project Type'),
            'project_extend':('Project Extent'),
            'project_climate_condition':('Climate Conditions'),
            'rainfall_value':('Rainfall Value'),
            'project_location_features':('Location Features'),
            'public_places_nearby':('Marked Public Places Near Project'),
            'return_period':('Return Period')
        }

class Mhvra_section_two(forms.ModelForm):
    class Meta:
        model = models.mhvra_section_two
        fields = ["recongized_hazard","earthquake","landslide","flood","glof","slope_failure","heavy_rain","other","landslide_data","landslide_return_period","flood_data","flood_return_period","forest_reserves_data","forest_reserves_return_period","nature_reserves_data","nature_reserves_return_period","riverine_conservation_data","riverine_conservation_return_period","wetlands_data","wetlands_return_period","archeological_data","archeological_return_period","culture_data","culture_data_return_period"]
        widgets={
            'recongized_hazard':CheckboxSelectMultiple(choices=RECOGNIZED_HAZARD),
            'earthquake':RadioSelect(choices=HAZARD_LEVEL),
            'landslide':RadioSelect(choices=HAZARD_LEVEL),
            'flood':RadioSelect(choices=HAZARD_LEVEL),
            'glof':RadioSelect(choices=HAZARD_LEVEL),
            'slope_failure':RadioSelect(choices=HAZARD_LEVEL),
            'heavy_rain':RadioSelect(choices=HAZARD_LEVEL),
            'other':RadioSelect(choices=HAZARD_LEVEL),
            'landslide_data':RadioSelect(choices=DATA_AVAILABILITY),
            'flood_data':RadioSelect(choices=DATA_AVAILABILITY),
            'forest_reserves_data': RadioSelect(choices=DATA_AVAILABILITY),
            'nature_reserves_data': RadioSelect(choices=DATA_AVAILABILITY),
            'riverine_conservation_data': RadioSelect(choices=DATA_AVAILABILITY),
            'wetlands_data': RadioSelect(choices=DATA_AVAILABILITY),
            'archeological_data': RadioSelect(choices=DATA_AVAILABILITY),
            'culture_data': RadioSelect(choices=DATA_AVAILABILITY),
            'landslide_return_period':Select(choices=RETURN_PEROID),
            'flood_return_period': Select(choices=RETURN_PEROID),
            'forest_reserves_return_period': Select(choices=RETURN_PEROID),
            'nature_reserves_return_period': Select(choices=RETURN_PEROID),
            'riverine_conservation_return_period': Select(choices=RETURN_PEROID),
            'wetlands_return_period': Select(choices=RETURN_PEROID),
            'archeological_return_period': Select(choices=RETURN_PEROID),
            'culture_data_return_period': Select(choices=RETURN_PEROID),

            }
class Dia_section_four(forms.ModelForm):
    class Meta:
        model = models.SectionFour
        fields = ["building_codes","building_bye_laws","disaster_risk_reduction","flood_hazard_guideline","environmental_impact_assessment_field"]

        widgets={
            # 'filedoc':ClearableFileInput(attrs={'multiple': True}),
            'building_codes':RadioSelect(choices=SECTION_FOUR_CHECKLIST),
            'building_bye_laws': RadioSelect(choices=SECTION_FOUR_CHECKLIST),
            'disaster_risk_reduction': RadioSelect(choices=SECTION_FOUR_CHECKLIST),
            'flood_hazard_guideline': RadioSelect(choices=SECTION_FOUR_CHECKLIST),
            'environmental_impact_assessment_field': RadioSelect(choices=SECTION_FOUR_CHECKLIST),
        }

class Section_Four_Files_Field(forms.ModelForm):
    class Meta:
        model = models.SectionFourFiles
        fields = ['filedoc']
        widgets = {
            'filedoc': ClearableFileInput(attrs={'multiple': True}),
        }


class Dia_section_five(forms.ModelForm):
    class Meta:
        model = models.SectionFive
        fields = ["comments"]






