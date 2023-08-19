# Generated by Django 4.1.5 on 2023-08-19 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0019_alter_player_espn_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="DefensivePoints",
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
                ("year", models.SmallIntegerField()),
                ("points", models.SmallIntegerField()),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.team",
                    ),
                ),
            ],
            options={
                "db_table": "defensive_points",
                "managed": True,
            },
        ),
    ]