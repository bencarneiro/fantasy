import requests

from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Position, Player, PlayerPassing, Team
from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for year in range(2006,2023):
            sleep(3)
            w = requests.get(f"https://www.pro-football-reference.com/years/{year}/passing.htm").text
            players = w.split('<th scope="row" class="right "')
            players = players[2:]
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
                qb_rec = player.split('data-stat="qb_rec"')[1].split('>')[1].split('<')[0]
                pass_cmp = player.split('data-stat="pass_cmp" >')[1].split('<')[0]
                pass_att = player.split('data-stat="pass_att" >')[1].split('<')[0]
                pass_cmp_perc = player.split('data-stat="pass_cmp_perc" >')[1].split('<')[0]
                pass_yds = player.split('data-stat="pass_yds" >')[1].split('<')[0]
                pass_td = player.split('data-stat="pass_td" >')[1].split('<')[0]
                pass_td_perc = player.split('data-stat="pass_td_perc" >')[1].split('<')[0]
                pass_int = player.split('data-stat="pass_int" >')[1].split('<')[0]
                pass_int_perc = player.split('data-stat="pass_int_perc" >')[1].split('<')[0]
                pass_first_down = player.split('data-stat="pass_first_down" >')[1].split('<')[0]
                pass_long = player.split('data-stat="pass_long" >')[1].split('<')[0]
                pass_yds_per_att = player.split('data-stat="pass_yds_per_att" >')[1].split('<')[0]
                pass_adj_yds_per_att = player.split('data-stat="pass_adj_yds_per_att" >')[1].split('<')[0]
                pass_yds_per_cmp = player.split('data-stat="pass_yds_per_cmp" >')[1].split('<')[0]
                if not pass_yds_per_cmp:
                    pass_yds_per_cmp = 0
                pass_yds_per_g = player.split('data-stat="pass_yds_per_g" >')[1].split('<')[0]
                pass_rating = player.split('data-stat="pass_rating" >')[1].split('<')[0]
                qbr = player.split('data-stat="qbr" >')[1].split('<')[0]
                if not qbr:
                    qbr = 0
                pass_sacked = player.split('data-stat="pass_sacked" >')[1].split('<')[0]
                pass_sacked_yds = player.split('data-stat="pass_sacked_yds" >')[1].split('<')[0]
                pass_sacked_perc = player.split('data-stat="pass_sacked_perc" >')[1].split('<')[0]
                pass_net_yds_per_att = player.split('data-stat="pass_net_yds_per_att" >')[1].split('<')[0]
                pass_adj_net_yds_per_att = player.split('data-stat="pass_adj_net_yds_per_att" >')[1].split('<')[0]
                comebacks = player.split('data-stat="comebacks" >')[1].split('<')[0]
                if not comebacks:
                    comebacks = 0
                gwd = player.split('data-stat="gwd" >')[1].split('<')[0]
                if not gwd:
                    gwd = 0
                new_player_passing_entry = PlayerPassing(
                    player=player_obj,
                    year=year,
                    team=team,
                    pos=position,
                    age=age,
                    g=g,
                    gs=gs,
                    qb_rec=qb_rec,
                    pass_cmp=pass_cmp,
                    pass_att=pass_att,
                    pass_cmp_perc=pass_cmp_perc,
                    pass_yds=pass_yds,
                    pass_td=pass_td,
                    pass_td_perc=pass_td_perc,
                    pass_int=pass_int,
                    pass_int_perc=pass_int_perc,
                    pass_first_down=pass_first_down,
                    pass_long=pass_long,
                    pass_yds_per_att=pass_yds_per_att,
                    pass_adj_yds_per_att=pass_adj_yds_per_att,
                    pass_yds_per_cmp=pass_yds_per_cmp,
                    pass_yds_per_g=pass_yds_per_g,
                    pass_rating=pass_rating,
                    qbr=qbr,
                    pass_sacked=pass_sacked,
                    pass_sacked_yds=pass_sacked_yds,
                    pass_sacked_perc=pass_sacked_perc,
                    pass_net_yds_per_att=pass_net_yds_per_att,
                    pass_adj_net_yds_per_att=pass_adj_net_yds_per_att,
                    comebacks=comebacks,
                    gwd=gwd
                )
                new_player_passing_entry.save()

                print(f"SLUG: {player_slug}")
                print(f"year: {year}")
                # print(f"team slug: {team_slug}")
                print(f"age: {age}")
                print(f"Position: {position.full_name}")


            #     name = team.split("</a>")[0]
            
            #     data += [[team_name, wins, losses, ties, win_loss_perc, points, points_opp, points_diff, mov, sos_total, srs_total, srs_offense, srs_defense]]
            # standings = pd.DataFrame(columns=columns, data=data)
            # standings

        # class Player(models.Model):

        # id = models.AutoField(primary_key=True)
        # fbr_slug = models.CharField(max_length=64)
        # name = models.CharField(max_length=256)
        # team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
        

        # player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
        # year = models.SmallIntegerField(null=False)
        # team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
        # age = models.SmallIntegerField(null=False)
        # pos = models.CharField(max_length=16, default=None)
        # g = models.SmallIntegerField(null=False)
        # gs = models.SmallIntegerField(null=False)
        # qb_rec = models.CharField(max_length=32, default=None)
        # pass_cmp = models.SmallIntegerField(null=False)
        # pass_att = models.SmallIntegerField(null=False)
        # pass_cmp_perc = models.FloatField(null=False)
        # pass_yds = models.SmallIntegerField(null=False)
        # pass_td = models.SmallIntegerField(null=False)
        # pass_td_perc = models.FloatField()
        # pass_int = models.SmallIntegerField(null=False)
        # pass_int_perc = models.FloatField()
        # pass_first_down = models.SmallIntegerField(null=False)
        # pass_long = models.SmallIntegerField(null=False)
        # pass_yds_per_att = models.FloatField()
        # pass_adj_yds_per_att = models.FloatField()
        # pass_yds_per_cmp = models.FloatField()
        # pass_yds_per_g = models.FloatField()
        # pass_rating = models.FloatField()
        # qbr = models.FloatField()
        # pass_sacked = models.SmallIntegerField(null=False)
        # pass_sacked_yds = models.SmallIntegerField(null=False)
        # pass_sacked_perc = models.FloatField()
        # pass_net_yds_per_att = models.FloatField()
        # pass_adj_net_yds_per_att = models.FloatField()
        # comebacks = models.SmallIntegerField(null=False)
        # gwd = models.SmallIntegerField(null=False)
