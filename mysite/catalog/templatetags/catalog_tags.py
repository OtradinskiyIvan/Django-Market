from functools import lru_cache
from pathlib import Path

from django import template
from .. import views

from ..models import Category, Tag

register = template.Library()

ICONS_DIR = Path(__file__).resolve().parent.parent / 'static' / 'catalog' / 'img' / 'imgs'


@lru_cache(maxsize=None)
def _load_svg(filename):
    path = ICONS_DIR / filename
    if not path.is_file():
        return None
    return path.read_text(encoding='utf-8')


def _with_class(svg, extra_class):
    if 'class="' in svg:
        return svg.replace('class="', f'class="{extra_class} ', 1)
    return svg.replace('<svg', f'<svg class="{extra_class}"', 1)


@register.inclusion_tag('catalog/icon.html')
def icon(name, filled=False):
    svg = _load_svg(f'{name}-fill.svg') if filled else None
    if svg is None:
        svg = _load_svg(f'{name}.svg')
    return {'svg': _with_class(svg, 'icon') if svg else ''}

@register.simple_tag()
def get_cats():
    return views.test_cats

@register.inclusion_tag('catalog/list_cats.html', takes_context=True)
def show_cats(context):
    return {'cats': Category.objects.all(), 'active_cat': context.get('current_cat')}

@register.inclusion_tag('catalog/list_tags.html', takes_context=True)
def show_tags(context):
    request = context['request']
    selected = {int(v) for v in request.GET.getlist('tags') if v.isdigit()}
    return {'tags': Tag.objects.all(), 'selected': selected}