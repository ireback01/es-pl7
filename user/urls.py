from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    path('profile/edit_profile/',views.edit_profile,name="edit_profile"),
    path('logout/',views.logout_view,name="logout"),
    url('^', include('django.contrib.auth.urls')),
]
