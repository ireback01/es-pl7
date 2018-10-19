from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_tweets, name='home_tweets')
]
