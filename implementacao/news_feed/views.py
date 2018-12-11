from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import tweepy
from news_feed.forms import BookmarkForm #Custom register form
from news_feed.models import Bookmark
from user.models import Profile
import praw
import pdb
from user.forms import TweetForm
from datetime import datetime

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def home_tweets(request):
	tweet_form = TweetForm()
	bookmark_form = BookmarkForm()


	auth = tweepy.OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'))
	auth.set_access_token(getattr(settings, 'ACCESS_TOKEN'), getattr(settings, 'ACCESS_TOKEN_SECRET'))

	api = tweepy.API(auth)

	profile = Profile.objects.get(id=request.user.profile.id)
	interests = profile.interests.all()
	args_tweets = list()
	args = list()
	merged_list = list()
	
	if(profile.show_twitter):
		if interests.exists():
			for interest in interests:
				args_tweets.append(tweepy.Cursor(api.search,lang='en', q=str(interest)+" -filter:retweets", rpp=1, tweet_mode='extended').items(profile.tweet_ammount))

		for iterator in args_tweets:
			merged_list += iterator

	if(profile.show_reddit):
		if(request.user.profile.reddit_token): # if redditor token is assigned to user profile (i.e. user is logged in reddit)
			reddit = praw.Reddit(user_agent='labsync_pl7', client_id='h5QaB1Br2EWxoA', client_secret='BIUqL96PLsZy3vv5oiEyjERK4rc', refresh_token=request.user.profile.reddit_token)
			subreddits = list(reddit.user.subreddits())
			for subreddit in subreddits:
				posts = subreddit.hot(limit=5)
				args.append(posts)
		else:
			reddit = praw.Reddit(user_agent='labsync_pl7', client_id='h5QaB1Br2EWxoA', client_secret='BIUqL96PLsZy3vv5oiEyjERK4rc')
			subreddits = request.user.profile.subreddits
			if(subreddits is not ''):
				subreddits = subreddits.split(" ")
				for subreddit in subreddits:
					posts = reddit.subreddit(subreddit).hot(limit=5)
					args.append(posts)

		for iterator in args:
			merged_list += iterator

	merged_list.sort(key=lambda x: getattr(x, 'created_at', datetime.utcfromtimestamp(getattr(x, 'created_utc', 0))), reverse=True)

	return render(request,'feed/home_tweets.html',{'args': merged_list, 'tweet_form': tweet_form, 'bookmark_form': bookmark_form})

@login_required(redirect_field_name=None)
def search_bookmarks(request, hashtag):
	bookmark_list = Bookmark.objects.filter(hashtags__text == hashtag).distinct()
	return bookmark_list