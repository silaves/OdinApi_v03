from django.apps import AppConfig


class EmpresaConfig(AppConfig):
    name = 'apps.empresa'
    verbose_name = "Comida rapida - E-commerce"

    # def ready(self):
    #     # everytime server restarts
    #     import apps.empresa.signals