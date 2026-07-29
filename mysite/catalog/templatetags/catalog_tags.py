from django import template
from .. import views

from ..models import Category

register = template.Library()

@register.simple_tag()
def get_cats():
    return views.test_cats

@register.inclusion_tag('catalog/list_cats.html')
def show_cats():
    cats = Category.objects.all()
    return {'cats': cats}