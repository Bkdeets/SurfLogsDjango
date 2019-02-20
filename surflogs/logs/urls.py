from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('<int:session_id>/', views.detail, name='detail'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.profileEdit, name='profileEdit'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]
