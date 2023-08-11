from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Team, League, Conference, Division


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        conferences = ["AFC East", "AFC North", "AFC South", "AFC West", "NFC East", "NFC North", "NFC South", "NFC West"]
        offense = "https://www.pro-football-reference.com/years/2022/"
        offense_r = requests.get(offense)
        offense_tables = offense_r.text.split("<table") 
        afc_standings = offense_tables[1].split('<a')
        afc_standings = afc_standings[1:]
        nfc_standings = offense_tables[2].split('<a')
        nfc_standings = nfc_standings[1:]
        nfl = League.objects.get(name="National Football League")
        afc = Conference.objects.get(name="American Football Conference")
        nfc = Conference.objects.get(name="National Football Conference")
        counter = 0
        for team in afc_standings:
            team_name = team.split('2022.htm">')[1].split('</a')[0]
            short_name = team_name.split(" ")[-1]
            slug = team.split('/teams/')[1].split('/2022')[0]
            division = Division.objects.get(name=conferences[0])
            counter += 1
            if counter % 4 == 0:
                conferences = conferences[1:]
                counter = 0
            Team(
                name=team_name,
                short_name=short_name,
                slug=slug,
                league=nfl,
                conference=afc,
                division=division
            ).save()
            print(team_name)
            print(division.name)

        for team in nfc_standings:
            team_name = team.split('2022.htm">')[1].split('</a')[0]
            short_name = team_name.split(" ")[-1]
            slug = team.split('/teams/')[1].split('/2022')[0]
            division = Division.objects.get(name=conferences[0])
            counter += 1
            if counter % 4 == 0:
                conferences = conferences[1:]
                counter = 0
            Team(
                name=team_name,
                short_name=short_name,
                slug=slug,
                league=nfl,
                conference=nfc,
                division=division
            ).save()
            print(team_name)
            print(division.name)
