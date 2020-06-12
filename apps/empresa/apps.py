from django.conf import settings
from django.apps import AppConfig


class EmpresaConfig(AppConfig):
    name = 'apps.empresa'
    verbose_name = "Comida rapida - E-commerce"

    def ready(self):
        if settings.SCHEDULER_AUTOSTART is True:
            from . import scheduler