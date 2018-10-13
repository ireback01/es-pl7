from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from news_feed.models import Post
from user.models import Profile
from news_feed.forms import PostForm

@login_required
def home(request):
	form = PostForm()
	post_list = Post.objects.all()
	profile = Profile.objects.get(id=request.user.id)
	return render(request,'home/index.html', context={'posts':post_list, 'profile':profile, 'form':form})
