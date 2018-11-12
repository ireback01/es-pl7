from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation  = models.CharField(max_length=30, blank=True)
    facebook     = models.URLField(max_length=256,blank=True)
    linked_in    = models.URLField(max_length=256,blank=True)
    image        = models.ImageField(upload_to='images/', blank=True, null=True)
    orcid		 = models.CharField(max_length=19, blank=True)
    subreddits	 = models.CharField(max_length=512, blank=True)
    reddit_token = models.CharField(max_length=256, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
