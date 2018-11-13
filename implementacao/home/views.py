from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from news_feed.models import Bookmark
from user.models import Profile
from user.forms import TweetForm

@login_required
def home(request):
	return
