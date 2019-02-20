
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username','password1')

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('homespot','bio')

class SigninForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
