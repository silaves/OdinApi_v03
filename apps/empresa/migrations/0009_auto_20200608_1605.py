# Generated by Django 3.0.4 on 2020-06-08 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0008_auto_20200608_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='calificacion',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sucursal',
            name='cant_calificacion',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
