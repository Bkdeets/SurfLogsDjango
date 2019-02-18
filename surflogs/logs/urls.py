from django.urls import path
from . import views

app_name = 'logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:session_id>/', views.detail, name='detail'),
    path('<str:username>/', views.profile, name='profile'),
    path('signin/', views.signin, name='signin'),
    ]
