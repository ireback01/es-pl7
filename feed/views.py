from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login

from feed.forms import SignUp #Custom register form

def home(request):
    return render(request,'home/home.html')

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
