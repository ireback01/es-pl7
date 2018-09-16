from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

from feed.forms import SignUp, PostForm #Custom register form
from .models import Post

def home(request):
	post_list = Post.objects.all()
	return render(request,'home/index.html', context={'posts':post_list})

def register(request):
	if request.method == 'POST':
		form = SignUp(request.POST)

		if form.is_valid(): 
			form.save() #Save info to database -> create new user
			username = form.cleaned_data['username'] #take username from form
			password = form.cleaned_data['password1'] #take password from form
			user = authenticate(username=username, password=password) #takes care of hashing and so on
			messages.info(request, 'User created with Sucess!')
			return redirect('login')

	else:
		form = SignUp()
	
	
	return render(request,'registration/register.html',{'form' : form } )

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