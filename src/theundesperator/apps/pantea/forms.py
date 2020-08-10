from django import forms

from theundesperator.apps.pantea.models import PanTeaOrganizer, Decoration, PanTeaGuest


class PanTeaOrganizerFrontForm(forms.ModelForm):
    class Meta:
        model = PanTeaOrganizer
        fields = [
            'soda_quantity',
            'diet_soda_quantity',
            'juice_quantity',
            'diet_juice_quantity',
            'food_cook',
            'how_to_get_the_food',
            'food_price',
            'food_ready',
            'drinks_ready',
        ]


class PanTeaGuestFrontForm(forms.ModelForm):
    class Meta:
        model = PanTeaGuest
        fields = [
            'name',
        ]


class DecorationFrontForm(forms.ModelForm):
    class Meta:
        model = Decoration
        fields = [
            'item',
            'check',
            'price',
        ]
