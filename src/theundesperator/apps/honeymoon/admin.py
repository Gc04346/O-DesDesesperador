from .models import Budget, HoneymoonOrganizer
from django.contrib import admin
from django.utils.translation import ugettext as _

admin.site.register(HoneymoonOrganizer)
admin.site.register(Budget)