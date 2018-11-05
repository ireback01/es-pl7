from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from news_feed.models import Post, Bookmark
from user.models import Profile

@login_required
def home(request):
	post_list = Post.objects.all()
	return render(request,'home/index.html', context={'posts':post_list})

#@login_required
#def bookmark_area(request):
#	bookmark_list = Bookmark.objects.all()