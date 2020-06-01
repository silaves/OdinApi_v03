from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.empresa.models import Producto, CategoriaProducto

# class atributo(serializer.Serializer):


class Test_Serializer(serializers.ModelSerializer):
    data = serializers.JSONField(source='atributos',required=True)

    class Meta:
        model = Producto
        fields = ['nombre','precio','sucursal','data']

    #  def validate(self, data):
    #     sr = attrs.get('data')
    #     if config_field:
    #         serializer = ConfigFieldsSerializer(data=config_field)
    #         serializer.is_valid(raise_exception=True)
    #     return data

class ShowCategoriaProducto_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'codigo':instance.codigo
        }


class ShowCategoriaProductoNivel_Serializer(serializers.Serializer):

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
            'codigo':instance.codigo,
            'sub_categorias': ShowCategoriaNivel_Serializer( query, many=True, context={'estado':estado} ).data
        }





class CrearArticulo_Serializer(serializers.ModelSerializer):
    fotos = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','sucursal','categoria','atributos','fotos']
        extra_kwargs = {
            'categoria': {'required': True}
        }

    def validate_fotos(self, obj):
        for f in obj:
            MiB = settings.MAXIMO_TAM_ARCHIVOS
            limit = MiB * 1024 * 1024
            if f.size > limit:
                raise serializers.ValidationError('La imagen '+str(f)+' no debe exceder los '+str(MiB)+'Mb')
        return obj




class EditarArticulo_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','atributos']









# RESPONSES FOR SWAGGER



class ResponseCategoriaProductoNivel2(serializers.ModelSerializer):
    sub_categorias = serializers.ListField()

    class Meta:
        model = CategoriaProducto
        fields = ['id','nombre','codigo','sub_categorias']
    

class ResponseCategoriaProductoNivel(serializers.ModelSerializer):
    sub_categorias = ResponseCategoriaProductoNivel2(source='padre', read_only=True)

    class Meta:
        model = CategoriaProducto
        fields = ['id','nombre','codigo','sub_categorias']


class ResponseCategoriaProducto(serializers.ModelSerializer):

    class Meta:
        model = CategoriaProducto
        fields = ['id','nombre','codigo']