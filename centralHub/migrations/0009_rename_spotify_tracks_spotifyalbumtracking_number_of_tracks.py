# Generated by Django 4.2.13 on 2024-06-07 02:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("centralHub", "0008_spotifyartistinfo_spotify_image_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="spotifyalbumtracking",
            old_name="spotify_tracks",
            new_name="number_of_tracks",
        ),
    ]
