from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class AuthForm(AuthenticationForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    role = forms.ChoiceField(choices=Profile.Role.choices)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

