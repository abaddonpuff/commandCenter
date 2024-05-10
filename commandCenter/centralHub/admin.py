from django.contrib import admin
from centralHub.models import TwitterFramework

# Register your models here.

# twitter_handle = models.CharField(max_length = 20, unique=True)
#     twitter_handle_avatar = models.URLField(blank=True)
#     twitter_handle_post_type = models.CharField(max_length = 20)
#     twitter_post_to_link = models.URLField(blank=True)

@admin.register(TwitterFramework)
class CommandAdmin(admin.ModelAdmin):
    list_fields = ['twitter_handle','twitter_handle_avatar','twitter_handle_post_type','twitter_post_to_links']