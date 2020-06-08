from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils.html import format_html

from apps.autenticacion.models import Usuario
from apps.empresa.models import Empresa, Sucursal, Pedido, Combo, Chat_Pedido, Producto, CategoriaEmpresa, CategoriaProducto, FotoProducto

# @admin.register(CategoriaProducto)
# class CategoriaProductoAdmin(admin.ModelAdmin):
#     exclude=("codigo",)
#     readonly_fields=('codigo', )
     
#     def get_changeform_initial_data(self, request):
#         return {'codigo': '3.23.'}



# admin.site.unregister(Producto)

class FotoProducto(admin.StackedInline):
    model = FotoProducto
    fields = ('foto',)
    can_delete = False
    extra = 0

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','id','estado','sucursal','creado')
    list_filter = ('sucursal', 'is_combo','estado')
    inlines = (FotoProducto,)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal','repartidor','total','fecha')
    list_filter = ('sucursal', 'repartidor','fecha')
    search_fields = ('total',)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre','id','estado','categoria','empresario_link')
    list_filter = ('categoria','estado')
    search_fields = ('nombre',)
    actions = ('activar_empresa','dar_baja_empresa')

    def empresario_link(self, obj):
        author = obj.empresario
        opts = author._meta
        author_edit_url = reverse('admin:autenticacion_usuario_change', args=[author.pk])
        return format_html(
            '<a{}>{}</a>', flatatt({'href': author_edit_url}), author.username)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def activar_empresa(self, request, queryset):
        queryset.update(estado=True)

    def dar_baja_empresa(self, request, queryset):
        queryset.update(estado=False)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        q0 = qs.filter(pk=request.user.id)
        if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD):
            try:
                _ciudad = request.user.ciudad.id
            except:
                _ciudad = 0
            q1 = qs.filter(empresario__ciudad__id=_ciudad)
            return (q0|q1).distinct()
        return qs
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(EmpresaAdmin, self).get_form(request, obj, **kwargs)
        if request.user.groups.filter(name=settings.GRUPO_ENCARGADO_CIUDAD).exists():
            try:
                _ciudad = request.user.ciudad.id
            except:
                _ciudad = 0
            form.base_fields['empresario'].queryset = Usuario.objects.filter(is_active=True,ciudad__id=_ciudad,groups__name=settings.GRUPO_EMPRESARIO)
        else:
            form = super(EmpresaAdmin, self).get_form(request, obj, **kwargs)
            form.base_fields['empresario'].queryset = Usuario.objects.filter(is_active=True,groups__name=settings.GRUPO_EMPRESARIO)
        return form

# admin.site.register(Empresa)
admin.site.register(Sucursal)

# admin.site.register(Pedido)
# admin.site.register(Pedido, ProductoAdmin)
# admin.site.register(Combo, ComboAdmin)
# admin.site.register(Chat_Pedido)
admin.site.register(CategoriaEmpresa)
admin.site.register(CategoriaProducto)