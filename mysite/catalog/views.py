from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import datetime

from django.urls import reverse
from django.template.loader import render_to_string

from .models import Catalog, Category


menu = [
    {'title': 'About us', 'url': 'about_us'},
    {'title': 'Add item', 'url': 'catalog_add_item'},
    {'title': 'Contact us', 'url': 'contact_us'},
    {'title': 'Login', 'url': 'login'},
]

def index(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Main page',
        'menu': menu,
        'items_list': test_items,
    }
    return render(request, 'catalog/index.html', data)

def add_item(request: HttpRequest, ):
    return HttpResponse('Stub add')

def login(request: HttpRequest, ):
    return HttpResponse('Stub login')

def contact_us(request: HttpRequest, ):
    return HttpResponse('Stub contact')

def about_us(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'About us',
        'menu': menu,
    }
    return render(request, 'catalog/about_us.html', data)

def category_by_id(request: HttpRequest, cat_id: int) -> HttpResponse | Http404:
    cat = get_object_or_404(Category, pk=cat_id)

    try:
        data = {
            'title': cat.title,
            'items_list': cat.catalog_set.all(),
        }
        return render(request, 'catalog/category.html', data)

    except Exception as exc:
        raise exc

def category_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse | Http404:
    cat = get_object_or_404(Category, slug=cat_slug)

    try:
        data = {
            'title': cat.title,
            'items_list': cat.catalog_set.all(),
        }
        return render(request, 'catalog/category.html', data)

    except Exception as exc:
        raise exc


def item_by_slug(request: HttpRequest, item_slug: str) -> HttpResponse | Http404:
    item = get_object_or_404(Catalog, slug=item_slug)
    
    try:
        data = {
            'title': item.title,
            'cat': item.category.title,
            'price': item.price,
            'desc': item.desc,
        }
        return render(request, 'catalog/item.html', data)

    except Exception as exc:
        raise exc

def item_by_id(request: HttpRequest, item_id: int) -> HttpResponse | Http404:
    item = get_object_or_404(Catalog, pk=item_id)

    try:
        data = {
            'title': item.title,
            'cat': item.category.title,
            'price': item.price,
            'desc': item.desc,
        }
        return render(request, 'catalog/item.html', data)

    except Exception as exc:
        raise exc

def archive(request: HttpRequest, year: int) -> HttpResponse | HttpResponseRedirect:
    if year > datetime.datetime.now().year:
        uri = reverse('catalog_main')
        return HttpResponseRedirect(uri)
    
    return HttpResponse(f'<h1>Archive</h1><p>Year: {year}<p/>')

def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Page not found</h1><p>Description: {exception}</p>")
