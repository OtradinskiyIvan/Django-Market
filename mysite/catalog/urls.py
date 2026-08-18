from django.urls import path, register_converter
from .views import *
from .converters import YearConverter

register_converter(YearConverter, 'year_conv')

urlpatterns = [
    path('', index, name='catalog_main'),
    path('about_us/', about_us, name='about_us'),
    path('cats/<int:cat_id>/', category_by_id, name='catalog_cat_id'),
    path('cats/<slug:cat_slug>/', category_by_slug, name='catalog_cat_slug'),
    path('archive/<year_conv:year>/', archive, name='catalog_archive'),
    path('item/<int:item_id>/', item_by_id, name='catalog_item_id'),
    path('item/<slug:item_slug>/', item_by_slug, name='catalog_item_slug'),
    path('add_item/', add_item, name='catalog_add_item'),
    path('contact_us/', contact_us, name='contact_us'),
    path('tag/<int:tag_id>/', tag_by_id, name='catalog_tag_id'),
    path('tag/<slug:tag_slug>/', tag_by_slug, name='catalog_tag_slug'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:item_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', cart_remove, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', orders, name='orders'),
    path('orders/accept/<int:order_id>/', order_accept, name='order_accept'),
    path('orders/decline/<int:order_id>/', order_decline, name='order_decline'),
    path('favorites/', favorites, name='favorites'),
    path('favorites/toggle/<int:item_id>/', favorite_toggle, name='favorite_toggle'),
    path('seller/cabinet/', seller_cabinet, name='seller_cabinet'),
    path('seller/stock/', seller_stock, name='seller_stock'),
    path('seller/stock/<int:item_id>/', stock_change, name='stock_change'),
    path('seller/orders/', seller_orders, name='seller_orders'),
    path('seller/orders/ship/<int:order_id>/', order_ship, name='order_ship'),
]
