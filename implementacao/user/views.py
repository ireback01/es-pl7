from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.forms import SignUp,ProfileForm,EditProfileForm
from django.http import HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User
from news_feed.models import Hashtag
from news_feed.forms import BookmarkForm #Custom register form
from news_feed.models import Bookmark
from django.conf import settings

import tweepy


@login_required
def profile(request,username):
	user = User.objects.get(username=username)
	profile = Profile.objects.get(id=user.id)
	string = ""
	if(request.user.profile.interests != None):
		for interest in request.user.profile.interests.all():
			string = string + str(interest)
	arg = {
		'user' : user,
		'profile' : profile,
		'interests' : string,
	}
	return render(request,'profile/profile.html',arg)


@login_required
def logout_view(request):
	logout(request)
	return redirect('/')

def register(request):
	if request.user.is_authenticated: #So a logged in user doesn't go to register
   		return HttpResponseRedirect("/")

	if request.method == 'POST':
		user_form = SignUp(request.POST)

		if user_form.is_valid():
			user_form.save() #Save info to database -> create new user
			username = user_form.cleaned_data['username'] #take username fromcleaned_data form
			password = user_form.cleaned_data['password1'] #take password from form
			user = authenticate(username=username, password=password) #takes care of hashing and so on
			messages.info(request, 'User created with Success!')
			login(request,user)
			profile = Profile.objects.get(id=user.id)
			arg={
				'user':user,
				'profile' : profile 
			}
			return redirect('/profile/edit_profile/',arg)
	else:
		user_form = SignUp()
	return render(request,'registration/register.html',{'user_form' : user_form } )

@login_required
def edit_profile(request):
	#Processes 2 forms.. 1 Auth user and 1 custom model (profile)
	profile = Profile.objects.get(id=request.user.id)
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		user_form = EditProfileForm(request.POST, instance=request.user)
		#return render_to_response('profile/debug.html', {'profile_form': profile_form})
		if profile_form.is_valid() and user_form.is_valid():
			request.user.profile.interests.clear()
			interests_string = profile_form.cleaned_data['interests'].strip()
			if not interests_string == "":
				interests = interests_string.split(" ")
				for interest in interests:
					try:
					    bk = Hashtag.objects.get(text=interest)   
					except Hashtag.DoesNotExist:
					    bk = Hashtag.objects.create(text=interest)
					request.user.profile.interests.add(bk)
					request.user.save
			profile_form.save()
			user_form.save()
			return redirect('/')
		else:
			return render(request, 'profile/edit_profile.html', {
			'user_form':user_form,
			'profile_form':profile_form,
			'profile':profile
			} ) 
	else:
		string = ""
		if(request.user.profile.interests != None):
			for interest in request.user.profile.interests.all():
				string = string + str(interest)
		profile_form = ProfileForm(instance = request.user.profile, initial = {'interests': string})
		user_form = EditProfileForm(instance = request.user)
		return render(request, 'profile/edit_profile.html', {
			'user_form':user_form,
			'profile_form':profile_form,
			'profile':profile
			} )

@login_required
def create_bookmark(request):
	if request.method == 'POST':
		form = BookmarkForm(request.POST)

		if form.is_valid():
			aux = form.save()
			interests_string = form.cleaned_data['interests']
			interests = interests_string.split(" ")
			for interest in interests:
				try:
				    bk = Hashtag.objects.get(text=interest)   
				except Hashtag.DoesNotExist:
				    bk = Hashtag.objects.create(text=interest)
			aux.user = request.user.profile
			aux.hashtags.add(bk)
			aux.save()
			return redirect('home')
	else:
		form = BookmarkForm()
	return render(request, 'profile/new_bookmark.html', {'form': form})

@login_required
def index_bookmarks(request):
	bookmark_list = request.user.profile.bookmarks.all()
	return render(request, 'profile/index_bookmark.html', {'bookmarks': bookmark_list})



@login_required
def login_twitter(request):
	auth = tweepy.OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'),'localhost:8000')

	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
		print('Error! Failed to get request token.')

		#session.set('request_token', auth.request_token)

		verifier = request.GET.get('oauth_verifier')
