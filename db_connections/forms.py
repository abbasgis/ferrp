from django import forms


class Table_List_Form(forms.Form):
    # TYPE_CHOICES = (
    #     ('single', 'Single'),
    #     ('tile', 'Tile'),
    # )
    # # tables_name = forms.ChoiceField()
    # Select_Tables = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=TYPE_CHOICES,
    #                                                                     attrs={'id': 'table_name',
    #                                                                            'class': "radio-inline"}))

    def __init__(self, table_list, *args, **kwargs):
        super(Table_List_Form, self).__init__(*args, **kwargs)
        choices = [(o, str(o)) for o in table_list]
        choices.insert(0, ('All', 'Select All'))
        self.fields['Select_Tables'] = forms.CharField(
            widget=forms.CheckboxSelectMultiple(
                choices= choices
            )
        )
