# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intenciones',
            name='individual',
            field=models.BooleanField(default=None, help_text=b'Marque para indicar que la intenci\xc3\xb3n ser\xc3\xa1 la \xc3\xbanica en la misa', verbose_name=b'Es \xc3\xbanica?'),
        ),
        migrations.AlterField(
            model_name='matrimonio',
            name='vigente',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='periodoasignacionparroquia',
            name='estado',
            field=models.BooleanField(default=None, help_text=b'Marque la casilla activo para indicar que el usuario puede acceder al sistema', verbose_name=b'Es administrador?'),
        ),
    ]
