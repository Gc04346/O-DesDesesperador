from django.apps import AppConfig
from django.utils.translation import gettext as _


class ArtistsConfig(AppConfig):
    name = 'theundesperator.apps.cerimony'
    label = _('Cerimony')