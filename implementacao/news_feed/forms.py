from django import forms
from django.forms import ModelForm
from .models import Bookmark

class BookmarkForm(ModelForm):
	text = forms.CharField(widget=forms.Textarea, required = True)

	class Meta:
		model = Bookmark
		fields = ('link', 'description')
