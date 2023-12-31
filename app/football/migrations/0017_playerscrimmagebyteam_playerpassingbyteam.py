# Generated by Django 4.1.5 on 2023-08-15 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0016_alter_injurystatus_options_alter_injurystatus_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerScrimmageByTeam",
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
                ("age", models.SmallIntegerField()),
                ("g", models.SmallIntegerField()),
                ("gs", models.SmallIntegerField()),
                ("rush_att", models.SmallIntegerField()),
                ("rush_yds", models.SmallIntegerField()),
                ("rush_td", models.SmallIntegerField()),
                ("rush_long", models.SmallIntegerField()),
                ("rush_yds_per_att", models.FloatField()),
                ("rush_yds_per_g", models.FloatField()),
                ("rush_att_per_g", models.FloatField()),
                ("targets", models.SmallIntegerField()),
                ("rec", models.SmallIntegerField()),
                ("rec_yds", models.SmallIntegerField()),
                ("rec_yds_per_rec", models.FloatField()),
                ("rec_td", models.SmallIntegerField()),
                ("rec_long", models.SmallIntegerField()),
                ("rec_per_g", models.FloatField()),
                ("rec_yds_per_g", models.FloatField()),
                ("catch_pct", models.FloatField()),
                ("rec_yds_per_tgt", models.FloatField()),
                ("touches", models.SmallIntegerField()),
                ("yds_per_touch", models.FloatField()),
                ("yds_from_scrimmage", models.SmallIntegerField()),
                ("rush_receive_td", models.SmallIntegerField()),
                ("fumbles", models.SmallIntegerField()),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.player",
                    ),
                ),
                (
                    "pos",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.position",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.team",
                    ),
                ),
            ],
            options={
                "db_table": "player_scrimmage_by_team",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="PlayerPassingByTeam",
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
                ("age", models.SmallIntegerField()),
                ("g", models.SmallIntegerField()),
                ("gs", models.SmallIntegerField()),
                ("qb_rec", models.CharField(default=None, max_length=32)),
                ("pass_cmp", models.SmallIntegerField()),
                ("pass_att", models.SmallIntegerField()),
                ("pass_cmp_perc", models.FloatField()),
                ("pass_yds", models.SmallIntegerField()),
                ("pass_td", models.SmallIntegerField()),
                ("pass_td_perc", models.FloatField()),
                ("pass_int", models.SmallIntegerField()),
                ("pass_int_perc", models.FloatField()),
                ("pass_long", models.SmallIntegerField()),
                ("pass_yds_per_att", models.FloatField()),
                ("pass_adj_yds_per_att", models.FloatField()),
                ("pass_yds_per_cmp", models.FloatField()),
                ("pass_yds_per_g", models.FloatField()),
                ("pass_rating", models.FloatField()),
                ("qbr", models.FloatField()),
                ("pass_sacked", models.SmallIntegerField()),
                ("pass_sacked_yds", models.SmallIntegerField()),
                ("pass_sacked_perc", models.FloatField()),
                ("pass_net_yds_per_att", models.FloatField()),
                ("pass_adj_net_yds_per_att", models.FloatField()),
                ("comebacks", models.SmallIntegerField()),
                ("gwd", models.SmallIntegerField()),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.player",
                    ),
                ),
                (
                    "pos",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.position",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="football.team",
                    ),
                ),
            ],
            options={
                "db_table": "player_passing_by_team",
                "managed": True,
            },
        ),
    ]
