from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    path('profile/(?P<username>[a-zA-Z0-9]+)$',views.profile,
    name="profile_user"),
    path('profile/edit_profile/',views.edit_profile,name="edit_profile"),
    path('logout/',views.logout_view,name="logout"),
    url('^', include('django.contrib.auth.urls')),
]
