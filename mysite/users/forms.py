from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from phonenumber_field.formfields import PhoneNumberField


class AuthForm(AuthenticationForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = PhoneNumberField()
    role = forms.ChoiceField(choices=Profile.Role.choices)
    password = forms.CharField(widget=forms.PasswordInput())
    password_conf = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        password_conf = clean_data.get('password_conf')

        if password and password_conf and password != password_conf:
            raise forms.ValidationError("Passwords didnt match")


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

