# Generated by Django 4.2.12 on 2024-06-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("centralHub", "0010_spotifyartistinfo_spotify_artist_albums_registered"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spotifyalbumtracking",
            name="spotify_albums",
            field=models.CharField(max_length=200),
        ),
    ]
