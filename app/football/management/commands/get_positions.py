from django.core.management.base import BaseCommand
# import pandas as pd
from football.models import Position


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Position(
            name="QB",
            full_name="Quarterback"
        ).save()
        Position(
            name="RB",
            full_name="Running back"
        ).save()
        Position(
            name="FB",
            full_name="Fullback"
        ).save()
        Position(
            name="HB",
            full_name="Halfback"
        ).save()
        Position(
            name="TB",
            full_name="Tailback"
        ).save()
        Position(
            name="WR",
            full_name="Wide Receiver"
        ).save()
        Position(
            name="TE",
            full_name="Tight End"
        ).save()
        Position(
            name="K",
            full_name="Kicker"
        ).save()
        Position(
            name="P",
            full_name="Punter"
        ).save()
