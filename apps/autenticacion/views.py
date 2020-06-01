import jwt
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from requests.exceptions import HTTPError
from django.db.models import F

from rest_framework import permissions, exceptions
from rest_framework import generics, permissions, status, views
from rest_framework.exceptions import NotFound,PermissionDenied, ParseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from django.contrib.auth.models import Group
from .serializers import (RegistrarseSerializer, LoginSerializer, UsuarioSerializer, PerfilSerializer, 
    UsuarioNormalSerializer,PerfilNormalSerializer, ChangePasswordSerializer, UsuarioEditResponse,CrearEmpresario_Serializer)
from . import serializers
from .renderers import UserJSONRenderer
from .models import Usuario, Perfil



# parar verificar si el usuario tiene permisos
def permission_required(permission_name, raise_exception=False):
    class PermissionRequired(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user.has_perm(permission_name):
                if raise_exception:
                    raise exceptions.PermissionDenied("No tiene permiso")
                return False
            return True
    return PermissionRequired



# # @method_decorator(csrf_exempt)
# @swagger_auto_schema(method="GET",operation_id="mas bien lokita",operation_description="mas bien lokitaaaaaaa")
# @swagger_auto_schema(method="POST",request_body=UsuarioSerializer,operation_id="mas bien lokita",operation_description="mas bien lokitaaaaaaa")
# @api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated,))
# def hello_world(request):
#     user = get_user_by_token(request)
#     print(user.username,'  def hello_world()')
#     print(request.META.get('HTTP_AUTHORIZATION'))
#     # print(request.headers.get('HTTP_AUTHORIZATION'))
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})



# @api_view(['POST'])
# @permission_classes([
#     IsAuthenticated,
#     permission_required("autenticacion.add_usuario", raise_exception=True),
# ])
# def ver_perfil(request):
#     return Response({"message":"loka vieja"})

# USUARIOS




class RegistrarseAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrarseSerializer

    @swagger_auto_schema(request_body=RegistrarseSerializer,responses={200:'ok'},operation_id="Registrarse")
    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    @swagger_auto_schema(request_body=LoginSerializer,operation_id="Login")
    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class UsuarioRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UsuarioSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



# registrar usuarios mediante redes sociales (google, facebook)
class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = serializers.SocialSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(request_body=serializers.SocialSerializer,operation_id="Social Login")
    def post(self, request):
        print('RATAS1')
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        # backend = load_backend(strategy=strategy, name=provider,redirect_uri=None)
        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
            print(backend,'----')
        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        print('RATAS2')
        try:
            authenticated_user = backend.do_auth(access_token, user=user)
       
        except HTTPError as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
       
        except AuthForbidden as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
        if authenticated_user and authenticated_user.is_active:
            #generate JWT token
            # login(request, authenticated_user)
            print(user)
            data={
                "token": user.token
                }
            #customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token')
            }


            #      dt = datetime.now() + timedelta(days=60)

            # token = jwt.encode({
            #     'id': self.pk,
            #     'exp': int(dt.strftime('%s'))
            # }, settings.SECRET_KEY, algorithm='HS256')

            # return token.decode('utf-8')


            return Response(status=status.HTTP_200_OK, data=response)


# lista de usuarios
@swagger_auto_schema(method="GET",operation_id="Listar todos los Usuarios")
@api_view(['GET'])
@permission_classes([IsAuthenticated,permission_required("autenticacion.view_usuario", raise_exception=True),])
def getUsuariosList(request):
    us = Usuario.objects.all()
    data = UsuarioSerializer(us, many=True).data
    return Response(data)


# detalle usuario
# @permission_classes([IsAuthenticated,permission_required("autenticacion.view_usuario", raise_exception=True),])
@swagger_auto_schema(method="GET",responses={200: PerfilSerializer},operation_id="Ver Usuario")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getDetalleUsuario(request, pk):
    try:
        us = Usuario.objects.get(pk=pk)
    except:
        return Response({'error':'No se encontro al usuario'})
    data = PerfilSerializer(us).data
    return Response(data)


# cambiar contrasena
@swagger_auto_schema(method="POST",request_body=ChangePasswordSerializer,
    responses={status.HTTP_200_OK:'La contrasenia se cambio correctamente'},operation_id="Cambiar Contrasena")
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def cambiar_contrasena(request):
    print('ratamons')
    usuario = get_user_by_token(request)
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.data.get('old_password')
        if not usuario.check_password(old_password):
            raise ParseError('contrasenia incorrecta','password_error')
        usuario.set_password(serializer.data.get('new_password'))
        usuario.save()
        return Response({'mensaje':'La contrasenia se cambio correctamente'})
    raise ParseError('errores en algunos de los campos y/o la contrasena debe tener al menos 8 caracteres','password_error')



# PERFILES

# Ver Perfil
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer},operation_id="Ver Perfil Usuario by Token")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getPerfil(request):
    try:
        usuario = get_user_by_token(request)
    except Exception as e:
        print(e)
        return Response({'error':'No se pudo cargar los datos'})
    print(Usuario.grupos(usuario),'---------------------++++++++++++++')
    data = PerfilSerializer(usuario).data
    return Response(data)


# editar usuario
@swagger_auto_schema(method="POST",request_body=UsuarioEditResponse,
    responses={status.HTTP_200_OK:'Se actualizaron los valores correctamente'},operation_id="Editar Usuario by Token")
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def editar_usuario(request):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se pudo cargar los datos'})
    obj = UsuarioNormalSerializer(usuario,data=request.data)
    if not Perfil.objects.filter(usuario=usuario).exists():
        perfil = Perfil()
        perfil.usuario = usuario
        perfil.save()
    else:
        perfil = Perfil.objects.get(usuario=usuario)
    obj_perfil = PerfilNormalSerializer(perfil,data=request.data)
    
    obj.is_valid(raise_exception=True)
    obj_perfil.is_valid(raise_exception=True)
    obj.save()
    obj_perfil.save()
    return Response({"mensaje":"Se actualizaron los valores correctamente"})


# Taxistas

# listar taxistas libres
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Taxistas Libres")
@api_view(['GET'])
@permission_classes([AllowAny,])
def getTaxistasLibres(request):
    try:
        usuario = Usuario.objects.filter(id__in=Perfil.objects.filter(disponibilidad='L').values('usuario__id'))
        # perfil = Perfil.objects.filter(disponibilidad='L').values('id','telefono','calificacion','disponibilidad','usuario')
    except Exception as e:
        print(e)
        return Response({'error':'No se pudo cargar los datos'})
    data = PerfilSerializer(usuario, many=True).data
    return Response(data)


# listar taxistas ocupados
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Taxistas Ocupados")
@api_view(['GET'])
@permission_classes([AllowAny,])
def getTaxistasOcupados(request):
    try:
        usuario = Usuario.objects.filter(id__in=Perfil.objects.filter(disponibilidad='O').values('usuario__id'))
        # perfil = Perfil.objects.filter(disponibilidad='L').values('id','telefono','calificacion','disponibilidad','usuario')
    except Exception as e:
        print(e)
        return Response({'error':'No se pudo cargar los datos'})
    data = PerfilSerializer(usuario, many=True).data
    return Response(data)


# listar taxistas no disponibles
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Taxistas no Disponibles")
@api_view(['GET'])
@permission_classes([AllowAny,])
def getTaxistasNoDisponibles(request):
    try:
        usuario = Usuario.objects.filter(id__in=Perfil.objects.filter(disponibilidad='N').values('usuario__id'))
        # perfil = Perfil.objects.filter(disponibilidad='L').values('id','telefono','calificacion','disponibilidad','usuario')
    except Exception as e:
        print(e)
        return Response({'error':'No se pudo cargar los datos'})
    data = PerfilSerializer(usuario, many=True).data
    return Response(data)


# CLIENTES

# lista clientes activos
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Clientes Activos")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getClientes_activos(request):
    try:
        clientes = Usuario.objects.filter(is_active=True,groups__name='cliente')
    except:
        return Response({'error':'Hubo un error al cargar los datos'})
    data = PerfilSerializer(clientes, many=True).data
    return Response(data)


# lista clientes inactivos
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Clientes Inactivos")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getClientes_inactivos(request):
    try:
        clientes = Usuario.objects.filter(is_active=False,groups__name='cliente')
    except:
        return Response({'error':'Hubo un error al cargar los datos'})
    data = PerfilSerializer(clientes, many=True).data
    return Response(data)




# Empresarios


# Ver Perfil Empresario
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer},operation_id="Ver Empresario by Token")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getPerfil_empresario(request):
    try:
        usuario = get_user_by_token(request)
    except Exception as e:
        return Response({'error':'No se pudo cargar los datos'})
    if not is_member(usuario, 'empresario'):
        return Response({'error':'Usted no esta autorizado'})
    data = PerfilSerializer(usuario).data
    return Response(data)


# lista empresarios activos
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Empresarios Activos")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getEmpresarios_activos(request):
    try:
        empresarios = Usuario.objects.filter(is_active=True,groups__name='empresario')
    except:
        return Response({'error':'Hubo un error al cargar los datos'})
    data = PerfilSerializer(empresarios, many=True).data
    return Response(data)


# lista empresarios inactivos
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Empresarios Inactivos")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getEmpresarios_inactivos(request):
    try:
        empresarios = Usuario.objects.filter(is_active=False,groups__name='empresario')
    except:
        return Response({'error':'Hubo un error al cargar los datos'})
    data = PerfilSerializer(empresarios, many=True).data
    return Response(data)


# Taxistas

# lista taxistas activos
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Taxistas Activos")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getTaxistas_activos(request):
    try:
        taxistas = Usuario.objects.filter(is_active=True,groups__name='taxista')
    except:
        return Response({'error':'Hubo un error al cargar los datos'})
    data = PerfilSerializer(taxistas, many=True).data
    return Response(data)


# lista taxistas inactivos
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Taxistas Inactivos")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getTaxistas_inactivos(request):
    try:
        taxistas = Usuario.objects.filter(is_active=False,groups__name='taxista')
    except:
        return Response({'error':'Hubo un error al cargar los datos'})
    data = PerfilSerializer(taxistas, many=True).data
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny,])
def crear_empresario(request):
    obj = CrearEmpresario_Serializer(data=request.data)
    obj.is_valid(raise_exception=True)
    try:
        telefono = obj.validated_data['telefono']
    except:
        telefono = 0
    usuario = obj.save()
    grupo = Group.objects.get(name='empresario')
    usuario.groups.add(grupo)
    usuario.save()
    perfil = Perfil()
    
    perfil.telefono = telefono
    perfil.usuario = usuario
    perfil.save()
    return Response({'mensaje':'Se ha creado el empresario correctamente'})




# funcion para otener el usuario de acuerdo al token del request
def get_user_by_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    data = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithm='HS256')
    user = Usuario.objects.get(id=data['id'])
    return user

# verificar si un usuario pertence a un grupo
def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()


