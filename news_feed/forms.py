from django import forms
from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
	text = forms.CharField(widget=forms.Textarea, required = True)

	class Meta:
		model = Post
		fields = ('text',)