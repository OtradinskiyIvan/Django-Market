from django.contrib import admin
from django.urls import path, register_converter
from .views import index, category_by_id, category_by_slug, archive, about_us
from .converters import YearConverter

register_converter(YearConverter, 'year_conv')

urlpatterns = [
    path('', index, name='catalog_main'),
    path('about_us/', about_us, name='about_us'),
    path('cats/<int:cat_id>/', category_by_id, name='catalog_cat_id'),
    path('cats/<slug:cat_slug>/', category_by_slug, name='catalog_cat_slug'),
    path('archive/<year_conv:year>/', archive, name='catalog_archive'),
]
