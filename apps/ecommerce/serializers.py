from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_naive
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from rest_framework import serializers

from apps.autenticacion.models import Ciudad
from apps.empresa.models import Producto, CategoriaProducto, FotoProducto, Empresa, Sucursal
# from apps.empresa.serializers import ShowSucursal_Serializer

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
            query = CategoriaProducto.objects.filter(padre__id=instance.id, estado=True)
        elif estado == 'I':
            query = CategoriaProducto.objects.filter(padre__id=instance.id, estado=False)
        else:
            query = CategoriaProducto.objects.filter(padre__id=instance.id)

        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'codigo':instance.codigo,
            'sub_categorias': ShowCategoriaProductoNivel_Serializer( query, many=True, context={'estado':estado} ).data
        }


# SUCURSAL

class ShowSucursal_Serializer(serializers.Serializer):

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
            'foto_150':thumbnail_url(instance.foto, '150'),
            'foto_300':thumbnail_url(instance.foto, '300'),
            'foto_450':thumbnail_url(instance.foto, '450'),
            # 'foto':self.context.get('request').build_absolute_uri(instance.foto.url) if instance.foto else None,
            'empresa':{
                'id':instance.empresa.id, 
                'nombre':instance.empresa.nombre,
                'descripcion':instance.empresa.descripcion,
                'categoria':{
                    'id':instance.empresa.categoria.id,
                    'nombre':instance.empresa.categoria.nombre,
                    'estado':instance.empresa.categoria.estado
                }
            },
            'hora_inicio':instance.hora_inicio,
            'hora_fin':instance.hora_fin,
            'ciudad':{
                'id':instance.ciudad.id,
                'nombre':instance.ciudad.nombre,
                'estado':instance.ciudad.estado,
                'comision_porcentaje':str(instance.ciudad.comision_porcentaje)
            }
        }


# ARTICULOS
def validar_categoria(categoria, tipo):
    c = categoria.padre
    es = False
    while c is not None:
        if c.nombre == tipo:
            es = True
            break
        else:
            c = c.padre
    return es


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
    
    def validate_categoria(self, value):
        if value.padre is None:
            raise serializers.ValidationError('La categoria debe tener un padre')
        if value.estado is False:
            raise serializers.ValidationError('La categoria esta inactiva')
        if not validar_categoria(value, settings._ECOMMERCE_):
            raise serializers.ValidationError('La categoria no pertenece a ecommerce')
        return value




class EditarArticulo_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','atributos','categoria','foto']
    
    def validate_categoria(self, value):
        if value.padre is None:
            raise serializers.ValidationError('La categoria debe tener un padre')
        if value.estado is False:
            raise serializers.ValidationError('La categoria esta inactiva')
        if not validar_categoria(value, settings._ECOMMERCE_):
            raise serializers.ValidationError('La categoria no pertenece a ecommerce')
        return value



class ShowBasicArticulo_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'precio':str(instance.precio),
            'foto':instance.foto.url if instance.foto else None,
            'foto_150':thumbnail_url(instance.foto, '150'),
            'foto_300':thumbnail_url(instance.foto, '300'),
            'foto_450':thumbnail_url(instance.foto, '450'),
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
            'precio':str(instance.precio),
            'estado':instance.estado,
            'foto':instance.foto.url if instance.foto else None,
            'foto_150':thumbnail_url(instance.foto, '150'),
            'foto_300':thumbnail_url(instance.foto, '300'),
            'foto_450':thumbnail_url(instance.foto, '450'),
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