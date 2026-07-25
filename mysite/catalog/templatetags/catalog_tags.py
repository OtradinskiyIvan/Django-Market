from django import template
from .. import views

register = template.Library()

@register.simple_tag()
def get_cats():
    return views.test_cats

@register.inclusion_tag('catalog/list_cats.html')
def show_cats():
    cats = views.test_cats
    return {'cats': cats}