# Generated by Django 3.0.4 on 2020-06-03 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0007_auto_20200603_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='costo_min',
            field=models.DecimalField(decimal_places=1, help_text='Costo minimo de un envio en Bs.', max_digits=7, verbose_name='Costo minimo'),
        ),
    ]