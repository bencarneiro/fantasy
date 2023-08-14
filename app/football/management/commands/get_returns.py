import requests

from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Position, Player, PlayerReturning, Team
from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for year in range(2006,2023):
            sleep(3)
            w = requests.get(f"https://www.pro-football-reference.com/years/{year}/returns.htm").text
            players = w.split('<th scope="row" class="right "')
            players = players[1:]
            for player in players:
                # print(player)
                player_slug = player.split('data-append-csv="')[1].split('"')[0]
                try: 
                    player_obj = Player.objects.get(fbr_slug=player_slug)
                except:
                    player_name = player.split('.htm">')[1].split('<')[0]
                    last_initial = player_name.split(' ')[-1][0]
                    player_url = f"https://www.pro-football-reference.com/players/{last_initial}/{player_slug}.htm"
                    # print(player_url)
                    sleep(3)
                    player_page = requests.get(player_url).text
                    try:
                        team_slug = player_page.split('<strong>Team</strong>: <span><a href="')[1][7:10]
                        team = Team.objects.get(slug=team_slug)
                    except:
                        team = None
                    player_obj = Player(
                        name=player_name,
                        fbr_slug=player_slug,
                        team=team
                    )
                    player_obj.save()
                try:
                    team_slug = player.split('<a href="/teams/')[1].split('/')[0]
                    team = Team.objects.get(slug=team_slug)
                except:
                    team = None
                age = player.split('data-stat="age" >')[1].split('<')[0]
                position_str = player.split('data-stat="pos" >')[1].split("<")[0]
                try:
                    position = Position.objects.get(name=position_str)
                except:
                    position = None
                g = player.split('data-stat="g" >')[1].split('<')[0]
                gs = player.split('data-stat="gs" >')[1].split('<')[0]
                punt_ret = player.split('data-stat="punt_ret" >')[1].split('<')[0]
                if not punt_ret:
                    punt_ret = 0
                punt_ret_yds = player.split('data-stat="punt_ret_yds" >')[1].split('<')[0]
                if not punt_ret_yds:
                    punt_ret_yds = 0
                punt_ret_td = player.split('data-stat="punt_ret_td" >')[1].split('<')[0]
                punt_ret_long = player.split('data-stat="punt_ret_long" >')[1].split('<')[0]
                if not punt_ret_long:
                    punt_ret_long = 0
                punt_ret_yds_per_ret = player.split('data-stat="punt_ret_yds_per_ret" >')[1].split('<')[0]
                if not punt_ret_yds_per_ret:
                    punt_ret_yds_per_ret = 0
                kick_ret = player.split('data-stat="kick_ret" >')[1].split('<')[0]
                if not kick_ret:
                    kick_ret = 0
                kick_ret_yds = player.split('data-stat="kick_ret_yds" >')[1].split('<')[0]
                if not kick_ret_yds:
                    kick_ret_yds = 0
                kick_ret_td = player.split('data-stat="kick_ret_td" >')[1].split('<')[0]
                kick_ret_long = player.split('data-stat="kick_ret_long" >')[1].split('<')[0]
                if not kick_ret_long:
                    kick_ret_long = 0
                kick_ret_yds_per_ret = player.split('data-stat="kick_ret_yds_per_ret" >')[1].split('<')[0]
                if not kick_ret_yds_per_ret:
                    kick_ret_yds_per_ret = 0
                all_purpose_yds = player.split('data-stat="all_purpose_yds" >')[1].split('<')[0]
                

                new_player_rushing_entry = PlayerReturning(
                    player=player_obj,
                    year=year,
                    team=team,
                    pos=position,
                    age=age,
                    g=g,
                    gs=gs,
                    punt_ret=punt_ret,
                    punt_ret_yds=punt_ret_yds,
                    punt_ret_td=punt_ret_td,
                    punt_ret_long=punt_ret_long,
                    punt_ret_yds_per_ret=punt_ret_yds_per_ret,
                    kick_ret=kick_ret,
                    kick_ret_yds=kick_ret_yds,
                    kick_ret_td=kick_ret_td,
                    kick_ret_long=kick_ret_long,
                    kick_ret_yds_per_ret=kick_ret_yds_per_ret,
                    all_purpose_yds=all_purpose_yds
                )
                new_player_rushing_entry.save()

                print(f"SLUG: {player_slug}")
                print(f"year: {year}")
                # print(f"age: {age}")


        # class Player(models.Model):

        # id = models.AutoField(primary_key=True)
        # fbr_slug = models.CharField(max_length=64)
        # name = models.CharField(max_length=256)
        # team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
        


    # player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    # year = models.SmallIntegerField(null=False)
    # team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    # age = models.SmallIntegerField(null=False)
    # pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    # g = models.SmallIntegerField(null=False)
    # gs = models.SmallIntegerField(null=False)
    # punt_ret = models.SmallIntegerField(null=False)
    # punt_ret_yds = models.SmallIntegerField(null=False)
    # punt_ret_td = models.SmallIntegerField(null=False)
    # punt_ret_long = models.SmallIntegerField(null=False)
    # punt_ret_yds_per_ret = models.FloatField()
    # kick_ret = models.SmallIntegerField(null=False)
    # kick_ret_yds = models.SmallIntegerField(null=False)
    # kick_ret_td = models.SmallIntegerField(null=False)
    # kick_ret_long = models.SmallIntegerField(null=False)
    # kick_ret_yds_per_ret = models.FloatField()
    # all_purpose_yds = models.SmallIntegerField(null=False)