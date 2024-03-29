from datetime import date
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,register_events, register_job

from apps.empresa.models import Producto
from .cleanup import remove_unused_media

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler,'cron', hour='6')
def activar_desactivar_productos_del_dia():
    dia = date.today().weekday()
    productos = Producto.objects.select_related('sucursal__empresa__categoria').filter(sucursal__empresa__categoria__nombre=settings.COMIDA)
    for p in productos:
        if p.dias_activos[dia] == '0':
            p.combo_activo = False
        else:
            p.combo_activo = True
        p.save()


@register_job(scheduler,'cron', hour='6', minute='5')
def eliminar_imagenes_huerfanas():
    # remove_unused_media(['*.png','*.jpeg'])
    remove_unused_media()

register_events(scheduler)
scheduler.start()
print('Scheduler is Active')