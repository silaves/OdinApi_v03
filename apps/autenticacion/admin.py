from django.shortcuts import redirect
from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
# Register your models here.
from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.db.models.sql.datastructures import Join
from django.forms.models import BaseInlineFormSet

from social_django.models import Association, Nonce, UserSocialAuth

from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupForm, UsuarioForm,EditUsuarioForm
from .models import Usuario, Perfil, Horario,VersionesAndroidApp, Ciudad, EncargadoCiudad, TarifaCostoEnvio


class PerfilInline(admin.StackedInline):
    model = Perfil
    # fields = ('telefono', 'calificacion','disponibilidad' )
    readonly_fields = ('cant_calificacion','calificacion',)
    can_delete = False

    def get_fields(self, request, obj=None):
        if obj is None:
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
                return ('telefono',)    
            return ('telefono', 'cant_calificacion','calificacion','disponibilidad')
        else:
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
                return ('telefono','disponibilidad',)    
            return ('telefono', 'cant_calificacion', 'calificacion','disponibilidad')

class HorarioForm(forms.ModelForm):
    entrada = forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))

    class Meta:
        model = Horario
        fields = '__all__'
    
    def clean(self):
        entrada = self.cleaned_data.get('entrada')
        salida = self.cleaned_data.get('salida')
        if entrada and salida:
            if entrada > salida:
                raise forms.ValidationError({'entrada':['El horario de entrada no puede ser mayor al de salida']})
            elif entrada == salida:
                raise forms.ValidationError({'entrada':['El horario de entrada no puede ser igual al de salida']})
        return self.cleaned_data


class HorarioInline(admin.StackedInline):
    model = Horario
    form = HorarioForm
    fields = ('entrada', 'salida','estado' )
    can_delete = True
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = UsuarioForm
    change_form = EditUsuarioForm
    model = Usuario
    list_display = ('username','id', 'email','nombres', 'apellidos', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active', 'groups')
    # fieldsets = (
    #     ('Informacion Personal', {'fields': ('username', 'password', 'nombres', 'apellidos','email','foto','ciudad')}),
    #     ('Permisos', {'fields': ('is_staff', 'is_active','groups', 'user_permissions')}),
    # )
    # add_fieldsets =(        
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2', 'nombres',  'apellidos', 'foto','email', 'is_staff', 'is_active')}
    #     ),
    # )
    ordering = ('-id',)
    inlines = (PerfilInline, HorarioInline,)
    search_fields = ('username','email',)
    # ordering = ('username',)
    actions = ['activar_usuario','dar_baja_usuario']

    class Media:
        js = ['own/js/admin.js']

    def get_actions(self, request):#eliminar la accion de eliminar
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def activar_usuario(self, request, queryset):#acciones masivas
        queryset.update(is_active=True)
    
    def dar_baja_usuario(self, request, queryset):#acciones masivas
        queryset.update(is_active=False)

    def get_groups(self, obj):
        print(obj)
        print("*-*-*-*-*-*-*-")
        #qs = Group.objects.filter(CustomUser.username = obj)
        #print(qs)
        q1 = Usuario.objects.get(username = obj)
        q2 = Group.objects.filter(user=q1)
        str_groups = ""
        for p in q2:
            str_groups += p.name+", "
        if str_groups=="":
            return ""
        else:
            return str_groups[:len(str_groups)-2]

    def get_form(self, request, obj=None, **kwargs):
        grupos_disponibles_encargado = [settings.GRUPO_EMPRESARIO,settings.GRUPO_REPARTIDOR]
        if not obj:
            self.form = self.add_form
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
                self.form.base_fields['ciudad'].queryset = Ciudad.objects.filter(pk=request.user.ciudad.id)
                self.form.base_fields['ciudad'].empty_label = None
                self.form.base_fields['groups'].queryset = Group.objects.filter(name__in=grupos_disponibles_encargado)
                self.form.base_fields['groups'].required = True
            return self.form
        else:
            self.form = self.change_form
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
                self.form.base_fields['ciudad'].queryset = Ciudad.objects.filter(pk=request.user.ciudad.id)
                self.form.base_fields['ciudad'].empty_label = None
                if request.user.id == obj.id:
                    self.form.base_fields['groups'].queryset = Group.objects.filter(name=settings.GRUPO_ENCARGADO_CIUDAD)
                else:
                    self.form.base_fields['groups'].queryset = Group.objects.filter(name__in=grupos_disponibles_encargado)
                self.form.base_fields['groups'].required = True
            else:
                self.form.base_fields['ciudad'].queryset = Ciudad.objects.filter(estado=True)
                self.form.base_fields['groups'].queryset = Group.objects.all()
            return self.form

    
    # def get_changeform_initial_data(self, request):
    #     return {'ciudad': Ciudad.objects.filter(pk=request.user.ciudad.id)}

    def get_fieldsets(self,request,obj=None):
        if obj:
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
                return ([
                    ('Informacion Personal', {'fields': ('username','password', 'nombres', 'apellidos','email','ciudad')}),
                    ('Permisos', {'fields': ('is_active','groups')}),
                ])
            else:
                return ([
                    ('Informacion Personal', {'fields': ('username','password','nombres', 'apellidos','email','ciudad','foto')}),
                    ('Permisos', {'fields': ('is_staff', 'is_active','is_register','groups', 'user_permissions')}),
                ])
        else:
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
                return ([
                    ('Informacion Personal', {'fields': ('username','password1','password2', 'nombres', 'apellidos','email','ciudad')}),
                    ('Permisos', {'fields': ('is_active','groups')}),
                ])
            else:
                return ([
                    ('Informacion Personal', {'fields': ('username','password1','password2','nombres', 'apellidos','email','ciudad','foto')}),
                    ('Permisos', {'fields': ('is_staff', 'is_active','groups', 'user_permissions')}),
                ])
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        show_usarios_for_encargado = [settings.GRUPO_EMPRESARIO,settings.GRUPO_REPARTIDOR]
        q0 = qs.filter(pk=request.user.id)
        if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD):
            q1 = qs.filter(groups__name__in=show_usarios_for_encargado, ciudad__id=request.user.ciudad.id)
            return (q0|q1).distinct()

        return qs

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields + ('is_staff',)
    #     return self.readonly_fields
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/autenticacion/usuario')
    
    def save_model(self, request, obj, form, change):
        if obj:
            if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD):
                if request.user.id == obj.id:
                    obj.is_staff = True
        super(CustomUserAdmin, self).save_model(request, obj, form, change)






# GROUP PROXY PARA CAMBIAR VERBOSE_NAME_PLURAL, ESTO GENERA UNA MIGRACION EN LOS LIB DE CONTRIB DE DJANGO TOMAR EN CUENTA
class Grupo(Group):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name_plural = '3. Grupos'

class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    model = Group
    search_fields = ('name',)
    ordering = ('name',)




# CIUDAD
class EncargadoCiudadForm(forms.ModelForm):
    class Meta:
        model = EncargadoCiudad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EncargadoCiudadForm, self).__init__(*args, **kwargs)
        try:
            self.fields['usuario'].queryset = Usuario.objects.filter(groups__name=settings.GRUPO_ENCARGADO_CIUDAD)
        except (AttributeError, ObjectDoesNotExist):
            pass

class EncargadoCiudadAdmin(admin.StackedInline):
    model = EncargadoCiudad
    form = EncargadoCiudadForm
    extra = 0

class TarifaCostoEnvioCiudadAdmin(admin.StackedInline):
    model = TarifaCostoEnvio
    extra = 0

class CiudadAdmin(admin.ModelAdmin):
    inlines = [TarifaCostoEnvioCiudadAdmin,EncargadoCiudadAdmin,]
    list_display = ('nombre','id','estado')



admin.site.register(VersionesAndroidApp)
# admin.site.unregister(Usuario)
admin.site.register(Usuario, CustomUserAdmin)
# admin.site.register(Permission)
admin.site.unregister(Group)
admin.site.register(Grupo, GroupAdmin)
admin.site.register(Ciudad,CiudadAdmin)

admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)