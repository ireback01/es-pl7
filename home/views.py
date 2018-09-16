from django.shortcuts import render, redirect

from news_feed.models import Post

def home(request):
	post_list = Post.objects.all()
	return render(request,'home/index.html', context={'posts':post_list})
