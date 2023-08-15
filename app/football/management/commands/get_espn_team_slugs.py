from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Team


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get('https://www.espn.com/nfl/teams', headers=headers)
        teams = r.text.split('<section class="TeamLinks flex items-center">')
        teams = teams[1:]
        for team in teams:
            team_name = team.split('alt="')[1].split('"')[0]
            espn_slug = team.split('/nfl/team/_/name/')[1].split('/')[0]
            team_obj = Team.objects.get(name=team_name)
            team_obj.espn_slug = espn_slug
            team_obj.save()
