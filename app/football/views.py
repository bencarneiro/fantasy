from django.shortcuts import render

# Create your views here.


from django.db.models import Sum, Count, Q, F, Avg, Value
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from football.models import DepthChart, PlayerPassing, PlayerProjections, DepthChart, PlayerKicking, PlayerRushing, PlayerReceiving, PlayerReturning

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
    for player_projection in fantasy_projections:
        if player_projection.proj_points < 1:
            continue
        # if player_projection.proj_points ==
        ppr = player_projection.proj_points
        standard = ppr - player_projection.proj_rec
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

        if not rushing_data['seasons'] and not receiving_data['seasons']:
            ppr_avg = 0
            standard_avg = 0
            print(player_projection.player.name)
            print(rushing_data)
            print(receiving_data)
        else:
            seasons = 0
            if rushing_data['seasons'] and rushing_data['seasons'] > seasons:
                seasons = rushing_data['seasons']
            if receiving_data['seasons'] and receiving_data['seasons'] > seasons:
                seasons = receiving_data['seasons']

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
            ppr_avg = round((rec_pts_ppr + rush_pts) / seasons)
            standard_avg = round((rec_pts + rush_pts) / seasons)

        
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
            team_name = player_projection.player.team.name
        else:
            team_name = "Free Agent"
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
            "team": team_name,
            "PPR": round(ppr),
            "STANDARD": round(standard),
            "position": position,
            # "roster_spot": roster_spot,
            "string": string,
            "rush_yds_per_g": rushing_data['yards_per_game'],
            "rec_yds_per_g": receiving_data['yards_per_game'],
            "ppr_avg": ppr_avg,
            "standard_avg": standard_avg
        }
        players += [new_player]
    context = {"fantasy": players}
    return render(request, "home.html", context=context)