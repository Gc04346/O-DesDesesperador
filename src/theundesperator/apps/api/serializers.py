from rest_framework import serializers
from theundesperator.apps.apartments.models import Room, Apartment, Expense, Item
from theundesperator.apps.ceremony.models import Category, Ceremony, Music, ClothesPlanner, Groomsman, Guest, Occasion, \
    Provider
from theundesperator.apps.honeymoon.models import Budget, HoneymoonOrganizer
from theundesperator.apps.pantea.models import Decoration, PanTeaGuest, PanTeaOrganizer


# ================================== #
#          APP APARTMENTS            #
# ================================== #


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


# ================================== #
#            APP CEREMONY            #
# ================================== #

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CeremonySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceremony
        fields = '__all__'


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'


class ClothesPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesPlanner
        fields = '__all__'


class GroomsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groomsman
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


# ================================== #
#           APP HONEYMOON            #
# ================================== #


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class HoneymoonOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoneymoonOrganizer
        fields = '__all__'


# ================================== #
#             APP PANTEA             #
# ================================== #


class DecorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = '__all__'


class PanTeaGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanTeaGuest
        fields = '__all__'


class PanTeaOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanTeaOrganizer
        fields = '__all__'
