from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class SignUp(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Insert Valid Email  ')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)

    class Meta:
        model = User
        fields=(
            'first_name',
            'last_name',
            'password',
        )
class ProfileForm(forms.ModelForm):
    interests = forms.CharField(max_length=256, required=False)
    affiliation = forms.CharField(max_length=30, required=False)
    facebook = forms.URLField(required=False,help_text='Insert Facebook url')
    linked_in =forms.URLField(required=False,help_text='Insert Linked In url')
    image = forms.ImageField(required=False)
    orcid = forms.CharField(max_length=19, required=True)

    class Meta:
        model = Profile
        fields = (
            'affiliation',
            'facebook',
            'linked_in',
            'image',
            'orcid',
            )
