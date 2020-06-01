from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.autenticacion.models import Usuario
from .validators import tamaño_del_archivo


# class Ubicacion(models.Model):
#     nombre = models.CharField(max_length=50)
#     longitud = models.FloatField()
#     latitud = models.FloatField()
#     favorito = models.BooleanField()
#     cliente = models.ForeignKey(Usuario, on_delete=models.PROTECT)


# class PedidoTaxi(models.Model):
#     calificacion_taxista = models.IntegerField()
#     calificacion_cliente = models.IntegerField()
#     taxista = models.ForeignKey(Usuario, on_delete=models.PROTECT)
#     ubicacion_inicio_cliente = models.TextField()
#     ubicacion_destino_cliente = models.ForeignKey(Usuario, on_delete=models.PROTECT)


# class ChatTaxi(models.Model):
#     ci = models.CharField(max_length=20)
#     mensaje = models.TextField()
#     pedido_taxi = models.ForeignKey(PedidoTaxi, on_delete=models.PROTECT)


class Movil(models.Model):
    placa = models.CharField(max_length=10, blank=False, unique=True)
    color = models.CharField(max_length=30, blank=False)
    modelo = models.CharField(max_length=50, blank=False)
    foto = models.ImageField(upload_to="moviles/",default = 'moviles/no-img.jpg', null=True, blank=True,
        validators=[
            tamaño_del_archivo,
        ],
        help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS
    )
    taxista = models.ForeignKey(Usuario,related_name='movil', on_delete=models.PROTECT)

    class Meta:
        db_table = 'MOVIL'
        verbose_name = _('movil')
        verbose_name_plural = _('moviles')
    
    def __str__(self):
        return self.placa