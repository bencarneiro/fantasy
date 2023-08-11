from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import League, Conference, Division


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        nfl = League(
            name="National Football League",
            initials="NFL"
        )
        nfl.save()
        afc = Conference(
            name="American Football Conference",
            initials="AFC",
            league=nfl
        )
        afc.save()
        nfc = Conference(
            name="National Football Conference",
            initials="NFC",
            league=nfl
        )
        nfc.save()
        Division(
            league=nfl,
            conference=nfc,
            name="NFC East"
        ).save()
        Division(
            league=nfl,
            conference=nfc,
            name="NFC West"
        ).save()
        Division(
            league=nfl,
            conference=nfc,
            name="NFC North"
        ).save()
        Division(
            league=nfl,
            conference=nfc,
            name="NFC South"
        ).save()
        Division(
            league=nfl,
            conference=afc,
            name="AFC South"
        ).save()
        Division(
            league=nfl,
            conference=afc,
            name="AFC North"
        ).save()
        Division(
            league=nfl,
            conference=afc,
            name="AFC East"
        ).save()
        Division(
            league=nfl,
            conference=afc,
            name="AFC West"
        ).save()
