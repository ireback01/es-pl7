from django.urls import path
from . import views

urlpatterns = [
    path('new_bookmark', views.create_bookmark, name='new_bookmark'),
]
