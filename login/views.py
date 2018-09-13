from django.shortcuts import render

def home(request):
    return render(request,'/templates/home/home.html')
