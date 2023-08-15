from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Team, Player, DepthChart, Position, InjuryStatus
from time import sleep
import json


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        teams = Team.objects.all()
        for team in teams:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            sleep(3)
            r = requests.get(f"https://www.espn.com/nfl/team/depth/_/name/{team.espn_slug}", headers=headers)
            depth_chart = r.text.split('"dethTeamGroups":')[1].split(',{"name":"')[0]
            depth_chart = depth_chart[1:]
            rows = json.loads(depth_chart)['rows']
            roster_spot = 0
            for row in rows:
                roster_spot += 1
                pos_str = row[0]
                position = Position.objects.get(name=pos_str)
                players = row[1:]
                string = 1
                for player in players:
                    player_name = player['name']
                    injury_list = player['injuries']
                    if len(injury_list) == 1:
                        injury_status = injury_list[0]
                    
                    if len(injury_list) == 0:
                        injury_status = None

                    if len(injury_list) > 1:
                        injury_status = ""
                        for x in injury_list:
                            injury_status += x
                            injury_status += " / "
                        injury_status = injury_status[:-3]


                    espn_player_id = player['href'].split('http://www.espn.com/nfl/player/_/id/')[1].split('/')[0]
                    # print(team)
                    # print(f"{pos_str} - {string}: {player_name}")
                    # print(espn_player_id)
                    potential_match = Player.objects.filter(team=team, name=player_name)
                    if len(potential_match) == 1:
                        unique_player_obj = potential_match[0]
                        unique_player_obj.espn_id = espn_player_id
                        unique_player_obj.save()
                        # print(potential_match[0].fbr_slug)
                    
                    if len(potential_match) == 0:
                        last_name = player_name.split(' ')[-1]
                        if last_name in ["Jr.", "I", "II", "III", "IV", "V"]:
                            last_name = player_name.split(' ')[-2]
                        last_name_match = Player.objects.filter(team=team, name__icontains=last_name)
                        if len(last_name_match) == 1:
                            unique_player_obj = last_name_match[0]
                            unique_player_obj.espn_id = espn_player_id
                            unique_player_obj.save()
                            # print(last_name_match[0].fbr_slug)
                        else:
                            unique_player_obj = Player(
                                name=player_name,
                                espn_id=espn_player_id,
                                team=team,
                            )
                            unique_player_obj.save()
                            # print("CREATE PLAYER ENTRY")
                    unique_player_obj
                    dc = DepthChart(
                        player=unique_player_obj,
                        team=team,
                        position=position,
                        roster_spot=roster_spot,
                        string=string
                    )
                    dc.save()
                    if injury_status:
                        inj_status = InjuryStatus(
                            player=unique_player_obj,
                            status=injury_status
                        )
                        inj_status.save()
                    string += 1