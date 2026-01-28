"""All the forms for the account page in the web app. (Only one basic form right now)"""
from django import forms
from django.contrib.auth.models import User


# Shared input CSS classes used across fields, keeps it consistent.
INPUT = 'w-full py-3 px-4 rounded-xl border'

class ProfileForm(forms.ModelForm):
    # profile edit form for first/last name and email
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT}),
            'last_name': forms.TextInput(attrs={'class': INPUT}),
            'email': forms.EmailInput(attrs={'class': INPUT}),
        }
