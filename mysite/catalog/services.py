from collections import defaultdict

from django.db import transaction
from django.utils import timezone

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
        for item, qty in locked:
            OrderItem.objects.create(order=order, item=item, quantity=qty, price=item.price)
            item.quantity -= qty
            if item.quantity == 0:
                item.is_available = Catalog.Status.ARCHIVED
            item.save()

        profile.balance -= total
        profile.save()
    return order


def accept_order(order):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(pk=order.pk)
        if order.status != Order.Status.SHIPPED:
            return
        seller_totals = defaultdict(int)
        for oi in order.orderitem_set.select_related('item'):
            seller_totals[oi.item.seller_id] += oi.price * oi.quantity
        for seller in Profile.objects.select_for_update().filter(pk__in=seller_totals):
            seller.balance += seller_totals[seller.pk]
            seller.save()
        order.status = Order.Status.ACCEPTED
        order.closed_at = timezone.now()
        order.save(update_fields=['status', 'closed_at'])


def decline_order(order):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(pk=order.pk)
        if order.status not in (Order.Status.ORDERED, Order.Status.SHIPPED):
            return
        buyer = Profile.objects.select_for_update().get(pk=order.user_id)
        buyer.balance += order.total
        buyer.save()
        for oi in order.orderitem_set.all():
            item = Catalog.objects.select_for_update().get(pk=oi.item_id)
            item.quantity += oi.quantity
            if item.is_available != Catalog.Status.AVAILABLE:
                item.is_available = Catalog.Status.AVAILABLE
            item.save()
        order.status = Order.Status.DECLINED
        order.save(update_fields=['status'])

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
