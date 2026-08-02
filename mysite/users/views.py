from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import *

from catalog.views import menu


def login(request: HttpRequest, ) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = LoginForm()

    data = {
        'title': 'Login',
        'menu': menu,
        'form': form,
    }
    return render(request, 'catalog/login.html', data)
