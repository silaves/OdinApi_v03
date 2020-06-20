import math
from decimal import Decimal
from operator import itemgetter

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
            sucu['distancia'] = km
            _sucursal.append(sucu)
        else:
            pass
    return sorted(_sucursal, key=itemgetter('distancia'), reverse=False)
        

def _get_values_ubicacion(ubicacion):
    values = []
    val = ubicacion[:-1].split(',')
    values.append( float( val[0].split(':')[1] ) )
    values.append( float( val[1].split(':')[1] ) )
    return values