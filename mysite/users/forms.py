from django import forms
from .models import Profile

class LoginForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    role = forms.ChoiceField(choices=Profile.Role.choices)
