# Generated by Django 4.2.12 on 2024-06-19 03:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("centralHub", "0012_twitteruser_twitter_last_post_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="twitteruser",
            name="twitter_last_post_id",
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
