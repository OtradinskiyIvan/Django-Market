from django.contrib import admin
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
    path('login/', login, name='login'),
    path('add_item/', add_item, name='catalog_add_item'),
    path('contact_us/', contact_us, name='contact_us'),
    path('tag/<int:tag_id>/', tag_by_id, name='catalog_tag_id'),
    path('tag/<slug:tag_slug>/', tag_by_slug, name='catalog_tag_slug'),
]
