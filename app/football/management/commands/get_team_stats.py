from django.core.management.base import BaseCommand
# import pandas as pd
import requests
from football.models import Team, TeamOffense, TeamDefense
from time import sleep


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for year in range(2003,2023):
            offense = f"https://www.pro-football-reference.com/years/{year}/"
            sleep(4)
            offense_r = requests.get(offense)
            offense_tables = offense_r.text.split("<table")
            # print(offense_tables)
            # print(len(offense_tables))
            team_offense = offense_tables[6].split('data-stat="team"')
            team_offense = team_offense[2:]
            for entry in team_offense:
                # print(entry)
                try:
                    team_slug = entry.split('href="/teams/')[1].split("/")[0]
                    team = Team.objects.get(slug=team_slug)
                    games_played = entry.split('"g" >')[1].split('</td>')[0]
                    points = entry.split('"points" >')[1].split('</td>')[0]
                    total_yards = entry.split('"total_yards" >')[1].split('</td>')[0]
                    plays_offense = entry.split('"plays_offense" >')[1].split('</td>')[0]
                    yds_per_play_offense = entry.split('"yds_per_play_offense" >')[1].split('</td>')[0]
                    turnovers = entry.split('"turnovers" >')[1].split('</td>')[0]
                    fumbles_lost = entry.split('"fumbles_lost" >')[1].split('</td>')[0]
                    first_down = entry.split('"first_down" >')[1].split('</td>')[0]
                    pass_cmp = entry.split('"pass_cmp" >')[1].split('</td>')[0]
                    pass_att = entry.split('"pass_att" >')[1].split('</td>')[0]
                    pass_yds = entry.split('"pass_yds" >')[1].split('</td>')[0]
                    pass_td = entry.split('"pass_td" >')[1].split('</td>')[0]
                    pass_int = entry.split('"pass_int" >')[1].split('</td>')[0]
                    pass_net_yds_per_att = entry.split('"pass_net_yds_per_att" >')[1].split('</td>')[0]
                    pass_fd = entry.split('"pass_fd" >')[1].split('</td>')[0]
                    rush_att = entry.split('"rush_att" >')[1].split('</td>')[0]
                    rush_yds = entry.split('"rush_yds" >')[1].split('</td>')[0]
                    rush_td = entry.split('"rush_td" >')[1].split('</td>')[0]
                    rush_yds_per_att = entry.split('"rush_yds_per_att" >')[1].split('</td>')[0]
                    rush_fd = entry.split('"rush_fd" >')[1].split('</td>')[0]
                    penalties = entry.split('"penalties" >')[1].split('</td>')[0]
                    penalties_yds = entry.split('"penalties_yds" >')[1].split('</td>')[0]
                    pen_fd = entry.split('"pen_fd" >')[1].split('</td>')[0]
                    score_pct = entry.split('"score_pct" >')[1].split('</td>')[0]
                    turnover_pct = entry.split('"turnover_pct" >')[1].split('</td>')[0]
                    exp_pts_tot = entry.split('"exp_pts_tot" >')[1].split('</td>')[0]
                    team_offense = TeamOffense(
                        team=team,
                        year=year,
                        games_played=games_played,
                        points=points,
                        total_yards=total_yards,
                        plays_offense=plays_offense,
                        yds_per_play_offense=yds_per_play_offense,
                        turnovers=turnovers,
                        fumbles_lost=fumbles_lost,
                        first_down=first_down,
                        pass_cmp=pass_cmp,
                        pass_att=pass_att,
                        pass_yds=pass_yds,
                        pass_td=pass_td,
                        pass_int=pass_int,
                        pass_net_yds_per_att=pass_net_yds_per_att,
                        pass_fd=pass_fd,
                        rush_att=rush_att,
                        rush_yds=rush_yds,
                        rush_td=rush_td,
                        rush_yds_per_att=rush_yds_per_att,
                        rush_fd=rush_fd,
                        penalties=penalties,
                        penalties_yds=penalties_yds,
                        pen_fd=pen_fd,
                        score_pct=score_pct,
                        turnover_pct=turnover_pct,
                        exp_pts_tot=exp_pts_tot
                    )
                    team_offense.save()
                    print(f"{year} {team_offense.team.name} offense saved")
                    # print("saved")
                    # print(team_offense.team.name)
                except Exception as e:
                    print(year)
                    print(e)
                    print("finished offense")

                

            
            defense = f"https://www.pro-football-reference.com/years/{year}/opp.htm"
            sleep(4)
            defense_r = requests.get(defense)
            defense_tables = defense_r.text.split("<table")
            team_defense = defense_tables[1].split('data-stat="team"')
            team_defense = team_defense[2:]
            for entry in team_defense:
                try:
                    # print(entry)
                    team_slug = entry.split('href="/teams/')[1].split("/")[0]
                    team = Team.objects.get(slug=team_slug)
                    games_played = entry.split('"g" >')[1].split('</td>')[0]
                    points = entry.split('"points" >')[1].split('</td>')[0]
                    total_yards = entry.split('"total_yards" >')[1].split('</td>')[0]
                    plays_offense = entry.split('"plays_offense" >')[1].split('</td>')[0]
                    yds_per_play_offense = entry.split('"yds_per_play_offense" >')[1].split('</td>')[0]
                    turnovers = entry.split('"turnovers" >')[1].split('</td>')[0]
                    fumbles_lost = entry.split('"fumbles_lost" >')[1].split('</td>')[0]
                    first_down = entry.split('"first_down" >')[1].split('</td>')[0]
                    pass_cmp = entry.split('"pass_cmp" >')[1].split('</td>')[0]
                    pass_att = entry.split('"pass_att" >')[1].split('</td>')[0]
                    pass_yds = entry.split('"pass_yds" >')[1].split('</td>')[0]
                    pass_td = entry.split('"pass_td" >')[1].split('</td>')[0]
                    pass_int = entry.split('"pass_int" >')[1].split('</td>')[0]
                    pass_net_yds_per_att = entry.split('"pass_net_yds_per_att" >')[1].split('</td>')[0]
                    pass_fd = entry.split('"pass_fd" >')[1].split('</td>')[0]
                    rush_att = entry.split('"rush_att" >')[1].split('</td>')[0]
                    rush_yds = entry.split('"rush_yds" >')[1].split('</td>')[0]
                    rush_td = entry.split('"rush_td" >')[1].split('</td>')[0]
                    rush_yds_per_att = entry.split('"rush_yds_per_att" >')[1].split('</td>')[0]
                    rush_fd = entry.split('"rush_fd" >')[1].split('</td>')[0]
                    penalties = entry.split('"penalties" >')[1].split('</td>')[0]
                    penalties_yds = entry.split('"penalties_yds" >')[1].split('</td>')[0]
                    pen_fd = entry.split('"pen_fd" >')[1].split('</td>')[0]
                    score_pct = entry.split('"score_pct" >')[1].split('</td>')[0]
                    turnover_pct = entry.split('"turnover_pct" >')[1].split('</td>')[0]
                    exp_pts_def_tot = entry.split('"exp_pts_def_tot" >')[1].split('</td>')[0]
                    team_defense = TeamDefense(
                        team=team,
                        year=year,
                        games_played=games_played,
                        points=points,
                        total_yards=total_yards,
                        plays_offense=plays_offense,
                        yds_per_play_offense=yds_per_play_offense,
                        turnovers=turnovers,
                        fumbles_lost=fumbles_lost,
                        first_down=first_down,
                        pass_cmp=pass_cmp,
                        pass_att=pass_att,
                        pass_yds=pass_yds,
                        pass_td=pass_td,
                        pass_int=pass_int,
                        pass_net_yds_per_att=pass_net_yds_per_att,
                        pass_fd=pass_fd,
                        rush_att=rush_att,
                        rush_yds=rush_yds,
                        rush_td=rush_td,
                        rush_yds_per_att=rush_yds_per_att,
                        rush_fd=rush_fd,
                        penalties=penalties,
                        penalties_yds=penalties_yds,
                        pen_fd=pen_fd,
                        score_pct=score_pct,
                        turnover_pct=turnover_pct,
                        exp_pts_def_tot=exp_pts_def_tot
                    )
                    team_defense.save()
                    print(f"{year} {team_defense.team.name} defense saved")
                    # print("saved")
                    # print(team_offense.team.name)
                except Exception as e:
                    print(year)
                    print("finished defense")
                    print(e)
            