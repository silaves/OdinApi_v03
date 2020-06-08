from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_naive

from rest_framework import serializers

from apps.autenticacion.models import Ciudad
from apps.empresa.models import Producto, CategoriaProducto, FotoProducto, Empresa, Sucursal
from apps.empresa.serializers import ShowSucursal_Serializer

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
    fotos = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','atributos','categoria']



class ShowBasicArticulo_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'precio':instance.precio,
            'foto':instance.foto.url if instance.foto else None,
            'creado':make_naive(instance.creado)
        }




# VER ARTICULO

class ShowArticuloSucursal_Serializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'disponible':instance.disponible,
            'estado':instance.estado,
            'telefono':instance.telefono,
            'ubicacion':instance.ubicacion,
            'direccion':instance.direccion,
            'foto':instance.foto.url if instance.foto else None,
            'empresa':{
                'id':instance.empresa.id, 
                'nombre':instance.empresa.nombre,
                'descripcion':instance.empresa.descripcion,
                'empresario':instance.empresa.empresario.id,
            },
            'hora_inicio':instance.hora_inicio,
            'hora_fin':instance.hora_fin,
            'ciudad':{
                'id':instance.ciudad.id,
                'nombre':instance.ciudad.nombre
            }
        }

class ShowBasicFotoProductoArticulo_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'foto':instance.foto.url if instance.foto else None
        }

class ShowAdvancedArticulo_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'precio':instance.precio,
            'estado':instance.estado,
            'foto':instance.foto.url if instance.foto else None,
            'creado':make_naive(instance.creado),
            'atributos':instance.atributos,
            'sucursal':ShowArticuloSucursal_Serializer(instance.sucursal).data,
            'categoria':ShowCategoriaProducto_Serializer(instance.categoria).data,
            'fotos':ShowBasicFotoProductoArticulo_Serializer(FotoProducto.objects.filter(producto__id=instance.id), many=True).data,
        }





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


class ResponseBasicProducto(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['id','nombre','precio','foto','creado']



# response ver producto

class ResponseCiudad_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ['id','nombre','estado']

class ResponseArtEmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = ['id','nombre','descripcion','empresario']

class ResponseSucursalSerializer(serializers.ModelSerializer):
    empresa = ResponseArtEmpresaSerializer()
    ciudad = ResponseCiudad_Serializer()

    class Meta:
        model = Sucursal
        fields = ['id','nombre','disponible','estado','telefono','ubicacion','direccion','foto','empresa','hora_inicio','hora_fin','ciudad']

class ResponseFotoProducto(serializers.ModelSerializer):
    class Meta:
        model = FotoProducto
        fields = ['id','foto']


class ResponseBasicProducto(serializers.ModelSerializer):
    categoria = ResponseCategoriaProducto()
    sucursal = ResponseSucursalSerializer()
    fotos = ResponseFotoProducto(many=True)

    class Meta:
        model = Producto
        fields = ['id','descripcion','nombre','precio','foto','creado','atributos','sucursal','categoria','fotos']