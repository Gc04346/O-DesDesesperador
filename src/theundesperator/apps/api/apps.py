from django.apps import AppConfig
from django.utils.translation import gettext as _


class ApiConfig(AppConfig):
    name = 'theundesperator.apps.api'
    label = _('Api')
