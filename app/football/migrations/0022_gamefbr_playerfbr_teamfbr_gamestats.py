# Generated by Django 4.1.5 on 2024-08-10 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0021_pinnacledata"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameFBR",
            fields=[
                (
                    "id",
                    models.CharField(max_length=64, primary_key=True, serialize=False),
                ),
                ("dt", models.DateTimeField()),
            ],
            options={
                "db_table": "game_fbr",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="PlayerFBR",
            fields=[
                (
                    "id",
                    models.CharField(max_length=16, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=256)),
                ("url", models.CharField(max_length=256)),
            ],
            options={
                "db_table": "player_fbr",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="TeamFBR",
            fields=[
                (
                    "id",
                    models.CharField(max_length=16, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=256)),
                ("short_name", models.CharField(max_length=256)),
            ],
            options={
                "db_table": "team_fbr",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="GameStats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("passing_completions", models.IntegerField(default=0)),
                ("passing_attempts", models.IntegerField(default=0)),
                ("passing_yards", models.IntegerField(default=0)),
                ("passing_tds", models.IntegerField(default=0)),
                ("interceptions", models.IntegerField(default=0)),
                ("sacks", models.IntegerField(default=0)),
                ("sack_yards", models.IntegerField(default=0)),
                ("passing_long", models.IntegerField(default=0)),
                ("passer_rating", models.FloatField(blank=True, null=True)),
                ("rushing_attempts", models.IntegerField(default=0)),
                ("rushing_yards", models.IntegerField(default=0)),
                ("rushing_tds", models.IntegerField(default=0)),
                ("rushing_long", models.IntegerField(default=0)),
                ("targets", models.IntegerField(default=0)),
                ("receptions", models.IntegerField(default=0)),
                ("receiving_yards", models.IntegerField(default=0)),
                ("receiving_tds", models.IntegerField(default=0)),
                ("receiving_long", models.IntegerField(default=0)),
                ("fumbles", models.IntegerField(default=0)),
                ("fumbles_lost", models.IntegerField(default=0)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.gamefbr",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.playerfbr",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.teamfbr",
                    ),
                ),
            ],
            options={
                "db_table": "game_stats",
                "managed": True,
            },
        ),
    ]