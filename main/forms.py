from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    """
    SignupForm built on Django UserCreationForm
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    """
    TODO in the future. Currently inherits all behavior from AuthenticationForm unchanged.
    """
    pass
