from django.forms import ModelForm
from user_web.models import Profile

from django.contrib.auth.forms import UserCreationForm

#UserProfileForm
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
