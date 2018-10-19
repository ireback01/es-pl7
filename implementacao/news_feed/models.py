from django.db import models
from django.conf import settings
from user.models import Profile

# Create your models here.
class Hashtag(models.Model):
    text = models.CharField(max_length=100)
    user = models.ManyToManyField(Profile, related_name="interests")

    def __str__(self):
        return self.text + " "

class Post(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    pubdate = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # Metadata
    class Meta: 
        ordering = ["-pubdate"]
        permissions = (("can_change_status", "Can see and change articles"),)

    def __str__(self):
        return self.text

class Bookmark(models.Model):
    link = models.URLField()
    description = models.CharField(max_length=100, blank=True, null= True)
    user = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name="bookmarks")
    hashtags = models.ManyToManyField(Hashtag, related_name="bookmarks")

    def __str__(self):
        return self.description
