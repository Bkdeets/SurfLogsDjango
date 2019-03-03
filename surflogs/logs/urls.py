from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('<int:session_id>/', views.detail, name='detail'),
    path('profile/', views.profile, name='profile'),
    path('login_success/', views.profile, name='login_success'),
    path('profile/edit', views.profileEdit, name='profile_edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('feed/', views.feed, name='feed'),
    path('post_session/', views.post_session, name='post_session'),
    path('upload_photo/', views.upload_profile_pic, name='upload_photo'),
    path('signup/', views.signup, name='signup')
    ]
