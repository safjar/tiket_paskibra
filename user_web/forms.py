from django.forms import ModelForm
from user_web.models import User, Profile
from django import forms

from django.contrib.auth.forms import UserCreationForm

#UserProfileForm
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'tanggl_lahir': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        }

#SignUpForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','password1','password2',)