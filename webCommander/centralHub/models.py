from django.db import models

class TwitterUser(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    twitter_handle = models.CharField(max_length = 20, unique=True)
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
        return f'{self.TwitterUser.twitter_handle} Posts'