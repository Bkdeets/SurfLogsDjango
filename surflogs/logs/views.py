### Imports ####################################################################
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Session,Report,Spot,Profile
import numpy as np
from .forms import UserForm, SigninForm, UserEditForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
################################################################################



### Index View #################################################################
def index(request):
    sessions = Session.objects.all()
    users = User.objects.all()
    errors = ''

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.homespot = Spot.objects.filter(name='Pipeline')[0]
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('logs:profileEdit')
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
################################################################################



### Signin View ################################################################
def signin(request):
    errors = ''
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('logs:profile')
    else:
        form = SigninForm()

    context = {
        'signin_form':form,
        'errors':errors,
    }
    return render(request, 'logs/signin.html', context)
################################################################################



### Detail View ################################################################
def detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'logs/detail.html', {'session': session})
################################################################################



### Profile View ###############################################################
def profile(request):
    user = request.user
    sessions = Session.objects.filter(user=user)
    reports = Report.objects.filter(user=user)

    numSessions = len(sessions)
    waveCount = sum([s.waves_caught for s in sessions])
    averageRating = np.mean([s.rating for s in sessions])
    if len(sessions) > 0:
        lastSpot = sessions[len(sessions)-1].spot
    else:
        lastSpot = None
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
################################################################################



### Profile and User Edit View #################################################
def profileEdit(request):
    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    errors = ''

    if user:
        if request.method == 'POST':
            user_edit_form = UserEditForm(data=request.POST, instance=request.user)
            profile_edit_form = ProfileForm(request.POST, instance=profile)

            if user_edit_form.is_valid() and profile_edit_form.is_valid():
                user = user_edit_form.save()
                profile = profile_edit_form.save()
                return redirect('logs:profile')
            else:
                errors = [user_edit_form.errors, profile_edit_form.errors]
        else:
            user_fields = {
                'username':  user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
             }
            profile_fields = {
                'user':user,
                'homespot':  profile.homespot,
                'bio': profile.bio,
             }
            user_edit_form = UserEditForm(user_fields)
            profile_edit_form = ProfileForm(profile_fields)



    context = {
        'user': user,
        'errors': errors,
        'profile_edit_form': profile_edit_form,
        'user_edit_form': user_edit_form,
    }
    return render(request, 'logs/profileEdit.html', context)
################################################################################



### Feed View ##################################################################
def feed(request):
    if request.user:
        user = request.user
    else:
        user = None

    sessions = Session.objects.order_by('date')[:30]
    reports = Reports.objects.order_by('date')[:30]

    context = {
        'user':user,
        'sessions':sessions,
        'reports':reports,
    }

    return render(request, 'logs/profile.html',context)
################################################################################
