from decimal import Decimal
from rest_framework import serializers
from django.conf import settings
from apps.autenticacion.models import Usuario
from apps.autenticacion.models import Perfil, Usuario
from .models import Movil



class MovilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movil
        fields = ('placa','color','modelo','foto')

class PerfilSerializer(serializers.ModelSerializer):
    telefono = serializers.SerializerMethodField('getTelefono')
    calificacion = serializers.SerializerMethodField('getCalificacion')
    disponibilidad = serializers.SerializerMethodField('getDisponibilidad')
    movil = MovilSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ('id','username','email','nombres','apellidos','foto','perfil','telefono','calificacion','disponibilidad','movil')
    
    def getTelefono(self, usuario):
        try:
            telefono = Perfil.objects.get(pk=usuario.id).telefono
        except:
            telefono = ""
        return telefono
    
    def getCalificacion(self, usuario):
        try:
            calificacion = Perfil.objects.get(pk=usuario.id).calificacion
        except:
            calificacion = 0
        return calificacion
    
    def getDisponibilidad(self, usuario):
        try:
            disponibilidad = Perfil.objects.get(pk=usuario.id).disponibilidad
        except:
            disponibilidad = 0
        return disponibilidad