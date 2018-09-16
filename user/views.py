from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.forms import SignUp #Custom register form

@login_required
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
			messages.info(request, 'User created with Sucess!')
			return redirect('login')

	else:
		form = SignUp()
	
	return render(request,'registration/register.html',{'form' : form } )

@login_required
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


