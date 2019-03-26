### Imports ####################################################################
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Session,Report,Spot,Profile,Photo,UserSummary
import numpy as np
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from itertools import chain
from .sql import RawOperations
import datetime
from django.utils import timezone
################################################################################




### Signup View #################################################################
def signup(request):
    sessions = Session.objects.all()
    user = request.user
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
            user_summary = UserSummary(user.user_id, user.username)
            user_summary.save()
            return redirect('logs:profile_edit')
        else:
            errors = form.errors
    else:
        form = UserForm()

    context = {
        'sessions': sessions,
        'user':user,
        'user_form':form,
        'errors':errors,
    }
    return render(request, 'logs/signup.html', context)
################################################################################



### Index ######################################################################
def index(request):
    return render(request, 'index.html')
################################################################################


### Signin View ################################################################
def signin(request):
    errors = ''
    username = password = ''
    if request.POST:
        form = SigninForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                profile = Profile.objects.filter(user=user)
                if profile:
                    login(request, user)
                    return redirect('logs:profile')
                else:
                    profile = Profile(user=user)
                    login(request, user)
                    return redirect('logs:profile_edit')
        else:
            errors = form.errors
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

    #form =
    return render(request, 'logs/detail.html', {'session': session})
################################################################################


### CSC 455 Version ###
### Profile View ###############################################################
def profile(request):
    user = request.user
    if not user.is_anonymous:
        userImage = user.profile.photo
        raw_op = RawOperations()

        print(userImage)

        ## View for user? ##
        ## can make an sql function with this ##
        sessions = Session.objects.raw('SELECT * FROM logs_session WHERE user_id = %s',[user.id])
        reports = Report.objects.raw('SELECT * FROM logs_report WHERE user_id = %s',[user.id])

        ## Aggregate queries
        numSessions = raw_op.execSQL('SELECT COUNT(*) FROM logs_session WHERE user_id = %s',[user.id])[0][0]
        waveCount = raw_op.execSQL('SELECT SUM(waves_caught) FROM logs_session WHERE user_id = %s',[user.id])[0][0]
        averageRating = raw_op.execSQL('SELECT AVG(rating) FROM logs_session WHERE user_id = %s',[user.id])[0][0]

        ## Nested queries
        averageWaveHeight = raw_op.execSQL('SELECT AVG(wave_height) FROM logs_wave_data WHERE (SELECT wave_data_id FROM logs_session WHERE user_id = %s) = logs_wave_data.wave_data_id;',[user.id])[0][0]

        #raw_op.build_stored_functions()

        #level = raw_op.execSQL('UserLevel(%s)',[numSessions])
        #print(level)

        ## Needs time operations queries
        avgSessionLength = 0#Session.objects.raw('SELECT AVERAGE(len) FROM logs_session WHERE user_id = %s',[user.id])
        # if numSessions[0] > 0:
        #     lastSpot = None ## query to find most recent spot
        # else:
        #     lastSpot = None
        lastSpot = None
        timeSurfed = 0 #np.mean([s.end_time - s.start_time for s in sessions])
        avgStartTime = 0 #np.mean([s.start_time for s in sessions])
        avgEndTime = 0 #np.mean([s.end_time for s in sessions])

        users = User.objects.all()
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
            'users': users
        }
        return render(request, 'logs/profile.html',context)
    else:
        return redirect('logs:login')
################################################################################

##### Production Version ################
# ### Profile View ###############################################################
# def profile(request):
#     user = request.user
#     if not user.is_anonymous:
#         userImage = user.profile.photo
#         print(userImage)
#
#         sessions = Session.objects.raw('SELECT * FROM logs_session WHERE user_id = %s',[user.id])
#         reports = Report.objects.raw('SELECT * FROM logs_report WHERE user_id = %s',[user.id])
#
#         numSessions = len(sessions)
#         waveCount = sum([s.waves_caught for s in sessions])
#         averageRating = np.mean([s.rating for s in sessions])
#         if len(sessions) > 0:
#             lastSpot = sessions[len(sessions)-1].spot
#         else:
#             lastSpot = None
#
#         avgSessionLength = 0 #np.mean([s.end_time - s.start_time for s in sessions])
#         ## **** STORED FUNCTION for mean **** ##
#         timeSurfed = 0 #np.mean([s.end_time - s.start_time for s in sessions])
#         averageWaveHeight = 0 #np.mean([r.wave_height for r in reports])
#         avgStartTime = 0 #np.mean([s.start_time for s in sessions])
#         avgEndTime = 0 #np.mean([s.end_time for s in sessions])
#
#         context = {
#             'user':user,
#             'sessions':sessions,
#             'numSessions':numSessions,
#             'waveCount':waveCount,
#             'averageRating':averageRating,
#             'lastSpot':lastSpot,
#             'avgSessionLength':avgSessionLength,
#             'timeSurfed':timeSurfed,
#             'averageWaveHeight':averageWaveHeight,
#             'avgStartTime':avgStartTime,
#             'avgEndTime':avgEndTime,
#         }
#         return render(request, 'logs/profile.html',context)
#     else:
#         return redirect('logs:login')
# ################################################################################



### Profile and User Edit View #################################################
def profileEdit(request):
    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    errors = ''

    if user:
        if request.method == 'POST':
            user_edit_form = UserEditForm(data=request.POST, instance=request.user)
            profile_edit_form = ProfileForm(request.POST, request.FILES, instance=profile)

            if user_edit_form.is_valid() and profile_edit_form.is_valid():
                user = user_edit_form.save()
                profile = profile_edit_form.save()
                #profile.photo=request.FILES['photo']
                profile.save()
                user_summary = UserSummary.objects.filter(username=user.username)
                if user_summary:
                    user_summary.username = user.username
                    user_summary.bio = profile.bio
                    user_summary.homespot = profile.homespot
                    user_summary.photo = profile.photo
                else:
                    user_summary = UserSummary(
                        user.id,
                        user.username,
                        profile.bio,
                        profile.homespot,
                        profile.photo
                        )
                user_summary.save()
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
            user_edit_form = UserEditForm(user_fields, instance=request.user)
            profile_edit_form = ProfileForm(profile_fields, instance=profile)

    context = {
        'user': user,
        'errors': errors,
        'profile_edit_form': profile_edit_form,
        'user_edit_form': user_edit_form,
    }
    return render(request, 'logs/profile_edit.html', context)
################################################################################



### Feed View ##################################################################
def feed(request):
    if request.user:
        user = request.user
    else:
        user = None

    sessions = Session.objects.order_by('date')[:30]
    reports = Report.objects.order_by('date')[:30]
    print(reports)
    print(sessions)

    context = {
        'user':user,
        'sessions':sessions,
        'reports':reports,
    }

    return render(request, 'logs/feed.html', context)
################################################################################



### Login Redirect #############################################################
def login_success(request):
    profile = Profile.objects.filter(user=user)[0]

    if profile:
        # user is an admin
        return redirect('logs:profile')
    else:
        return redirect('logs:profile_edit')
################################################################################



### Post Session ###############################################################
def post_session(request):
    errors = ''
    if request.user:
        user = request.user
    else:
        return redirect('logs:signin')
    if user:
        if request.method == 'POST':
            session_post_form = SessionForm(request.POST)
            wave_data_form = WaveDataForm(request.POST)
            if session_post_form.is_valid() and wave_data_form.is_valid():

                session = session_post_form.save(commit=False)
                wave_data = wave_data_form.save(commit=False)


                wave_data.spot = session.spot
                wave_data.date = session.date
                wave_data.time = session.end_time

                session.user = user
                wave_data.save()
                session.wave_data = wave_data
                session.save()

                return redirect('logs:profile')

            else:
                errors = session_post_form.errors
        else:
            session_post_form = SessionForm()
            wave_data_form = WaveDataForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'session_post_form':session_post_form,
        'wave_data_form':wave_data_form,
        'errors':errors
    }

    return render(request, 'logs/post_session.html', context)
################################################################################



### Post Report ###############################################################
def post_report(request):
    errors = ''
    if request.user:
        user = request.user
    else:
        return redirect('logs:signin')
    if user:
        if request.method == 'POST':
            report_post_form = ReportForm(request.POST)
            wave_data_form = WaveDataForm(request.POST)

            if report_post_form.is_valid() and wave_data_form.is_valid():

                # Calling raw sql to do an INSERT operation with Prepared Statements
                # raw_op = RawOperations()
                # report_id = raw_op.processReportFormAndReturnId(report_post_form=report_post_form, user=user.id)
                # report = Report.objects.filter(report_id=report_id)[0]
                report = report_post_form.save(commit=False)
                wave_data = wave_data_form.save(commit=False)

                report.user = user

                wave_data.date = report.date
                wave_data.spot = report.spot
                wave_data.save()
                report.wave_data = wave_data
                report.save()

                return redirect('logs:profile')

            else:
                errors = report_post_form.errors

        else:
            report_post_form = ReportForm()
            wave_data_form = WaveDataForm()
    else:
        return redirect('logs:signin')

    context = {
        'user':user,
        'report_post_form':report_post_form,
        'wave_data_form':wave_data_form,
        'errors':errors
    }

    return render(request, 'logs/post_report.html', context)
################################################################################




### Upload Profile Image #######################################################
def upload_profile_pic(request):
    user = request.user
    profile = user.profile
    errors = ''

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            return redirect('logs:profile')
        else:
            errors = form.errors
    else:
        form = ImageUploadForm({'referencing_id':user.id})


    context = {
        'user':user,
        'form':form,
        'errors':errors
    }
    return render(request, 'logs/upload_photo.html', context)
################################################################################



### User Summary View #######################################################
def user_summary(request, username="default"):
    user = request.user
    if user.username != username:
        #raw_op = RawOperations()
        #raw_op.create_usersummarys()
        print(UserSummary.objects.all())
        print(username)
        user_summary = UserSummary.objects.filter(username=username)[0]
        print(user_summary)
        # user2 = User.objects.filter(username=username)
        # sessions = Session.objects.filter(user=user2)
        sessions = []
        context = {
            'user_summary' : user_summary,
            'sessions' : sessions
        }
        return render(request, 'logs/user_summary.html', context)
    else:
        return redirect('logs:profile')
################################################################################
