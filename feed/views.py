from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from feed.forms import SignUp, PostForm #Custom register form
from .models import Post

def home(request):
	post_list = Post.objects.all()
	return render(request,'home/index.html', context={'posts':post_list})

def settings(request):
       return render(request,'profile/settings.html')


def register(request):
	if request.method == 'POST':
		form = SignUp(request.POST)

        if form.is_valid(): 
            form.save() #Save info to database -> create new user
            username = form.cleaned_data['username'] #take username from form
            password = form.cleaned_data['password1'] #take password from form
            user = authenticate(username=username, password=password) #takes care of hashing and so on
            messages.sucess(request, 'User created with Sucess!')
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
def change_password(request):
    if request.method == 'POST':
        form = passwordChange(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.sucess(request,'Password changed successfully!')
            return render(request,'home/home.html')
        else:
            messages.error(request,'Error below')
    else:
        form = passwordChange(request.user)
    return render(request, 'accounts/change_password.html', {'form': form} )


