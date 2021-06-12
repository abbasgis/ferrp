from django import forms


class ConnectionParamsForm(forms.Form):
    db_choices = (
    ('django.contrib.gis.db.backends.postgis', 'Postgres'), ('MySQL', 'MySQL'), ('SQLServer', 'SQLServer'),
    ('Oracle', 'Oracle'))
    connection_title = forms.CharField(widget=forms.TextInput()) #attrs={"value": "test gis"}
    database_type = forms.ChoiceField(required=True, choices=db_choices)
    IP_address_v4 = forms.CharField(required=True, widget=forms.TextInput()) #attrs={"value": "127.0.0.1"}
    port = forms.CharField(required=True, widget=forms.TextInput()) #attrs={"value": "5432"}
    database_name = forms.CharField(widget=forms.TextInput(), required=True) #attrs={"value": "dhaisl_data"}
    db_user = forms.CharField(required=True, widget=forms.TextInput()) #attrs={"value": "postgres"}
    db_password = forms.CharField(widget=forms.PasswordInput(), required=True) #attrs={"value": "postgres"})


class Table_List_Form(forms.Form):
    def __init__(self, table_list, conn_name, integrated_table_list={}, *args, **kwargs):
        super(Table_List_Form, self).__init__(*args, **kwargs)
        self.fields['Connection_Name'] = forms.CharField(
            widget=forms.HiddenInput(attrs={"value": conn_name, "id": "hidConnName"}))
        choices = []
        for o in table_list:
            if o not in integrated_table_list:
                choices.append((o, str(o)))
        # choices = [(o, str(o)) for o in table_list]
        choices.insert(0, ('All', 'Select All'))
        self.fields['Select_Tables'] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=choices
        )
