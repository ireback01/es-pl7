from django.db import models
from django.conf import settings
from user.models import Profile

# Create your models here.
class Bookmark(models.Model):
    link = models.URLField()
    description = models.CharField(max_length=100, blank=True, null= True)
    user = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name="bookmarks")

    def __str__(self):
        return self.description

    def interests(self):
        string = ""
        if(self.hashtags != None):
            for interest in self.hashtags.all():
                string = string + str(interest)
        return string

class Hashtag(models.Model):
    text = models.CharField(max_length=100)
    user = models.ManyToManyField(Profile, related_name="interests", blank=True)    
    bookmarks = models.ManyToManyField(Bookmark, related_name="hashtags", blank=True)

    def __str__(self):
        return self.text