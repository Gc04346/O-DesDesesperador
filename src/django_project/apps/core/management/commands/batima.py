from django.core.management.base import BaseCommand
from post_office import mail
from django.utils.translation import ugettext as _
from django_project.apps.core.models import Event, MusicianEvent


class Command(BaseCommand):
    help = 'Temp'

    def handle(self, **other):
        import re

        phonenumber = "(31)91111-2222"

        regex = "\(\d{2}\)9\d{4}-\d{4}"

        if re.search(regex, phonenumber):
            print("Valid phone number")
        else:
            print("Invalid phone number")