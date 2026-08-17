from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import *
from .models import Profile


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'
    extra = {'title': 'Authentication'}

    def get_success_url(self):
        return reverse_lazy('catalog_main')


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration'}

    def form_valid(self, form):
        user = form.save()
        user.email = form.cleaned_data['email']
        user = form.save()
        user.profile.name = form.cleaned_data['name']
        user.profile.phone = str(form.cleaned_data['phone'])
        user.profile.role = int(form.cleaned_data['role'])
        user.profile.save()
        return redirect('login')

    def get_success_url(self):
        return reverse_lazy('login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = Profile

    form_class = ProfileForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Profile'}

    def get_object(self, queryset=None):       
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile')