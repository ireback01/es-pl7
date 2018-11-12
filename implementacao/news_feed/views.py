from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import tweepy
from news_feed.forms import BookmarkForm #Custom register form
from news_feed.models import Bookmark
from user.models import Profile
import praw
import pdb
from user.forms import TweetForm

@login_required
def home_tweets(request):
	tweet_form = TweetForm()
	bookmark_form = BookmarkForm()


	auth = tweepy.OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'))
	auth.set_access_token(getattr(settings, 'ACCESS_TOKEN'), getattr(settings, 'ACCESS_TOKEN_SECRET'))

	api = tweepy.API(auth)

	profile = Profile.objects.get(id=request.user.id)
	interests = profile.interests.all()
	args = list()

	if interests.exists():
		for interest in interests:
			args.append(tweepy.Cursor(api.search,lang='en', q=str(interest)+" -filter:retweets", rpp=1, tweet_mode='extended').items(profile.tweet_ammount))
	return render(request,'feed/home_tweets.html',{'args': args, 'tweet_form': tweet_form, 'bookmark_form': bookmark_form})

@login_required
def home_reddit(request):
	args = list()
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
	return render(request, 'feed/home_reddit.html', {'args': args})

@login_required
def search_bookmarks(request, hashtag):
	bookmark_list = Bookmark.objects.filter(hashtags__text == hashtag).distinct()
	return bookmark_list