# Generated by Django 2.1.1 on 2018-11-13 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookmarks', to='user.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='hashtags', to='news_feed.Bookmark')),
                ('user', models.ManyToManyField(blank=True, related_name='interests', to='user.Profile')),
            ],
        ),
    ]
