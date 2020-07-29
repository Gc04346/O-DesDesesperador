import os
import uuid

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    """Base model with mandatory fields

    Attributes:
        created_at (datetime): Date and time of model's creation.
        updated_at (datetime): Date and time of model's last update.
    """
    # uuid = models.UUIDField(verbose_name=trans('UUID'), default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        abstract = True