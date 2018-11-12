from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

def validate_orcid(value):
    split = value.split("-")
    if len(split) != 4:
        raise ValidationError(
            _('%(value)s needs to have 4 groups of characters'),
            params={'value': value},
        )
    for string in split:
        if len(string) != 4:
            raise ValidationError(
                _('%(value)s each groups needs to have 4 characters'),
                params={'value': value},
            )

class ProfileForm(forms.ModelForm):
    interests = forms.CharField(max_length=256, required=False)
    affiliation = forms.CharField(max_length=30, required=False)
    facebook = forms.URLField(required=False,help_text='Insert Facebook url')
    linked_in =forms.URLField(required=False,help_text='Insert Linked In url')
    image = forms.ImageField(required=False)
    orcid = forms.CharField(max_length=19, required=True, validators=[validate_orcid])
    subreddits = forms.CharField(max_length=512, required=False)

    class Meta:
        model = Profile
        fields = (
            'affiliation',
            'facebook',
            'linked_in',
            'image',
            'orcid',
            'subreddits',
            )
