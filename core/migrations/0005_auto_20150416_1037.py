# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150416_1013'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Funcion',
        ),
        migrations.AlterField(
            model_name='funcionalidad',
            name='estado',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')]),
        ),
        migrations.AlterField(
            model_name='modulo',
            name='estado',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')]),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='estado',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')]),
        ),
    ]
