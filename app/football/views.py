from django.shortcuts import render

# Create your views here.


from django.db.models import Sum, Count, Q, F, Avg, Value
from django.db.models.functions import Round

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from football.models import DepthChart, PlayerPassing, PlayerProjections, DepthChart, PlayerKicking, PlayerRushing, PlayerReceiving, PlayerReturning, Team, TeamOffense, TeamDefense, PlayerPassingByTeam, PlayerScrimmageByTeam

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
            yards_per_game=Sum("pass_yds")/Sum("g"),
            td_per_game=Sum("pass_td")/Sum("g"),
            yards=Sum("pass_yds"),
            g=Sum("g"),
            tds=Sum("pass_td"),
            points=( Sum("pass_yds") / 25 ) + (Sum("pass_td") * 6)
        )

        rushing_data = PlayerRushing.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            yards_per_game=Sum("rush_yds")/Sum("g"),
            td_per_game=Sum("rush_td")/Sum("g"),
            yards_per_carry=Sum("rush_yds")/Sum("rush_att"),
            attempts=Sum("rush_att"),
            yards=Sum("rush_yds"),
            tds=Sum("rush_td"),
            g=Sum("g"),
            points=( Sum("rush_yds") / 10 ) + (Sum("rush_td") * 6)
        )
        receiving_data = PlayerReceiving.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            yards_per_game=Sum("rec_yds")/Sum("g"),
            td_per_game=Sum("rec_td")/Sum("g"),
            yards_per_reception=Sum("rec_yds")/Sum("rec"),
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
        kicking_data = PlayerKicking.objects.filter(player=player_projection.player, year__gte=2020, year__lte=2022).aggregate(
            seasons=Count("year"),
            fga=Sum("fga"),
            fgm=Sum("fgm"),
            fga1=Sum("fga1"),
            fgm1=Sum("fgm1"),
            fga2=Sum("fga2"),
            fgm2=Sum("fgm2"),
            fga3=Sum("fga3"),
            fgm3=Sum("fgm3"),
            fga4=Sum("fga4"),
            fgm4=Sum("fgm4"),
            fga5=Sum("fga5"),
            fgm5=Sum("fgm5"),
            xpa=Sum("xpa"),
            xpm=Sum("xpm"),
            g=Sum("g"),
            points=((Sum("fgm1") * 3) - (Sum("fga1") - Sum("fgm1"))) + ((Sum("fgm2") * 3) - (Sum("fga2") - Sum("fgm2"))) + ((Sum("fgm3") * 3) - (Sum("fga3") - Sum("fgm3"))) + ((Sum("fgm4") * 4) - (Sum("fga4") - Sum("fgm4"))) + ((Sum("fgm5") * 5) - (Sum("fga5") - Sum("fgm5"))) + (Sum("xpm") - (Sum("xpa") - Sum("xpm")))
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
            print(player_projection.player.name)
            print(rushing_data)
            print(receiving_data)
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



        
        # print(player_projection.player.name)
        # print(rushing_data['yards_per_game'])
        # try:
        #     ppr_avg = round((rushing_data['points'] + receiving_data['points_ppr']) / rushing_data['seasons'])
        # except Exception as e:
        #     print(e)
        #     print(rushing_data)
        #     print(receiving_data)
        #     ppr_avg=0
        # try:
        #     standard_avg = round((rushing_data['points'] + receiving_data['points']) / rushing_data['seasons'])
        # except:
        #     standard_avg=0

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
            position = "Defense"
            team_name = player_projection.player.name.split(" ")[0]
            # roster_spot = 1
            string = 1
        else:
            pk = PlayerKicking.objects.filter(player_id=player_projection.player.id)
            if len(pk) > 0:
                position = "Kicker"
                # roster_spot = 1
                string = 1
            else:
                position = "N/A"
                # roster_spot = "N/A"
                string = "N/A"
        new_player = {
            "name": player_projection.player.name,
            "espn_link": espn_link,
            "team": team_name,
            "team_url": team_url,
            "PPR": round(ppr, 1),
            "STANDARD": round(standard, 1),
            "position": position,
            # "roster_spot": roster_spot,
            "string": string,
            "rush_yds_per_g": rushing_data['yards_per_game'],
            "rec_yds_per_g": receiving_data['yards_per_game'],
            "ppr_avg": ppr_avg,
            "standard_avg": standard_avg,
            "ppg_ppr": ppg_ppr,
            "ppg_standard": ppg_standard,
            "points_per_touch_ppr": points_per_touch_ppr,
            "points_per_touch_standard": points_per_touch_standard,
            "index": index
        }
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
        print(dc)
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
            "pass_net_yds_per_att": team_offense['pass_net_yds_per_att']
        }
        return render(request, "team.html", context=context)