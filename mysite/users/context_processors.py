from django.http import HttpRequest

from catalog.utils import menu
from users.models import Profile


def get_catalog_context(request: HttpRequest):
    cart = request.session.get('cart', {})
    is_seller = (
        request.user.is_authenticated
        and request.user.profile.role == Profile.Role.SELLER
    )
    return {'menu': menu, 'cart_count': sum(cart.values()), 'is_seller': is_seller}
