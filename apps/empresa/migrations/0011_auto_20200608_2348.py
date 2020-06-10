# Generated by Django 3.0.4 on 2020-06-09 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0010_auto_20200608_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('A', 'Activo'), ('E', 'En Curso'), ('M', 'En Marcha'), ('F', 'Finalizado'), ('C', 'Cancelado')], default='N', max_length=1),
        ),
    ]