from django.db import models

class TwitterFramework(models.Model):
    twitter_handle = models.CharField(max_length = 20, unique=True)
    twitter_handle_avatar = models.URLField(blank=True)
    twitter_post_type = models.CharField(max_length = 20)
    twitter_post_to_link = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.twitter_handle