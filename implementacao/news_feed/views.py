from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import tweepy
from news_feed.forms import BookmarkForm #Custom register form
from news_feed.models import Bookmark
from user.models import Profile

@login_required
def home_tweets(request):
	auth = tweepy.OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'))
	auth.set_access_token(getattr(settings, 'ACCESS_TOKEN'), getattr(settings, 'ACCESS_TOKEN_SECRET'))

	api = tweepy.API(auth)
	
	profile = Profile.objects.get(id=request.user.id)
	interests = profile.interests.all()

	args = list()
	for interest in interests:
		args.append(tweepy.Cursor(api.search, q=str(interest), rpp=2).items(2))

	return render(request,'feed/home_tweets.html',{'args':args})

@login_required
def search_bookmarks(request, hashtag):
	bookmark_list = Bookmark.objects.filter(hashtags__text == hashtag).distinct()
	return bookmark_list
