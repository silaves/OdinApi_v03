#nuevo
from django import forms
from django.contrib import admin
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (
        authenticate, get_user_model, password_validation,
    )
from django.contrib.auth.models import Permission, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, Http404
from django.contrib.admin.widgets import FilteredSelectMultiple

from apps.autenticacion.models import Usuario

#formulario para crear usuario
class CustomUserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Las dos contrasenas no coinciden",
        'custom_error': "el nombre de pati ya existe",
    }
    password1 = forms.CharField(label="Contrasena", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirma la contrasena", widget=forms.PasswordInput,
                                help_text="Ingrese la misma contrasena para verificar.")

    class Meta:
        model = Usuario
        fields = ('username','password1','password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    # limpieza del username
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username=='nombreusuario':
            raise forms.ValidationError(
                self.error_messages['custom_error'],
                code='custom_error',
                )
        return username

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#formulario para editar usuario
class CustomUserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
        help_text="Las contraseñas sin procesar no se almacenan, por lo que no hay forma de ver la contraseña "
        "de este usuario, pero puede cambiarla usando <a href=\"../password/\">este formulario</a>.")
    user_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.exclude(content_type__app_label='auth').exclude(content_type__app_label='admin').
            exclude(content_type__app_label='contenttypes').exclude(content_type__app_label='sessions'),
        widget=admin.widgets.FilteredSelectMultiple(_('permissions'), False))

    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]

#formulario de autentificacion - login
class AuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    print("-------------------------------authentication formulario")
    error_messages = {
        'invalid_login': _("Hubo un problema con la autentificacion. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("La cuenta esta inactiva"),
        'incorrect_pass':_("La contrasena es incorrecta"),
        'not_found':_("El usuario no existe"),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            print(self.user_cache, "                        ***********************")
            if self.user_cache is None:
                try:
                    cuser = get_object_or_404(CustomUser, username=username)
                    if cuser.check_password(password) == True:
                        if cuser.is_active == False:
                            raise forms.ValidationError(
                                self.error_messages['inactive'],
                                code='inactive',
                                params={'username':self.username_field.verbose_name},
                            )
                        else:
                            raise forms.ValidationError(
                                self.error_messages['invalid_login'],
                                code='invalid_login',
                                params={'username':self.username_field.verbose_name},
                            )
                    else:
                        raise forms.ValidationError(
                                self.error_messages['incorrect_pass'],
                                code='incorrect_pass',
                                params={'username':self.username_field.verbose_name},
                        )
                except Http404:
                    print("no se encontro el usuario")

                raise forms.ValidationError(
                    self.error_messages['not_found'],
                    code='not_found',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        Permission.objects.exclude(content_type__app_label='auth').exclude(content_type__app_label='admin').
            exclude(content_type__app_label='contenttypes').exclude(content_type__app_label='sessions'),
            widget=admin.widgets.FilteredSelectMultiple(_('permissions'), False))
    
    class Meta:
        model = Group
        fields = '__all__'


class UsuarioForm(CustomUserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by('name'),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=Group._meta.verbose_name,
            is_stacked=False)
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.order_by('id'),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=Permission._meta.verbose_name,
            is_stacked=False)
    )

    class Meta(CustomUserCreationForm):
        model = Usuario
        fields = ('username','email','password1','password2','nombres','apellidos','email','foto','ciudad','is_staff','is_active',
            'groups','user_permissions',)


class EditUsuarioForm(CustomUserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by('name'),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=Group._meta.verbose_name,
            is_stacked=False)
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.order_by('id'),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=Permission._meta.verbose_name,
            is_stacked=False)
    )
    class Meta(CustomUserChangeForm):
        model = Usuario
        fields = ('username','password','nombres','apellidos','email','foto','ciudad','is_staff','is_active',
            'groups','user_permissions',)