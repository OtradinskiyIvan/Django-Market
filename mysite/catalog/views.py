from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from functools import wraps
import datetime

from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone

from .services import *
from .utils import menu

from .models import Catalog, Category, Tag
from .forms import *


def seller_required(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.profile.role != Profile.Role.SELLER:
            return render(request, 'catalog/access_denied.html', {'title': 'Access denied', 'menu': menu})
        return view_func(request, *args, **kwargs)
    return _wrapper


def index(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Main page',
        'menu': menu,
        'items_list': Catalog.available.all(),
    }
    return render(request, 'catalog/index.html', data)

@login_required
def add_item(request: HttpRequest, ) -> HttpResponse:
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.cleaned_data.copy()
                data.pop('images', None)
                data.pop('video', None)
                tag = data.pop('tags', None)
                item = Catalog.objects.create(
                    seller=request.user.profile,
                    **data,
                )

                if tag:
                    item.tags.set([tag])
                for file in request.FILES.getlist('images'):
                    item.images.create(image=file)
                if video := request.FILES.get('video'):
                    item.video.create(video=video)

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
            'item': item,
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
            'item': item,
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

@login_required
def cart_add(request, item_id):
    item = get_object_or_404(Catalog, pk=item_id)
    next_url = request.POST.get('next')
    if item.seller_id == request.user.profile.id:
        messages.error(request, 'Cannot buy your own item')
        return redirect(next_url or reverse('catalog_item_id', args=[item_id]))
    form = CartAddForm(request.POST)
    if form.is_valid():
        qty = form.cleaned_data['quantity']
        if qty > item.quantity:
            messages.error(request, f'Not enough stock for {item.title}')
        else:
            add_to_cart(request, item_id, qty)
            messages.success(request, f'{item.title} added to cart')
    return redirect(next_url or reverse('catalog_item_id', args=[item_id]))

@login_required
def cart_remove(request, item_id):
    remove_from_cart(request, item_id)
    return redirect('cart')

@login_required
def cart(request):
    lines, total = cart_lines(request)
    data = {'title': 'Cart', 'menu': menu, 'lines': lines, 'total': total,
            'balance': request.user.profile.balance}
    return render(request, 'catalog/cart.html', data)

@login_required
def checkout(request):
    if request.method == 'POST':
        lines, _ = cart_lines(request)
        if not lines:
            messages.error(request, 'Cart is empty')
            return redirect('cart')
        try:
            create_order(request.user.profile, [(it, q) for it, q, _ in lines])
            clear_cart(request)
            messages.success(request, 'Order created')
            return redirect('orders')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart')
    return redirect('cart')

@login_required
def order_accept(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user.profile)
    accept_order(order)
    return redirect('orders')


@login_required
def order_decline(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user.profile)
    decline_order(order)
    return redirect('orders')


@seller_required
def order_ship(request, order_id):
    profile = request.user.profile
    order = get_object_or_404(
        Order.objects.filter(orderitem__item__seller=profile).distinct(),
        pk=order_id,
    )
    if order.status == Order.Status.ORDERED:
        order.status = Order.Status.SHIPPED
        order.shipped_at = timezone.now()
        order.save(update_fields=['status', 'shipped_at'])
    return redirect('seller_orders')


@login_required
def orders(request):
    orders_list = (request.user.profile.orders
                   .prefetch_related('orderitem_set__item')
                   .order_by('-created_at'))
    data = {'title': 'My orders', 'menu': menu, 'orders': orders_list}
    return render(request, 'catalog/orders.html', data)

@login_required
def favorite_toggle(request, item_id):
    item = get_object_or_404(Catalog, pk=item_id)
    profile = request.user.profile
    if profile.favorites.filter(pk=item.pk).exists():
        profile.favorites.remove(item)
        messages.success(request, f'{item.title} removed from favorites')
    else:
        profile.favorites.add(item)
        messages.success(request, f'{item.title} added to favorites')
    return redirect('catalog_item_id', item_id=item_id)

@login_required
def favorites(request):
    items_list = request.user.profile.favorites.all()
    data = {'title': 'Favorites', 'menu': menu, 'items_list': items_list}
    return render(request, 'catalog/favorites.html', data)

@seller_required
def seller_cabinet(request):
    profile = request.user.profile
    stats = (OrderItem.objects
             .filter(item__seller=profile)
             .values('item_id', 'item__title')
             .annotate(total_qty=Sum('quantity'),
                       revenue=Sum(F('quantity') * F('price')))
             .order_by('-revenue'))
    pending = (OrderItem.objects
               .filter(item__seller=profile,
                       order__status__in=[Order.Status.ORDERED, Order.Status.SHIPPED])
               .aggregate(p=Sum(F('quantity') * F('price')))['p'] or 0)
    data = {
        'title': 'Seller cabinet',
        'menu': menu,
        'balance': profile.balance,
        'pending': pending,
        'stats': stats,
        'avg_rating': profile.review_received.aggregate(Avg('rating'))['rating__avg'],
        'reviews': profile.review_received.select_related('customer').order_by('-created_at'),
    }
    return render(request, 'catalog/seller_cabinet.html', data)

@seller_required
def seller_stock(request):
    items = (Catalog.objects
             .filter(seller=request.user.profile)
             .order_by('-created_at'))
    data = {'title': 'Seller stock', 'menu': menu, 'items': items}
    return render(request, 'catalog/seller_stock.html', data)

@seller_required
def stock_change(request, item_id):
    item = get_object_or_404(Catalog, pk=item_id)
    if item.seller_id != request.user.profile.id:
        return redirect('seller_stock')
    action = request.POST.get('action', 'inc')
    try:
        amount = int(request.POST.get('amount', 1))
    except (TypeError, ValueError):
        amount = 1
    amount = max(0, amount)
    delta = -amount if action == 'dec' else amount
    item.quantity = max(0, item.quantity + delta)
    if item.quantity == 0:
        item.is_available = Catalog.Status.ARCHIVED
    elif item.is_available != Catalog.Status.AVAILABLE:
        item.is_available = Catalog.Status.AVAILABLE
    item.save(update_fields=['quantity', 'is_available'])
    messages.success(request, f'{item.title}: quantity = {item.quantity}')
    return redirect('seller_stock')

@seller_required
def seller_orders(request):
    profile = request.user.profile
    orders_list = (Order.objects
                   .filter(orderitem__item__seller=profile)
                   .distinct()
                   .order_by('-created_at')
                   .prefetch_related('orderitem_set__item'))
    data = {'title': 'Seller orders', 'menu': menu, 'orders': orders_list, 'profile': profile}
    return render(request, 'catalog/seller_orders.html', data)