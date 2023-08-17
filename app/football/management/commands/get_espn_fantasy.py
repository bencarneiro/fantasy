from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from time import sleep
from football.models import Player, PlayerProjections, Team


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        api_url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2023/segments/0/leaguedefaults/3?view=kona_player_info"
        offset = 0
        more_players = True
        while more_players:
            header_string_1 = '{"players":{"filterStatsForExternalIds":{"value":[2022,2023]},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForSourceIds":{"value":[0,1]},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102023"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"STANDARD"},"sortPercOwned":{"sortAsc":false,"sortPriority":4},"limit":50,"offset":'
            header_string_2 = ',"filterRanksForScoringPeriodIds":{"value":[1]},"filterRanksForRankTypes":{"value":["STANDARD"]},"filterRanksForSlotIds":{"value":[0,2,4,6,17,16]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002023","102023","002022","022023"]}}}'
            header_string = header_string_1 + str(offset) + header_string_2
            headers = {'x-fantasy-filter': header_string}
            sleep(2)
            r = requests.get(api_url, headers=headers)
            response = r.json()
            # print(response)
            if len(response['players']) == 0:
                more_players = False
            for player in response['players']:
                player_espn_id = player['id']
                try:
                    player_obj = Player.objects.get(espn_id=player_espn_id)
                except:
                    player_name = player['player']['fullName']
                    try:
                        player_obj = Player.objects.get(name=player_name)
                        player_obj.espn_id = player_espn_id
                        player_obj.save()
                    except:
                        last_initial = player_name.split(' ')[-1][0]
                        player_url = f"https://www.pro-football-reference.com/players/{last_initial}/{player_espn_id}.htm"
                        # print(player_url)
                        sleep(2)
                        player_page = requests.get(player_url).text
                        try:
                            team_slug = player_page.split('<strong>Team</strong>: <span><a href="')[1][7:10]
                            team = Team.objects.get(slug=team_slug)
                        except:
                            team = None
                        player_obj = Player(
                            espn_id = player_espn_id,
                            name = player_name, 
                            team = team
                        )
                        player_obj.save()

                proj_points = player['player']['stats'][-1]['appliedTotal']

                try:
                    proj_carries =  player['player']['stats'][-1]['stats']['23']
                except:
                    proj_carries = 0
                try:
                    proj_rush_yd =  player['player']['stats'][-1]['stats']['24']
                except:
                    proj_rush_yd = 0
                try:
                    proj_rush_td =  player['player']['stats'][-1]['stats']['25']
                except:
                    proj_rush_td = 0
                try:
                    proj_tgt =  player['player']['stats'][-1]['stats']['58']
                except:
                    proj_tgt = 0
                try:
                    proj_rec =  player['player']['stats'][-1]['stats']['53']
                except:
                    proj_rec = 0
                try:
                    proj_rec_yd =  player['player']['stats'][-1]['stats']['42']
                except:
                    proj_rec_yd = 0
                try:
                    proj_rec_td =  player['player']['stats'][-1]['stats']['43']
                except:
                    proj_rec_td = 0
                    
                player_proj = PlayerProjections(
                    player=player_obj,
                    proj_points=proj_points,
                    proj_carries=proj_carries,
                    proj_rush_yd=proj_rush_yd,
                    proj_rush_td=proj_rush_td,
                    proj_tgt=proj_tgt,
                    proj_rec=proj_rec,
                    proj_rec_yd=proj_rec_yd,
                    proj_rec_td=proj_rec_td
                )
                player_proj.save()
                print(f"{player_proj.player.name} is saved")
            offset += 50




    # PROJ
# 23: Carries
# 24: Rushing Yards
# 25: Rushing TDs
    
# 53: Receptions
# 42: Receiving Yards
# 43: Receiving TDs
# 58: Targets

    # player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    # proj_carries = models.FloatField(null=True)
    # proj_rush_yd  = models.FloatField(null=True)
    # proj_rush_td = models.FloatField(null=True)
    # proj_tgt = models.FloatField(null=True)
    # proj_rec = models.FloatField(null=True)
    # proj_rec_yd = models.FloatField(null=True)
    # proj_rec_td = models.FloatField(null=True)
    # proj_points = models.FloatField(null=True)