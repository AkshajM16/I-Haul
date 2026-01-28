from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

app_name = 'main'

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # Signup flow
    path('signup/', views.signup, name='signup'),
    # Use Django LoginView with our LoginForm
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html',
        authentication_form=LoginForm
    ), name='login')
]
