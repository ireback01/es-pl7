from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=500)
    pubdate = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # Metadata
    class Meta: 
        ordering = ["-pubdate"]
        permissions = (("can_change_status", "Can see and change articles"),)

    def __str__(self):
        return self.text

