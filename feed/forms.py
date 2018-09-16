from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post


class SignUp(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Insert Valid Email  ')

    #add database Columns if needed
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class PostForm(ModelForm):
	text = forms.CharField(widget=forms.Textarea, required = True)

	class Meta:
		model = Post
		fields = ('text',)