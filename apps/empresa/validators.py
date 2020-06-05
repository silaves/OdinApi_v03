import json
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings


def tamaño_del_archivo(value):
    MiB = settings.MAXIMO_TAM_ARCHIVOS
    limit = MiB * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo muy grande. No debe exceder los %s MiB.' % str(settings.MAXIMO_TAM_ARCHIVOS))

def cantidad_min_value(value):
    if value < 1:
        raise ValidationError('La cantidad minima es de 1')

def cantidad_max_value(value):
    if value > 100:
        raise ValidationError('La cantidad maxima es de 100')

def validate_latitude_longitude(value):
    if value[0] == '{' and value[len(value)-1] == '}':  
        try:
            val = value[:-1].split(',')
            v1 = val[0].split(':')[1]
            v2 = val[1].split(':')[1]
        except:
            raise ValidationError('Formato incorrecto de ubicacion')
    else:
        raise ValidationError('Formato incorrecto de ubicacion')
    # val = value.split(',')
    try:
        latitude = Decimal(v1)
        longitude = Decimal(v2)
    except:
        raise ValidationError('Formato incorrecto de ubicacion')

    if latitude.compare(Decimal(-90.0)) == Decimal(-1):
        raise ValidationError('Latitud incorrecta')
    elif latitude.compare(Decimal(90.0)) == Decimal(1):
        raise ValidationError('Latitud incorrecta')
    if longitude.compare(Decimal(-180.0)) == -1:
        raise ValidationError('Longitud incorrecta')
    elif longitude.compare(Decimal(180.0)) == 1:
        raise ValidationError('Longitud incorrecta')