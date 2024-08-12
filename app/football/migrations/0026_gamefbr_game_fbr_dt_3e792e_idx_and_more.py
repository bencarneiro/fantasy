# Generated by Django 4.1.5 on 2024-08-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0025_playerfbr_team"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="gamefbr",
            index=models.Index(fields=["dt"], name="game_fbr_dt_3e792e_idx"),
        ),
        migrations.AddIndex(
            model_name="gamestats",
            index=models.Index(fields=["player"], name="game_stats_player__de5c6f_idx"),
        ),
        migrations.AddIndex(
            model_name="gamestats",
            index=models.Index(fields=["game"], name="game_stats_game_id_9c0a1b_idx"),
        ),
    ]
