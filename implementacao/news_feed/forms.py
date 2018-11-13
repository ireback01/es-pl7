from django import forms
from django.forms import ModelForm
from .models import Bookmark, Hashtag

class BookmarkForm(ModelForm):
	interests = forms.CharField(required=False)

	class Meta:
		model = Bookmark
		fields = ('link', 'description')

class HashtagForm(ModelForm):
	class Meta:
		model = Hashtag
		fields = ('text',)
