import re
import json
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_naive

from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from apps.autenticacion.models import Usuario, Ciudad, Horario
from apps.autenticacion.serializers import PerfilSerializer, VerCiudad_Serializer
from .models import Empresa, Sucursal, Combo, Producto, CategoriaEmpresa, Pedido, PedidoProducto,CategoriaProducto


class CategoriaEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEmpresa
        fields = ['id','nombre','estado']


class EmpresaSerializer(serializers.ModelSerializer):
    categoria = CategoriaEmpresaSerializer()
    
    class Meta:
        model = Empresa
        fields = ['id','nombre','descripcion','empresario','categoria']
    
    def create(self, validate_data):
        return Empresa.objects.create(**validate_data)
    
    def validate_nombre(self, value):
        if len(value) > 40:
            raise forms.ValidationError('El nombre es muy largo')
        return value
    
    def validate_descripcion(self, value):
        if len(value) > 500:
            raise forms.ValidationError('la descripcion es muy larga')
        return value


class EmpresaEditarSerializer(serializers.ModelSerializer):
    categoria = CategoriaEmpresaSerializer(read_only=True)
    
    class Meta:
        model = Empresa
        fields = ['id','nombre','descripcion','categoria']
    
    def validate_nombre(self, value):
        if len(value) > 40:
            raise forms.ValidationError('El nombre es muy largo')
        return value
    
    def validate_descripcion(self, value):
        if len(value) > 500:
            raise forms.ValidationError('la descripcion es muy larga')
        return value




# sucursales

class CrearSucursal_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Sucursal
        fields = ['id','nombre','disponible','estado','telefono','ubicacion','direccion','foto','empresa','hora_inicio','hora_fin','ciudad','categoria']   


class SucursalEditarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['nombre','telefono','ubicacion','direccion','foto','hora_inicio','hora_fin','estado','ciudad','categoria']

class VerCategoria_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = ['id','nombre','codigo','estado']

class Ubicacion_Serializer(serializers.Serializer):
    ubicacion = serializers.CharField(max_length=255, required=True)

    def validate_ubicacion(self, value):
        if value[0] == '{' and value[len(value)-1] == '}':  
            try:
                val = value[:-1].split(',')
                v1 = val[0].split(':')[1]
                v2 = val[1].split(':')[1]
            except:
                raise serializers.ValidationError('Formato incorrecto de ubicacion')
        else:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        try:
            latitude = Decimal(v1)
            longitude = Decimal(v2)
        except:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        return value

class SucursalSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    ciudad = VerCiudad_Serializer()
    categoria = VerCategoria_Serializer()
    foto_150 = serializers.SerializerMethodField()
    foto_300 = serializers.SerializerMethodField()
    foto_450 = serializers.SerializerMethodField()

    class Meta:
        model = Sucursal
        fields = ['id','nombre','disponible','estado','telefono','ubicacion','direccion','foto','empresa','hora_inicio','hora_fin','ciudad',
            'calificacion','categoria','foto_150','foto_300','foto_450']
    
    def get_foto_150(self, obj):
        return thumbnail_url(obj.foto, '150')
    
    def get_foto_300(self, obj):
        return thumbnail_url(obj.foto, '300')
    
    def get_foto_450(self, obj):
        return thumbnail_url(obj.foto, '450')


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
            'calificacion':str(instance.calificacion.normalize()),
            'cant_calificacion':instance.cant_calificacion,
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
            },
            'categoria':{
                'id':instance.categoria.id,
                'nombre':instance.categoria.nombre,
                'codigo':instance.categoria.codigo
            }
        }


class CambiarDisponibleSucursal_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['disponible']


class ResponseTokenFirebase(serializers.Serializer):
    token_firebase = serializers.CharField(max_length=255, read_only=True)





# PRODUCTO

# para crear producto
class ProductoSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Producto
        fields = ['id','nombre','descripcion','precio','sucursal','foto','categoria']
    
    def validate_categoria(self, value):
        if value.padre is None:
            raise serializers.ValidationError('La categoria debe tener un padre')
        if value.estado is False:
            raise serializers.ValidationError('La categoria esta inactiva')
        # if not validar_categoria(value, settings._COMIDA_):
        #     raise serializers.ValidationError('La categoria no pertenece a comida')
        return value
        
    # def create(self, validate_data):
    #     return Producto.objects.create(**validate_data)

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

class ProductoEditarSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','estado','foto','categoria']
    
    def validate_categoria(self, value):
        if value.padre is None:
            raise serializers.ValidationError('La categoria debe tener un padre')
        if value.estado is False:
            raise serializers.ValidationError('La categoria esta inactiva')
        # if not validar_categoria(value, settings._COMIDA_):
        #     raise serializers.ValidationError('La categoria no pertenece a comida')
        return value



class ShowProductoBasicHijo_Serializer(serializers.Serializer): # revisar
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'precio':str(instance.precio),
            'estado':instance.estado,
            'sucursal':instance.sucursal.id,
            'foto':instance.foto.url if instance.foto else None,
            'dias_activos':instance.dias_activos,
            # 'foto':self.context.get('request').build_absolute_uri(instance.foto.url) if instance.foto else None,
            'cantidad':Combo.objects.filter(combo__id=self.context.get('padre'),producto__id=instance.id).values('cantidad')[0]['cantidad']
        }

class ShowCategoriaProducto_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'codigo':instance.codigo
        }

class ShowProductoBasic_Serializer(serializers.Serializer): # revisar
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'precio':str(instance.precio),
            'estado':instance.estado,
            'sucursal':instance.sucursal.id,
            'foto':instance.foto.url if instance.foto else None,
            'foto_150':thumbnail_url(instance.foto, '150'),
            'foto_300':thumbnail_url(instance.foto, '300'),
            'foto_450':thumbnail_url(instance.foto, '450'),
            # 'foto':self.context.get('request').build_absolute_uri(instance.foto.url) if instance.foto else None,
            'is_combo':instance.is_combo,
            'calificacion':str(instance.calificacion.normalize()),
            'cant_calificacion':instance.cant_calificacion,
            'is_calificado':self.context.get('is_calificado'),
            'dias_activos':instance.dias_activos,
            'categoria':ShowCategoriaProducto_Serializer(instance.categoria).data,
            'combo':ShowProductoBasicHijo_Serializer( Producto.objects.select_related('sucursal','sucursal__empresa').filter(id__in=Combo.objects.filter(combo_id=instance.id).values('producto')),
            many=True,context={'request':self.context.get('request'),'padre':instance.id} ).data if instance.is_combo is True else False
        }


# ver combo
class VerProductoSerializer(serializers.ModelSerializer): # revisar
    foto = serializers.ImageField(max_length=None, use_url=True)
    combo = serializers.SerializerMethodField('cargar_pro')

    class Meta:
        model = Producto
        fields = ['id','nombre','descripcion','precio','estado','sucursal','foto','is_combo','combo']
    
    def cargar_pro(self, obj):
        if obj.id:
            if obj.is_combo is True:
                pros = Producto.objects.select_related('sucursal','empresa')
                return ShowProducto_Serializer()
            # pros = Producto.objects.filter(id__in=Combo.objects.filter(combo_id=obj.id).values('producto'))
            # if len(pros) > 0:
            #     return ProSerializer(pros, many=True).data
            # else:
            #     return False
        else:
            return None


class ShowProductoAdvanced_Serializer(serializers.Serializer): # revisar
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'precio':str(instance.precio),
            'estado':instance.estado,
            # 'creado':instance.creado,
            'sucursal':{
                'id':instance.sucursal.id,
                'nombre':instance.sucursal.nombre,
                'disponible':instance.sucursal.disponible,
                'estado':instance.sucursal.estado,
                'telefono':instance.sucursal.telefono,
                'ubicacion':instance.sucursal.ubicacion,
                'direccion':instance.sucursal.direccion,
                'foto':instance.sucursal.foto.url if instance.sucursal.foto else None,
                # 'foto':self.context.get('request').build_absolute_uri(instance.sucursal.foto.url) if instance.sucursal.foto else None,
                'empresa':{
                    'id':instance.sucursal.empresa.id, 
                    'nombre':instance.sucursal.empresa.nombre,
                    'descripcion':instance.sucursal.empresa.descripcion
                    },
                'hora_inicio':instance.sucursal.hora_inicio,
                'hora_fin':instance.sucursal.hora_fin
                # 'ciudad':{
                #     'id':instance.sucursal.ciudad.id,
                #     'nombre':instance.sucursal.ciudad.nombre,
                #     'estado':instance.sucursal.ciudad.estado
                # }
            },
            'categoria':ShowCategoriaProducto_Serializer(instance.categoria).data,
            'foto':instance.foto.url if instance.foto else None,
            'foto_150':thumbnail_url(instance.foto, '150'),
            'foto_300':thumbnail_url(instance.foto, '300'),
            'foto_450':thumbnail_url(instance.foto, '450'),
            # 'foto':self.context.get('request').build_absolute_uri(instance.foto.url) if instance.foto else None,
            'is_combo':instance.is_combo,
            'calificacion':str(instance.calificacion.normalize()),
            'dias_activos':instance.dias_activos,
            # 'combo':ShowProducto_Serializer( Producto.objects.select_related('sucursal','sucursal__empresa').filter(id__in=Combo.objects.filter(combo_id=obj.id).values('producto')), many=True ).data if instance.is_combo is True else False
        }


# class ProductoVerSerializer(serializers.ModelSerializer):
#     foto = serializers.ImageField(max_length=None, use_url=True)

#     class Meta:
#         model = Producto
#         fields = ['id','nombre','descripcion','precio','estado','sucursal','foto']

class ShowProductoMedio_Serializer(serializers.Serializer):
    
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'precio':str(instance.precio),
            'estado':instance.estado,
            'sucursal':instance.sucursal.id,
            'foto':instance.foto.url if instance.foto else None,
            # 'foto':self.context.get('request').build_absolute_uri(instance.sucursal.foto.url) if instance.sucursal.foto else None,
            'is_combo':instance.is_combo,
            'calificacion':str(instance.calificacion.normalize()),
            'dias_activos':instance.dias_activos
        }




# Combo


#crear combo

class CrearComboSerializer(serializers.ModelSerializer):
    combo = serializers.RegexField('^(\d{1,8}[-]\d{1,2}[&]){0,}?$',max_length=255, required=False)

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','sucursal','foto','combo','dias_activos','categoria']
        
    def validate(self, data):
        index = 0
        ides = []
        try:
            combos = data['combo'].split('&')
            combos.pop(len(combos)-1)
            for x in combos:
                line = x.split('-')
                ides.append(int(line[0]))
                if line[0] == '0' or line[1] == '0':
                    raise serializers.ValidationError({'combo':{str(index):['Los valores no pueden ser negativos o ceros.']}})
                try:
                    producto = Producto.objects.get(pk=int(line[0]))
                except:
                    raise serializers.ValidationError({'combo':{str(index):['No existe el producto.']}})
                if producto.sucursal.id != data['sucursal'].id:
                    raise serializers.ValidationError({'combo':{str(index):['La sucursal del producto no esta asociada a la del padre.']}})
                index+=1
            while len(ides) > 0:
                try:
                    value = ides.pop()
                except:
                    value = -1
                if value in ides:
                    raise serializers.ValidationError({'combo':['No debe haber productos repetidos en el combo']})
        except:
            pass
        return data
    
    def validate_dias_activos(self, value):
        if not re.match("^[01]{7}$",value):
            raise serializers.ValidationError('El campo debe tener 7 caracteres y/o ser ceros o unos')
        return value
    
    def validate_categoria(self, value):
        if value.padre is None:
            raise serializers.ValidationError('La categoria debe tener un padre')
        if value.estado is False:
            raise serializers.ValidationError('La categoria esta inactiva')
        if not validar_categoria(value, settings._COMIDA_):
            raise serializers.ValidationError('La categoria no pertenece a comida')
        return value

    def create(self, validated_data):
        try:
            data = validated_data.pop('combo')
        except:
            pass
        return Producto.objects.create(**validated_data)



# editar combo
class EditarComboSerializer(serializers.ModelSerializer):
    combo = serializers.RegexField('^(\d{1,8}[-]\d{1,2}[&]){0,}?$',max_length=255)
    nombre = serializers.CharField(required=False,max_length=50)
    precio = serializers.DecimalField(max_digits=7, decimal_places=1, required=False)

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','foto','combo','dias_activos','estado','categoria']
    
    def validate(self, data):
        index = 0
        ides = []
        theris_pr = True
        try:
            combos = data['combo'].split('&')
            combos.pop(len(combos)-1)
        except:
            theris_pr = False
        
        if theris_pr:
            for x in combos:
                line = x.split('-')
                ides.append(int(line[0]))
                if line[0] == '0' or line[1] == '0':
                    raise serializers.ValidationError({'combo':{str(index):['Los valores no pueden ser negativos o ceros.']}})
                try:
                    producto = Producto.objects.get(pk=int(line[0]))
                except:
                    raise serializers.ValidationError({'combo':{str(index):['No existe el producto.']}})
                if producto.sucursal.id != self.instance.sucursal.id:
                    raise serializers.ValidationError({'combo':{str(index):['La sucursal del producto no esta asociada a la del padre.']}})
                index+=1
            while len(ides) > 0:
                try:
                    value = ides.pop()
                except:
                    value = -1
                if value in ides:
                    raise serializers.ValidationError({'combo':['No debe haber productos repetidos en el combo']})
        return data
    
    def validate_dias_activos(self, value):
        if not re.match("^[01]{7}$",value):
            raise serializers.ValidationError('El campo debe tener 7 caracteres y/o ser ceros o unos')
        return value
    
    def validate_categoria(self, value):
        if value.padre is None:
            raise serializers.ValidationError('La categoria debe tener un padre')
        if value.estado is False:
            raise serializers.ValidationError('La categoria esta inactiva')
        if not validar_categoria(value, settings._COMIDA_):
            raise serializers.ValidationError('La categoria no pertenece a comida')
        return value






# PEDIDOS

# CREAR PEDDIDOS FINAL

class PedidoProductos(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(required=True,max_value=99, min_value=1)

    class Meta:
        model = PedidoProducto
        fields = ('cantidad','producto_final')

    def validate_producto_final(self, value):
        if value.estado == False:
            raise serializers.ValidationError('El producto esta inactivo')
        return value

class CrearPedidoSerializer(serializers.ModelSerializer):
    productos = PedidoProductos(required=True,many=True)

    class Meta:
        model = Pedido
        fields = ('sucursal','ubicacion','productos','nota')
    
    def validate(self, data):
        for x in data['productos']:
            if x['producto_final'].sucursal.id != data['sucursal'].id:
                raise serializers.ValidationError({'productos':'Hay productos(s) que no pertenecen a la sucursal.'})
        return data
    
    def validate_ubicacion(self, value):
        if value[0] == '{' and value[len(value)-1] == '}':  
            try:
                val = value[:-1].split(',')
                v1 = val[0].split(':')[1]
                v2 = val[1].split(':')[1]
            except:
                raise serializers.ValidationError('Formato incorrecto de ubicacion')
        else:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')

        try:
            latitude = Decimal(v1)
            longitude = Decimal(v2)
        except:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        if latitude.compare(Decimal(-90.0)) == Decimal(-1):
            raise serializers.ValidationError('Latitud incorrecta')
        elif latitude.compare(Decimal(90.0)) == Decimal(1):
            raise serializers.ValidationError('Latitud incorrecta')
        if longitude.compare(Decimal(-180.0)) == -1:
            raise serializers.ValidationError('Longitud incorrecta')
        elif longitude.compare(Decimal(180.0)) == 1:
            raise serializers.ValidationError('Longitud incorrecta')
        return value

    def validate_productos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('El pedido debe tener al menos 1 producto.')
        return value




#asd
class EditarPedidoSerializer(serializers.ModelSerializer):
    productos = PedidoProductos(required=False,many=True)

    class Meta:
        model = Pedido
        fields = ('ubicacion','productos','nota')
    
    def validate(self, data):
        try:
            data['productos']
            is_productos = True
        except:
            is_productos = False
        if is_productos is True:
            for x in data['productos']:
                if x['producto_final'].sucursal.id != self.instance.sucursal.id:
                    raise serializers.ValidationError({'productos':'Hay productos(s) que no pertenecen a la sucursal.'})
        return data

    def validate_ubicacion(self, value):
        if value[0] == '{' and value[len(value)-1] == '}':  
            try:
                val = value[:-1].split(',')
                v1 = val[0].split(':')[1]
                v2 = val[1].split(':')[1]
            except:
                raise serializers.ValidationError('Formato incorrecto de ubicacion')
        else:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')

        try:
            latitude = Decimal(v1)
            longitude = Decimal(v2)
        except:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        if latitude.compare(Decimal(-90.0)) == Decimal(-1):
            raise serializers.ValidationError('Latitud incorrecta')
        elif latitude.compare(Decimal(90.0)) == Decimal(1):
            raise serializers.ValidationError('Latitud incorrecta')
        if longitude.compare(Decimal(-180.0)) == -1:
            raise serializers.ValidationError('Longitud incorrecta')
        elif longitude.compare(Decimal(180.0)) == 1:
            raise serializers.ValidationError('Longitud incorrecta')
        return value

    def validate_productos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('El pedido debe tener al menos 1 producto.')
        return value















# PEDIDOS PARA EMPRESARIOS INI

# CREAR PEDDIDOS EMPRESARIO

class CrearPedidoSerializer_Empresario(serializers.ModelSerializer):
    productos = PedidoProductos(required=False,many=True)

    class Meta:
        model = Pedido
        fields = ('sucursal','ubicacion','productos','nota')
    
    def validate(self, data):
        try:
            data['productos']
            is_productos = True
        except:
            is_productos = False
        if is_productos is True:
            for x in data['productos']:
                if x['producto_final'].sucursal.id != data['sucursal'].id:
                    raise serializers.ValidationError({'productos':'Hay productos(s) que no pertenecen a la sucursal.'})
        return data
    
    def validate_ubicacion(self, value):
        if value[0] == '{' and value[len(value)-1] == '}':  
            try:
                val = value[:-1].split(',')
                v1 = val[0].split(':')[1]
                v2 = val[1].split(':')[1]
            except:
                raise serializers.ValidationError('Formato incorrecto de ubicacion')
        else:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        # val = v.split(',')
        try:
            latitude = Decimal(v1)
            longitude = Decimal(v2)
        except:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        if latitude.compare(Decimal(-90.0)) == Decimal(-1):
            raise serializers.ValidationError('Latitud incorrecta')
        elif latitude.compare(Decimal(90.0)) == Decimal(1):
            raise serializers.ValidationError('Latitud incorrecta')
        if longitude.compare(Decimal(-180.0)) == -1:
            raise serializers.ValidationError('Longitud incorrecta')
        elif longitude.compare(Decimal(180.0)) == 1:
            raise serializers.ValidationError('Longitud incorrecta')
        return value

    def validate_productos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('El pedido debe tener al menos 1 producto.')
        return value




#asd
class EditarPedidoSerializer_Empresario(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=7, decimal_places=1, required=False)
    productos = PedidoProductos(required=False,many=True)

    class Meta:
        model = Pedido
        fields = ('ubicacion','total','productos','nota')
    
    def validate(self, data):
        try:
            data['productos']
            is_productos = True
        except:
            is_productos = False
        if is_productos is True:
            for x in data['productos']:
                if x['producto_final'].sucursal.id != self.instance.sucursal.id:
                    raise serializers.ValidationError({'productos':'Hay productos(s) que no pertenecen a la sucursal.'})
        return data
    
    def validate_ubicacion(self, value):
        if value[0] == '{' and value[len(value)-1] == '}':  
            try:
                val = value[:-1].split(',')
                v1 = val[0].split(':')[1]
                v2 = val[1].split(':')[1]
            except:
                raise serializers.ValidationError('Formato incorrecto de ubicacion')
        else:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        # val = v.split(',')
        try:
            latitude = Decimal(v1)
            longitude = Decimal(v2)
        except:
            raise serializers.ValidationError('Formato incorrecto de ubicacion')
        if latitude.compare(Decimal(-90.0)) == Decimal(-1):
            raise serializers.ValidationError('Latitud incorrecta')
        elif latitude.compare(Decimal(90.0)) == Decimal(1):
            raise serializers.ValidationError('Latitud incorrecta')
        if longitude.compare(Decimal(-180.0)) == -1:
            raise serializers.ValidationError('Longitud incorrecta')
        elif longitude.compare(Decimal(180.0)) == 1:
            raise serializers.ValidationError('Longitud incorrecta')
        return value

    def validate_productos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('El pedido debe tener al menos 1 producto.')
        return value

# FIN








class PedidoEmpresaSerializer(serializers.ModelSerializer):
    categoria = CategoriaEmpresaSerializer()
    empresario = PerfilSerializer()
    
    class Meta:
        model = Empresa
        fields = ['id','nombre','descripcion','empresario','categoria']

class PedidoSucursalSerializer(serializers.ModelSerializer):
    empresa = PedidoEmpresaSerializer()

    class Meta:
        model = Sucursal
        fields = ['id','nombre','disponible','estado','telefono','ubicacion','direccion','foto','empresa','hora_inicio','hora_fin','ciudad']


class ProFinalSucursalSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)
    # combo = serializers.SerializerMethodField('cargar_pro')

    class Meta:
        model = Producto
        fields = ['id','nombre','descripcion','precio','estado','foto']

class PedidosSucursalCustomSerializer(serializers.ModelSerializer):
    cliente = PerfilSerializer()
    sucursal = PedidoSucursalSerializer()
    productos = serializers.SerializerMethodField('cargar_productos')
    repartidor = PerfilSerializer()

    class Meta:
        model = Pedido
        fields = ('id','sucursal','cliente','repartidor','estado','fecha','ubicacion','productos','total')
    
    def cargar_productos(self, obj):
        if obj.id:
            productos = Producto.objects.filter(id__in=PedidoProducto.objects.filter(pedido=obj.id).values('producto_final'))
            return ProFinalSucursalSerializer(productos, many=True).data


# class ShowCiudad_Serializer(serializers.Serializer):
#     def to_representation(self, instance):
#         return {
#             'id':instance.id,
#             'nombre':instance.nombre,
#             'estado':instance.estado,
#         }

# class ShowUsuario_Serializer(serializers.Serializer):
#     def to_representation(self, instance):
#         return {
#             'id':instance.id,
#             'username':instance.username,
#             'email':instance.email,
#             'nombres':instance.nombres,
#             'apellidos':instance.apellidos,
#             'token_firebase':instance.token_firebase,
#             # 'foto':instance.sucursal.empresa.empresario.foto,
#             'username':instance.username,
#             'telefono':instance.perfil.telefono,
#         }

# class ShowEmpresa_Serializer(serializers.Serializer):
#     def to_representation(self, instance):
#         return {
#             'id':instance.id,
#             'nombre':instance.nombre,
#             'descripcion':instance.descripcion,
#         }

# class ShowSucursal_Serializer(serializers.Serializer):
#     def to_representation(self, instance):
#         return {
#             'id':instance.id,
#             'nombre':instance.nombre,
#             'disponible':instance.disponible,
#             'estado':instance.estado,
#             'ubicacion':instance.ubicacion,
#             'telefono':instance.telefono,
#             'direccion':instance.direccion,
#             # 'foto':instance.sucursal.foto.url,
#             'foto':self.context.get('request').build_absolute_uri(instance.foto.url) if instance.foto else None,
#             'hora_inicio':instance.hora_inicio,
#             'hora_fin':instance.hora_fin
#         }


class ShowHorario_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'entrada':instance.entrada,
            'salida':instance.salida,
            'estado':instance.estado,
        }

class ShowProductoPedido_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.producto_final.id,
            'nombre':instance.producto_final.nombre,
            # 'descripcion':instance.producto_final.descripcion,
            'precio':str(instance.producto_final.precio),
            # 'estado':instance.producto_final.estado,
            # 'sucursal':instance.producto_final.sucursal.id,
            'foto':instance.producto_final.foto.url if instance.producto_final.foto else None,
            # 'foto':self.context.get('request').build_absolute_uri(instance.producto_final.foto.url) if instance.producto_final.foto else None,
            'cantidad':instance.cantidad
        }


class ShowPedido_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'estado':instance.estado,
            'fecha':make_naive(instance.fecha),
            'ubicacion':instance.ubicacion,
            'total':str(instance.total),
            'costo_envio':str(instance.costo_envio),
            'precio_final':str(instance.precio_final),
            'is_calificado_cliente':instance.is_calificado_cliente,
            'is_calificado_empresario':instance.is_calificado_empresario,
            'is_calificado_repartidor':instance.is_calificado_repartidor,
            'nota':instance.nota,
            'sucursal':{
                'id':instance.sucursal.id,
                'nombre':instance.sucursal.nombre,
                'disponible':instance.sucursal.disponible,
                'estado':instance.sucursal.estado,
                'ubicacion':instance.sucursal.ubicacion,
                'telefono':instance.sucursal.telefono,
                'direccion':instance.sucursal.direccion,
                'foto':instance.sucursal.foto.url if instance.sucursal.foto else None,
                # 'foto':self.context.get('request').build_absolute_uri(instance.sucursal.foto.url) if instance.sucursal.foto else None,
                'hora_inicio':instance.sucursal.hora_inicio,
                'hora_fin':instance.sucursal.hora_fin,
                'ciudad':instance.sucursal.ciudad.id,
                'empresa':{
                    'id':instance.sucursal.empresa.id,
                    'nombre':instance.sucursal.empresa.nombre,
                    'descripcion':instance.sucursal.empresa.descripcion,
                    'empresario':{
                        'id':instance.sucursal.empresa.empresario.id,
                        'username':instance.sucursal.empresa.empresario.username,
                        'email':instance.sucursal.empresa.empresario.email,
                        'nombres':instance.sucursal.empresa.empresario.nombres,
                        'apellidos':instance.sucursal.empresa.empresario.apellidos,
                        'token_firebase':instance.sucursal.empresa.empresario.token_firebase,
                        # 'foto':instance.sucursal.empresa.empresario.foto,
                        'username':instance.sucursal.empresa.empresario.username,
                        'telefono':instance.sucursal.empresa.empresario.perfil.telefono,
                        'ciudad':{
                            'id':instance.sucursal.empresa.empresario.ciudad.id,
                            'nombre':instance.sucursal.empresa.empresario.ciudad.nombre,
                            'estado':instance.sucursal.empresa.empresario.ciudad.estado,
                        }
                    }
                }
            },
            'cliente':{
                'id':instance.cliente.id,
                'username':instance.cliente.username,
                'email':instance.cliente.email,
                'nombres':instance.cliente.nombres,
                'apellidos':instance.cliente.apellidos,
                'token_firebase':instance.cliente.token_firebase,
                'foto':instance.cliente.foto.url if instance.cliente.foto else None,
                # 'foto':self.context.get('request').build_absolute_uri(instance.cliente.foto.url) if instance.cliente.foto else None,
                'username':instance.cliente.username,
                'telefono':instance.cliente.perfil.telefono,
                'ciudad':{
                    'id':instance.cliente.ciudad.id,
                    'nombre':instance.cliente.ciudad.nombre,
                    'estado':instance.cliente.ciudad.estado,
                }
            },
            'repartidor':{
                'id':instance.repartidor.id,
                'username':instance.repartidor.username,
                'email':instance.repartidor.email,
                'nombres':instance.repartidor.nombres,
                'apellidos':instance.repartidor.apellidos,
                'token_firebase':instance.repartidor.token_firebase,
                'foto':instance.repartidor.foto.url if instance.repartidor.foto else None,
                # 'foto':self.context.get('request').build_absolute_uri(instance.repartidor.foto.url) if instance.repartidor.foto else None,
                'username':instance.repartidor.username,
                'telefono':instance.repartidor.perfil.telefono,
                'calificacion':instance.repartidor.perfil.calificacion,
                'ciudad':{
                    'id':instance.repartidor.ciudad.id,
                    'nombre':instance.repartidor.ciudad.nombre,
                    'estado':instance.repartidor.ciudad.estado,
                }
                # 'horario':ShowHorario_Serializer( Horario.objects.filter(usuario__id=instance.repartidor.id), many=True ).data
            } if instance.repartidor is not None else None,
            'productos':ShowProductoPedido_Serializer( PedidoProducto.objects.select_related('producto_final').filter(pedido__id=instance.id), many=True, context={'request':self.context.get('request')} ).data
        }


# pedidor rango de fechas
class PedidosRangoFecha_Sucursal(serializers.Serializer):
    fecha_inicio = serializers.DateField(format=settings.DATE_FORMAT,required=True)
    fecha_fin = serializers.DateField(format=settings.DATE_FORMAT,required=True)

    def validate(self, data):
        f1 = data['fecha_inicio']
        f2 = data['fecha_fin']
        if f1 > f2:
            raise serializers.ValidationError('La fecha_inicio no puede ser mayor a la fecha_fin')
        elif f1 > date.today():
            raise serializers.ValidationError('La fecha_inicio esta fuera del rango')
        return data



class ShowPedido_forCliente_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'estado':instance.estado,
            'fecha':make_naive(instance.fecha),
            'ubicacion':instance.ubicacion,
            'total':str(instance.total),
            'costo_envio':str(instance.costo_envio),
            'precio_final':str(instance.precio_final),
            'is_calificado_cliente':instance.is_calificado_cliente,
            'is_calificado_empresario':instance.is_calificado_empresario,
            'is_calificado_repartidor':instance.is_calificado_repartidor,
            'nota':instance.nota,
            'sucursal':instance.sucursal.id,
            'cliente':instance.cliente.id,
            'repartidor':instance.repartidor.id if instance.repartidor is not None else None,
            'productos':ShowProductoPedido_Serializer( PedidoProducto.objects.select_related('producto_final').filter(pedido__id=instance.id), many=True, context={'request':self.context.get('request')} ).data
        }




# REPARTIDOR

class RepartidorDisponible_Serializer(serializers.Serializer):
    disponible = serializers.ChoiceField(required=True,choices=(('L','Libre'),('N', 'No Disponible')))








class ProductoFinal_Paginator_Serializer(serializers.Serializer):
    
    def to_representation(self, instance):
        # print(Sucursal.objects.select_related('').get(pk=instance.id))
        # combo = serializers.SerializerMethodField('cargar_pro')
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'descripcion':instance.descripcion,
            'precio':instance.precio,
            'estado':instance.estado,
            'sucursal':instance.sucursal.id,
            # 'sucursal':Pedido.objects.select_related('sucursal')
            'foto':instance.foto.url if instance.foto else None
            # 'combo':True if Combo.objects.select_related('producto').exists() else False
            # 'combo':True if Combo.objects.filter(combo__id=instance.id).count() > 0 else False
        }




# CALIFICAR

class CalificarCliente_Serializer(serializers.Serializer):
    value_repartidor = serializers.IntegerField(max_value=5,min_value=0, required=True)
    value_empresario = serializers.IntegerField(max_value=5,min_value=0, required=True)

class CalificarRepartidor_Serializer(serializers.Serializer):
    value_cliente = serializers.IntegerField(max_value=5,min_value=0, required=True)
    value_empresario = serializers.IntegerField(max_value=5,min_value=0, required=True)

class CalificarEmpresario_Serializer(serializers.Serializer):
    value_cliente = serializers.IntegerField(max_value=5,min_value=0, required=True)
    value_repartidor = serializers.IntegerField(max_value=5,min_value=0, required=True)

class CalificarProducto_Serializer(serializers.Serializer):
    puntuacion = serializers.IntegerField(max_value=5,min_value=0, required=True)
