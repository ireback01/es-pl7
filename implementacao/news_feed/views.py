from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from news_feed.forms import PostForm #Custom register form
from news_feed.models import Post
import tweepy

'''
@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)

		if form.is_valid():
			#Saves the object without sending it to the database
			aux = form.save(commit=False) 
			#Checks there is an authenticated user
			if request.user.is_authenticated:
				aux.person = request.user
			aux.save()
			return redirect('home')
	else:
		form = PostForm()
	return render(request, 'feed/new_post.html', {'form': form})
'''



@login_required
def home_tweets(request):
	consumer_key = "oH5g7eTSBNDnZu6599WkOovjI"
	consumer_secret = "9EIZusmUf7qWdtDTaRvVmpPFDnTUzrr5P20Tlk9OhAfNOoHKPY"
	access_token = "1052857003385778177-oEgxU5nlfm8RwHYSqLESH6tPCS1gAd"
	access_token_secret = "WAfh4YvQ9lueDiu9PRnAVuibFo7zGSR6C5zVh08pOrhCV"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	profile = Profile.objects.get(request.user.id)
	interests = profile.interests

	args={}
	for interest : interests:
		tweet = tweepy.Cursor(api.search, q=interest, rpp=2).items(2)
		args.update({'tweet':tweet})

	


	return render(request,'feed/home_tweets.html',args)