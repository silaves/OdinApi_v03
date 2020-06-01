from django.shortcuts import render
from datetime import date, datetime, time
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework import permissions, exceptions
from rest_framework import generics, permissions, status, views
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, renderer_classes, parser_classes, action

from .models import *
from .serializers import *
from .pagination import CursorPagination


# CATEGORIA NOTICIAS

# listar categorias
@swagger_auto_schema(method="GET",responses={200:ResponseCategoria(many=True)},operation_id="Lista de todas las Categorias")
@api_view(['GET'])
def get_categorias(request, estado):
    revisar_estado_AIT(estado)
    if estado == 'A':
        query = CategoriaNoticia.objects.filter(estado=True)
    elif estado == 'I':
        query = CategoriaNoticia.objects.filter(estado=False)
    else:
        query = CategoriaNoticia.objects.filter()
    data = ShowCategoria_Serializer(query, many=True).data
    return Response(data)



# listar categorias - por niveles
@swagger_auto_schema(method="GET",responses={200:ResponseCategoriaNivel(many=True)},operation_id="Lista de todas las Categorias por NIVELES")
@api_view(['GET'])
def get_categorias_niveles(request, estado):
    revisar_estado_AIT(estado)
    if estado == 'A':
        query = CategoriaNoticia.objects.filter(padre=None,estado=True)
    elif estado == 'I':
        query = CategoriaNoticia.objects.filter(padre=None,estado=False)
    else:
        query = CategoriaNoticia.objects.filter(padre=None)
    data = ShowCategoriaNivel_Serializer(query, many=True, context={'estado':estado}).data
    return Response(data)



def solve_categoria_lista(id_padre,estado, _ids):
    if estado == 'A':
        qs = CategoriaNoticia.objects.filter(padre__id=id_padre,estado=True)
    elif estado == 'I':
        qs = CategoriaNoticia.objects.filter(padre__id=id_padre,estado=False)
    else:
        qs = CategoriaNoticia.objects.filter(padre__id=id_padre)
    
    if qs.count() == 0:
        return _ids

    for q in qs:
        _ids.append(q.id)
        solve_categoria_lista(q.id, estado, _ids)


# listar categorias - por hijos lista
@swagger_auto_schema(method="GET",responses={200:ResponseCategoria(many=True)},operation_id="Lista de todas las Categorias de una categoria Padre LISTA")
@api_view(['GET'])
def get_categorias_hijo(request, id_categoria, estado):
    revisar_estado_AIT(estado)
    _ids = []
    query = CategoriaNoticia.objects.filter(pk__in=_ids)
    data = ShowCategoria_Serializer(query, many=True).data
    return Response(data)


# listar categorias - por hijos niveles
@swagger_auto_schema(method="GET",responses={200:ResponseCategoriaNivel(many=True)},operation_id="Lista de todas las Categorias de una categoria Padre por NIVELES")
@api_view(['GET'])
def get_categorias_hijo_niveles(request, id_categoria, estado):

    revisar_estado_AIT(estado)
    if estado == 'A':
        query = CategoriaNoticia.objects.filter(padre__id=id_categoria,estado=True)
    elif estado == 'I':
        query = CategoriaNoticia.objects.filter(padre__id=id_categoria,estado=False)
    else:
        query = CategoriaNoticia.objects.filter(padre__id=id_categoria)
    data = ShowCategoriaNivel_Serializer(query, many=True, context={'estado':estado}).data
    return Response(data)


# Noticia

# lista de todas las noticias
@swagger_auto_schema(method="GET",responses={200:ReponseNoticiaList(many=True)},operation_id="Lista de todas las Noticias")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_noticias_all(request, estado):
    # print(datetime.now())
    # print(timezone.now())
    revisar_estado_AIT(estado)
    
    if estado == 'A':
        query = Noticia.objects.select_related('empresa').filter(estado=True)
    elif estado == 'I':
        query = Noticia.objects.select_related('empresa').filter(estado=False)
    else:
        query = Noticia.objects.select_related('empresa').all()
    
    data = ShowNoticias_Serializer(query, many=True).data
    return Response(data)

# lista de todas las noticias - cursor
@swagger_auto_schema(method="GET",responses={200:ReponseNoticiaList(many=True)},operation_id="Lista de todas las Noticias - PAGINADOR CURSOR")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_noticias_all_paginacion_cursor(request, estado):
    revisar_estado_AIT(estado)
    
    if estado == 'A':
        query = Noticia.objects.select_related('empresa').filter(estado=True)
    elif estado == 'I':
        query = Noticia.objects.select_related('empresa').filter(estado=False)
    else:
        query = Noticia.objects.select_related('empresa').all()
    
    paginator = CursorPagination()
    page = paginator.paginate_queryset(query, request)


    sr = ShowNoticias_Serializer(page, many=True).data
    data = paginator.get_paginated_response(sr)
    return data








# lista de noticias por empresa
@swagger_auto_schema(method="GET",responses={200:ReponseNoticiaList(many=True)},operation_id="Lista de todas las Noticias por Empresa")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_noticias_by_empresa(request, id_empresa, estado):
    revisar_estado_AIT(estado)
    if not Empresa.objects.filter(pk=id_empresa,categoria__nombre='periodico').exists():
        raise NotFound('El Periodico no existe')
        
    if estado == 'A':
        query = Noticia.objects.select_related('empresa').filter(empresa__id=id_empresa,estado=True)
    elif estado == 'I':
        query = Noticia.objects.select_related('empresa').filter(empresa__id=id_empresa,estado=False)
    else:
        query = Noticia.objects.select_related('empresa').filter(empresa__id=id_empresa)
    
    data = ShowNoticias_Serializer(query,many=True).data
    return Response(data)


# lista de noticias por empresa - cursor
@swagger_auto_schema(method="GET",responses={200:ReponseNoticiaList(many=True)},operation_id="Lista de todas las Noticias por Empresa - PAGINADOR CURSOR")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_noticias_by_empresa_paginacion_cursor(request, id_empresa, estado):
    revisar_estado_AIT(estado)
    if not Empresa.objects.filter(pk=id_empresa,categoria__nombre='periodico').exists():
        raise NotFound('El Periodico no existe')
        
    if estado == 'A':
        query = Noticia.objects.select_related('empresa').filter(empresa__id=id_empresa,estado=True)
    elif estado == 'I':
        query = Noticia.objects.select_related('empresa').filter(empresa__id=id_empresa,estado=False)
    else:
        query = Noticia.objects.select_related('empresa').filter(empresa__id=id_empresa)
    
    paginator = CursorPagination()
    page = paginator.paginate_queryset(query, request)
    sr = ShowNoticias_Serializer(page,many=True).data
    data = paginator.get_paginated_response(sr)
    return data








# lista de noticias por categoria
@swagger_auto_schema(method="GET",responses={200:ReponseNoticiaList(many=True)},operation_id="Lista de todas las Noticias por Categoria")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_noticias_by_categoria(request, id_categoria, estado):
    revisar_estado_AIT(estado)

    if estado == 'A':
        query = Noticia.objects.select_related('empresa').filter(categoria__id=id_categoria,estado=True)
    elif estado == 'I':
        query = Noticia.objects.select_related('empresa').filter(categoria__id=id_categoria,estado=False)
    else:
        query = Noticia.objects.select_related('empresa').filter(categoria__id=id_categoria)
    
    data = ShowNoticias_Serializer(query, many=True).data
    
    return Response(data)


# lista de noticias por categoria - cursor
@swagger_auto_schema(method="GET",responses={200:ReponseNoticiaList(many=True)},operation_id="Lista de todas las Noticias por Categoria - PAGINADOR CURSOR")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_noticias_by_categoria_paginacion_cursor(request, id_categoria, estado):
    revisar_estado_AIT(estado)

    if estado == 'A':
        query = Noticia.objects.select_related('empresa').filter(categoria__id=id_categoria,estado=True)
    elif estado == 'I':
        query = Noticia.objects.select_related('empresa').filter(categoria__id=id_categoria,estado=False)
    else:
        query = Noticia.objects.select_related('empresa').filter(categoria__id=id_categoria)
    
    paginator = CursorPagination()
    page = paginator.paginate_queryset(query, request)
    sr = ShowNoticias_Serializer(page, many=True).data
    data = paginator.get_paginated_response(sr)
    return data
    







# obtener noticia
@swagger_auto_schema(method="GET",responses={200:ResponseNoticia},operation_id="Ver Noticia")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_noticia(request, id_noticia):
    try:
        noticia = Noticia.objects.get(pk=id_noticia)
    except:
        raise NotFound('No se encontro la noticia')

    data = ShowVerNoticia_Serializer(noticia).data
    return Response(data)




def revisar_estado_AIT(estado):
    if not (estado == 'A' or estado == 'I' or estado == 'T'):
        raise NotFound('No se encontro la ruta')
    return estado