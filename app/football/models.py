from django.db import models

class Sport(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = True
        db_table = "sport"

class League(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    initials = models.CharField(max_length=16)
    
    class Meta:
        managed = True
        db_table = "league"


class Conference(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    initials = models.CharField(max_length=16)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = "conference"

class Division(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    conference = models.ForeignKey(Conference, on_delete=models.DO_NOTHING)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = "division"



class Team(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=64)
    slug = models.CharField(max_length=16)
    espn_slug = models.CharField(max_length=16, null=True)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    conference = models.ForeignKey(Conference, on_delete=models.DO_NOTHING)
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = "team"


class Player(models.Model):

    id = models.AutoField(primary_key=True)
    fbr_slug = models.CharField(max_length=64)
    espn_id = models.IntegerField(null=True)
    name = models.CharField(max_length=256)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = "player"
    
class InjuryStatus(models.Model):

    player = models.ForeignKey(Player, primary_key=True, null=False, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16)

    class Meta:
        managed = True
        db_table = "injury_status"   
    
class Position(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    full_name = models.CharField(max_length=64)


    class Meta:
        managed = True
        db_table = "position"   

class DepthChart(models.Model):

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
        
# class TeamReturns (models.Model):
#     team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
#     year = models.SmallIntegerField(null=False)

# class TeamKicking(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
#     year = models.SmallIntegerField(null=False)

# class TeamPunting(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
#     year = models.SmallIntegerField(null=False)

class PlayerPassing(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    qb_rec = models.CharField(max_length=32, default=None)
    pass_cmp = models.SmallIntegerField(null=False)
    pass_att = models.SmallIntegerField(null=False)
    pass_cmp_perc = models.FloatField(null=False)
    pass_yds = models.SmallIntegerField(null=False)
    pass_td = models.SmallIntegerField(null=False)
    pass_td_perc = models.FloatField()
    pass_int = models.SmallIntegerField(null=False)
    pass_int_perc = models.FloatField()
    pass_first_down = models.SmallIntegerField(null=False)
    pass_long = models.SmallIntegerField(null=False)
    pass_yds_per_att = models.FloatField()
    pass_adj_yds_per_att = models.FloatField()
    pass_yds_per_cmp = models.FloatField()
    pass_yds_per_g = models.FloatField()
    pass_rating = models.FloatField()
    qbr = models.FloatField()
    pass_sacked = models.SmallIntegerField(null=False)
    pass_sacked_yds = models.SmallIntegerField(null=False)
    pass_sacked_perc = models.FloatField()
    pass_net_yds_per_att = models.FloatField()
    pass_adj_net_yds_per_att = models.FloatField()
    comebacks = models.SmallIntegerField(null=False)
    gwd = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "player_passing"   


class PlayerRushing(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    rush_att = models.SmallIntegerField(null=False)
    rush_yds = models.SmallIntegerField(null=False)
    rush_td = models.SmallIntegerField(null=False)
    rush_first_down = models.SmallIntegerField(null=False)
    rush_long = models.SmallIntegerField(null=False)
    rush_yds_per_att = models.FloatField()
    rush_yds_per_g = models.FloatField()
    fumbles = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "player_rushing"   

class PlayerReceiving(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    targets = models.SmallIntegerField(null=False)
    rec = models.SmallIntegerField(null=False)
    catch_pct = models.FloatField()
    rec_yds = models.SmallIntegerField(null=False)
    rec_yds_per_rec = models.FloatField()
    rec_td = models.SmallIntegerField(null=False)
    rec_first_down = models.SmallIntegerField(null=False)
    rec_long = models.SmallIntegerField(null=False)
    rec_yds_per_tgt = models.FloatField()
    rec_per_g = models.FloatField()
    rec_yds_per_g = models.FloatField()
    fumbles = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "player_receiving"   

class PlayerKicking(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    fga1 = models.SmallIntegerField(null=False)
    fgm1 = models.SmallIntegerField(null=False)
    fga2 = models.SmallIntegerField(null=False)
    fgm2 = models.SmallIntegerField(null=False)
    fga3 = models.SmallIntegerField(null=False)
    fgm3 = models.SmallIntegerField(null=False)
    fga4 = models.SmallIntegerField(null=False)
    fgm4 = models.SmallIntegerField(null=False)
    fga5 = models.SmallIntegerField(null=False)
    fgm5 = models.SmallIntegerField(null=False)
    fga = models.SmallIntegerField(null=False)
    fgm = models.SmallIntegerField(null=False)
    fg_long = models.SmallIntegerField(null=False)
    fg_perc = models.FloatField()
    xpa = models.SmallIntegerField(null=False)
    xpm = models.SmallIntegerField(null=False)
    xp_perc = models.FloatField()

    class Meta:
        managed = True
        db_table = "player_kicking"   


class PlayerReturning(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    punt_ret = models.SmallIntegerField(null=False)
    punt_ret_yds = models.SmallIntegerField(null=False)
    punt_ret_td = models.SmallIntegerField(null=False)
    punt_ret_long = models.SmallIntegerField(null=False)
    punt_ret_yds_per_ret = models.FloatField()
    kick_ret = models.SmallIntegerField(null=False)
    kick_ret_yds = models.SmallIntegerField(null=False)
    kick_ret_td = models.SmallIntegerField(null=False)
    kick_ret_long = models.SmallIntegerField(null=False)
    kick_ret_yds_per_ret = models.FloatField()
    all_purpose_yds = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "player_returning"   


class PlayerPassingByTeam(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    qb_rec = models.CharField(max_length=32, default=None)
    pass_cmp = models.SmallIntegerField(null=False)
    pass_att = models.SmallIntegerField(null=False)
    pass_cmp_perc = models.FloatField(null=False)
    pass_yds = models.SmallIntegerField(null=False)
    pass_td = models.SmallIntegerField(null=False)
    pass_td_perc = models.FloatField()
    pass_int = models.SmallIntegerField(null=False)
    pass_int_perc = models.FloatField()
    # pass_first_down = models.SmallIntegerField(null=False)
    pass_long = models.SmallIntegerField(null=False)
    pass_yds_per_att = models.FloatField()
    pass_adj_yds_per_att = models.FloatField()
    pass_yds_per_cmp = models.FloatField()
    pass_yds_per_g = models.FloatField()
    pass_rating = models.FloatField()
    qbr = models.FloatField()
    pass_sacked = models.SmallIntegerField(null=False)
    pass_sacked_yds = models.SmallIntegerField(null=False)
    pass_sacked_perc = models.FloatField()
    pass_net_yds_per_att = models.FloatField()
    pass_adj_net_yds_per_att = models.FloatField()
    comebacks = models.SmallIntegerField(null=False)
    gwd = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "player_passing_by_team"   


class PlayerScrimmageByTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    age = models.SmallIntegerField(null=False)
    pos = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)
    g = models.SmallIntegerField(null=False)
    gs = models.SmallIntegerField(null=False)
    rush_att = models.SmallIntegerField(null=False)
    rush_yds = models.SmallIntegerField(null=False)
    rush_td = models.SmallIntegerField(null=False)
    rush_long = models.SmallIntegerField(null=False)
    rush_yds_per_att = models.FloatField(null=False)
    rush_yds_per_g = models.FloatField(null=False)
    rush_att_per_g = models.FloatField(null=False)
    targets = models.SmallIntegerField(null=False)
    rec = models.SmallIntegerField(null=False)
    rec_yds = models.SmallIntegerField(null=False)
    rec_yds_per_rec = models.FloatField(null=False)
    rec_td = models.SmallIntegerField(null=False)
    rec_long = models.SmallIntegerField(null=False)
    rec_per_g = models.FloatField(null=False)
    rec_yds_per_g = models.FloatField(null=False)
    catch_pct = models.FloatField(null=False)
    rec_yds_per_tgt = models.FloatField(null=False)
    touches = models.SmallIntegerField(null=False)
    yds_per_touch = models.FloatField(null=False)
    yds_from_scrimmage = models.SmallIntegerField(null=False)
    rush_receive_td = models.SmallIntegerField(null=False)
    fumbles = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "player_scrimmage_by_team"


class PlayerProjections(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    proj_carries = models.FloatField(null=True)
    proj_rush_yd  = models.FloatField(null=True)
    proj_rush_td = models.FloatField(null=True)
    proj_tgt = models.FloatField(null=True)
    proj_rec = models.FloatField(null=True)
    proj_rec_yd = models.FloatField(null=True)
    proj_rec_td = models.FloatField(null=True)
    proj_points = models.FloatField(null=True)

    class Meta:
        managed = True
        db_table = "player_projection"


class DefensivePoints(models.Model):

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    year = models.SmallIntegerField(null=False)
    points = models.SmallIntegerField(null=False)

    class Meta:
        managed = True
        db_table = "defensive_points"


class PinnacleData(models.Model):
    
    created = models.DateTimeField(null=False, blank=False)
    data = models.JSONField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = "pinnacle_data"



class TeamFBR(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=256, null=False, blank=False)
    short_name = models.CharField(max_length=256, null=False, blank=False)
    fbr_slug = models.CharField(max_length=256, null=True, blank=True)
    espn_depth_chart = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "team_fbr"
        managed = True


class PlayerFBR(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=256, null=False, blank=False)
    url = models.CharField(max_length=256, null=False, blank=False)
    position = models.CharField(max_length=16, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    team = models.ForeignKey(TeamFBR, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = "player_fbr"
        managed = True


class GameFBR(models.Model):

    id = models.CharField(primary_key=True, max_length=64)
    dt = models.DateTimeField(null=False, blank=False)

    class Meta:
        db_table = "game_fbr"
        managed = True        
        indexes = [
            models.Index(fields=['dt']),
        ]



class GameStats(models.Model):


    player = models.ForeignKey(PlayerFBR, on_delete = models.DO_NOTHING)
    team = models.ForeignKey(TeamFBR, on_delete = models.DO_NOTHING)
    game = models.ForeignKey(GameFBR, on_delete = models.DO_NOTHING)

    passing_completions = models.IntegerField(null=False, blank=False, default=0)
    passing_attempts = models.IntegerField(null=False, blank=False, default=0)
    passing_yards = models.IntegerField(null=False, blank=False, default=0)
    passing_tds = models.IntegerField(null=False, blank=False, default=0)
    interceptions = models.IntegerField(null=False, blank=False, default=0)
    sacks = models.IntegerField(null=False, blank=False, default=0)
    sack_yards = models.IntegerField(null=False, blank=False, default=0)
    passing_long = models.IntegerField(null=False, blank=False, default=0)
    passer_rating = models.FloatField(null=True, blank=True)
    rushing_attempts = models.IntegerField(null=False, blank=False, default=0)
    rushing_yards = models.IntegerField(null=False, blank=False, default=0)
    rushing_tds = models.IntegerField(null=False, blank=False, default=0)
    rushing_long = models.IntegerField(null=False, blank=False, default=0)
    targets = models.IntegerField(null=False, blank=False, default=0)
    receptions = models.IntegerField(null=False, blank=False, default=0)
    receiving_yards = models.IntegerField(null=False, blank=False, default=0)
    receiving_tds = models.IntegerField(null=False, blank=False, default=0)
    receiving_long = models.IntegerField(null=False, blank=False, default=0)
    fumbles = models.IntegerField(null=False, blank=False, default=0)
    fumbles_lost = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        db_table = "game_stats"
        managed = True        
        indexes = [
            models.Index(fields=['player']),
            models.Index(fields=['game']),
        ]
