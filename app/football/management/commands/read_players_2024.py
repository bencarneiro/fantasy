from time import sleep
import requests
from django.core.management.base import BaseCommand

from football.models import PlayerFBR, TeamFBR


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        roster_links = [
            'https://www.pro-football-reference.com/teams/crd/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/atl/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/rav/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/buf/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/car/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/chi/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/cin/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/cle/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/dal/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/den/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/det/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/gnb/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/htx/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/clt/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/jax/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/kan/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/rai/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/sdg/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/ram/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/mia/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/min/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/nwe/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/nor/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/nyg/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/nyj/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/phi/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/pit/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/sfo/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/sea/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/tam/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/oti/2024_roster.htm',
            'https://www.pro-football-reference.com/teams/was/2024_roster.htm',
        ]
        for link in roster_links:
            team = TeamFBR.objects.get(fbr_slug=link.split("/teams/")[1].split("/")[0])
            team_id = team.id
            sleep(6)
            r = requests.get(link)
            players = r.text.split('<tr >')[1:]
            for player in players:
                try:
                    id = player.split('data-append-csv="')[1].split('"')[0]
                except:
                    continue
                position = player.split('data-stat="pos"')[1].split('>')[1].split("<")[0]
                name = player.split('data-stat="player"')[1].split('.htm">')[1].split("<")[0]
                age = player.split(' data-stat="age" >')[1].split('<')[0]
                if not age:
                    age = "NULL"
                url = player.split('<a href="')[1].split('"')[0]
                print()
                print(f"""
                INSERT INTO player_fbr
                (`id`, `name`, `url`, `position`, `age`, `team_id`)
                VALUES
                ("{id}", "{name}", "{url}", "{position}", {age}, "{team_id}");
                """)