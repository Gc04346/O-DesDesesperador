from .models import PanTeaOrganizer, PanTeaGuest, Decoration
from django.contrib import admin
from django.utils.translation import ugettext as _

admin.site.register(PanTeaOrganizer)
admin.site.register(PanTeaGuest)
admin.site.register(Decoration)