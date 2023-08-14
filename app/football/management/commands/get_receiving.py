import requests

from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Position, Player, PlayerReceiving, Team
from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for year in range(2006,2023):
            sleep(3)
            w = requests.get(f"https://www.pro-football-reference.com/years/{year}/receiving.htm").text
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
                targets = player.split('data-stat="targets" >')[1].split('<')[0]
                if not targets:
                    targets = 0
                rec = player.split('data-stat="rec" >')[1].split('<')[0]
                catch_pct = player.split('data-stat="catch_pct" >')[1].split('%<')[0]
                rec_yds = player.split('data-stat="rec_yds" >')[1].split('<')[0]
                rec_yds_per_rec = player.split('data-stat="rec_yds_per_rec" >')[1].split('<')[0]
                if not rec_yds_per_rec:
                    rec_yds_per_rec = 0
                rec_td = player.split('data-stat="rec_td" >')[1].split('<')[0]
                rec_first_down = player.split('data-stat="rec_first_down" >')[1].split('<')[0]
                rec_long = player.split('data-stat="rec_long" >')[1].split('<')[0]
                rec_yds_per_tgt = player.split('data-stat="rec_yds_per_tgt" >')[1].split('<')[0]
                if not rec_yds_per_tgt:
                    rec_yds_per_tgt = 0
                rec_per_g = player.split('data-stat="rec_per_g" >')[1].split('<')[0]
                rec_yds_per_g = player.split('data-stat="rec_yds_per_g" >')[1].split('<')[0]
                fumbles = player.split('data-stat="fumbles" >')[1].split('<')[0]
                if not fumbles:
                    fumbles = 0

                new_player_receiving_entry = PlayerReceiving(
                    player=player_obj,
                    year=year,
                    team=team,
                    pos=position,
                    age=age,
                    g=g,
                    gs=gs,
                    targets=targets,
                    rec=rec,
                    catch_pct=catch_pct,
                    rec_yds=rec_yds,
                    rec_yds_per_rec=rec_yds_per_rec,
                    rec_td=rec_td,
                    rec_first_down=rec_first_down,
                    rec_long=rec_long,
                    rec_yds_per_tgt=rec_yds_per_tgt,
                    rec_per_g=rec_per_g,
                    rec_yds_per_g=rec_yds_per_g,
                    fumbles=fumbles
                )
                new_player_receiving_entry.save()

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
    # pos = models.CharField(max_length=16, default=None)
    # g = models.SmallIntegerField(null=False)
    # gs = models.SmallIntegerField(null=False)
    # targets = models.SmallIntegerField(null=False)
    # rec = models.SmallIntegerField(null=False)
    # catch_pct = models.FloatField()
    # rec_yds = models.SmallIntegerField(null=False)
    # rec_yds_per_rec = models.FloatField()
    # rec_td = models.SmallIntegerField(null=False)
    # rec_first_down = models.SmallIntegerField(null=False)
    # rec_long = models.SmallIntegerField(null=False)
    # rec_yds_per_tgt = models.FloatField()
    # rec_per_g = models.FloatField()
    # rec_yds_per_g = models.FloatField()
    # fumbles = models.SmallIntegerField(null=False)