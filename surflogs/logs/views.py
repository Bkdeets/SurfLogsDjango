from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Session


def index(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions}
    return render(request, 'logs/index.html', context)


def detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'logs/detail.html', {'session': session})
