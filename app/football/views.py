from django.shortcuts import render

# Create your views here.


from django.db.models import Sum, Count, Q, F, Avg, Value, FloatField
from django.db.models.functions import Round, Cast

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from football.models import GameStats, InjuryStatus, DepthChart, PlayerPassing, PlayerProjections, DepthChart, PlayerKicking, PlayerRushing, PlayerReceiving, PlayerReturning, Team, TeamOffense, TeamDefense, PlayerPassingByTeam, PlayerScrimmageByTeam, DefensivePoints

@csrf_exempt
def depth_chart(request):
    print(request.GET)
    if "team" in request.GET and request.GET['team']:
        chart = DepthChart.objects.filter(team_id__slug=request.GET['team'])
        for ch in chart:
            print(ch.player.name)
            print(f"{ch.position.name} - {ch.string}")
            pass_yds = PlayerPassing.objects.filter(player=ch.player, year=2022)
            if len(pass_yds) > 0:
                print(pass_yds[0].pass_yds)
        return JsonResponse({"Hi": "Hello"})

    return JsonResponse({"Good": "Bye"})

@csrf_exempt
def home(request):
    if "position" in request.GET and request.GET['position']:
        position_param = request.GET['position']
    else:
        position_param = None
    players = []
    fantasy_projections = PlayerProjections.objects.all()
    index = 1
    for player_projection in fantasy_projections:
        espn_link = "https://www.espn.com/nfl/player/stats/_/id/" + str(player_projection.player.espn_id)
        if player_projection.proj_points < .25:
            continue
        # if player_projection.proj_points ==
        ppr = player_projection.proj_points
        standard = ppr - player_projection.proj_rec


        passing_data = PlayerPassing.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            # yards_per_game=Sum("pass_yds")/Sum("g"),
            # td_per_game=Sum("pass_td")/Sum("g"),
            attempts=Sum("pass_att"),
            completions=Sum("pass_cmp"),
            yards=Sum("pass_yds"),
            interceptions=Sum("pass_int"),
            g=Sum("g"),
            tds=Sum("pass_td"),
            points=( Sum("pass_yds") / 25 ) + (Sum("pass_td") * 6)
        )
        if passing_data['g']:
            pass_att_per_game = passing_data['attempts'] / passing_data['g']
            pass_cmp_per_game = passing_data['completions'] / passing_data['g']
            pass_yds_per_game = passing_data['yards'] / passing_data['g']
            pass_td_per_game = passing_data['tds'] / passing_data['g']
            int_per_game = passing_data['interceptions'] / passing_data['g']
        else:
            pass_att_per_game = 0
            pass_cmp_per_game = 0
            pass_yds_per_game = 0
            pass_td_per_game = 0
            int_per_game = 0

        rushing_data = PlayerRushing.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            # yards_per_carry=Sum("rush_yds")/Sum("rush_att"),
            attempts=Sum("rush_att"),
            yards=Sum("rush_yds"),
            tds=Sum("rush_td"),
            g=Sum("g"),
            points=( Sum("rush_yds") / 10 ) + (Sum("rush_td") * 6)
        )

        if rushing_data['g']:
            rush_att_per_game = rushing_data['attempts'] / rushing_data['g']
            rush_yds_per_game = rushing_data['yards'] / rushing_data['g']
            rush_td_per_game = rushing_data['tds'] / rushing_data['g']
        else:
            rush_att_per_game = 0
            rush_yds_per_game = 0
            rush_td_per_game = 0

        if rushing_data['attempts']:
            yards_per_carry = rushing_data['yards'] / rushing_data['attempts']
        else:
            yards_per_carry = 0


        receiving_data = PlayerReceiving.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            # yards_per_reception=Sum("rec_yds")/Sum("rec"),
            targets=Sum("targets"),
            receptions=Sum("rec"),
            yards=Sum("rec_yds"),
            tds=Sum("rec_td"),
            g=Sum("g"),
            points=( Sum("rec_yds") / 10 ) + (Sum("rec_td") * 6),
            points_ppr=( Sum("rec_yds") / 10 ) + (Sum("rec_td") * 6) + (Sum("rec"))
            # points_per_g=(( Sum("rec_yds") / 10 ) + (Sum("rec_td") * 6)) / (Sum("g")),
            # points_per_g_ppr=(( Sum("rec_yds") / 10 ) + (Sum("rec_td") * 6) + (Sum("rec"))) / (Sum("g"))
        )

        if receiving_data['g']:
            rec_tgt_per_game = receiving_data['targets'] / receiving_data['g']
            rec_rec_per_game = receiving_data['receptions'] / receiving_data['g']
            rec_yds_per_game = receiving_data['yards'] / receiving_data['g']
            rec_td_per_game = receiving_data['tds'] / receiving_data['g']
        else:
            rec_tgt_per_game = 0
            rec_rec_per_game = 0
            rec_yds_per_game = 0
            rec_td_per_game = 0
        
        if receiving_data['receptions']:
            yards_per_catch = receiving_data['yards'] / receiving_data['receptions']
        else:
            yards_per_catch = 0

        kicking_data = PlayerKicking.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            fga=Sum("fga"),
            fgm=Sum("fgm"),
            fga_1=Sum("fga1"),
            fgm_1=Sum("fgm1"),
            fga_2=Sum("fga2"),
            fgm_2=Sum("fgm2"),
            fga_3=Sum("fga3"),
            fgm_3=Sum("fgm3"),
            fga_4=Sum("fga4"),
            fgm_4=Sum("fgm4"),
            fga_5=Sum("fga5"),
            fgm_5=Sum("fgm5"),
            xpa_1=Sum("xpa"),
            xpm_1=Sum("xpm"),
            g=Sum("g"),
            points=((Sum(F("fgm1")) * 3) - (Sum(F("fga1")) - Sum(F("fgm1")))) + ((Sum(F("fgm2")) * 3) - (Sum(F("fga2")) - Sum(F("fgm2")))) + ((Sum(F("fgm3")) * 3) - (Sum(F("fga3")) - Sum(F("fgm3")))) + ((Sum(F("fgm4")) * 4) - (Sum(F("fga4")) - Sum(F("fgm4")))) + ((Sum(F("fgm5")) * 5) - (Sum(F("fga5")) - Sum(F("fgm5")))) + (Sum(F("xpm")) - (Sum(F("xpa")) - Sum(F("xpm"))))
            # points=( Sum("rec_yds") / 10 ) + (Sum("rec_td") * 6),
            # points_ppr=( Sum("rec_yds") / 10 ) + (Sum("rec_td") * 6) + (Sum("rec"))
        )

        

        if not passing_data['seasons'] and not rushing_data['seasons'] and not receiving_data['seasons'] and not kicking_data['seasons']:
            ppr_avg = None
            standard_avg = None
        else:
            seasons = 0
            if passing_data['seasons'] and passing_data['seasons'] > seasons:
                seasons = passing_data['seasons']
            if rushing_data['seasons'] and rushing_data['seasons'] > seasons:
                seasons = rushing_data['seasons']
            if receiving_data['seasons'] and receiving_data['seasons'] > seasons:
                seasons = receiving_data['seasons']
            if kicking_data['seasons'] and kicking_data['seasons'] > seasons:
                seasons = kicking_data['seasons']
            if not passing_data['points']:
                pass_pts = 0
            else:
                pass_pts = passing_data['points']
            if not rushing_data['points']:
                rush_pts = 0
            else:
                rush_pts = rushing_data['points']
            if not kicking_data['points']:
                kicking_pts = 0
            else:
                kicking_pts = kicking_data['points']
            if not receiving_data['points']:
                rec_pts = 0
            else:
                rec_pts = receiving_data['points']
            if not receiving_data['points_ppr']:
                rec_pts_ppr = 0
            else:
                rec_pts_ppr = receiving_data['points_ppr']
            ppr_avg = round((rec_pts_ppr + rush_pts + pass_pts + kicking_pts) / seasons)
            standard_avg = round((rec_pts + rush_pts + pass_pts + kicking_pts) / seasons)


        if not passing_data['g'] and not rushing_data['g'] and not receiving_data['g'] and not kicking_data['g']:
            ppg_ppr = None
            ppg_standard = None
        else:
            g = 0
            if passing_data['g'] and passing_data['g'] > g:
                g = passing_data['g']
            if rushing_data['g'] and rushing_data['g'] > g:
                g = rushing_data['g']
            if receiving_data['g'] and receiving_data['g'] > g:
                g = receiving_data['g']
            if kicking_data['g'] and kicking_data['g'] > g:
                g = kicking_data['g']
            # if not passing_data['points']:
            #     pass_pts = 0
            # else:
            #     pass_pts = passing_data['points']
            # if not rushing_data['points']:
            #     rush_pts = 0
            # else:
            #     rush_pts = rushing_data['points']
            # if not receiving_data['points']:
            #     rec_pts = 0
            # else:
            #     rec_pts = receiving_data['points']
            # if not receiving_data['points_ppr']:
            #     rec_pts_ppr = 0
            # else:
            #     rec_pts_ppr = receiving_data['points_ppr']
            ppg_ppr = round((rec_pts_ppr + rush_pts + pass_pts + kicking_pts) / g, 1)
            ppg_standard = round((rec_pts + rush_pts + pass_pts + kicking_pts) / g, 1)


        if not rushing_data['attempts'] and not receiving_data['receptions']:
            points_per_touch_ppr = None
            points_per_touch_standard = None
            touches = None
        else:
            touches = 0
            if rushing_data['attempts']:
                touches += rushing_data['attempts']
            if receiving_data['receptions']:
                touches += receiving_data['receptions']

            if not rushing_data['points']:
                rush_pts = 0
            else:
                rush_pts = rushing_data['points']

            if not receiving_data['points']:
                rec_pts = 0
            else:
                rec_pts = receiving_data['points']

            if not receiving_data['points_ppr']:
                rec_pts_ppr = 0
            else:
                rec_pts_ppr = receiving_data['points_ppr']

            points_per_touch_ppr = round((rec_pts_ppr + rush_pts) / touches, 2)
            points_per_touch_standard = round((rec_pts + rush_pts) / touches, 2)


        if player_projection.player.team:
            team_name = player_projection.player.team.short_name
            team_url = "/team/?team=" + player_projection.player.team.slug
        else:
            team_name = "Free Agent"
            team_url = ""
        player_id = player_projection.player.id

        depth_chart = DepthChart.objects.filter(player_id=player_id)
        if len(depth_chart) >= 1:
            position = depth_chart[0].position.name
            # roster_spot = depth_chart[0].roster_spot
            string = depth_chart[0].string
        elif "D/ST" in player_projection.player.name:
            position = "D/ST"
            team_name = player_projection.player.name.split(" ")[0]
            # roster_spot = 1
            string = 1
            def_pts = DefensivePoints.objects.get(year=2022,team_id__short_name=team_name)
            ppr_avg = def_pts.points
            standard_avg = def_pts.points
            if team_name in ['Bills', 'Bengals']:
                ppg_ppr = round(def_pts.points / 16, 1)
                ppg_standard = round(def_pts.points / 16, 1)
            else:
                ppg_ppr = round(def_pts.points / 17, 1)
                ppg_standard = round(def_pts.points / 17, 1)
            # defense_team = Team.objects.get(short_name=player_projection.player.name.split(" ")[0])
            # team_defense = TeamDefense.objects.filter(team=defense_team, year__lte=2022, year__gte=2020).aggregate(
            #     g=Sum("games_played"),
            #     points=Sum("points"),
            #     turnovers=Sum("turnovers")
            # )
            # points_allowed_per_game = team_defense['points'] / team_defense['g']
            # turnovers_per_game = team_defense['turnovers'] / team_defense['g']
            # print(points_allowed_per_game)
            # print(turnovers_per_game)
        else:
            pk = PlayerKicking.objects.filter(player_id=player_projection.player.id)
            if len(pk) > 0:
                position = "K"
                # roster_spot = 1
                string = 1
            else:
                position = "N/A"
                # roster_spot = "N/A"
                string = "N/A"
        position_url = "?position=" + position
        try:
            injury = InjuryStatus.objects.get(player=player_projection.player)
            injury_status=injury.status
        except:
            injury_status = ""
            
        new_player = {
            "name": player_projection.player.name,
            "injury_status": injury_status,
            "espn_link": espn_link,
            "team": team_name,
            "team_url": team_url,
            "PPR": round(ppr, 1),
            "STANDARD": round(standard, 1),
            "position": position,
            "position_url": position_url,
            # "roster_spot": roster_spot,
            "string": string,
            "ppr_avg": ppr_avg,
            "standard_avg": standard_avg,
            "ppg_ppr": ppg_ppr,
            "ppg_standard": ppg_standard,
            "points_per_touch_ppr": points_per_touch_ppr,
            "points_per_touch_standard": points_per_touch_standard,
            "ppr_rank": index,
            "pass_att_per_g": pass_att_per_game,
            "pass_cmp_per_g": pass_cmp_per_game,
            "pass_yds_per_g": pass_yds_per_game,
            "pass_td_per_g": pass_td_per_game,
            "int_per_g": int_per_game,
            "rush_att_per_g": rush_att_per_game,
            "rush_yds_per_g": rush_yds_per_game,
            "rush_td_per_g": rush_td_per_game,
            "yards_per_carry": yards_per_carry,
            "rec_tgt_per_g": rec_tgt_per_game,
            "rec_rec_per_g": rec_rec_per_game,
            "rec_yds_per_g": rec_yds_per_game,
            "rec_td_per_g": rec_td_per_game,
            "yards_per_catch": yards_per_catch


        }
        if not position_param or position == position_param:
            players += [new_player]
            index += 1
    context = {"fantasy": players}
    return render(request, "home.html", context=context)


@csrf_exempt
def team_page(request):
    if "team" in request.GET and request.GET['team']:

        
        team = Team.objects.get(slug=request.GET['team'])
        depth_chart = DepthChart.objects.filter(team=team).exclude(position_id__name__in=["C", "RT", "LT", "RG", "LG"]).order_by("roster_spot","string")
        dc = {}
        for entry in depth_chart:
            if entry.roster_spot in dc:
                dc[entry.roster_spot] += [{
                    "name": entry.player.name,
                    "position": entry.position.name,
                    "string": entry.string
                }]
            else:
                dc[entry.roster_spot] = [{
                    "name": entry.player.name,
                    "position": entry.position.name,
                    "string": entry.string
                }]
            # dc += [{
            #     "name": entry.player.name,
            #     "position": entry.position.name,
            #     "string": entry.string
            # }]
        

        team_offense = TeamOffense.objects.filter(team=team, year=2022).aggregate(

            rush_yds = Sum("rush_yds"),
            pass_yds = Sum("pass_yds"),
            rush_att = Sum("rush_att"),
            pass_att = Sum("pass_att"),
            rush_td = Sum("rush_td"),
            pass_td = Sum("pass_td"),
            completions = Sum("pass_cmp"),
            rush_yds_per_att = Sum("rush_yds_per_att"),
            pass_net_yds_per_att = Sum("pass_net_yds_per_att")
            # rush_pct = Round(Sum("rush_att") / (Sum("rush_att") + Sum("pass_att")), 3)
        )
        # print(team_offense['rush_pct'])
        rush_pct = team_offense['rush_att'] / (team_offense['rush_att'] + team_offense['pass_att'])
        pass_pct = team_offense['pass_att'] / (team_offense['rush_att'] + team_offense['pass_att'])

        team_defense = TeamDefense.objects.filter(team=team, year=2022).aggregate(

            rush_yds = Sum("rush_yds"),
            pass_yds = Sum("pass_yds"),
            rush_att = Sum("rush_att"),
            pass_att = Sum("pass_att"),
            rush_td = Sum("rush_td"),
            pass_td = Sum("pass_td"),
            completions = Sum("pass_cmp"),
            rush_yds_per_att = Sum("rush_yds_per_att"),
            pass_net_yds_per_att = Sum("pass_net_yds_per_att")
            # rush_pct = Round(Sum("rush_att") / (Sum("rush_att") + Sum("pass_att")), 3)
        )
        # print(team_offense['rush_pct'])
        rush_pct_d = team_defense['rush_att'] / (team_defense['rush_att'] + team_defense['pass_att'])
        pass_pct_d = team_defense['pass_att'] / (team_defense['rush_att'] + team_defense['pass_att'])
        # yards_per_rush = team_offense['rush_yds'] / team_offense['rush_att']
        # pass_net_yds_per_att = 

        team_pass_offense = PlayerPassingByTeam.objects.filter(team=team, year=2022)
        team_scrimmage_offense = PlayerScrimmageByTeam.objects.filter(team=team, year=2022)
        context = {
            "team": team.name, 
            "depth_chart": dc, 
            "team_pass_offense": team_pass_offense,
            "team_scrimmage_offense": team_scrimmage_offense,
            "rush_yds": team_offense['rush_yds'],
            "pass_yds": team_offense['pass_yds'],
            "rush_td": team_offense['rush_td'],
            "pass_td": team_offense['pass_td'],
            "rush_att": team_offense['rush_att'], 
            "pass_att": team_offense['pass_att'],
            "completions": team_offense['completions'],
            "rush_pct": rush_pct,
            "pass_pct": pass_pct,
            "rush_yds_per_att": team_offense['rush_yds_per_att'],
            "pass_net_yds_per_att": team_offense['pass_net_yds_per_att'],
            "rush_yds_d": team_defense['rush_yds'],
            "pass_yds_d": team_defense['pass_yds'],
            "rush_td_d": team_defense['rush_td'],
            "pass_td_d": team_defense['pass_td'],
            "rush_att_d": team_defense['rush_att'], 
            "pass_att_d": team_defense['pass_att'],
            "completions_d": team_defense['completions'],
            "rush_pct_d": rush_pct_d,
            "pass_pct_d": pass_pct_d,
            "rush_yds_per_att_d": team_defense['rush_yds_per_att'],
            "pass_net_yds_per_att_d": team_defense['pass_net_yds_per_att']
        }
        return render(request, "team.html", context=context)

@csrf_exempt
def donate(request):
    return render(request, "donate.html")


@csrf_exempt
def getstats(request):

    stats = GameStats.objects.filter(
        # game__dt__lte="2021-07-01"\
        # passing_attempts__lt=20
    )\
    .values(
        "player__name"
    )\
    .annotate(
        games_played=Count("*"),
        passing_completions=Sum("passing_completions"),
        passing_attempts=Sum("passing_attempts"),
        passing_yards=Sum("passing_yards"),
        passing_tds=Sum("passing_tds"),
        interceptions=Sum("interceptions"),
        sacks=Sum("sacks"),
        sack_yards=Sum("sack_yards"),
        rushing_yards=Sum("rushing_yards"),
        rushing_attempts=Sum("rushing_attempts"),
        rushing_tds=Sum("rushing_tds"),
        targets=Sum("targets"),
        receptions=Sum("receptions"),
        receiving_yards=Sum("receiving_yards"),
        receiving_tds=Sum("receiving_tds"),
        fumbles=Sum("fumbles"),
        fumbles_lost=Sum("fumbles_lost"),

        passing_yards_per_game = Cast(F("passing_yards") / F("games_played"), FloatField()),
        passing_tds_per_game = Cast(F("passing_tds") / F("games_played"), FloatField()),
        rushing_yards_per_game = Cast(F("rushing_yards") / F("games_played"), FloatField()),
        rushing_tds_per_game = Cast(F("rushing_tds") / F("games_played"), FloatField()),
        receiving_yards_per_game = Cast(F("receiving_yards") / F("games_played"), FloatField()),
        receiving_tds_per_game = Cast(F("receiving_tds") / F("games_played"), FloatField()),


        attempts_per_game = Cast(F("passing_attempts") / F("games_played"), FloatField()),
        completions_per_game = Cast(F("passing_completions") / F("games_played"), FloatField()),
        completion_percentage = Cast(F("passing_completions") / F("passing_attempts"), FloatField()),
        yards_per_completion = Cast(F("passing_yards") / F("passing_completions"), FloatField()),
        yards_per_attempt = Cast(F("passing_yards") / F("passing_attempts"), FloatField()),

        carries_per_game = Cast(F("rushing_attempts") / F("games_played"), FloatField()),
        yards_per_carry = Cast(F("rushing_yards") / F("rushing_attempts"), FloatField()),
        rushing_td_per_carry = Cast(F("rushing_tds") / F("rushing_attempts"), FloatField()),

        yards_per_reception = Cast(F("receiving_yards") / F("receptions"), FloatField()),
        yards_per_target = Cast(F("receiving_yards") / F("targets"), FloatField()),
        catch_percentage = Cast(F("receptions") / F("targets"), FloatField()),

        touches = Cast(F("receptions") + F("rushing_attempts"), FloatField()),

        scrimmage_yards = Cast(F("rushing_yards") +  F("receiving_yards"), FloatField()),

        total_tds = Cast(F("rushing_tds") +  F("receiving_tds"), FloatField()),

        touches_per_game = Cast(F("touches") / F("games_played"), FloatField()),

        fantasy_points = Cast((F("receiving_yards") * .1) + (F("rushing_yards") * .1 ) + (F("total_tds") * 6) + (F("passing_yards") * .04) +  (F("passing_tds") * 4)  + (F("fumbles_lost") * -2) + (F("interceptions") * -2) , FloatField()),
        
        fantasy_points_per_game =  Cast(F("fantasy_points") / F("games_played"), FloatField()),

        fantasy_points_per_touch =  Cast(F("fantasy_points") / F("touches"), FloatField())

    )\
    .order_by(
        "-touches_per_game"
    )
    
    context={"stats": stats}
    return render(request, "stats.html", context)



@csrf_exempt
def teamstats(request):

    stats = GameStats.objects.filter(
        # game__dt__lte="2021-07-01"
    )\
    .values(
        "team__name"
    )\
    .annotate(
        games_played=Count("game__id", distinct=True),
        passing_completions=Sum("passing_completions"),
        passing_attempts=Sum("passing_attempts"),
        passing_yards=Sum("passing_yards"),
        passing_tds=Sum("passing_tds"),
        interceptions=Sum("interceptions"),
        sacks=Sum("sacks"),
        sack_yards=Sum("sack_yards"),
        rushing_yards=Sum("rushing_yards"),
        rushing_attempts=Sum("rushing_attempts"),
        rushing_tds=Sum("rushing_tds"),
        targets=Sum("targets"),
        receptions=Sum("receptions"),
        receiving_yards=Sum("receiving_yards"),
        receiving_tds=Sum("receiving_tds"),
        fumbles=Sum("fumbles"),
        fumbles_lost=Sum("fumbles_lost"),

        passing_yards_per_game = Cast(F("passing_yards") / F("games_played"), FloatField()),
        passing_tds_per_game = Cast(F("passing_tds") / F("games_played"), FloatField()),
        rushing_yards_per_game = Cast(F("rushing_yards") / F("games_played"), FloatField()),
        rushing_tds_per_game = Cast(F("rushing_tds") / F("games_played"), FloatField()),
        receiving_yards_per_game = Cast(F("receiving_yards") / F("games_played"), FloatField()),
        receiving_tds_per_game = Cast(F("receiving_tds") / F("games_played"), FloatField()),


        attempts_per_game = Cast(F("passing_attempts") / F("games_played"), FloatField()),
        completions_per_game = Cast(F("passing_completions") / F("games_played"), FloatField()),
        completion_percentage = Cast(F("passing_completions") / F("passing_attempts"), FloatField()),
        yards_per_completion = Cast(F("passing_yards") / F("passing_completions"), FloatField()),
        yards_per_attempt = Cast(F("passing_yards") / F("passing_attempts"), FloatField()),

        carries_per_game = Cast(F("rushing_attempts") / F("games_played"), FloatField()),
        yards_per_carry = Cast(F("rushing_yards") / F("rushing_attempts"), FloatField()),
        rushing_td_per_carry = Cast(F("rushing_tds") / F("rushing_attempts"), FloatField()),

        yards_per_reception = Cast(F("receiving_yards") / F("receptions"), FloatField()),
        yards_per_target = Cast(F("receiving_yards") / F("targets"), FloatField()),
        catch_percentage = Cast(F("receptions") / F("targets"), FloatField()),

        touches = Cast(F("receptions") + F("rushing_attempts"), FloatField()),

        scrimmage_yards = Cast(F("rushing_yards") +  F("receiving_yards"), FloatField()),

        total_tds = Cast(F("rushing_tds") +  F("receiving_tds"), FloatField()),

        touches_per_game = Cast(F("touches") / F("games_played"), FloatField()),

        fantasy_points = Cast((F("receiving_yards") * .1) + (F("rushing_yards") * .1 ) + (F("total_tds") * 6) + (F("passing_yards") * .04) +  (F("passing_tds") * 4)  + (F("fumbles_lost") * -2) + (F("interceptions") * -2) , FloatField()),
        
        fantasy_points_per_game =  Cast(F("fantasy_points") / F("games_played"), FloatField()),

        fantasy_points_per_touch =  Cast(F("fantasy_points") / F("touches"), FloatField())

    )\
    .order_by(
        "-fantasy_points_per_game"
    )
    
    
    context={"stats": stats}
    return render(request, "teamstats.html", context)
