from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Catalog main page')

def categories(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>Categories</h1>')