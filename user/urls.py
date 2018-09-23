from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    path('profile/edit_password/',views.edit_password,name="edit_password"),
    path('profile/edit_profile/',views.edit_profile,name="edit_profile"),
]
