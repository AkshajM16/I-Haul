"""URL routes for the Account area (profile + auth helpers)"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    # Profile home: show the current users account details and their listings
    path('', views.profile, name='profile'),

    # Edit account details for the user
    path('edit/', views.edit_profile, name='edit'),

    # Django logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password change using Django. It redirects back to profile on success
    path('password/', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change.html',
        success_url='/account/'
    ), name='password'),
]
