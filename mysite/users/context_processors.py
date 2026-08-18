from django.http import HttpRequest

from catalog.utils import menu


def get_catalog_context(request: HttpRequest):
    cart = request.session.get('cart', {})
    return {'menu': menu, 'cart_count': sum(cart.values())}
