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

        Position(
            name="SS",
            full_name="Strong Safety"
        ).save()
        Position(
            name="FS",
            full_name="Free Safety"
        ).save()
        Position(
            name="DB",
            full_name="Defensive Back"
        ).save()
        Position(
            name="LCB",
            full_name="Left Cornerback"
        ).save()
        Position(
            name="RCB",
            full_name="Right Cornerback"
        ).save()
        Position(
            name="RT",
            full_name="Right Tackle"
        ).save()
        Position(
            name="LT",
            full_name="Left Tackle"
        ).save()
        Position(
            name="RG",
            full_name="Right Guard"
        ).save()
        Position(
            name="LG",
            full_name="Left Guard"
        ).save()
        Position(
            name="G",
            full_name="Guard"
        ).save()
        Position(
            name="C",
            full_name="Center"
        ).save()
        Position(
            name="DE",
            full_name="Defensive End"
        ).save()