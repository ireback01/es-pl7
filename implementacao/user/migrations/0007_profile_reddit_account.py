# Generated by Django 2.1.1 on 2018-11-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_profile_twitter_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reddit_account',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]