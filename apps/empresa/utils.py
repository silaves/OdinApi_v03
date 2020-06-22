import json
import math
import requests
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP,ROUND_UP,ROUND_DOWN
from operator import itemgetter
from apps.autenticacion.models import Ciudad,TarifaCostoEnvio


def haversine(lat1, lon1, lat2, lon2):
    # calcular distancia entre puntos latitud longitud
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
    # convertir a radianes
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
  
    # aplicar formula
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    # radio de la tierra (6371 km)
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


def calcular_distancia(lat1, long1, lat2, long2):
    return haversine(lat1, long1, lat2, long2)

def calcular_sucursal_distances(sucursales, ubicacion):
    _sucursal = []
    _uvalues = _get_values_ubicacion(ubicacion)
    u1 = _uvalues[0]
    u2 = _uvalues[1]
    for sucu in sucursales:
        if sucu['ubicacion']:
            _suvalues = _get_values_ubicacion( str(sucu['ubicacion']) )
            p1 = _suvalues[0]
            p2 = _suvalues[1]
            km = calcular_distancia(u1, u2, p1, p2)
            # sucu['distancia'] = Decimal(km).quantize(Decimal('0.00001'),ROUND_HALF_UP)
            sucu['distancia'] = ( Decimal(km)*1000 ).quantize(Decimal('0.01'),ROUND_HALF_UP)
            _sucursal.append(sucu)
        else:
            pass
    return sorted(_sucursal, key=itemgetter('distancia'), reverse=False)
    # return _sucursal
        

def _get_values_ubicacion(ubicacion):
    values = []
    val = ubicacion[:-1].split(',')
    values.append( float( val[0].split(':')[1] ) )
    values.append( float( val[1].split(':')[1] ) )
    return values


# calcular precio delivery
# def asd(kmp):
    
    
#     ciudad = Ciudad.objects.get(pk=1)
#     min_tarifa = ciudad.costo_min
#     query = TarifaCostoEnvio.objects.filter(ciudad__id=1, estado=True).order_by('-km_inicial')
#     if query.count() <= 0:
#         return None
#     cont = query.count()
#     _next = -1
#     result = Decimal(0)
#     for x in query:
#         if kmp >= x.km_inicial:
#             result = kmp*x.costo
#             if _next > 0:
#                 if result > _next:
#                     result = _next
#                 if result < min_tarifa:
#                     result = min_tarifa
#             break
#         _next = x.km_inicial*x.costo
#     # result = result.quantize(Decimal('0.1'),ROUND_UP)
#     result = result.quantize(Decimal('0.00'),ROUND_DOWN)
#     return result

# calcular precio del delivery

def calculate_distance(origin, destination):
    url = settings.URL_MATRIX
    key = settings.API_KEY_MATRIX
    result = requests.get(url + 'units=metric&origins='+origin+'&destinations='+destination+'&key='+key)
    if result:
        pass
    else:
        return Decimal(0)
    js = result.json()
    # if js['status'] != 'OK':
    #     return Decimal(0)
    try:
        metros = js['rows'][0]['elements'][0]['distance']['value']
    except:
        return Decimal(0)
    return Decimal(metros/1000)

def _converter(value):
    val = value[:-1].split(',')
    v1 = val[0].split(':')[1]
    v2 = val[1].split(':')[1]
    return v1+','+v2

def calcular_tarifa(origin, destination, ciudad):
    kmt = calculate_distance(_converter(origin), _converter(destination))
    result = ciudad.costo_min
    query = TarifaCostoEnvio.objects.filter(ciudad=ciudad, estado=True).order_by('-km_inicial')
    for c in query:
        if kmt >= c.km_inicial:
            result += (kmt-c.km_inicial) * c.costo
            kmt -= kmt-c.km_inicial
    return result.quantize(Decimal('0'),ROUND_DOWN)
