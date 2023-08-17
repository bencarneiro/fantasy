import requests

from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from football.models import Player, PlayerProjections, DepthChart, InjuryStatus
# from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        dupes = Player.objects.values('name').annotate(Count('id')) .order_by().filter(id__count__gt=1)
        for dupe in dupes:
            player_name = dupe['name']
            duplicate_entries = Player.objects.filter(name=player_name)
            if len(duplicate_entries) == 2:
                print(f"attempting {player_name}")
                fbr_entry = duplicate_entries[0]
                espn_entry = duplicate_entries[1]
                fbr_entry.espn_id = espn_entry.espn_id
                fbr_entry.team_id = espn_entry.team_id
                fbr_entry.save()
                try:
                    depth_chart = DepthChart.objects.get(player_id = espn_entry.id)
                    depth_chart.player_id = fbr_entry.id
                    depth_chart.save()
                except Exception as e:
                    print(f"{player_name} failed on depth_chart {e}")
                try:
                    player_projection = PlayerProjections.objects.get(player_id=espn_entry.id)
                    player_projection.player_id = fbr_entry.id
                    player_projection.save()
                except Exception as e:
                    print(f"{player_name} failed on fantasy projection {e}")
                try:
                    injury_status = InjuryStatus.objects.get(player_id=espn_entry.id)
                    injury_status.player_id = fbr_entry.id
                    injury_status.save()
                except Exception as e:
                    print(f"NO INJURY {e}")
                
                print(f"just finished {player_name}")

            else:
                print(f"Nahhhh that shit didn't work for {player_name}")