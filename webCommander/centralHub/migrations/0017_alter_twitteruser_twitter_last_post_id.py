# Generated by Django 4.2.12 on 2024-06-19 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centralHub', '0016_alter_spotifyartistinfo_spotify_artist_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteruser',
            name='twitter_last_post_id',
            field=models.PositiveIntegerField(blank=True, unique=True),
        ),
    ]
