import jwt
from django.conf import settings
from rest_framework import permissions
from rest_framework import authentication, exceptions
from .models import Usuario

class IsCliente(permissions.BasePermission):
    group_name = settings.GRUPO_CLIENTE
    message = 'Solo usuarios %s pueden acceder' % group_name 

    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name=self.group_name))
