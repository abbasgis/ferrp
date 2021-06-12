from django import forms

from ferrp.meeting_management.models import TblUsers

INITIATIVE_CHOICES = [
    ('all', 'All Initiatives'),
    ('important', 'Important Initiatives'),
    ('short', 'Short Initiatives'),
    ('long', 'Long Initiatives'),
]


class SyncForm(forms.Form):
    initiatives_to_sync = forms.ChoiceField(label='Select Initiatives', choices=INITIATIVE_CHOICES)
    users_to_monitor = forms.ModelMultipleChoiceField(queryset=TblUsers.objects.all(), required=False)

