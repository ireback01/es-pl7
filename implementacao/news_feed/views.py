from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from news_feed.forms import PostForm #Custom register form
from news_feed.models import Post

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


