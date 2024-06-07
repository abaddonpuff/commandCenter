from django.contrib import admin
from centralHub.models import TwitterUser, TwitterUserPosts, SpotifyArtistInfo, SpotifyAlbumTracking

# Register your models here.

@admin.register(TwitterUser)
class TwitterAdminUsers(admin.ModelAdmin):
    list_fields = ['twitter_handle','twitter_user_id','twitter_handle_avatar']

@admin.register(TwitterUserPosts)
class TwitterAdminPosts(admin.ModelAdmin):
    list_fields = ['twitter_post_type','twitter_post_id','twitter_text','twitter_post_to_link']

@admin.register(SpotifyArtistInfo)
class TwitterAdminPosts(admin.ModelAdmin):
    list_fields = ['spotify_artist','spotify_image','spotify_popularity']

@admin.register(SpotifyAlbumTracking)
class TwitterAdminPosts(admin.ModelAdmin):
    list_fields = ['spotify_user','spotify_albums','number_of_tracks','spotify_image_url']