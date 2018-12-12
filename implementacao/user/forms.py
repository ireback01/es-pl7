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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

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
    CHOICES = [('Male', 'male'),
               ('Female', 'female')]

    interests    = forms.CharField(max_length=256, required=False)
    subreddits = forms.CharField(max_length=512, required=False)
    research_group = forms.URLField(max_length=100, required=True, help_text='*')
    linked_in    = forms.URLField(required=False, help_text='Insert Linked In url')
    image        = forms.ImageField(required=False)
    birth_date   = forms.DateField(required=True,  help_text='Format: yyyy-mm-dd')
    gender       = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),required=False)
    about_me     = forms.CharField(max_length=300, help_text='Max: 300 letters', required=False)
    tweet_ammount= forms.IntegerField(required=True, help_text='* Ammount of Tweets per Interest: 1-20')
    show_reddit = forms.BooleanField(required=False)
    show_twitter = forms.BooleanField(required=False)
    twitter_account = forms.CharField(max_length=100, required=False)
    reddit_account = forms.EmailField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = (
            'research_group',
            'linked_in',
            'image',
            'subreddits',
            'birth_date',
            'gender',
            'about_me',
            'tweet_ammount',
            'show_reddit',
            'show_twitter',
            'twitter_account',
            'reddit_account',
            )


class TweetForm(forms.Form):
    text = forms.CharField(max_length=150, help_text='Max: 150chars', required=True)
    image = forms.ImageField(required=False)

    class Meta:
        fields = ('text',
                  'image',
                  )

    def clean(self):
        cleaned_data = super(TweetForm, self).clean()
        text = cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('You have to write something!')
