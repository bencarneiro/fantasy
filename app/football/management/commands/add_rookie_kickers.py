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
        b_aubrey.team=cowboys
        b_aubrey.save()

        dc_2 = DepthChart(
            player=t_brown,
            team=rams,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_2.save()
        t_brown.team=rams
        t_brown.save()

                
        dc_3 = DepthChart(
            player=a_carlson,
            team=gb,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_3.save()
        a_carlson.team=gb
        a_carlson.save()
        
        dc_4 = DepthChart(
            player=j_moody,
            team=sf,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_4.save()
        j_moody.team=sf
        j_moody.save()


        pats = Team.objects.get(name="New England Patriots")
        c_ryland = Player.objects.get(name="Chad Ryland")
        dc_5 = DepthChart(
            player=c_ryland,
            team=pats,
            roster_spot=13,
            position=kicker,
            string=1
        )
        dc_5.save()
        c_ryland.team=pats
        c_ryland.save()