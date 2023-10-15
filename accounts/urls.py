from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
