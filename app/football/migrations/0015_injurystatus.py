# Generated by Django 4.1.5 on 2023-08-15 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0014_alter_player_espn_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="InjuryStatus",
            fields=[
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="football.player",
                    ),
                ),
                ("status", models.CharField(max_length=16)),
            ],
        ),
    ]