# Generated by Django 4.2.13 on 2024-05-31 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centralHub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='twitter_name',
            field=models.CharField(default='NoneApplied', max_length=100, unique=True),
        ),
    ]
