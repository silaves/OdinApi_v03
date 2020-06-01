from django.conf import settings
from django.contrib import admin
from apps.empresa.models import Empresa, Sucursal, Pedido, Combo, Chat_Pedido, Producto, CategoriaEmpresa, Ciudad, CategoriaProducto, FotoProducto
from django.utils.safestring import mark_safe

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

# class Combo_inline(admin.StackedInline):
#     model = ComboProducto

# class ComboAdmin(admin.ModelAdmin):
#     inlines = [Combo_inline]

admin.site.register(Empresa)
admin.site.register(Sucursal)
admin.site.register(Ciudad)
# admin.site.register(Pedido)
# admin.site.register(Pedido, ProductoAdmin)
# admin.site.register(Combo, ComboAdmin)
# admin.site.register(Chat_Pedido)
admin.site.register(CategoriaEmpresa)
admin.site.register(CategoriaProducto)