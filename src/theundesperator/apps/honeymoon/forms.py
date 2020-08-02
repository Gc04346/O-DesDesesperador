from django import forms
from django.utils.translation import ugettext as _

from theundesperator.apps.honeymoon.models import HoneymoonOrganizer, Budget


class HoneymoonOrganizerFrontForm(forms.ModelForm):
    class Meta:
        model = HoneymoonOrganizer
        fields = [
            'when',
            'how_long',
            'where',
            'script',
        ]
        widgets = {
            'when': forms.TextInput(attrs={'type': 'date'})
        }


class BudgetFrontForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            'hotel_name',
            'hotel_price',
            'tickets_price',
            'leave_date',
            'arrival_date',
            'tour_company',
        ]
        widgets = {
            'leave_date': forms.TextInput(attrs={'type': 'date'}),
            'arrival_date': forms.TextInput(attrs={'type': 'date'})
        }
