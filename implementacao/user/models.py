from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation  = models.CharField(max_length=100, editable=False)
    orcid		 = models.CharField(max_length=100, editable=False)

    research_group = models.URLField(max_length=30, blank=True)
    linked_in    = models.URLField(max_length=256,blank=True)
    image        = models.ImageField(upload_to='images/', blank=True, null=True)
    subreddits	 = models.CharField(max_length=512, blank=True)
    gender       = models.CharField(max_length= 10, blank=True)
    birth_date   = models.DateField(default=date.today, blank=False)
    about_me     = models.CharField(max_length=300, blank=True)
    tweet_ammount= models.IntegerField(default=10, blank=True, validators=[MinValueValidator(1), MaxValueValidator(20)])
    show_reddit = models.BooleanField(default=True, blank=True)
    show_twitter = models.BooleanField(default=True, blank=True)
    twitter_account = models.CharField(max_length=100, blank=True)
    reddit_account = models.CharField(max_length=100, blank=True)

    reddit_token = models.CharField(max_length=256, blank=True)
    tweet_request_token       = models.CharField(max_length=300, blank=True)
    tweet_access_token        = models.CharField(max_length=300, blank=True)
    tweet_access_token_secret = models.CharField(max_length=300, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
