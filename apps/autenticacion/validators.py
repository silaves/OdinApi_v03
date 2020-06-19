import json
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings


def tamaño_del_archivo(value):
    MiB = settings.MAXIMO_TAM_ARCHIVOS
    limit = MiB * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo muy grande. No debe exceder los %s MiB.' % str(settings.MAXIMO_TAM_ARCHIVOS))

def validar_porcentaje(value):
    if value.compare(Decimal('0')) == -1 :
        raise ValidationError('El valor no puede ser negativo')
    if value.compare(Decimal('100')) == 1:
        raise ValidationError('El valor no debe ser mayor a 100')


def validar_telefono(value):
    if len(str(value)) != 8:
        raise ValidationError('Formato de numero de telefono incorrecto')