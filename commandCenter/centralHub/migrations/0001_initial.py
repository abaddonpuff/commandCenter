# Generated by Django 4.2.12 on 2024-05-10 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterFramework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_handle', models.CharField(max_length=20, unique=True)),
                ('twitter_handle_avatar', models.URLField(blank=True)),
                ('twitter_handle_post_type', models.CharField(max_length=20)),
                ('twitter_handle_link', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
