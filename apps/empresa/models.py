from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.autenticacion.models import Usuario, Ciudad
from .validators import *
# Create your models here.

class CategoriaEmpresa(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    estado = models.BooleanField(default=True)
    # sub_categoria = models.IntegerField()

    class Meta:
        db_table = 'CATEGORIA_EMPRESA'
        verbose_name = _('categoria empresa')
        verbose_name_plural = _('4. Categorias Empresa')
    
    def __str__(self):
        return self.nombre



class Empresa(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    empresario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaEmpresa, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True, blank=True)
    
    class Meta:
        db_table = 'EMPRESA'
        verbose_name = _('empresa')
        verbose_name_plural = _('5. Empresas')
    
    def __str__(self):
        return self.nombre



class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    estado = models.BooleanField(default=True)
    padre = models.ForeignKey('self',blank=True,null=True,on_delete=models.PROTECT)

    class Meta:
        db_table = 'CATEGORIA_ARTICULO'
        verbose_name = _('categoria producto')
        verbose_name_plural = _('7. Categorias de un Producto')
    
    def __str__(self):
        return self.codigo +' '+ self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(_('Zona'),max_length=20)
    telefono = models.IntegerField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True, validators=[validate_latitude_longitude,])
    direccion = models.CharField(max_length=255)
    hora_inicio = models.TimeField(default='15:00:00',blank=True)
    hora_fin = models.TimeField(default='15:00:00',blank=True)
    disponible = models.BooleanField(default=False, blank=True)
    estado = models.BooleanField(default=True, blank=True)
    foto = models.ImageField(upload_to="sucursal/", null=True, blank=True,
        validators=[tamaño_del_archivo,],help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS
    )
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad,blank=True,null=True, on_delete=models.PROTECT)
    # encargado = models.ForeignKey(Usuario,blank=True,null=True, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT)
    cant_calificacion = models.PositiveIntegerField(default=0)
    calificacion = models.DecimalField(_('Calificacion'),default=0,max_digits=10, decimal_places=9)

    class Meta:
        db_table = 'SUCURSAL'
        verbose_name = _('sucursal')
        verbose_name_plural = _('6. Sucursales')
    
    def __str__(self):
        return self.nombre+' - '+self.empresa.nombre


class FotoSucursal(models.Model):
    foto = models.ImageField(upload_to="sucursal/",blank=False,
        validators=[tamaño_del_archivo,],help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS)
    sucursal = models.ForeignKey(Sucursal, related_name='fotos',on_delete=models.CASCADE)

    class Meta:
        db_table = 'FOTO_TIENDA'
        verbose_name = _('foto tienda')
        verbose_name_plural = _('fotos tienda')
    
    def __str__(self):
        return self.id




class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(max_digits=7, decimal_places=1, blank=False)
    estado = models.BooleanField(default=True, blank=True)
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    is_combo = models.BooleanField(default=False)
    combo_activo = models.BooleanField(default=True)
    dias_activos = models.CharField(max_length=7, default='1111111', blank=False)
    atributos = JSONField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT)
    creado = models.DateTimeField(auto_now_add=True)
    cant_calificacion = models.PositiveIntegerField(default=0)
    calificacion = models.DecimalField(default=0,max_digits=10, decimal_places=9)

    class Meta:
        db_table = 'PRODUCTO'
        verbose_name = _('producto')
        verbose_name_plural = _('8. Productos')
    
    def __str__(self):
        return self.nombre
    
    # @property
    # def load_sucursal(self, value):
    #     return self.sucursa

class Combo(models.Model):
    combo = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='combo')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='producto')
    cantidad = models.PositiveSmallIntegerField(default=1, validators=[cantidad_min_value,cantidad_max_value])

    def clean(self):
        if self.combo.sucursal.id != self.producto.sucursal.id:
            raise ValidationError({'producto':'el producto es una mierda'})

    def save(self, *args, **kwargs):
        super(Combo,self).save(*args, **kwargs)

    class Meta:
        unique_together =  (('combo','producto'),)
        db_table = 'COMBO'
        verbose_name = _('combo')
        verbose_name_plural = _('combos')
    
    def __str__(self):
        return self.producto


class FotoProducto(models.Model):
    foto = models.ImageField(upload_to="productos/", null=True,blank=True,
        validators=[tamaño_del_archivo,],help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'FOTO_PRODUCTO'
        verbose_name = _('foto producto')
        verbose_name_plural = _('fotos productos')
    
    def __str__(self):
        return str(self.id)



class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =  (('usuario','producto'),)
        db_table = 'FAVORITO'
        verbose_name = _('favorito')
        verbose_name_plural = _('favoritos')
    
    def __str__(self):
        return str(self.id)


class RankingProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.IntegerField(blank=False)
    puntuacion = models.IntegerField(default=0)
    is_calificado = models.BooleanField(default=False)

    class Meta:
        unique_together =  (('producto','usuario'),)
        db_table = 'RANKING_PRODUCTO'
    

# class SubCategoriaProducto(models.Model):
#     hijo = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name='categoria_hijo')
#     padre = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name='sub_categorias')

#     class Meta:
#         unique_together =  (('hijo','padre'),)
#         db_table = 'SUB_CATEGORIA_PRODUCTO'
#         verbose_name = _('sub categoria - producto')
#         verbose_name_plural = _('sub categorias - producto')
    
#     def __str__(self):
#         return self.id






class Pedido(models.Model):
    total = models.DecimalField(_('Monto Total de productos'),max_digits=7, decimal_places=1, blank=False)
    costo_envio = models.DecimalField(_('costo de envio'),max_digits=7, decimal_places=1, blank=False)
    precio_final = models.DecimalField(_('precio final'),max_digits=7, decimal_places=1, blank=False)
    cliente = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, default='N',choices=(
		('A','Activo'),('E', 'En Curso'),('M', 'En Marcha'),('F', 'Finalizado'),('C', 'Cancelado')
	))
    ubicacion = models.CharField(_('Ubicacion'), max_length=255, blank=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    repartidor = models.ForeignKey(Usuario,blank=True,null=True,related_name='repartidor', on_delete=models.CASCADE)
    is_calificado_cliente = models.BooleanField(default=False, blank=False)
    is_calificado_empresario = models.BooleanField(default=False, blank=False)
    is_calificado_repartidor = models.BooleanField(default=False, blank=False)

    class Meta:
        db_table = 'PEDIDO'
        verbose_name = _('pedido')
        verbose_name_plural = _('9. Pedidos')
    
    def __str__(self):
        return self.cliente.nombres


class PedidoProducto(models.Model):
    cantidad = models.PositiveSmallIntegerField(default=1, validators=[cantidad_min_value,cantidad_max_value])
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    producto_final = models.ForeignKey(Producto, on_delete=models.PROTECT)

    class Meta:
        db_table = 'PEDIDO_PRODUCTO'
        verbose_name = _('pedido_producto')
        verbose_name_plural = _('pedido_productos')
    
    def __str__(self):
        return self.id


class Chat_Pedido(models.Model):
    ci = models.CharField(max_length=14)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)

    class Meta:
        db_table = 'CHAT_PEDIDO'
        verbose_name = _('chat_pedido')
        verbose_name_plural = _('chat_pedidos')
    
    def __str__(self):
        return self.id


class ChatProducto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CHAT_PRODUCTO'
        verbose_name = _('chat producto')
        verbose_name_plural = _('chat productos')
    
    def __str__(self):
        return self.id

class MensajeChat(models.Model):
    id_propietario = models.IntegerField(blank=False)
    mensaje = models.TextField(blank=False)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    chat = models.ForeignKey(ChatProducto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'MENSAJE_CHAT'
        verbose_name = _('mensaje')
        verbose_name_plural = _('mensajes')
    
    def __str__(self):
        return self.id