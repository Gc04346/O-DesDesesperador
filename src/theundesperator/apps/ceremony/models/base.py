import os
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models

from theundesperator.apps.contrib.models import BaseModel


class Category(BaseModel):
    name = models.CharField(verbose_name=_('Category'), max_length=100)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Occasion(BaseModel):
    name = models.CharField(verbose_name=_('Occasion'), max_length=100)

    class Meta:
        verbose_name = _('Occasion')
        verbose_name_plural = _('Occasions')

    def __str__(self):
        return self.name


class Ceremony(BaseModel):
    place = models.CharField(verbose_name=_('Place'), max_length=100, null=True, blank=True)
    date = models.DateField(verbose_name=_('Date'), null=True, blank=True)

    class Meta:
        verbose_name = _('Ceremony')
        verbose_name_plural = _('Ceremonies')

    def __str__(self):
        return f'{self.place} / {self.date}'


class ClothesPlanner(BaseModel):
    grooms_mom_dress_color = models.CharField(verbose_name=_('Groom\'s Mom Dress Color'), max_length=15, null=True,
                                              blank=True)
    brides_mom_dress_color = models.CharField(verbose_name=_('Bride\'s Mom Dress Color'), max_length=15, null=True,
                                              blank=True)
    kids_dress_color = models.CharField(verbose_name=_('Kid\'s Dress Color'), max_length=15, null=True, blank=True)
    ring_bearer_costume_color = models.CharField(verbose_name=_('Ring Bearer Costume Color'), max_length=15, null=True,
                                                 blank=True)
    brides_dress = models.FileField(verbose_name=_('Bride\'s Dress'), upload_to='clothes_planner', null=True,
                                    blank=True)
    brides_shoes = models.FileField(verbose_name=_('Bride\'s Shoes'), upload_to='clothes_planner', null=True,
                                    blank=True)
    brides_hairstyle = models.FileField(verbose_name=_('Bride\'s Hairstyle'), upload_to='clothes_planner', null=True,
                                        blank=True)
    brides_makeup = models.FileField(verbose_name=_('Bride\'s Makeup'), upload_to='clothes_planner', null=True,
                                     blank=True)
    brides_hair_accessories = models.FileField(verbose_name=_('Bride\'s Hair Acessories'), upload_to='clothes_planner',
                                               null=True, blank=True)
    brides_body_accessories = models.FileField(verbose_name=_('Bride\'s Body Acessories'), upload_to='clothes_planner',
                                               null=True, blank=True)
    brides_lingerie = models.FileField(verbose_name=_('Bride\'s Lingerie'), upload_to='clothes_planner', null=True,
                                       blank=True)
    grooms_suit = models.FileField(verbose_name=_('Groom\'s Suit'), upload_to='clothes_planner', null=True, blank=True)
    grooms_shoes = models.FileField(verbose_name=_('Groom\'s Shoes'), upload_to='clothes_planner', null=True,
                                    blank=True)

    class Meta:
        verbose_name = _('Clothes Planner')
        verbose_name_plural = _('Clothes Planners')

    def __str__(self):
        return self.grooms_mom_dress_color


class Provider(BaseModel):
    category = models.ForeignKey(verbose_name=_('Category'), to=Category, on_delete=models.SET_NULL, null=True,
                                 blank=True)
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    phone = models.CharField(verbose_name=_('Phone'), max_length=60, null=True, blank=True)
    website = models.CharField(verbose_name=_('Website'), max_length=100, null=True, blank=True)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=7, decimal_places=2, null=True, blank=True)
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)
    card = models.FileField(verbose_name=_('Card'), upload_to='files/', null=True, blank=True)
    favorite = models.BooleanField(verbose_name=_('Favorite'))

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def __str__(self):
        return self.name


class Guest(BaseModel):
    GUEST_GROUPS = (
        ('GFA', _('Groom\'s Family')),
        ('BFA', _('Bride\'s  Family')),
        ('GFR', _('Groom\'s Friend')),
        ('BFR', _('Bride\'s Friend')),
        ('UNW', _('Don\'t want to invite, but have to')),
    )
    group = models.CharField(verbose_name=_('Group'), max_length=40, choices=GUEST_GROUPS)
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    indispensability = models.PositiveSmallIntegerField(verbose_name=_('Indispensability'), help_text=_(
        'Indicates how much you really want this person to go'))

    class Meta:
        verbose_name = _('Guest')
        verbose_name_plural = _('Guests')

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_guest_groups():
        return [group for group in Guest.GUEST_GROUPS]


class Music(BaseModel):
    occasion = models.ForeignKey(verbose_name=_('Occasion'), to=Occasion, on_delete=models.SET_NULL, null=True,
                                 blank=True)
    name = models.CharField(verbose_name=_('Song Name'), max_length=50)
    duration = models.TimeField(verbose_name=_('Song duration'), blank=True, null=True)
    link = models.CharField(verbose_name=_('Link to the song'), max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = _('Music')
        verbose_name_plural = _('Musics')

    def __str__(self):
        return self.name


class Groomsman(BaseModel):
    SELECTORS = (
        ('GR', _('Groom')),
        ('BR', _('Bride'))
    )
    selector = models.CharField(verbose_name=_('Sponsored'), max_length=6, choices=SELECTORS,
                                help_text=_('Who chose the groomsman'), default='BR')
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    duo = models.ForeignKey(verbose_name=_('Duo'), to='self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Groomsman')
        verbose_name_plural = _('Groomsmen')

    def __str__(self):
        return self.name
