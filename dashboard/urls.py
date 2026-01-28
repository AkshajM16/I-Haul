from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Only route is for dashboard home, where user sees their own listings.
    path('', views.index, name='index')
]
