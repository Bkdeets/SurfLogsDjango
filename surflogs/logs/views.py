from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Session,User,Report
import numpy as np

def index(request):
    sessions = Session.objects.all()
    users = User.objects.all()
    context = {
        'sessions': sessions,
        'users':users,
    }
    return render(request, 'logs/index.html', context)


def detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'logs/detail.html', {'session': session})


def profile(request, username):
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
