# Generated by Django 3.0.4 on 2020-06-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0016_auto_20200613_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sucursal',
            name='calificacion',
            field=models.DecimalField(decimal_places=9, default=0, max_digits=10, verbose_name='Calificacion'),
        ),
    ]