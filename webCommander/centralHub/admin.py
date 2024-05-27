from django.contrib import admin
from centralHub.models import TwitterUser, TwitterUserPosts

# Register your models here.

@admin.register(TwitterUser)
class TwitterAdminUsers(admin.ModelAdmin):
    list_fields = ['twitter_handle','twitter_user_id','twitter_handle_avatar']

@admin.register(TwitterUserPosts)
class TwitterAdminPosts(admin.ModelAdmin):
    list_fields = ['twitter_post_type','twitter_post_id','twitter_text','twitter_post_to_link']