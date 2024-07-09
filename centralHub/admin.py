from django.contrib import admin
from centralHub.models import (
    TwitterUser,
    TwitterUserPosts,
    SpotifyArtistInfo,
    SpotifyAlbumTracking,
)

# Register your models here.


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    list_display = [
        "twitter_handle",
        "twitter_name",
        "twitter_user_id",
        "twitter_handle_avatar",
        "twitter_last_post_id",
    ]


@admin.register(TwitterUserPosts)
class TwitterUserPostsAdmin(admin.ModelAdmin):
    list_display = [
        "twitter_post_type",
        "twitter_post_id",
        "twitter_text",
        "twitter_post_to_link",
    ]


@admin.register(SpotifyArtistInfo)
class SpotifyArtistInfoAdmin(admin.ModelAdmin):
    list_display = ["spotify_artist", "spotify_image", "spotify_popularity"]


@admin.register(SpotifyAlbumTracking)
class SpotifyAlbumTrackingAdmin(admin.ModelAdmin):
    list_display = [
        "spotify_user",
        "spotify_albums",
        "number_of_tracks",
        "spotify_image_url",
    ]
