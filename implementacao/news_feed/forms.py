from django import forms
from django.forms import ModelForm
from .models import Bookmark

class BookmarkForm(ModelForm):
	interests = forms.CharField()

	class Meta:
		model = Bookmark
		fields = ('link', 'description')
