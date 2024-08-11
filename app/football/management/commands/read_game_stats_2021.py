from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import PlayerFBR, TeamFBR, GameFBR, GameStats
from time import sleep
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        GameStats.objects.filter(game__dt__gte="2021-07-01",game__dt__lte="2022-07-01").delete()
        r = requests.get("https://www.pro-football-reference.com/years/2021/games.htm")
        sleep(6)
        box_score_links = []
        z = r.text.split('",\n\t\t\t"url": "')
        for y in z[1:]:
            box_score_links += [y.split('",\n\t\t"eventStatus": "')[0]]
        for box_score_link in box_score_links:
            game_id = box_score_link.split("/boxscores/")[1].split(".htm")[0]
            print(box_score_link)
            game = requests.get(box_score_link)
            start_time = game.text.split("Start Time</strong>: ")[1].split("</div>")[0]
            if "pm" in start_time and "12:" not in start_time:
                hour = int(start_time.split(":")[0]) + 12
            else:
                hour = int(start_time.split(":")[0])
            dt = datetime(
                year=int(game_id[:4]),
                month=int(game_id[4:6]),
                day=int(game_id[6:8]),
                hour=hour,
                minute=int(start_time.split(":")[1][:2])
            )
            new_game = GameFBR(
                id=game_id,
                dt=dt
            )
            new_game.save()
            print(start_time)
            sleep(6)
            players = game.text.split('data-stat="fumbles_lost" scope="col" class=" poptip center" data-tip="Fumbles Lost by Player (since 1994) or Team" data-over-header="Fumbles" >FL</th>\n      </tr>\n      </thead>\n<tbody><tr ><th scope="row" class="left " data-append-csv="')[1]
            for player in players.split('data-append-csv="'):
                if player == '<th scope="row" class="left " ':
                    continue
                slug = player.split('"')[0]
                link = player.split('a href="')[1].split('">')[0]
                name = player.split('.htm">')[1].split("<")[0]
                team = player.split('data-stat="team" >')[1].split('<')[0]
                if 'data-stat="pass_cmp' not in player:
                    break
                passing_completions = player.split('data-stat="pass_cmp" >')[1].split('<')[0]
                passing_attempts = player.split('data-stat="pass_att" >')[1].split('<')[0]
                passing_yards = player.split('data-stat="pass_yds" >')[1].split('<')[0]
                passing_tds = player.split('data-stat="pass_td" >')[1].split('<')[0]
                interceptions = player.split('data-stat="pass_int" >')[1].split('<')[0]
                
                sacks = player.split('data-stat="pass_sacked" >')[1].split('<')[0]
                sack_yards = player.split('data-stat="pass_sacked_yds" >')[1].split('<')[0]
                
                passing_long = player.split('data-stat="pass_long" >')[1].split('<')[0]
                passer_rating = player.split('data-stat="pass_rating" >')[1].split('<')[0]
                if passer_rating == "":
                    passer_rating = None
                rushing_attempts = player.split('data-stat="rush_att" >')[1].split('<')[0]
                rushing_yards = player.split('data-stat="rush_yds" >')[1].split('<')[0]
                rushing_tds = player.split('data-stat="rush_td" >')[1].split('<')[0]
                rushing_long = player.split('data-stat="rush_long" >')[1].split('<')[0]
                
                targets = player.split('data-stat="targets" >')[1].split('<')[0]
                receptions = player.split('data-stat="rec" >')[1].split('<')[0]
                receiving_yards = player.split('data-stat="rec_yds" >')[1].split('<')[0]
                receiving_long = player.split('data-stat="rec_long" >')[1].split('<')[0]
                receiving_tds = player.split('data-stat="rec_tds" >')[1].split('<')[0]
                fumbles = player.split('data-stat="fumbles" >')[1].split('<')[0]
                fumbles_lost = player.split('data-stat="fumbles" >')[1].split('<')[0]

                try:
                    player = PlayerFBR.objects.get(id=slug)
                except:
                    player = PlayerFBR(id=slug, name=name, url=link)
                    player.save()
                try:
                    team = TeamFBR.objects.get(id=team)
                except:
                    team = TeamFBR(id=team, name=team, short_name=team)
                    team.save()

                new_game_stats = GameStats(
                    game=new_game,
                    team=team,
                    player=player,
                    passing_completions=passing_completions,
                    passing_attempts = passing_attempts,
                    passing_yards = passing_yards,
                    passing_tds = passing_tds,
                    interceptions = interceptions,
                    
                    sacks = sacks,
                    sack_yards = sack_yards,
                    
                    passing_long = passing_long,
                    passer_rating = passer_rating,
                    
                    rushing_attempts = rushing_attempts,
                    rushing_yards = rushing_yards,
                    rushing_tds = rushing_tds,
                    rushing_long = rushing_long,
                    
                    targets = targets,
                    receptions = receptions,
                    receiving_yards = receiving_yards,
                    receiving_long = receiving_long,
                    receiving_tds = receiving_tds,
                    fumbles = fumbles,
                    fumbles_lost = fumbles_lost
                )
                new_game_stats.save()
                print(f"SAVED {player.id} on {team.id}")
            
