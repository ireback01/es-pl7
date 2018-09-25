from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from user.forms import SignUp,edit_profile #Custom register form

@login_required
def profile(request):
	arg = {'user': request.user}
	return render(request,'profile/profile.html',arg)

def register(request): 		
	if request.method == 'POST':
		form = SignUp(request.POST)

		if form.is_valid():
			form.save() #Save info to database -> create new user
			username = form.cleaned_data['username'] #take username from form
			password = form.cleaned_data['password1'] #take password from form
			user = authenticate(username=username, password=password) #takes care of hashing and so on
			messages.info(request, 'User created with Success!')
			return redirect('login')

	else:
		form = SignUp()
	
	return render(request,'registration/register.html',{'form' : form } )

@login_required
def edit_password(request):
	if request.method == 'POST':
		form = passwordChange(request.POST, instance=request.user)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.info(request,'Password changed successfully!')
			return render(request,'home/home.html')
		else:
			messages.error(request,'Error Below')
	else:
		form = passwordChange(request.user)
	return render(request, 'profile/change_password.html', {'form': form} )


@login_required
def edit_profile(request):
	if request.method == 'POST':
		form = edit_profile(request.POST ,instance=request.user, request = request)

		if form.is_valid:
			user  = form.save()
			return redirect('/profile')
	else:
		form = edit_profile(instance=request.user)
		return render(request, 'profile/edit_profile.html', {'form':form} )
