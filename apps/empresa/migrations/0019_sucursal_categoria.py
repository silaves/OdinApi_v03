# Generated by Django 3.0.4 on 2020-06-18 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0018_auto_20200616_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='empresa.CategoriaProducto'),
            preserve_default=False,
        ),
    ]
