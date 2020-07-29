import os
import uuid
from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models

from theundesperator.apps.contrib.models import BaseModel


class PanTeaGuest(BaseModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)

    class Meta:
        verbose_name = _('Pan Tea Guest')
        verbose_name_plural = _('Pan Tea Guests')

    def __str__(self):
        return self.name


class PanTeaOrganizer(BaseModel):
    soda_quantity = models.PositiveSmallIntegerField(verbose_name=_('Soda Quantity'), null=True, blank=True)
    diet_soda_quantity = models.PositiveSmallIntegerField(verbose_name=_('Diet Soda Quantity'), null=True, blank=True)
    juice_quantity = models.PositiveSmallIntegerField(verbose_name=_('Juice Quantity'), null=True, blank=True)
    diet_juice_quantity = models.PositiveSmallIntegerField(verbose_name=_('Diet Juice Quantity'), null=True, blank=True)
    food_cook = models.CharField(verbose_name=_('Food Cook'), max_length=50, null=True, blank=True)
    how_to_get_the_food = models.CharField(verbose_name=_('How to Get The Food'), max_length=100, null=True, blank=True)
    food_price = models.DecimalField(verbose_name=_('Food Price'), max_digits=7, decimal_places=2, null=True,
                                     blank=True)
    food_ready = models.BooleanField(verbose_name=_('Food Ready'), default=False)
    drinks_ready = models.BooleanField(verbose_name=_('Drinks Ready'), default=False)

    class Meta:
        verbose_name = _('Pan Tea Organizer')
        verbose_name_plural = _('Pan Tea Organizers')

    def __str__(self):
        return self.soda_quantity


class Decoration(BaseModel):
    item = models.CharField(verbose_name=_('Item'), max_length=150)
    check = models.BooleanField(verbose_name=_('Check'), default=False)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _('Decoration')
        verbose_name_plural = _('Decorations')

    def __str__(self):
        return self.item
