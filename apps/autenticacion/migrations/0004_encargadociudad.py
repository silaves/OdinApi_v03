# Generated by Django 3.0.4 on 2020-06-03 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0003_versionesandroidapp'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncargadoCiudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.Ciudad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Encargado Region',
                'verbose_name_plural': 'Encargados de Regiones',
                'db_table': 'ENCARGADO_CIUDAD',
                'unique_together': {('usuario', 'ciudad')},
            },
        ),
    ]