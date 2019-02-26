
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Session, Report, Wave_Data
from django.contrib.auth.forms import UserCreationForm, User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password1'
        )

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            'homespot',
            'bio'
        )

class SessionForm(ModelForm):
    notes =          forms.CharField(required=False)
    waves_caught = 	 forms.IntegerField(required=False)
    rating =         forms.IntegerField(required=False)
    class Meta:
        model = Session
        fields = (
            'date',
            'start_time',
            'end_time',
            'spot',
            'waves_caught',
            'rating',
            'notes'
        )

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = (
            'date',
            'time',
            'spot',
            'wave_quality',
            'notes'
        )

class WaveDataForm(ModelForm):
    tide =          forms.CharField(required=False)
    crowd =         forms.CharField(required=False)
    wind_dir =      forms.CharField(required=False)
    wave_height =   forms.IntegerField(required=False)
    wave_period =   forms.CharField(required=False)
    wind_speed =    forms.CharField(required=False)
    conditions =    forms.CharField(required=False)
    class Meta:
        model = Wave_Data
        fields = (
            'tide',
            'crowd',
            'wind_dir',
            'wave_height',
            'wave_period',
            'wind_speed',
            'conditions'
        )
