from django.db import models


class TwitterUser(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    twitter_handle = models.CharField(max_length=20, unique=True)
    twitter_name = models.CharField(max_length=100)
    twitter_user_id = models.PositiveBigIntegerField(unique=True)
    twitter_handle_avatar = models.URLField(blank=True)
    twitter_last_post_id = models.PositiveBigIntegerField(
        unique=True, null=True, blank=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.twitter_handle


class TwitterUserPosts(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    twitter_user = models.ForeignKey(
        TwitterUser, related_name="user_posts", on_delete=models.CASCADE
    )
    twitter_post_type = models.CharField(max_length=20)
    twitter_post_id = models.PositiveBigIntegerField(unique=True)
    twitter_text = models.TextField(max_length=20)
    twitter_post_to_link = models.URLField(blank=True)

    class Meta:
        unique_together = [("twitter_user", "twitter_text")]

    def __str__(self):
        return f"Post # {self.twitter_post_id} - {self.twitter_user}"


class SpotifyArtistInfo(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    spotify_artist = models.CharField(max_length=100, unique=True)
    spotify_artist_id = models.CharField(max_length=22, unique=True)
    spotify_image = models.URLField(blank=True)
    spotify_popularity = models.PositiveIntegerField(blank=True)
    spotify_artist_albums_registered = models.PositiveIntegerField(
        blank=True, editable=True, default=0
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.spotify_artist


class SpotifyAlbumTracking(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    spotify_user = models.ForeignKey(
        SpotifyArtistInfo, related_name="artist_album", on_delete=models.CASCADE
    )
    spotify_albums = models.CharField(max_length=200)
    number_of_tracks = models.PositiveIntegerField(blank=True)
    spotify_image_url = models.URLField(blank=True)

    class Meta:
        unique_together = [("spotify_user", "spotify_albums")]

    def __str__(self):
        return self.spotify_albums
