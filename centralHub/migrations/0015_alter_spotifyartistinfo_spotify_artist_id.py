# Generated by Django 4.2.12 on 2024-06-19 03:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("centralHub", "0014_spotifyartistinfo_spotify_artist_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spotifyartistinfo",
            name="spotify_artist_id",
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
