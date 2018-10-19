from django.contrib import admin
from .models import Bookmark, Hashtag

# Register your models here.
admin.site.register(Bookmark)
admin.site.register(Hashtag)