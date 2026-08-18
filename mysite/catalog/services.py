from collections import defaultdict

from django.db import transaction

from users.models import Profile
from .models import *


def create_order(profile, items):
    with transaction.atomic():
        profile = Profile.objects.select_for_update().get(pk=profile.pk)
        locked = []
        
        for item, qty in items:
            item = Catalog.objects.select_for_update().get(pk=item.pk)
            if item.seller_id == profile.id:
                raise ValueError(f'Cannot buy your own item: {item.title}')
            if qty > item.quantity:
                raise ValueError(f'Not enough stock for {item.title}')
            if item.is_available != Catalog.Status.AVAILABLE:
                raise ValueError(f'Item is not available: {item.title}')
            locked.append((item, qty))
            
        total = sum(it.price * q for it, q in locked)
        if total > profile.balance:
            raise ValueError('Not enough balance')
        
        order = Order.objects.create(user=profile)
        seller_totals = defaultdict(int)
        for item, qty in locked:
            OrderItem.objects.create(order=order, item=item, quantity=qty, price=item.price)
            item.quantity -= qty
            if item.quantity == 0:
                item.is_available = Catalog.Status.ARCHIVED
            item.save()
            seller_totals[item.seller_id] += item.price * qty

        profile.balance -= total
        profile.save()

        for seller in Profile.objects.select_for_update().filter(pk__in=seller_totals):
            seller.balance += seller_totals[seller.pk]
            seller.save()
    return order

def get_cart(request):
    return request.session.get('cart', {})

def add_to_cart(request, item_id, qty):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = qty
    request.session['cart'] = cart

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart

def clear_cart(request):
    request.session.pop('cart', None)

def cart_lines(request):
    cart = get_cart(request)
    lines = []
    total = 0
    for pk, qty in cart.items():
        item = Catalog.objects.filter(pk=int(pk)).first()
        if not item:
            continue
        lines.append((item, qty, item.price * qty))
        total += item.price * qty
    return lines, total
