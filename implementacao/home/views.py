from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from news_feed.models import Post, Bookmark
from user.models import Profile
from user.forms import TweetForm

@login_required
def home(request):
	post_list = Post.objects.all()
	profile = Profile.objects.get(id=request.user.id)
	tweet_form = TweetForm()
	return render(request,'home/index.html', context={'posts':post_list, 'profile':profile, 'tweet_form':tweet_form})

#@login_required
#def bookmark_area(request):
#	bookmark_list = Bookmark.objects.all()