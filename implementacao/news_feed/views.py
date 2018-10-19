from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from news_feed.forms import BookmarkForm #Custom register form
from news_feed.models import Bookmark

@login_required
def create_bookmark(request):
	if request.method == 'POST':
		form = BookmarkForm(request.POST)

		if form.is_valid():
			aux = form.save(commit=False)
			aux.save
			return redirect('home')
	else:
		form = BookmarkForm()

@login_required
def search_bookmarks(request, hashtag):
	bookmark_list = Bookmark.objects.filter(hashtags__text == hashtag).distinct()
	return bookmark_list
