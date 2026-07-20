from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
import datetime

from django.urls import reverse
from django.template.loader import render_to_string


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/index.html')

def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/about_us.html')

def category_by_id(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f'<h1>Categories</h1><p>cat id: {cat_id}<p/>')

def category_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f'<h1>Categories</h1><p>cat slug: {cat_slug}<p/>')

def archive(request: HttpRequest, year: int) -> HttpResponse | HttpResponseRedirect:
    if year > datetime.datetime.now().year:
        uri = reverse('catalog_main')
        return HttpResponseRedirect(uri)
    
    return HttpResponse(f'<h1>Archive</h1><p>Year: {year}<p/>')

def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Page not found</h1><p>Exception: {exception}</p>")
