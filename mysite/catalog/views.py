from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Catalog main page')

def category_by_id(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f'<h1>Categories</h1><p>cat id: {cat_id}<p/>')

def category_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f'<h1>Categories</h1><p>cat slug: {cat_slug}<p/>')

def archive(request: HttpRequest, year: int) -> HttpResponse:
    return HttpResponse(f'<h1>Archive</h1><p>Year: {year}<p/>')
