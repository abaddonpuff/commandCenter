from django.db import models

class TwitterUser(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    twitter_handle = models.CharField(max_length = 20, unique=True)
    twitter_name = models.CharField(max_length = 100)
    twitter_user_id = models.PositiveIntegerField(unique=True)
    twitter_handle_avatar = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.twitter_handle

class TwitterUserPosts(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    twitter_user = models.ForeignKey(TwitterUser,
        related_name='user_posts', 
        on_delete=models.CASCADE)
    twitter_post_type = models.CharField(max_length = 20)
    twitter_post_id = models.PositiveIntegerField(unique=True)
    twitter_text = models.TextField(max_length = 20)
    twitter_post_to_link = models.URLField(blank=True)

    class Meta:
        unique_together = [('twitter_user','twitter_text')]

    def __str__(self):
        return f'{self.twitter_user.twitter_handle} Posts'

class SpotifyArtistInfo(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    spotify_artist = models.CharField(max_length = 100, unique=True)
    spotify_albums = models.CharField(max_length = 100)
    spotify_tracks = models.PositiveIntegerField(blank=True)
    spotify_image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.spotify_artist