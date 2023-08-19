import requests

from django.core.management.base import BaseCommand
from football.models import Player, DepthChart, Team, Position, InjuryStatus, PlayerProjections
# from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # Frank Darby
        wr = Position.objects.get(name="WR")
        f_darby = Player.objects.get(id=2668)
        falcons = Team.objects.get(name="Atlanta Falcons")
        dc_1 = DepthChart(
            player=f_darby,
            team=falcons,
            roster_spot=5,
            position=wr,
            string=4
        )
        inj_1 = InjuryStatus(
            player_id=f_darby.id,
            status="IR"
        )
        dc_1.save()
        inj_1.save()


        # Irv Smith Jr.
        i_smith = Player.objects.get(id=2360)
        i_smith.espn_id = 4040980
        i_smith.team_id = 53
        i_smith.save()
        dc_2 = DepthChart.objects.get(id=3217)
        dc_2.player_id = 2360
        dc_2.save()
        pp_2 = PlayerProjections.objects.get(player_id = 5264)
        pp_2.player_id = 2360
        pp_2.save()
        wrong_irv = Player.objects.get(id=5264)
        wrong_irv.delete()

        # John Kelly Jr.

        j_kelly = Player.objects.get(id=5274)
        j_kelly.team_id=56
        j_kelly.fbr_slug="KellJo00"
        j_kelly.save()

        dc_3 = DepthChart.objects.get(id=3333)
        dc_3.player_id = 5274
        dc_3.save()

        # Cedrick wilson Jr.
        c_wilson = Player.objects.get(id=548)
        c_wilson.team_id=50
        c_wilson.save()

        dc_4 = DepthChart.objects.get(id=3079)
        dc_4.player_id=548
        dc_4.save()


        # Larry Rountree III


        l_rountree = Player.objects.get(id=2681)
        l_rountree.espn_id = 4241205
        l_rountree.save()

        texans = Team.objects.get(id=60)
        rb = Position.objects.get(name="RB")
        
        dc_5 = DepthChart(
            player=l_rountree,
            team=texans,
            roster_spot=2,
            position=rb,
            string=6
        )
        dc_5.save()

        pp_5 = PlayerProjections.objects.get(player_id=5289)
        pp_5.player=l_rountree
        pp_5.save()


        # Spencer Brown

        s_brown = Player.objects.get(id=5290)
        s_brown.team_id = 74
        s_brown.fbr_slug = "BrowSp01"
        s_brown.save()

        dc_6 = DepthChart.objects.get(id=4159)
        dc_6.player = s_brown
        dc_6.save()