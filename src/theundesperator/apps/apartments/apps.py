from django.apps import AppConfig
from django.utils.translation import gettext as _


class ApartmentsConfig(AppConfig):
    name = 'theundesperator.apps.apartments'
    label = _('Apartments')
