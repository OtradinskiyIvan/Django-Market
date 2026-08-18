from django import forms
from .models import Profile, SellerReview
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

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
    username = forms.CharField(label='Username or email')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                email=username,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = PhoneNumberField()
    role = forms.ChoiceField(choices=Profile.Role.choices)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('Email already registered')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and Profile.objects.filter(phone=str(phone), user__is_active=True).exists():
            raise forms.ValidationError('Phone already registered')
        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username, is_active=True):
            raise forms.ValidationError('Username already registered')
        return username



class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Username')
    email = forms.EmailField(disabled=True, label='Email')

    class Meta:
        model = Profile
        fields = ['phone', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email


class TopUpForm(forms.Form):
    amount = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2, label='Amount')


class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
    