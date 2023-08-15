from django.shortcuts import render

# Create your views here.



from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from football.models import DepthChart, PlayerPassing

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