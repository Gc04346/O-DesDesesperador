import os
import uuid

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base model with mandatory fields

    Attributes:
        uuid (str): Models friendly ID.
        created_at (datetime): Date and time of model's creation.
        updated_at (datetime): Date and time of model's last update.
    """
    # uuid = models.UUIDField(verbose_name=trans('UUID'), default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        abstract = True


class BaseContact(BaseModel):
    """Base model for contacts

    Attributes:
        name (str): Contact name. Eg: Sales.
        person_name (str): Contact Person.
        person_email (str): Contact Person email.
        person_phone (str): Contact Person phone.
        notes (str): Misc notes.
    """
    name = models.CharField(verbose_name=_('Name or Role'), max_length=100)
    person_name = models.CharField(verbose_name=_('Person Name'), max_length=100)
    person_email = models.CharField(verbose_name=_('Person Email'), max_length=100)
    person_phone = models.CharField(verbose_name=_('Person Phone'), max_length=100, blank=True)
    notes = models.TextField(verbose_name=_('Notes'), blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name) + " - " + str(self.person_name)


def get_file_path(instance, filename, folder='uploads'):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)


class BaseFile(BaseModel):
    """Base model for FILES

    Attributes:
        name (str):
        file (file):
    """
    file = models.FileField(verbose_name=_('Name'), upload_to=get_file_path)
    name = models.CharField(verbose_name=_('File Name'), help_text=_('Max file size 5mb.'), max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseAdminNoDeleteAction(admin.ModelAdmin):
    """Base model for Admin classe with no delete selected actions
    """

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class BaseApiDataClass:
    def get_data_for_api(self, **kwargs):
        """ Generic data

        :return: dict()
        """
        return {
            'class_name': self.__class__
        }
