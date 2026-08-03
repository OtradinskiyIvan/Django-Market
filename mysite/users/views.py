from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import *


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'
    extra = {'title': 'Authentication'}

    def get_success_url(self):
        return reverse_lazy('catalog_main')
    