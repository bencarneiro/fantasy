# Generated by Django 4.1.5 on 2023-08-16 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("football", "0018_playerprojections"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="espn_id",
            field=models.IntegerField(null=True),
        ),
    ]
