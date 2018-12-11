from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('register/',views.register,name="register"),
    path('profile/(?P<username>[a-zA-Z0-9]+)$',views.profile, name="profile"),
    path('profile/edit_profile/', views.edit_profile, name="edit_profile"),
    path('bookmarks/', views.index_bookmarks, name="index_bookmarks"),
    path('new_bookmark/', views.create_bookmark, name='new_bookmark'),
    path('logout/',views.logout_view, name="logout"),
    path('reddit_auth', views.reddit_auth, name='reddit_auth'),
    path('store_reddit_token', views.store_reddit_token, name='store_reddit_token'),
    path('reset_reddit', views.reset_reddit, name='reset_reddit'),
    path('login_twitter', views.login_twitter, name='login_twitter'),
    path('reset_twitter', views.reset_twitter, name='reset_twitter'),
    path('callback_url/', views.callback_url, name='callback'),
    path('post_tweet/', views.post_tweet, name='post_tweet'),
    path('handle_orcid/', views.handle_orcid, name='handle_orcid'),
    path('check_orcid/', views.check_orcid, name='check_orcid'),
    url('^', include('django.contrib.auth.urls')),
]
