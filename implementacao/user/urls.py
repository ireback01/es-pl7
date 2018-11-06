from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
	path('profile/new_interest', views.new_interest_user, name="new_interest_user"),
    path('register/',views.register,name="register"),
    path('profile/(?P<username>[a-zA-Z0-9]+)$',views.profile,
    name="profile"),
    path('profile/edit_profile/',views.edit_profile,name="edit_profile"),
    path('profile/bookmarks/', views.index_bookmarks, name="index_bookmarks"),
    path('new_bookmark/', views.create_bookmark, name='new_bookmark'),
    path('logout/',views.logout_view,name="logout"),
    url('^', include('django.contrib.auth.urls')),
]
