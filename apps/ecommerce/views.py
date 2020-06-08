from django.shortcuts import render
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, renderer_classes, parser_classes, action

from apps.autenticacion.views import get_user_by_token, is_member
from apps.empresa.models import (CategoriaEmpresa, Empresa, Sucursal,FotoSucursal, Producto, 
    Combo, FotoProducto, Favorito, CategoriaProducto)
from apps.autenticacion.models import Usuario, Ciudad, Perfil

from .serializers import *
from .pagination import CursorPagination, NumberPagination


@api_view(['POST'])
@permission_classes([AllowAny,])
def test1(request):

    data = Test_Serializer(data=request.data)
    data.is_valid(raise_exception=True)
    _json = data.validated_data['atributos']
    for x in _json:
        print(x,len(_json[x]))
    # x = request.data['data']
    # x = x+'s"s'
    # print(x)
    return Response({"mensaje":"ok"})


# CATEGORIA PRODUCTOS

# listar categorias productos
@swagger_auto_schema(method="GET",responses={200:ResponseCategoriaProducto(many=True)},operation_id="Lista de todas las Categorias Productos")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categorias_productos(request, estado):
    revisar_estado_AIT(estado)
    if estado == 'A':
        query = CategoriaProducto.objects.filter(estado=True)
    elif estado == 'I':
        query = CategoriaProducto.objects.filter(estado=False)
    else:
        query = CategoriaProducto.objects.filter()
    data = ShowCategoriaProducto_Serializer(query, many=True).data
    return Response(data)



# listar categorias productos - por niveles
@swagger_auto_schema(method="GET",responses={200:ResponseCategoriaProductoNivel(many=True)},operation_id="Lista de todas las Categorias Productos por NIVELES")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categorias_productos_niveles(request, estado):
    revisar_estado_AIT(estado)
    if estado == 'A':
        query = CategoriaProducto.objects.filter(padre=None,estado=True)
    elif estado == 'I':
        query = CategoriaProducto.objects.filter(padre=None,estado=False)
    else:
        query = CategoriaProducto.objects.filter(padre=None)
    data = ShowCategoriaProductoNivel_Serializer(query, many=True, context={'estado':estado}).data
    return Response(data)



def solve_categoria_lista(id_padre,estado, _ids):
    if estado == 'A':
        qs = CategoriaProducto.objects.filter(padre__id=id_padre,estado=True)
    elif estado == 'I':
        qs = CategoriaProducto.objects.filter(padre__id=id_padre,estado=False)
    else:
        qs = CategoriaProducto.objects.filter(padre__id=id_padre)
    
    if qs.count() == 0:
        return _ids

    for q in qs:
        _ids.append(q.id)
        solve_categoria_lista(q.id, estado, _ids)


# listar categorias productos - por hijos lista
@swagger_auto_schema(method="GET",responses={200:ResponseCategoriaProducto(many=True)},operation_id="Lista de todas las Categorias Productos de una Categoria Padre LISTA")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categorias_productos_hijo(request, id_categoria, estado):
    revisar_estado_AIT(estado)
    _ids = []
    query = CategoriaProducto.objects.filter(pk__in=_ids)
    data = ShowCategoriaProducto_Serializer(query, many=True).data
    return Response(data)


# listar categorias productos - por hijos niveles
@swagger_auto_schema(method="GET",responses={200:ResponseCategoriaProductoNivel(many=True)},operation_id="Lista de todas las Categorias Productos de una categoria Padre por NIVELES")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categorias_productos_hijo_niveles(request, id_categoria, estado):

    revisar_estado_AIT(estado)
    if estado == 'A':
        query = CategoriaProducto.objects.filter(padre__id=id_categoria,estado=True)
    elif estado == 'I':
        query = CategoriaProducto.objects.filter(padre__id=id_categoria,estado=False)
    else:
        query = CategoriaProducto.objects.filter(padre__id=id_categoria)
    data = ShowCategoriaProductoNivel_Serializer(query, many=True, context={'estado':estado}).data
    return Response(data)







    # ARTICULOS - PRODUCTOS



# crear articulo
@swagger_auto_schema(method="POST",responses={200:'Se ha creado el articulo'},operation_id="Crear Articulo")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_articulo(request):
    usuario = get_user_by_token(request)
    if is_member(usuario, 'empresario') is False:
        raise PermissionDenied('Usted no esta autorizado')
    obj = CrearArticulo_Serializer(data=request.data)
    obj.is_valid(raise_exception=True)
    revisar_propietario_sucursal(usuario, obj.validated_data['sucursal'])
    fotos = obj.validated_data.pop('fotos')
    articulo = obj.save()
    first_photo = fotos.pop(0)
    articulo.foto = first_photo
    articulo.save()
    for f in fotos:
        foto = FotoProducto.objects.create(foto=f,producto=articulo)

    return Response({'mensaje':'Se ha creado el articulo.'})


# editar articulo
@swagger_auto_schema(method="POST",responses={200:'Se ha modificado el articulo'},operation_id="Editar Articulo")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editar_articulo(request, id_producto):
    usuario = get_user_by_token(request)
    articulo = revisar_producto(id_producto)
    revisar_propietario_producto(usuario, id_producto)

    if is_member(usuario, 'empresario') is False:
        raise PermissionDenied('Usted no esta autorizado')
    obj = EditarArticulo_Serializer(articulo, data=request.data, partial=True)
    obj.is_valid(raise_exception=True)
    
    articulo = obj.save()

    # fotos = obj.validated_data.pop('fotos')

    # FotoProducto.objects.filter(producto__id=id_producto).delete()
    # articulo.foto = fotos.pop(0)
    # articulo.save()
    # c = 0
    # for f in fotos:
    #     foto = FotoProducto.objects.create(foto=f,producto=articulo)

    return Response({'mensaje':'Se ha modificado el articulo.'})



# ver articulo
@swagger_auto_schema(method="GET",responses={200:ResponseBasicProducto(many=True)},operation_id="Ver articulo")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_articulo(request, id_producto):
    try:
        articulo = Producto.objects.get(pk=id_producto)
    except:
        raise NotFound('No se encontro el articulo')
    sr = ShowAdvancedArticulo_Serializer(articulo).data
    return Response(sr)


# listar articulos
@swagger_auto_schema(method="GET",responses={200:ResponseBasicProducto(many=True)},operation_id="Lista de Todos lo articulos")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_articulos(request, estado):
    if estado == 'A':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE, estado=True).order_by('-creado')
    elif estado == 'I':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE, estado=False).order_by('-creado')
    elif estado == 'T':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE).order_by('-creado')
    else:
        raise NotFound('No se encontro la url')
    
    sr = ShowBasicArticulo_Serializer(query, many=True).data
    return Response(sr)


# listar articulos - pagination cursor
@swagger_auto_schema(method="GET",responses={200:ResponseBasicProducto(many=True)},operation_id="Lista de Todos lo articulos - Paginador Cursor")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_articulos_cursor_pagination(request, estado):
    if estado == 'A':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE, estado=True).order_by('-creado')
    elif estado == 'I':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE, estado=False).order_by('-creado')
    elif estado == 'T':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE).order_by('-creado')
    else:
        raise NotFound('No se encontro la url')

    paginator = CursorPagination()
    
    page = paginator.paginate_queryset(query, request)
    serializer = ShowBasicArticulo_Serializer(page, many=True).data
    data = paginator.get_paginated_response(serializer)
    return data




# listar articulos - pagination number
@swagger_auto_schema(method="GET",responses={200:ResponseBasicProducto(many=True)},operation_id="Lista de Todos lo articulos - Paginador Cursor")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_articulos_number_pagination(request, estado):
    if estado == 'A':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE, estado=True).order_by('-creado')
    elif estado == 'I':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE, estado=False).order_by('-creado')
    elif estado == 'T':
        query = Producto.objects.filter(sucursal__empresa__categoria__nombre=settings.ECOMMERCE).order_by('-creado')
    else:
        raise NotFound('No se encontro la url')

    paginator = NumberPagination()
    
    page = paginator.paginate_queryset(query, request)
    serializer = ShowBasicArticulo_Serializer(page, many=True).data
    data = paginator.get_paginated_response(serializer)
    return data











def revisar_producto(id_producto):
    try:
        articulo = Producto.objects.get(pk=id_producto)
        return articulo
    except:
        raise NotFound('No se encontro el producto')

def revisar_propietario_producto(usuario, id_producto):
    if Producto.objects.filter(sucursal__empresa__empresario__id=usuario.id).exists():
        return True
    else:
        raise PermissionDenied('Usted no es el propietario del producto')


def revisar_propietario_sucursal(usuario, sucursal):
    if usuario.id != sucursal.empresa.empresario.id:
        raise PermissionDenied('El usuario no esta asociado a la sucursal','no_permitido')
    return True

def revisar_estado_AI(estado):
    if not (estado == 'A' | estado == 'I' | estado == 'T'):
        raise NotFound('No se encontro la url')
    return estado
