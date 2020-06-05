from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    name = 'django_project.apps.core'
    verbose_name = _('core')
    label = 'core'
