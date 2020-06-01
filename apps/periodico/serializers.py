from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_naive

from rest_framework import serializers

from apps.empresa.models import Empresa
from .models import *

class ShowCategoria_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'nivel':instance.nivel,
            # 'estado':instance.categoria.estado
        }


class ShowCategoriaNivel_Serializer(serializers.Serializer):

    def to_representation(self, instance):
        estado = self.context.get('estado')
        if estado == 'A':
            query = CategoriaNoticia.objects.filter(padre__id=instance.id, estado=True)
        elif estado == 'I':
            query = CategoriaNoticia.objects.filter(padre__id=instance.id, estado=False)
        else:
            query = CategoriaNoticia.objects.filter(padre__id=instance.id)

        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'nivel':instance.nivel,
            'sub_categorias': ShowCategoriaNivel_Serializer( query, many=True, context={'estado':estado} ).data
        }


class ShowFotoNoticia_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'foto':instance.foto.url if instance.foto else None,
            'descripcion':instance.descripcion,
            'autor':instance.autor,
            'localidad':instance.localidad
        }


class ShowVerNoticia_Serializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'titulo':instance.titulo,
            'sub_titulo':instance.sub_titulo,
            'descripcion':instance.descripcion,
            'link_fuente':instance.link_fuente,
            'localidad':instance.localidad,
            'creado':make_naive(instance.creado),
            'estado':instance.estado,
            'empresa':{
                'id':instance.empresa.id, 
                'nombre':instance.empresa.nombre
            },
            'categoria':ShowCategoria_Serializer( instance.categoria.all(),many=True ).data,
            'foto': ShowFotoNoticia_Serializer( FotoNoticia.objects.filter(noticia__id=instance.id), many=True ).data
        }

class ShowNoticias_Serializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'titulo':instance.titulo,
            'sub_titulo':instance.sub_titulo,
            # 'descripcion':instance.descripcion,
            # 'link_fuente':instance.link_fuente,
            'localidad':instance.localidad,
            'creado':make_naive(instance.creado),
            # 'estado':instance.estado,
            # 'foto':instance.foto.url if instance.foto else None,
            # 'foto':self.context.get('request').build_absolute_uri(instance.foto.url) if instance.foto else None,
            'empresa':{
                'id':instance.empresa.id, 
                'nombre':instance.empresa.nombre
            },
            # 'categoria':{
            #     'id':instance.categoria.id,
            #     'nombre':instance.categoria.nombre,
            #     # 'nivel':instance.categoria.nivel,
            #     # 'estado':instance.categoria.estado
            # },
            'foto':FotoNoticia.objects.filter(noticia__id=instance.id).first().foto.url if FotoNoticia.objects.filter(noticia__id=instance.id).exists() else None
        }















# RESPONSES FOR SWAGGER

class ResponseEmpresa(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id','nombre']

class ResponseCate(serializers.ModelSerializer):
    class Meta:
        model = CategoriaNoticia
        fields = ['id','nombre','nivel']
        
class ResponseFotoNoticia(serializers.ModelSerializer):
    class Meta:
        model = FotoNoticia
        fields = ['id','foto','descripcion','autor','localidad']

class ResponseNoticia(serializers.ModelSerializer):
    # foto = serializers.ImageField(read_only=True)
    empresa = ResponseEmpresa(read_only=True)
    categoria = ResponseCate(many=True,read_only=True)
    foto = ResponseFotoNoticia(many=True,source='fotonoticia_set')

    class Meta:
        model = Noticia
        fields = ['id','titulo','sub_titulo','descripcion','link_fuente','localidad','creado','estado','empresa','categoria','foto']








class ReponseNoticiaList(serializers.ModelSerializer):
    foto = serializers.ImageField(read_only=True)
    empresa = serializers.SerializerMethodField('cargar_empresa', read_only=True)

    class Meta:
        model = Noticia
        fields = ['id','titulo','sub_titulo','localidad','creado','empresa','foto']
    
    def cargar_empresa(self, obj):
        return {
            'id':obj.empresa.id,
            'nombre':obj.empresa.nombre
        }


class ReponseNoticiaList(serializers.ModelSerializer):
    foto = serializers.ImageField(read_only=True)
    empresa = serializers.SerializerMethodField('cargar_empresa', read_only=True)

    class Meta:
        model = Noticia
        fields = ['id','titulo','sub_titulo','localidad','creado','empresa','foto']
    
    def cargar_empresa(self, obj):
        return {
            'id':obj.empresa.id,
            'nombre':obj.empresa.nombre
        }





class ResponseCategoriaNivel2(serializers.ModelSerializer):
    sub_categorias = serializers.ListField()

    class Meta:
        model = CategoriaNoticia
        fields = ['id','nombre','nivel','sub_categorias']
    

class ResponseCategoriaNivel(serializers.ModelSerializer):
    sub_categorias = ResponseCategoriaNivel2(source='padre', read_only=True)

    class Meta:
        model = CategoriaNoticia
        fields = ['id','nombre','nivel','sub_categorias']


class ResponseCategoria(serializers.ModelSerializer):

    class Meta:
        model = CategoriaNoticia
        fields = ['id','nombre','nivel']
    