from django.http import HttpRequest

from catalog.utils import menu


def get_catalog_context(request: HttpRequest):
    return {'menu': menu}