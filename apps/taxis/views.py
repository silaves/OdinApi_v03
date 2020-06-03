import json
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from requests.exceptions import HTTPError

from rest_framework import permissions, exceptions
from rest_framework import generics, permissions, status, views
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from social_django.utils import load_strategy, load_backend

from apps.autenticacion.views import permission_required
from .models import Movil
# from .serializers import 
from apps.autenticacion.serializers import UsuarioSerializer
from apps.autenticacion.models import Usuario
from apps.autenticacion.views import get_user_by_token
from .serializers import PerfilSerializer



# get movil por token
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def ver_taxista(request):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    if not is_member(usuario, settings.GRUPO_TAXISTA):
        return Response({'error':'El usuario no pertenece al grupo taxista'})
    try:
        movil = Movil.objects.get(taxista=usuario)
    except:
        return Response({'error':'No hay un movil vinculado al taxista'})

    data = PerfilSerializer(usuario).data
    return Response(data)



# get movil por id
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def ver_taxista_id(request, id_usuario):
    try:
        usuario = Usuario.objects.get(pk=id_usuario)
    except:
        return Response({'error':'No se encontro al usuario'})
    if not is_member(usuario, settings.GRUPO_TAXISTA):
        return Response({'error':'El usuario no pertenece al grupo taxista'})
    try:
        movil = Movil.objects.get(taxista=usuario)
    except:
        return Response({'error':'No hay un movil vinculado al taxista'})

    data = PerfilSerializer(usuario).data
    return Response(data)


# verificar si un usuario pertence a un grupo
def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()