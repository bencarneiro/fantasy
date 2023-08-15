from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Team, TeamOffense, TeamDefense, Position, Player, PlayerPassingByTeam, PlayerScrimmageByTeam
from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        teams = Team.objects.all()
        for year in range(2006,2023):
            for team in teams:
                sleep(3)
                r = requests.get(f"https://www.pro-football-reference.com/teams/{team.slug}/{year}.htm").text
                """
                This is where we steal the passing data
                
                """
                table = r.split("<table")[4]
                # print(table)
                players = table.split('<th scope="row" class="right "')
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
                    # try:
                    #     team_slug = player.split('<a href="/teams/')[1].split('/')[0]
                    #     team = Team.objects.get(slug=team_slug)
                    # except:
                    #     team = None
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
                    # pass_first_down = player.split('data-stat="pass_first_down" >')[1].split('<')[0]
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
                    ppbt = PlayerPassingByTeam(
                        player=player_obj,
                        team=team,
                        pos=position,
                        year=year,
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
                        pass_long=pass_long,
                        pass_yds_per_att=pass_yds_per_att,
                        pass_adj_yds_per_att=pass_adj_yds_per_att,
                        pass_yds_per_cmp=pass_yds_per_cmp,
                        pass_yds_per_g=pass_yds_per_g,
                        pass_rating=pass_rating,
                        pass_sacked=pass_sacked,
                        pass_sacked_yds=pass_sacked_yds,
                        pass_sacked_perc=pass_sacked_perc,
                        pass_net_yds_per_att=pass_net_yds_per_att,
                        pass_adj_net_yds_per_att=pass_adj_net_yds_per_att,
                        qbr=qbr,
                        comebacks=comebacks,
                        gwd=gwd
                    )
                    ppbt.save()
                    print(f"{year} - {player_obj.name} - {team.name} - Passing SAVED")
                """
                This is where we steal the Scrimmage data
                
                """
                table = r.split("<table")[5]
                # print(table)
                players = table.split('<th scope="row" class="right "')
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
                    # try:
                    #     team_slug = player.split('<a href="/teams/')[1].split('/')[0]
                    #     team = Team.objects.get(slug=team_slug)
                    # except:
                    #     team = None
                    age = player.split('data-stat="age" >')[1].split('<')[0]
                    position_str = player.split('data-stat="pos" >')[1].split("<")[0]
                    try:
                        position = Position.objects.get(name=position_str)
                    except:
                        position = None
                    g = player.split('data-stat="g" >')[1].split('<')[0]
                    gs = player.split('data-stat="gs" >')[1].split('<')[0]
                    rush_att = player.split('data-stat="rush_att" >')[1].split('<')[0]
                    if not rush_att:
                        rush_att = 0
                    rush_yds = player.split('data-stat="rush_yds" >')[1].split('<')[0]
                    if not rush_yds:
                        rush_yds = 0
                    rush_td = player.split('data-stat="rush_td" >')[1].split('<')[0]
                    if not rush_td:
                        rush_td = 0
                    rush_long = player.split('data-stat="rush_long" >')[1].split('<')[0]
                    if not rush_long:
                        rush_long = 0
                    rush_yds_per_att = player.split('data-stat="rush_yds_per_att" >')[1].split('<')[0]
                    if not rush_yds_per_att:
                        rush_yds_per_att = 0
                    rush_yds_per_g = player.split('data-stat="rush_yds_per_g" >')[1].split('<')[0]
                    if not rush_yds_per_g:
                        rush_yds_per_g = 0
                    rush_att_per_g = player.split('data-stat="rush_att_per_g" >')[1].split('<')[0]
                    if not rush_att_per_g:
                        rush_att_per_g = 0
                    targets = player.split('data-stat="targets" >')[1].split('<')[0]
                    if not targets:
                        targets = 0
                    rec = player.split('data-stat="rec" >')[1].split('<')[0]
                    if not rec:
                        rec = 0
                    rec_yds = player.split('data-stat="rec_yds" >')[1].split('<')[0]
                    if not rec_yds:
                        rec_yds = 0
                    rec_yds_per_rec = player.split('data-stat="rec_yds_per_rec" >')[1].split('<')[0]
                    if not rec_yds_per_rec:
                        rec_yds_per_rec = 0
                    rec_td = player.split('data-stat="rec_td" >')[1].split('<')[0]
                    if not rec_td:
                        rec_td = 0
                    rec_long = player.split('data-stat="rec_long" >')[1].split('<')[0]
                    if not rec_long:
                        rec_long = 0
                    rec_per_g = player.split('data-stat="rec_per_g" >')[1].split('<')[0]
                    if not rec_per_g:
                        rec_per_g= 0
                    rec_yds_per_g = player.split('data-stat="rec_yds_per_g" >')[1].split('<')[0]
                    if not rec_yds_per_g:
                        rec_yds_per_g = 0
                    catch_pct = player.split('data-stat="catch_pct" >')[1].split('<')[0]
                    if not catch_pct:
                        catch_pct = 0
                    else:
                        catch_pct = catch_pct[:-1]
                    rec_yds_per_tgt = player.split('data-stat="gs" >')[1].split('<')[0]
                    if not rec_yds_per_tgt:
                         rec_yds_per_tgt = 0
                    touches = player.split('data-stat="gs" >')[1].split('<')[0]
                    if not touches:
                        touches = 0
                    yds_per_touch = player.split('data-stat="gs" >')[1].split('<')[0]
                    if not yds_per_touch:
                        yds_per_touch = 0
                    yds_from_scrimmage = player.split('data-stat="gs" >')[1].split('<')[0]
                    if not yds_from_scrimmage:
                        yds_from_scrimmage = 0
                    rush_receive_td = player.split('data-stat="gs" >')[1].split('<')[0]
                    if not rush_receive_td:
                        rush_receive_td = 0
                    fumbles = player.split('data-stat="gs" >')[1].split('<')[0]
                    if not fumbles:
                        fumbles = 0
                    psbt = PlayerScrimmageByTeam(
                        player=player_obj,
                        team=team,
                        pos=position,
                        year=year,
                        age=age,
                        g=g,
                        gs=gs,
                        rush_att=rush_att,
                        rush_yds=rush_yds,
                        rush_td=rush_td,
                        rush_long=rush_long,
                        rush_yds_per_att=rush_yds_per_att,
                        rush_yds_per_g=rush_yds_per_g,
                        rush_att_per_g=rush_att_per_g,
                        targets=targets,
                        rec=rec,
                        rec_yds=rec_yds,
                        rec_yds_per_rec=rec_yds_per_rec,
                        rec_td=rec_td,
                        rec_long=rec_long,
                        rec_per_g=rec_per_g,
                        rec_yds_per_g=rec_yds_per_g,
                        catch_pct=catch_pct,
                        rec_yds_per_tgt=rec_yds_per_tgt,
                        touches=touches,
                        yds_per_touch=yds_per_touch,
                        yds_from_scrimmage=yds_from_scrimmage,
                        rush_receive_td=rush_receive_td,
                        fumbles=fumbles
                    )
                    psbt.save()

                    print(f"{year} - {player_obj.name} - {team.name} - Scrimmage SAVED")