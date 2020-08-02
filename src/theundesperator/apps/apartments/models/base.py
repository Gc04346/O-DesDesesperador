import os
import uuid
from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models

from theundesperator.apps.contrib.models import BaseModel


class Apartment(BaseModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name=_('Address'), max_length=250, null=True, blank=True)
    num_rooms = models.PositiveSmallIntegerField(verbose_name=_('Number of Rooms'), default=1)
    num_bathrooms = models.PositiveSmallIntegerField(verbose_name=_('Number of Bathrooms'), default=1)
    distance_to_subway = models.CharField(verbose_name=_('Distance to Subway'), max_length=20, null=True, blank=True)
    distance_to_bus_stop = models.CharField(verbose_name=_('Distance to Bus Stop'), max_length=20, null=True, blank=True)
    distance_to_essential_places = models.CharField(verbose_name=_('Distance to Essential Establishments'), max_length=20, null=True, blank=True)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=9, decimal_places=2, null=True, blank=True)
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)
    couple_grade = models.PositiveSmallIntegerField(verbose_name=_('Couple Grade'), default=0)
    system_grade = models.PositiveSmallIntegerField(verbose_name=_('System Grade'), default=0)
    picture = models.ImageField(verbose_name=_('Picture'), upload_to='apartment_photos', null=True, blank=True)
    contact = models.CharField(verbose_name=_('Contact'), max_length=250, null=True, blank=True)
    favorite = models.BooleanField(verbose_name=_('Favorite'), default=False)

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')

    def __str__(self):
        return self.name


class Room(BaseModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return f'{self.name}'


class Item(BaseModel):
    URGENCIES = (
        ('ES', _('Essential')),
        ('IM', _('Important')),
        ('DE', _('Delayable')),
    )
    urgency = models.CharField(verbose_name=_('Urgency'), max_length=10, choices=URGENCIES, default='ES')
    name = models.CharField(verbose_name=_('Name'), max_length=100, null=True, blank=True)
    unit_price = models.DecimalField(verbose_name=_('Price (Un.)'), max_digits=7, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity'), default=1)
    total_price = models.DecimalField(verbose_name=_('Price (Tt.)'), max_digits=7, decimal_places=2, null=True, blank=True)
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)
    done = models.BooleanField(verbose_name=_('Check'), default=False)
    room = models.ForeignKey(verbose_name=_('Room'), to=Room, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return f'{self.name} @ {self.room.name}'


class Expense(BaseModel):
    type = models.CharField(verbose_name=_('Type'), max_length=100)
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=7, decimal_places=2, default=0.00)
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return self.name
