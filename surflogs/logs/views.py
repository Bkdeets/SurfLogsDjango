from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Session,Report,Spot,Profile
import numpy as np
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def index(request):
    sessions = Session.objects.all()
    users = User.objects.all()
    errors = ''

    if request.method == 'POST':
        form = UserForm(request.POST)
        print('here')
        if form.is_valid():
            print('here 2')
            print(form)
            user = form.save()
            user.refresh_from_db()
            user.profile.homespot = Spot.objects.filter(name='Pipeline')[0]
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
        else:
            errors = form.errors
    else:
        form = UserForm()

    context = {
        'sessions': sessions,
        'users':users,
        'user_form':form,
        'errors':errors,
    }
    return render(request, 'logs/index.html', context)

def signin(request):
    errors = ''
    print("ITS BRITNEY BITCH")
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            print("ITS BRITNEY BITCH")
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile', username=user.username)
        else:
            errors = form.errors
    else:
        form = SigninForm()

    context = {
        'signin_form':form,
        'errors':errors,
    }
    return render(request, 'logs/signin.html', context)


def detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'logs/detail.html', {'session': session})


def profile(request, username):
    print(username)
    user = get_object_or_404(User, pk=username)
    sessions = Session.objects.filter(user=username)
    reports = Report.objects.filter(user=username)

    numSessions = len(sessions)
    waveCount = sum([s.waves_caught for s in sessions])
    averageRating = np.mean([s.rating for s in sessions])
    lastSpot = sessions[len(sessions)-1].spot
    avgSessionLength = 0 #np.mean([s.end_time - s.start_time for s in sessions])
    timeSurfed = 0 #np.mean([s.end_time - s.start_time for s in sessions])
    averageWaveHeight = 0 #np.mean([r.wave_height for r in reports])
    avgStartTime = 0 #np.mean([s.start_time for s in sessions])
    avgEndTime = 0 #np.mean([s.end_time for s in sessions])

    context = {
        'user':user,
        'sessions':sessions,
        'numSessions':numSessions,
        'waveCount':waveCount,
        'averageRating':averageRating,
        'lastSpot':lastSpot,
        'avgSessionLength':avgSessionLength,
        'timeSurfed':timeSurfed,
        'averageWaveHeight':averageWaveHeight,
        'avgStartTime':avgStartTime,
        'avgEndTime':avgEndTime,
    }
    return render(request, 'logs/profile.html',context)
