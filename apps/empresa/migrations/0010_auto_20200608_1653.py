# Generated by Django 3.0.4 on 2020-06-08 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0009_auto_20200608_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sucursal',
            name='calificacion',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Calificacion'),
        ),
    ]