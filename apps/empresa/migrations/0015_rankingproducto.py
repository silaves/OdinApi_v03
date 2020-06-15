# Generated by Django 3.0.4 on 2020-06-13 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0014_auto_20200612_0403'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.IntegerField()),
                ('puntuacion', models.IntegerField(default=0)),
                ('is_calificado', models.BooleanField(default=False)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.Producto')),
            ],
            options={
                'db_table': 'RANKING_PRODUCTO',
                'unique_together': {('producto', 'usuario')},
            },
        ),
    ]