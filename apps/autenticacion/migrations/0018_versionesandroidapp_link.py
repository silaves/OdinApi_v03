# Generated by Django 3.0.4 on 2020-06-28 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0017_versionesandroidapp_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionesandroidapp',
            name='link',
            field=models.URLField(blank=True, max_length=255),
        ),
    ]
