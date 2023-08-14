import requests

from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Position, Player, PlayerKicking, Team
from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for year in range(2006,2023):
            sleep(3)
            w = requests.get(f"https://www.pro-football-reference.com/years/{year}/kicking.htm").text
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
                fga1 = player.split('data-stat="fga1" >')[1].split('<')[0]
                if not fga1:
                    fga1 = 0
                fgm1 = player.split('data-stat="fgm1" >')[1].split('<')[0]
                if not fgm1:
                    fgm1 = 0
                fga2 = player.split('data-stat="fga2" >')[1].split('<')[0]
                if not fga2:
                    fga2 = 0
                fgm2 = player.split('data-stat="fgm2" >')[1].split('<')[0]
                if not fgm2:
                    fgm2 = 0
                fga3 = player.split('data-stat="fga3" >')[1].split('<')[0]
                if not fga3:
                    fga3 = 0
                fgm3 = player.split('data-stat="fgm3" >')[1].split('<')[0]
                if not fgm3:
                    fgm3 = 0
                fga4 = player.split('data-stat="fga4" >')[1].split('<')[0]
                if not fga4: 
                    fga4 = 0
                fgm4 = player.split('data-stat="fgm4" >')[1].split('<')[0]
                if not fgm4:
                    fgm4 = 0
                fga5 = player.split('data-stat="fga5" >')[1].split('<')[0]
                if not fga5:
                    fga5 = 0
                fgm5 = player.split('data-stat="fgm5" >')[1].split('<')[0]
                if not fgm5:
                    fgm5 = 0
                fga = player.split('data-stat="fga" >')[1].split('<')[0]
                if not fga:
                    fga = 0
                fgm = player.split('data-stat="fgm" >')[1].split('<')[0]
                if not fgm:
                    fgm = 0
                fg_long = player.split('data-stat="fg_long" >')[1].split('<')[0]
                if not fg_long:
                    fg_long = 0
                fg_perc = player.split('data-stat="fg_perc" >')[1].split('<')[0]
                if not fg_perc:
                    fg_perc = 0
                else:
                    fg_perc = fg_perc[:-1]
                xpa = player.split('data-stat="xpa" >')[1].split('<')[0]
                if not xpa:
                    xpa = 0
                xpm = player.split('data-stat="xpm" >')[1].split('<')[0]
                if not xpm:
                    xpm = 0
                xp_perc = player.split('data-stat="xp_perc" >')[1].split('<')[0]
                if not xp_perc:
                    xp_perc = 0
                else:
                    xp_perc = xp_perc[:-1]
                    
                

                new_player_rushing_entry = PlayerKicking(
                    player=player_obj,
                    year=year,
                    team=team,
                    pos=position,
                    age=age,
                    g=g,
                    gs=gs,
                    fga1=fga1,
                    fga2=fga2,
                    fga3=fga3,
                    fga4=fga4,
                    fga5=fga5,
                    fga=fga,
                    fgm1=fgm1,
                    fgm2=fgm2,
                    fgm3=fgm3,
                    fgm4=fgm4,
                    fgm5=fgm5,
                    fgm=fgm,
                    fg_long=fg_long,
                    fg_perc=fg_perc,
                    xpa=xpa,
                    xpm=xpm,
                    xp_perc=xp_perc
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
    # fga1 = models.SmallIntegerField(null=False)
    # fgm1 = models.SmallIntegerField(null=False)
    # fga2 = models.SmallIntegerField(null=False)
    # fgm2 = models.SmallIntegerField(null=False)
    # fga3 = models.SmallIntegerField(null=False)
    # fgm3 = models.SmallIntegerField(null=False)
    # fga4 = models.SmallIntegerField(null=False)
    # fgm4 = models.SmallIntegerField(null=False)
    # fga5 = models.SmallIntegerField(null=False)
    # fgm5 = models.SmallIntegerField(null=False)
    # fga = models.SmallIntegerField(null=False)
    # fgm = models.SmallIntegerField(null=False)
    # fg_long = models.SmallIntegerField(null=False)
    # fg_perc = models.FloatField()
    # xpa = models.SmallIntegerField(null=False)
    # xpm = models.SmallIntegerField(null=False)
    # xp_perc = models.FloatField()