# Generated by Django 4.2.13 on 2024-06-03 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centralHub', '0005_alter_twitteruser_twitter_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyArtistInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('spotify_artist', models.CharField(max_length=100, unique=True)),
                ('spotify_albums', models.CharField(max_length=100)),
                ('spotify_tracks', models.PositiveIntegerField(blank=True)),
                ('spotify_image_url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
