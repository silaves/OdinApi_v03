# Generated by Django 3.0.4 on 2020-06-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0014_auto_20200608_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='calificacion',
            field=models.DecimalField(decimal_places=9, default=0, max_digits=10, verbose_name='Calificacion'),
        ),
    ]
