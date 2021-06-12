from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class Document_Upload_Form(forms.Form):
    created_at = forms.DateField(widget=forms.SelectDateWidget())
    # dir_id = forms.CharField(widget=forms.HiddenInput())
    # project_id = forms.CharField(widget=forms.HiddenInput())
    select_document = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'id': "mulFileField", 'multiple': False, 'accept': '.pdf,.doc,.docx,.pptx,.ppt'}))

    # def __init__(self, *args, **kwargs):
    #     super(Document_Upload_Form, self).__init__(*args, **kwargs)
    #     self.fields['dir_id'].value = args[0]['dir_id']
    #     self.fields['project_id'].value = args[0]['project_id']
