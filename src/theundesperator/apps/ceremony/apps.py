from django.apps import AppConfig
from django.utils.translation import gettext as _


class CeremonyConfig(AppConfig):
    name = 'theundesperator.apps.ceremony'
    label = _('Ceremony')
