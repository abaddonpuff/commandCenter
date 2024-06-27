from django.core.management.base import BaseCommand, CommandError
from centralHub.models import TwitterUser, TwitterUserPosts, SpotifyArtistInfo, SpotifyAlbumTracking
from centralHub.spotify.spotifyAPI import search_spotify_artist, get_artist_albums, get_spotify_artist_by_id
from centralHub.xTwitter.twitterAPI import get_top_tweets_from_user, get_tweets_since_last, XAPIUsageExceeded
from centralHub.slackbot.slackbot_api import post_slack_message
from centralHub.views import insert_posts_to_x_db

class Command(BaseCommand):
    help = 'Updates all trackers for new data'

    def handle(self, *args, **options):
        alltweets = TwitterUser.objects.all()
        allartists = SpotifyArtistInfo.objects.all()

        albums = []

        for twitter_user in alltweets:
            try:
                new_posts = get_tweets_since_last(twitter_user.twitter_user_id,twitter_user.twitter_last_post_id)
                if 'data' in new_posts.keys():
                    created_count= insert_posts_to_x_db(twitter_user, new_posts)
                    if created_count >0:
                        post_slack_message(f"User {twitter_user.twitter_name} posted {created_count} new messages!")
                        self.stdout.write(self.style.SUCCESS(f"{created_count} new posts for user: '{twitter_user.twitter_name}'! Notifying..."))
                else:
                    self.stdout.write(self.style.ERROR(f'No new posts for user {twitter_user.twitter_name}!!'))

            except XAPIUsageExceeded:
                self.stdout.write(self.style.ERROR(f"API Usage exceeded to query user {twitter_user.twitter_name}: Could not check"))

        for artist in allartists:
            album_count = 0
            spotify_artist_albums = get_artist_albums(artist.spotify_artist_id)
            for artist_album in spotify_artist_albums:
                try:
                    album, created = SpotifyAlbumTracking.objects.get_or_create(
                        spotify_user=artist,
                        spotify_albums=artist_album.name,
                        number_of_tracks=artist_album.total_tracks,
                        spotify_image_url=artist_album.image
                    )
                    albums.append(album)
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"Album {artist_album.name} already in db for arist, skipping"))
                    continue
                if created:
                    album_count += 1
                    print(f"v) Album {album.spotify_albums} added")
            if album_count >0:
                post_slack_message(f"{album_count} new albums for artist: '{artist.spotify_artist}'! Notifying...")
                self.stdout.write(self.style.SUCCESS(f"{album_count} new albums for artist: '{artist.spotify_artist}'"))
            else:
                self.stdout.write(self.style.ERROR(f'No new albums for user {artist.spotify_artist}!!'))