from django.contrib import admin
from .models.base import Category, Provider, Occasion, Music, Guest, Groomsman, ClothesPlanner, Ceremony
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext as _

admin.site.register(Category)
admin.site.register(Provider)
admin.site.register(Occasion)
admin.site.register(Music)
admin.site.register(Guest)
admin.site.register(Groomsman)
admin.site.register(ClothesPlanner)
admin.site.register(Ceremony)
