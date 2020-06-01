from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .validators import tamaño_del_archivo
from apps.empresa.models import Empresa

class CategoriaNoticia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    nivel = models.PositiveSmallIntegerField(blank=False)
    estado = models.BooleanField(default=True)
    padre = models.ForeignKey('self',blank=True,null=True,on_delete=models.PROTECT)

    class Meta:
        db_table = 'CATEGORIA_NOTICIA'
        verbose_name = _('categoria noticia')
        verbose_name_plural = _('10. Categorias Noticias')
    
    def __str__(self):
        return str(self.nivel)+'-'+self.nombre



class Noticia(models.Model):
    titulo = models.CharField(max_length=200,blank=False,help_text='Ingrese el Titulo de la Noticia')
    sub_titulo = models.CharField(max_length=255,blank=False,help_text='Ingrese un subtitulo')
    descripcion = models.TextField(blank=False,help_text='Ingrese la descripcion')
    link_fuente = models.URLField(max_length=200, blank=True, help_text='Ingrese la url de la fuente de la noticia')
    localidad = models.CharField(max_length=40,blank=True,help_text='Lugar de la Noticia')
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    categoria = models.ManyToManyField(CategoriaNoticia)

    class Meta:
        db_table = 'NOTICIA'
        verbose_name = _('noticia')
        verbose_name_plural = _('11. Noticias')
    
    def __str__(self):
        return self.titulo
    

class FotoNoticia(models.Model):
    foto = models.ImageField(upload_to="noticias/", validators=[tamaño_del_archivo,],
        help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS)
    descripcion = models.CharField(max_length=150,blank=False,help_text='Ingrese breve descripcion de la foto')
    autor = models.CharField(max_length=50,blank=False,help_text='Ingrese el autor de la foto')
    localidad = models.CharField(max_length=20,blank=False,help_text='Ingrese la localidad de la foto')
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)

    class Meta:
        db_table = 'FOTO_NOTICIA'
        verbose_name = _('foto noticia')
        verbose_name_plural = _('foto noticias')
    
    # def __str__(self):
    #     return self.autor
    