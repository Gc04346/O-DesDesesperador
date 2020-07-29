from django.contrib import admin
from .models.base import Apartment, Item, Expense, Room
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext as _


admin.site.register(Apartment)
admin.site.register(Item)
admin.site.register(Expense)
admin.site.register(Room)
