from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import datetime

from django.urls import reverse
from django.template.loader import render_to_string
from .utils import menu

from .models import Catalog, Category, Tag
from .forms import *


def index(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Main page',
        'menu': menu,
        'items_list': Catalog.available.all(),
    }
    return render(request, 'catalog/index.html', data)

def add_item(request: HttpRequest, ) -> HttpResponse:
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data.copy()
                tag = data.pop('tags', None)
                item = Catalog.objects.create(**data)
                if tag:
                    item.tags.set([tag]) 
            except Exception as exc:
                form.add_error(None, f'Failed to add item with exception as: {exc}')
    else:
        form = AddItemForm()

    data = {
        'title': 'Add item',
        'menu': menu,
        'form': form,
    }
    return render(request, 'catalog/add_item.html', data)

def contact_us(request: HttpRequest, ) -> HttpResponse:
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ContactForm()

    data = {
        'title': 'Contact us',
        'menu': menu,
        'form': form,
    }
    return render(request, 'catalog/contact.html', data)

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
            'menu': menu,
            'items_list': cat.catalog_set.filter(is_available=1),
        }
        return render(request, 'catalog/category.html', data)

    except Exception as exc:
        raise exc

def category_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse | Http404:
    cat = get_object_or_404(Category, slug=cat_slug)

    try:
        data = {
            'title': cat.title,
            'menu': menu,
            'items_list': cat.catalog_set.filter(is_available=1),
        }
        return render(request, 'catalog/category.html', data)

    except Exception as exc:
        raise exc


def item_by_slug(request: HttpRequest, item_slug: str) -> HttpResponse | Http404:
    item = get_object_or_404(Catalog, slug=item_slug)
    
    try:
        data = {
            'title': item.title,
            'menu': menu,
            'cat': item.category.title,
            'price': item.price,
            'desc': item.desc,
            'tags': item.tags.all(),
        }
        return render(request, 'catalog/item.html', data)

    except Exception as exc:
        raise exc

def item_by_id(request: HttpRequest, item_id: int) -> HttpResponse | Http404:
    item = get_object_or_404(Catalog, pk=item_id)

    try:
        data = {
            'title': item.title,
            'menu': menu,
            'cat': item.category.title,
            'price': item.price,
            'desc': item.desc,
            'tags': item.tags.all(),
        }
        return render(request, 'catalog/item.html', data)

    except Exception as exc:
        raise exc

def tag_by_slug(request, tag_slug) -> HttpResponse | Http404:
    tag = get_object_or_404(Tag, slug=tag_slug)
    try:
        data = {
            'title': tag.title,
            'menu': menu,
            'items_list': tag.catalog_set.all(),
        }
        return render(request, 'catalog/category.html', data)

    except Exception as exc:
        raise exc

def tag_by_id(request, tag_id) -> HttpRequest | Http404:
    tag = get_object_or_404(Tag, pk=tag_id)
    try:
        data = {
            'title': tag.title,
            'menu': menu,
            'items_list': tag.catalog_set.all(),
        }
        return render(request, 'catalog/category.html', data)

    except Exception as exc:
        raise exc

def archive(request, year) -> HttpResponse | Http404:
    if year > datetime.datetime.now().year:
        return HttpResponseRedirect(reverse('catalog_main'))

    data = {
        'title': 'Main page',
        'menu': menu,
        'items_list': Catalog.objects.filter(created_at__year=year, is_available=0),
    }
    return render(request, 'catalog/tag.html', data)

def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Page not found</h1><p>Description: {exception}</p>")
