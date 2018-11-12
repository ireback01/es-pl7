from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from news_feed.models import Bookmark
from user.models import Profile

@login_required
def home(request):
	post_list = Post.objects.all()
<<<<<<< HEAD
	#profile = Profile.objects.get(id=request.user.id)
	return render(request,'home/index.html', context={'posts':post_list, 'profile':profile})
=======
	return render(request,'home/index.html', context={'posts':post_list})
>>>>>>> 0889a4d3c4e0ea4f80f3d75c1f64299aac98d0dc

#@login_required
#def bookmark_area(request):
#	bookmark_list = Bookmark.objects.all()