from django.apps import AppConfig
from .utils import ensure_bucket

class CatalogConfig(AppConfig):
    name = 'catalog'

    def ready(self):
        try:
            ensure_bucket()
        except Exception:
            pass
