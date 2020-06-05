import os
import uuid
from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models

from theundesperator.apps.contrib.models import BaseModel


class BaseChecklist(BaseModel):
    item = models.CharField(verbose_name=_('Item'), max_length=100)
    done = models.BooleanField(verbose_name=_('Check'), default=False)

    class Meta:
        abstract = True

