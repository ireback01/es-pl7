from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login

def home(request):
    return render(request,'home/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid(): 
            form.save() #Save info to database -> create new user
            username = form.cleaned_data['username'] #take username from form
            password = form.cleaned_data['password1'] #take password from form
            user = authenticate(username=username, password=password) #takes care of hashing and so on
            messages.info(request, 'User created with Sucess!')
            return redirect('login')

    else:
        form = UserCreationForm()
    
    
    context = {'form' : form } 
    return render(request,'registration/register.html',context)



#Fazer mais campos na form (Email entre outros)
#keep working on this