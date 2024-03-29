# Generated by Django 3.0.4 on 2020-06-01 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0002_auto_20200531_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='VersionesAndroidApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.IntegerField(default=1)),
                ('empresario', models.IntegerField(default=1)),
                ('repartidor', models.IntegerField(default=1)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Version de Aplicacion Android',
                'verbose_name_plural': '0. Versiones de Aplicaciones Android',
                'db_table': 'Versiones_AndroidApp',
            },
        ),
    ]
