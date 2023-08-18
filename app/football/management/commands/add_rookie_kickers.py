import requests

from django.core.management.base import BaseCommand
from football.models import Player, DepthChart, Team, Position
# from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        kicker = Position.objects.get(name="K")
        cowboys = Team.objects.get(name="Dallas Cowboys")
        sf = Team.objects.get(name="San Francisco 49ers")
        gb = Team.objects.get(name="Green Bay Packers")
        rams = Team.objects.get(name="Los Angeles Rams")
        b_aubrey = Player.objects.get(name="Brandon Aubrey")
        t_brown = Player.objects.get(name="Tanner Brown")
        a_carlson = Player.objects.get(name="Anders Carlson")
        j_moody = Player.objects.get(name="Jake Moody")

        dc_1 = DepthChart(
            player=b_aubrey,
            team=cowboys,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_1.save()

        dc_2 = DepthChart(
            player=t_brown,
            team=rams,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_2.save()
                
        dc_3 = DepthChart(
            player=a_carlson,
            team=gb,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_3.save()
        
        dc_4 = DepthChart(
            player=j_moody,
            team=sf,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_4.save()