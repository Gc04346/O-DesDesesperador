import os
import uuid
from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models

from theundesperator.apps.contrib.models import BaseModel


class HoneymoonOrganizer(BaseModel):
    when = models.DateField(verbose_name=_('When'), null=True, blank=True)
    how_long = models.PositiveSmallIntegerField(verbose_name=_('How many days'), null=True, blank=True)
    where = models.CharField(verbose_name=_('Where'), max_length=200, null=True, blank=True)
    script = models.FileField(verbose_name=_('Tour Script'), upload_to='honeymoon_scripts', null=True, blank=True)

    class Meta:
        verbose_name = _('Honeymoon Organizer')
        verbose_name_plural = _('Honeymoon Organizers')

    def __str__(self):
        return f'{self.where} @ {self.when}'


class Budget(BaseModel):
    hotel_name = models.CharField(verbose_name=_('Hotel Name'), max_length=150)
    hotel_price = models.DecimalField(verbose_name=_('Hotel Price'), max_digits=7, decimal_places=2, null=True, blank=True)
    tickets_price = models.DecimalField(verbose_name=_('Tickets Price'), max_digits=7, decimal_places=2, null=True, blank=True)
    leave_date = models.CharField(verbose_name=_('Leave Date'), max_length=200, null=True, blank=True)
    arrival_date = models.CharField(verbose_name=_('Arrival Date'), max_length=200, null=True, blank=True)
    tour_company = models.CharField(verbose_name=_('Tour Company'), max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    def __str__(self):
        return self.hotel_name
