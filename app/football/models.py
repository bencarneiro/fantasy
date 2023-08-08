from django.db import models

class Sport(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = True
        db_table = "sport"

class Team(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=64)
    slug = models.CharField(max_length=16)
    
    class Meta:
        managed = True
        db_table = "team"


class Player(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = "player"
    
class Position(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    full_name = models.CharField(max_length=64)


    class Meta:
        managed = True
        db_table = "position"   

class DepthChart(models.model):

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    roster_spot = models.SmallIntegerField(null=False)
    string = models.SmallIntegerField(null=False)
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)


    class Meta:
        managed = True
        db_table = "depth_chart"   


class TeamOffense(models.Model):

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    games_played = models.SmallIntegerField(null=False)
    points = models.SmallIntegerField(null=False)
    total_yards = models.SmallIntegerField(null=False)
    plays_offense = models.SmallIntegerField(null=False)
    yds_per_play_offense = models.FloatField(null=False)
    turnovers = models.SmallIntegerField(null=False)
    fumbles_lost = models.SmallIntegerField(null=False)
    first_down = models.SmallIntegerField(null=False)
    pass_cmp = models.SmallIntegerField(null=False)
    pass_att = models.SmallIntegerField(null=False)
    pass_yds = models.SmallIntegerField(null=False)
    pass_td = models.SmallIntegerField(null=False)
    pass_int = models.SmallIntegerField(null=False)
    pass_net_yds_per_att = models.FloatField(null=False)
    pass_fd = models.SmallIntegerField(null=False)
    rush_att = models.SmallIntegerField(null=False)
    rush_yds = models.SmallIntegerField(null=False)
    rush_td = models.SmallIntegerField(null=False)
    rush_yds_per_att = models.FloatField(null=False)
    rush_fd = models.SmallIntegerField(null=False)
    penalties = models.SmallIntegerField(null=False)
    penalties_yds = models.SmallIntegerField(null=False)
    pen_fd = models.SmallIntegerField(null=False)
    score_pct = models.FloatField(null=False)
    turnover_pct = models.FloatField(null=False)
    exp_pts_tot = models.FloatField(null=False)

    class Meta:
        managed = True
        db_table = "team_offense"   

class TeamDefense(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    games_played = models.SmallIntegerField(null=False)
    points = models.SmallIntegerField(null=False)
    total_yards = models.SmallIntegerField(null=False)
    plays_offense = models.SmallIntegerField(null=False)
    yds_per_play_offense = models.FloatField(null=False)
    turnovers = models.SmallIntegerField(null=False)
    fumbles_lost = models.SmallIntegerField(null=False)
    first_down = models.SmallIntegerField(null=False)
    pass_cmp = models.SmallIntegerField(null=False)
    pass_att = models.SmallIntegerField(null=False)
    pass_yds = models.SmallIntegerField(null=False)
    pass_td = models.SmallIntegerField(null=False)
    pass_int = models.SmallIntegerField(null=False)
    pass_net_yds_per_att = models.FloatField(null=False)
    pass_fd = models.SmallIntegerField(null=False)
    rush_att = models.SmallIntegerField(null=False)
    rush_yds = models.SmallIntegerField(null=False)
    rush_td = models.SmallIntegerField(null=False)
    rush_yds_per_att = models.FloatField(null=False)
    rush_fd = models.SmallIntegerField(null=False)
    penalties = models.SmallIntegerField(null=False)
    penalties_yds = models.SmallIntegerField(null=False)
    pen_fd = models.SmallIntegerField(null=False)
    score_pct = models.FloatField(null=False)
    turnover_pct = models.FloatField(null=False)
    exp_pts_def_tot = models.FloatField(null=False)

    class Meta:
        managed = True
        db_table = "team_defense"   

class TeamSpecialTeams(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)

class PlayerPassing(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)

class PlayerRushing(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)

class PlayerReceiving(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)

class PlayerKicking(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)

class PlayerReturning(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)

