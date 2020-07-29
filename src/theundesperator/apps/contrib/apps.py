from django.apps import AppConfig
from django.utils.translation import gettext as _


class ContribConfig(AppConfig):
    name = 'theundesperator.apps.contrib'
    label = _('contrib')
