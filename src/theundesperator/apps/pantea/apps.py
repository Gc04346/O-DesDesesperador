from django.apps import AppConfig
from django.utils.translation import gettext as _


class CoreConfig(AppConfig):
    name = 'theundesperator.apps.core'
    label = _('Core')
