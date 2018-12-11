from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from user.forms import SignUp, ProfileForm, TweetForm
from django.http import HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User
from news_feed.models import Hashtag
from news_feed.forms import BookmarkForm, HashtagForm #Custom register form
from news_feed.models import Bookmark, PublicAPI
from django.contrib.auth.signals import user_logged_in
import praw
from django.conf import settings
from tweepy.auth import OAuthHandler
import os
import tweepy

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(id=user.profile.id)
    tweet_form = TweetForm()
    bookmark_form = BookmarkForm()
    string = ""
    if(request.user.profile.interests != None):
        for interest in request.user.profile.interests.all():
            string = string + str(interest) + " "
    arg = {
        'user': user,
        'profile': profile,
        'interests': string,
        'tweet_form': tweet_form,
        'bookmark_form': bookmark_form,
    }
    return render(request, 'profile/profile.html', arg)


@login_required(redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.user.is_authenticated: #So a logged in user doesn't go to register
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        user_form = SignUp(request.POST)

        if user_form.is_valid():
            user_form.research_group = "teste"
            user_form.save() #Save info to database -> create new user
            username = user_form.cleaned_data['username'] #take username fromcleaned_data form
            password = user_form.cleaned_data['password1'] #take password from form
            user = authenticate(username=username, password=password) #takes care of hashing and so on
            messages.info(request, 'User created with Success!')
            login(request,user)
            api = PublicAPI(getattr(settings, 'ORCID_ID'), getattr(settings, 'ORCID_SECRET'))
            redirect_url = api.get_login_url('/authenticate', 'http://localhost:8000/handle_orcid')
            return redirect(redirect_url)
    else:
        user_form = SignUp()
    return render(request,'registration/register.html',{'user_form' : user_form } )

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def edit_profile(request):
    #Processes 2 forms.. 1 Auth user and 1 custom model (profile)
    profile = Profile.objects.get(user_id=request.user.profile.id)
    tweet_form = TweetForm()
    bookmark_form = BookmarkForm()
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = EditProfileForm(request.POST, instance=request.user)
        args = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
            'tweet_form': tweet_form,
            'bookmark_form' : bookmark_form,
        }
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
                    request.user.save()
            profile_form.save()
            user_form.save()
            return redirect('/')
        else:
            return render(request, 'profile/edit_profile.html', args)
    else:
        string = ""
        if request.user.profile.interests is not None:
            for interest in request.user.profile.interests.all():
                string = string + str(interest) + " "
        profile_form = ProfileForm(instance = request.user.profile, initial = {'interests': string})
        user_form = EditProfileForm(instance = request.user)
        args = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
            'tweet_form': tweet_form,
            'bookmark_form': bookmark_form,
        }
        return render(request, 'profile/edit_profile.html', args)

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
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

	bookmark_form = BookmarkForm()
	tweet_form = TweetForm()
	next = request.POST.get('next', '/')
	return HttpResponseRedirect(next)    

@login_required(redirect_field_name=None)
def handle_orcid(request):
    orcid_code = request.GET.get('code', '')
    if (orcid_code != ''):
        api = PublicAPI(getattr(settings, 'ORCID_ID'), getattr(settings, 'ORCID_SECRET'))
        response = api.get_token_from_authorization_code(orcid_code, 'http://localhost:8000/handle_orcid')
        token = api.get_search_token_from_orcid()

        orcid = response['orcid']
        profile_obj = request.user.profile
        profile_obj.orcid_token = token
        profile_obj.orcid = orcid
        profile_obj.save()

        get_orcid_info(request)

        return profile(request, request.user.username)
    else:
        logout(request)
        return redirect('/')

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def index_bookmarks(request):
    tweet_form = TweetForm()
    print(request.user.profile.bookmarks.all)
    bookmarks = request.user.profile.bookmarks.all()
    bookmark_form = BookmarkForm()
    return render(request, 'profile/index_bookmark.html', {'bookmarks': bookmarks, 'tweet_form': tweet_form, 'bookmark_form': bookmark_form})

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def reddit_auth(request):
    reddit = praw.Reddit(user_agent='labsync_pl7', client_id='h5QaB1Br2EWxoA', client_secret='BIUqL96PLsZy3vv5oiEyjERK4rc', redirect_uri='http://127.0.0.1:8000/store_reddit_token')
    url = reddit.auth.url(['identity', 'mysubreddits', 'read'], '...', 'permanent')
    return HttpResponseRedirect(url)

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def store_reddit_token(request):
	reddit = praw.Reddit(user_agent='labsync_pl7', client_id='h5QaB1Br2EWxoA', client_secret='BIUqL96PLsZy3vv5oiEyjERK4rc', redirect_uri='http://127.0.0.1:8000/store_reddit_token')
	refresh_token = reddit.auth.authorize(request.GET.get('code'))
	profile_user = request.user.profile
	profile_user.reddit_token = refresh_token
	profile_user.save(update_fields=["reddit_token"])
	return profile(request, request.user.username)

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def reset_reddit(request):
	profile_user = request.user.profile
	profile_user.reddit_token = ''
	profile_user.save(update_fields=["reddit_token"])
	return profile(request, request.user.username)

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def reset_twitter(request):
	profile_user = request.user.profile
	profile_user.tweet_access_token = ""
	profile_user.tweet_access_token_secret = ""
	profile_user.save(update_fields=["tweet_access_token", "tweet_access_token_secret"])
	return profile(request, request.user.username)

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def login_twitter(request):
    auth = OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'))

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    return HttpResponseRedirect(redirect_url)


@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def callback_url(request):
    auth = OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'))
    verifier = request.GET.get('oauth_verifier')

    auth.request_token = {
        'oauth_token': request.GET.get('oauth_token'),
        'oauth_token_secret': request.GET.get('oauth_token_verifier')
    }
    try:
        auth.get_access_token(verifier)

        # Saves on database the User access Tokens
        key = auth.access_token
        secret = auth.access_token_secret
        request.user.profile.tweet_access_token = key
        request.user.profile.tweet_access_token_secret = secret
        request.user.profile.save()

        # Set access to user
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        request.user.profile.twitter_account = "https://twitter.com/" + api.me().screen_name
        request.user.profile.save(update_fields=["twitter_account"])

    except tweepy.TweepError as e:
        print(e)

    return profile(request, request.user.username)

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def post_tweet(request):

    if request.method == 'POST':
        tweet_form = TweetForm(request.POST, request.FILES)
        if tweet_form.is_valid():
            # twitter user credentials
            access_token = request.user.profile.tweet_access_token
            access_token_secret = request.user.profile.tweet_access_token_secret

            auth = OAuthHandler(getattr(settings, 'CONSUMER_KEY'), getattr(settings, 'CONSUMER_SECRET'))
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)

            if tweet_form.cleaned_data.get('image') is not None:
                media = request.FILES['image']
                filename = "images/temp/" + media.name
                with open(filename, 'wb+') as image:
                    for chunk in media.chunks():
                        image.write(chunk)
                api.update_with_media(filename, status=tweet_form.cleaned_data.get('text'))
                os.remove(filename)

            else:
                api.update_status(tweet_form.cleaned_data.get('text'))

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

@login_required(redirect_field_name=None)
def check_orcid(request):
    if(request.user.profile.orcid_token == "" or request.user.profile.orcid == ""):
      api = PublicAPI(getattr(settings, 'ORCID_ID'), getattr(settings, 'ORCID_SECRET'))
      redirect_url = api.get_login_url('/authenticate', 'http://localhost:8000/handle_orcid')
      return redirect(redirect_url)
    else:
        get_orcid_info(request)
        return redirect('/')

@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.profile.orcid_token != "", login_url='/logout/')
def get_orcid_info(request):
    api = PublicAPI(getattr(settings, 'ORCID_ID'), getattr(settings, 'ORCID_SECRET'))
    info = api.read_record_public(request.user.profile.orcid, 'record', request.user.profile.orcid_token)
    first_name = info['person']['name']['given-names']['value']
    last_name = info['person']['name']['family-name']['value']
    keywords = info['person']['keywords']['keyword']

    request.user.first_name = first_name
    request.user.last_name = last_name
    request.user.save()

    request.user.profile.interests.clear()
    for keyword in keywords:
        interest = "#" + keyword['content']
        try:
            bk = Hashtag.objects.get(text=interest)   
        except Hashtag.DoesNotExist:
            bk = Hashtag.objects.create(text=interest)
        request.user.profile.interests.add(bk)
        request.user.profile.save()
