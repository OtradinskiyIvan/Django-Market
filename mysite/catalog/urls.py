from django.contrib import admin
from django.urls import path, register_converter
from .views import index, category_by_id, category_by_slug, archive
from .converters import YearConverter

register_converter(YearConverter, 'year_conv')

urlpatterns = [
    path('', index),
    path('cats/<int:cat_id>/', category_by_id),
    path('cats/<slug:cat_slug>/', category_by_slug),
    path('archive/<year_conv:year>/', archive),
]
