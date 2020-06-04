from django.contrib import admin
from django import forms

from .models import *

# Register your models here.

# class PersonForm(forms.ModelForm):
#     some_field = forms.ModelMultipleChoiceField(Person.objects.all(), widget=FilteredSelectMultiple("Person", False, attrs={'rows':'2'}))
#     class Meta:
#         model = CategoriaNoticia


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['categoria'].queryset = CategoriaNoticia.objects.filter(estado=True)
        self.fields['empresa'].queryset = Empresa.objects.filter(estado=True,categoria__nombre='periodico')


class FotoNoticiaInline(admin.StackedInline):
    model = FotoNoticia
    # form = HorarioForm
    fields = ('foto', 'descripcion','autor','localidad')
    can_delete = False
    extra = 1



class NoticiaAdmin(admin.ModelAdmin):
    model = Noticia
    form = NoticiaForm
    # list_display = ('id','titulo', 'sub_titulo', 'descripcion', 'link_fuente', 'estado', 'creado', 'empresa','categoria')
    # list_filter = ('username', 'is_staff', 'is_active', 'groups')
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
    inlines = (FotoNoticiaInline,)
    filter_horizontal = ('categoria',)
    # search_fields = ('username',)
    ordering = ('creado',)
    actions = ["activar_noticia"]


    def get_actions(self, request):#eliminar la accion de eliminar
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def activar_noticia(self, request, queryset):#acciones masivas
        queryset.update(is_active=True)



admin.site.register(CategoriaNoticia)
admin.site.register(Noticia,NoticiaAdmin)
# admin.site.register(FotoNoticia)