from django import forms
from django.utils.translation import ugettext as _
from theundesperator.apps.ceremony.models import Guest, Category, Provider, Ceremony, ClothesPlanner, Occasion, Music, \
    Groomsman


class CeremonyFrontForm(forms.ModelForm):
    class Meta:
        model = Ceremony
        fields = [
            'place',
            'date'
        ]
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'})
        }


class GuestFrontForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'group',
            'name',
            'indispensability',
        ]


class GroomsmanFrontForm(forms.ModelForm):
    class Meta:
        model = Groomsman
        fields = [
            'selector',
            'name',
            'duo',
        ]


class CategoryFrontForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
        ]


class OccasionFrontForm(forms.ModelForm):
    class Meta:
        model = Occasion
        fields = [
            'name',
        ]


class ProviderFrontForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            'category',
            'name',
            'phone',
            'website',
            'price',
            'notes',
            'card',
            'favorite',
        ]


class MusicFrontForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            'occasion',
            'name',
            'duration',
            'link',
        ]
        widgets = {
            'duration': forms.TimeInput(),
        }


class ClothesPlannerFrontForm(forms.ModelForm):
    class Meta:
        model = ClothesPlanner
        fields = [
            'grooms_mom_dress_color',
            'brides_mom_dress_color',
            'kids_dress_color',
            'ring_bearer_costume_color',
            'brides_dress',
            'brides_shoes',
            'brides_hairstyle',
            'brides_makeup',
            'brides_hair_accessories',
            'brides_body_accessories',
            'brides_lingerie',
            'grooms_suit',
            'grooms_shoes',
        ]
