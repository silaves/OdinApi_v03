from django.core.exceptions import ValidationError
from django.conf import settings


def tamaño_del_archivo(value):
    MiB = settings.MAXIMO_TAM_ARCHIVOS
    limit = MiB * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo muy grande. No debe exceder los %s MiB.' % str(settings.MAXIMO_TAM_ARCHIVOS))