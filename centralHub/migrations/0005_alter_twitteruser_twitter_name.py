# Generated by Django 4.2.13 on 2024-05-31 04:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("centralHub", "0004_twitteruser_twitter_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="twitteruser",
            name="twitter_name",
            field=models.CharField(max_length=100),
        ),
    ]
