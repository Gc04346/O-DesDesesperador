from django import forms

from theundesperator.apps.apartments.models import Apartment, Room, Expense


class ApartmentFrontForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'name',
            'address',
            'num_rooms',
            'num_bathrooms',
            'distance_to_subway',
            'distance_to_bus_stop',
            'distance_to_essential_places',
            'price',
            'notes',
            'couple_grade',
            'picture',
            'contact',
            'favorite',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 1})
        }


class RoomFrontForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'name',
        ]


class ExpenseFrontForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'type',
            'name',
            'price',
            'notes',
        ]
