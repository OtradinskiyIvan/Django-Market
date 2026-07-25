from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render
import datetime

from django.urls import reverse
from django.template.loader import render_to_string

test_items = [
    {'id': 1, 'slug': 'test-laptop', 'cat': 'test1', 'name': 'Laptop', 'price': 20_000, 'desc': 'Pretty nice <strong>laptop</strong>',},
    {'id': 2, 'slug': 'test-phone', 'cat': 'test1', 'name': 'PC', 'price': 80_000, 'desc': 'Pretty nice <strong>phone</strong>',},
    {'id': 3, 'slug': 'test-pc', 'cat': 'test2', 'name': 'IPhone', 'price': 75_000, 'desc': 'Pretty nice <strong>pc</strong>',},
]

test_cats = [
    {'id': 1, 'name': 'test1',},
    {'id': 2, 'name': 'test2',},
]

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
        'cats': test_cats,
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
    for cat in test_cats:
        if cat['id'] == cat_id:
            cat_items = [item for item in test_items if item['cat'] == cat['name']]
            data = {
                'title': cat['name'],
                'items_list': cat_items,
            }
            return render(request, 'catalog/category.html', data)
        
    return HttpResponse(f'<h1>Categories</h1><p>cat id: {cat_id}<p/>')

def category_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse | Http404:
    for cat in test_cats:
        if cat['id'] == cat_slug:
            cat_items = [item for item in test_items if item['cat'] == cat['name']]
            data = {
                'title': cat['name'],
                'items_list': cat_items,
            }
            return render(request, 'catalog/category.html', data)
        
    return HttpResponse(f'<h1>Categories</h1><p>cat id: {cat_slug}<p/>')

def item_by_slug(request: HttpRequest, item_slug: str) -> HttpResponse | Http404:
    for item in test_items:
        if item['slug'] == item_slug:
            data = {
                'title': item['name'],
                'cat': item['cat'],
                'price': item['price'],
                'desc': item['desc']
            }
            return render(request, 'catalog/item.html', data)

    raise Http404("Sorry, we don't have this item.")

def item_by_id(request: HttpRequest, item_id: int) -> HttpResponse | Http404:
    for item in test_items:
        if item['id'] == item_id:
            data = {
                'title': item['name'],
                'cat': item['cat'],
                'price': item['price'],
                'desc': item['desc']
            }
            return render(request, 'catalog/item.html', data)

    raise Http404("Sorry, we don't have this item.")

def archive(request: HttpRequest, year: int) -> HttpResponse | HttpResponseRedirect:
    if year > datetime.datetime.now().year:
        uri = reverse('catalog_main')
        return HttpResponseRedirect(uri)
    
    return HttpResponse(f'<h1>Archive</h1><p>Year: {year}<p/>')

def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Page not found</h1><p>Description: {exception}</p>")
