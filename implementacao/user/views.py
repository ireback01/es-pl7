from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.forms import SignUp,ProfileForm,EditProfileForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import Profile
from django.contrib.auth.models import User



@login_required
def profile(request,username):
	user = User.objects.get(username=username)
	profile = Profile.objects.get(id=user.id)

	arg = {
		'user' : user,
		'profile' : profile
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
			username = user_form.cleaned_data['username'] #take username from form
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
		profile_form = ProfileForm(instance = request.user.profile)
		user_form = EditProfileForm(instance = request.user)
		return render(request, 'profile/edit_profile.html', {
			'user_form':user_form,
			'profile_form':profile_form,
			'profile':profile
			} )