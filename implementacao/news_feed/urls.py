from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_tweets, name='home_tweets'),
    path('new_bookmark', views.create_bookmark, name='new_bookmark'),
]
